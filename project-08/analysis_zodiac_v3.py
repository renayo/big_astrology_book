#!/usr/bin/env python3
"""
Project 8 (v3): Full Zodiac "Graha" Shootout
============================================
Testing Tropical vs Sidereal efficacy using ALL traditional bodies:
Starring: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Rahu, Ketu.

New Hypothesis:
Maybe the "Sun Sign" isn't enough. Do the signs of the Moon, Mars, 
or the Nodes (Rahu/Ketu) provide the missing link to Profession?

We compare two systems:
1. TROPICAL ZODIAC (Seasonal)
2. SIDEREAL ZODIAC (Lahiri/Constellational)

Against a Baseline of:
- Harmonics Only (established in Project 6 to have some signal).

If Sidereal is "better", the model trained on Sidereal signs (Full Chart)
should outperform the Tropical model.
"""

import numpy as np
import pandas as pd
import swisseph as swe
from pathlib import Path
import sys
from datetime import datetime
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
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

# Planets for Harmonic Calc
HARMONIC_BODIES = [
    swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS, 
    swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO
]

# Bodies for Sign Features (Traditional 9 Grahas)
SIGN_BODIES = {
    swe.SUN: 'Sun', 
    swe.MOON: 'Moon', 
    swe.MERCURY: 'Mercury',
    swe.VENUS: 'Venus', 
    swe.MARS: 'Mars', 
    swe.JUPITER: 'Jupiter',
    swe.SATURN: 'Saturn', 
    swe.MEAN_NODE: 'Rahu'
}

def get_sign(lon):
    """Return sign index 0-11 from longitude."""
    return int(lon / 30) % 12

def calc_harmonic_strength(positions, h):
    """Vector Mean R for harmonic H."""
    angles = []
    n_p = len(positions)
    for i in range(n_p):
        for j in range(i+1, n_p):
            diff = abs(positions[i] - positions[j])
            if diff > 180: diff = 360 - diff
            angles.append(diff)
    if not angles: return 0.0
    rads = np.deg2rad(np.array(angles) * h)
    return np.sqrt(np.mean(np.cos(rads))**2 + np.mean(np.sin(rads))**2)

def process_chart(entry):
    s_date = f"{entry['date']} {entry['time']}"
    try:
        dt = datetime.strptime(s_date, "%Y-%m-%d %H:%M")
    except ValueError:
        return None

    hour = dt.hour + dt.minute/60.0
    jd = swe.julday(dt.year, dt.month, dt.day, hour)

    # --- 1. TROPICAL CALCS ---
    swe.set_sid_mode(0) # Tropical
    trop_features = {}
    trop_positions = [] # For Harmonics

    # Get Harmonic Bodies (Tropical Lons)
    for pid in HARMONIC_BODIES:
        lon = swe.calc_ut(jd, pid, 0)[0][0]
        trop_positions.append(lon)

    # Get Sign Bodies
    for pid, name in SIGN_BODIES.items():
        lon = swe.calc_ut(jd, pid, 0)[0][0]
        trop_features[f"{name}_Trop"] = get_sign(lon)

        # Derived Ketu
        if name == 'Rahu':
            ketu_lon = (lon + 180) % 360
            trop_features['Ketu_Trop'] = get_sign(ketu_lon)

    # --- 2. SIDEREAL CALCS (Lahiri) ---
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    sid_features = {}

    for pid, name in SIGN_BODIES.items():
        lon = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL)[0][0]
        sid_features[f"{name}_Sid"] = get_sign(lon)

        if name == 'Rahu':
            ketu_lon = (lon + 180) % 360
            sid_features['Ketu_Sid'] = get_sign(ketu_lon)

    # --- 3. HARMONICS ---
    # (Calculated on Tropical positions - angles are invariant)
    h4 = calc_harmonic_strength(trop_positions, 4)
    h5 = calc_harmonic_strength(trop_positions, 5)
    h7 = calc_harmonic_strength(trop_positions, 7)

    return {
        'Category': entry['category'],
        'H4': h4, 'H5': h5, 'H7': h7,
        **trop_features,
        **sid_features
    }

def run_experiment():
    print("Generating Dataset...")
    data = []
    for entry in CELEBRITY_DATA:
        if 'category' not in entry: continue
        row = process_chart(entry)
        if row: data.append(row)

    df = pd.DataFrame(data)
    print(f"Dataset Size: {len(df)}")

    X = df.drop('Category', axis=1)
    y = df['Category']

    # Common Harmonic Features
    harm_cols = ['H4', 'H5', 'H7']

    # Tropical Sign Columns
    trop_cols = [c for c in df.columns if "_Trop" in c]
    # Sidereal Sign Columns
    sid_cols = [c for c in df.columns if "_Sid" in c]

    print(f"Features per model: Harmonic={len(harm_cols)}, Signs={len(trop_cols)}")

    # --- MODEL 1: HARMONICS ONLY ---
    print("\n--- BASELINE: HARMONICS ONLY ---")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    scores = cross_val_score(clf, X[harm_cols], y, cv=LeaveOneOut())
    print(f"Accuracy: {scores.mean():.1%}")

    # --- MODEL 2: TROPICAL FULL ---
    print("\n--- TROPICAL FULL (9 Signs + Harmonics) ---")
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', harm_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), trop_cols)
        ])
    clf = Pipeline([('pre', preprocessor), ('clf', RandomForestClassifier(n_estimators=100, random_state=42))])
    scores = cross_val_score(clf, X[harm_cols + trop_cols], y, cv=LeaveOneOut())
    print(f"Accuracy: {scores.mean():.1%}")

    # --- MODEL 3: SIDEREAL FULL ---
    print("\n--- SIDEREAL FULL (9 Signs + Harmonics) ---")
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', harm_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), sid_cols)
        ])
    clf = Pipeline([('pre', preprocessor), ('clf', RandomForestClassifier(n_estimators=100, random_state=42))])
    scores = cross_val_score(clf, X[harm_cols + sid_cols], y, cv=LeaveOneOut())
    print(f"Accuracy: {scores.mean():.1%}")

    # --- DUMMY ---
    dummy = DummyClassifier(strategy="most_frequent")
    dummy.fit(X, y)
    print(f"\nRandom/Dummy Baseline: {dummy.score(X, y):.1%}")

if __name__ == "__main__":
    run_experiment()
