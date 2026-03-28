#!/usr/bin/env python3
"""
Project 8 (v2): The Zodiac-Harmonic Interaction Test
====================================================
Incorporating the "New Observations" from Project 6.

Project 6 Summary:
- Scientists have high H4 (Square) & H5 (Quintile) strength.
- Athletes have high H7 (Septile) strength.
- Artists have high H4 strength.

Project 8 Original Result:
- Classifying profession by Sun Sign alone failed (Null Result).

New Hypothesis:
Maybe Zodiac Signs *do* matter, but only when controlled for Harmonic Strength?
Or perhaps specific Zodiac systems align better with these Harmonic signatures?

We test 3 Models:
1. Baseline: Harmonic Strength Only (H4, H5, H7).
2. Tropical Model: Harmonics + Tropical Sun Sign.
3. Sidereal Model: Harmonics + Sidereal Sun Sign.

If Model 2 or 3 beats Model 1 significantly, we have evidence for the Zodiac.
"""

import numpy as np
import pandas as pd
import swisseph as swe
from pathlib import Path
import sys
from datetime import datetime
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyClassifier

# Import Data from Project 6
sys.path.append(str(Path(__file__).parent.parent / "06-harmonic-analysis-aspects"))
try:
    from celebrity_data import CELEBRITY_DATA
except ImportError:
    print("Error: Could not import celebrity_data.py")
    sys.exit(1)

OUTPUT_DIR = Path(__file__).parent
OUTPUT_DIR.mkdir(exist_ok=True)
swe.set_ephe_path(None)

PLANETS = {
    swe.SUN: 'Sun', swe.MOON: 'Moon', swe.MERCURY: 'Mercury', 
    swe.VENUS: 'Venus', swe.MARS: 'Mars', swe.JUPITER: 'Jupiter',
    swe.SATURN: 'Saturn', swe.URANUS: 'Uranus', 
    swe.NEPTUNE: 'Neptune', swe.PLUTO: 'Pluto'
}

def get_positions_and_sign(entry):
    """Calculate Planetary Longitudes and Sun Signs (Tropical/Sidereal)."""
    s_date = f"{entry['date']} {entry['time']}"
    try:
        dt = datetime.strptime(s_date, "%Y-%m-%d %H:%M")
    except ValueError:
        return None

    hour = dt.hour + dt.minute/60.0
    jd = swe.julday(dt.year, dt.month, dt.day, hour)

    # 1. Get Tropical Positions (for Aspect Calculation)
    # Aspects are zodiac-independent, so any frame works, but Tropical is standard base.
    swe.set_sid_mode(0)

    positions = []

    # Sun Sign Tropical
    res_sun = swe.calc_ut(jd, swe.SUN, 0)[0][0]
    sign_trop = int(res_sun / 30) % 12

    # Planetary Positions for Aspects
    for pid in PLANETS:
        lon = swe.calc_ut(jd, pid, 0)[0][0]
        positions.append(lon)

    # 2. Get Sidereal Sun Sign (Lahiri)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    res_sun_sid = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0][0]
    sign_sid = int(res_sun_sid / 30) % 12

    return positions, sign_trop, sign_sid

def calc_harmonic_strength(positions, h):
    """
    Calculate the strength of harmonic H for a single chart.
    Using Vector Mean R of all planetary pairs.
    """
    angles = []
    n_p = len(positions)
    for i in range(n_p):
        for j in range(i+1, n_p):
            # Shortest arc distance
            diff = abs(positions[i] - positions[j])
            if diff > 180: diff = 360 - diff
            angles.append(diff)

    if not angles: return 0.0

    # Vector transformation
    rads = np.deg2rad(np.array(angles) * h)
    R = np.sqrt(np.mean(np.cos(rads))**2 + np.mean(np.sin(rads))**2)
    return R

def prepare_dataset():
    data = []

    print(f"Processing {len(CELEBRITY_DATA)} charts...")

    for entry in CELEBRITY_DATA:
        if 'category' not in entry: continue

        res = get_positions_and_sign(entry)
        if not res: continue

        positions, sign_trop, sign_sid = res

        # Calculate Key Harmonics from Project 6
        h4 = calc_harmonic_strength(positions, 4) # Squares (Scientists/Artists)
        h5 = calc_harmonic_strength(positions, 5) # Quintiles (Scientists)
        h7 = calc_harmonic_strength(positions, 7) # Septiles (Athletes)

        data.append({
            'Category': entry['category'],
            'H4': h4,
            'H5': h5,
            'H7': h7,
            'Sign_Trop': str(sign_trop), # Categorical
            'Sign_Sid': str(sign_sid)    # Categorical
        })

    return pd.DataFrame(data)

def run_experiment():
    df = prepare_dataset()
    print(f"Valid Dataset: {len(df)} records\n")

    X = df.drop('Category', axis=1)
    y = df['Category']

    # 1. Baseline Model (Harmonics Only)
    # ----------------------------------
    print("--- MODEL A: HARMONICS ONLY (H4, H5, H7) ---")
    clf_base = RandomForestClassifier(n_estimators=100, random_state=42)
    scores_base = cross_val_score(clf_base, X[['H4', 'H5', 'H7']], y, cv=LeaveOneOut())
    print(f"Accuracy: {scores_base.mean():.1%}")

    # 2. Tropical Model (Harmonics + Tropical Sign)
    # ---------------------------------------------
    print("\n--- MODEL B: HARMONICS + TROPICAL ZODIAC ---")
    cat_features = ['Sign_Trop']
    num_features = ['H4', 'H5', 'H7']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
        ])

    clf_trop = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))])

    scores_trop = cross_val_score(clf_trop, X[['H4', 'H5', 'H7', 'Sign_Trop']], y, cv=LeaveOneOut())
    print(f"Accuracy: {scores_trop.mean():.1%}")

    # 3. Sidereal Model (Harmonics + Sidereal Sign)
    # ---------------------------------------------
    print("\n--- MODEL C: HARMONICS + SIDEREAL ZODIAC ---")
    cat_features = ['Sign_Sid']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
        ])

    clf_sid = Pipeline(steps=[('preprocessor', preprocessor),
                              ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))])

    scores_sid = cross_val_score(clf_sid, X[['H4', 'H5', 'H7', 'Sign_Sid']], y, cv=LeaveOneOut())
    print(f"Accuracy: {scores_sid.mean():.1%}")

    # Random Baseline
    dummy = DummyClassifier(strategy="stratified", random_state=42)
    scores_dum = cross_val_score(dummy, X, y, cv=LeaveOneOut())
    print(f"\nRandom Baseline: {scores_dum.mean():.1%}")

if __name__ == "__main__":
    run_experiment()
