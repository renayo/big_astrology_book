#!/usr/bin/env python3
"""
Project 8: Tropical vs Sidereal Zodiac (Classification Test)
============================================================
A rigorous test to determine which zodiac system (Tropical or Sidereal)
better aligns with observed reality (Professions of verified celebrities).

RESEARCH QUESTION:
Does the "Solar Sign" correlate with Profession better in the Tropical 
(Seasonal) Zodiac or the Sidereal (Constellation) Zodiac?

METHODOLOGY:
1. Use Project 6 Celebrity Dataset (N=Real).
2. Calculate Sun Sign in TROPICAL zodiac.
3. Calculate Sun Sign in SIDEREAL (Lahiri) zodiac.
4. Calculate Sun Sign in SIDEREAL (Fagan-Bradley) zodiac.
5. Train 3 separate Machine Learning models (Random Forest).
   - Features: Sun Sign (One-Hot Encoded)
   - Target: Profession (Science, Arts, Politics, Sports)
   - Validation: Leave-One-Out Cross Validation.
6. Compare Accuracy. If one zodiac is "Real", it should yield higher predictive power.
"""

import numpy as np
import pandas as pd
import swisseph as swe
from pathlib import Path
import sys
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import CategoricalNB
from sklearn.dummy import DummyClassifier
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

# Import Data from Project 6
sys.path.append(str(Path(__file__).parent.parent / "06-harmonic-analysis-aspects"))
try:
    from celebrity_data import CELEBRITY_DATA
except ImportError:
    print("Error: Could not import celebrity_data.py from Project 6 folder.")
    sys.exit(1)

OUTPUT_DIR = Path(__file__).parent
OUTPUT_DIR.mkdir(exist_ok=True)
swe.set_ephe_path(None)

def get_sun_sign(entry, mode='Tropical'):
    """Calculate Sun Sign (0-11) in requested zodiac mode."""
    # Convert date
    s_date = f"{entry['date']} {entry['time']}"
    try:
        dt = datetime.strptime(s_date, "%Y-%m-%d %H:%M")
    except ValueError:
        return None

    hour = dt.hour + dt.minute/60.0
    jd = swe.julday(dt.year, dt.month, dt.day, hour)

    # Set Sidereal Mode if needed
    if mode == 'Tropical':
        swe.set_sid_mode(0) # Off
        flags = 0
    elif mode == 'Sidereal_Lahiri':
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        flags = swe.FLG_SIDEREAL
    elif mode == 'Sidereal_Fagan':
        swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY)
        flags = swe.FLG_SIDEREAL

    # Calculate Sun
    res = swe.calc_ut(jd, swe.SUN, flags)[0][0]
    sign = int(res / 30) % 12
    return sign

def get_zodiac_dataset(mode):
    """Generate X, y dataset for a specific zodiac."""
    data = []
    labels = []

    for entry in CELEBRITY_DATA:
        if 'category' not in entry: continue

        sign = get_sun_sign(entry, mode)
        if sign is None: continue

        data.append([sign])
        labels.append(entry['category'])

    return np.array(data), np.array(labels)

def evaluate_zodiac(mode):
    """Train and Evaluate a classifier for one zodiac system."""
    X, y = get_zodiac_dataset(mode)

    # Filter small classes
    counts = pd.Series(y).value_counts()
    valid_cats = counts[counts >= 5].index
    mask = pd.Series(y).isin(valid_cats)
    X = X[mask]
    y = y[mask]

    # Encoder
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    # Model: Naive Bayes is good for categorical (Sign -> Category)
    # But sklearn's CategoricalNB needs careful input. 
    # Let's use Random Forest with simple features
    clf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)

    # Evaluation
    cv = LeaveOneOut()
    scores = cross_val_score(clf, X, y_enc, cv=cv, scoring='accuracy')

    return scores.mean()

def main():
    print("="*60)
    print("PROJECT 8: TROPICAL VS SIDEREAL - PREDICTIVE POWER TEST")
    print("="*60)
    print(f"Dataset: Verified Celebrities (N={len(CELEBRITY_DATA)})")

    modes = ['Tropical', 'Sidereal_Lahiri', 'Sidereal_Fagan']
    results = {}

    # 1. Baseline
    X, y = get_zodiac_dataset('Tropical')
    dummy = DummyClassifier(strategy='most_frequent')
    baseline = np.mean(cross_val_score(dummy, X, y, cv=LeaveOneOut()))
    print(f"Random/Frequent Baseline: {baseline:.4f}")
    print("-" * 60)

    # 2. Test Zodiacs
    for mode in modes:
        acc = evaluate_zodiac(mode)
        results[mode] = acc
        print(f"Zodiac: {mode:<20} Accuracy: {acc:.4f}")

    print("-" * 60)

    # 3. Analyze Differences
    best_mode = max(results, key=results.get)
    print(f"WINNER: {best_mode} (Acc: {results[best_mode]:.4f})")

    # 4. Save
    pd.DataFrame(list(results.items()), columns=['Zodiac', 'Accuracy']).to_csv(OUTPUT_DIR / 'zodiac_comparison_results.csv', index=False)

    # 5. Visualization
    plt.figure(figsize=(10, 6))
    bars = plt.bar(results.keys(), results.values(), color=['orange', 'purple', 'indigo'])
    plt.axhline(baseline, color='black', linestyle='--', label='Baseline')
    plt.ylabel('Classification Accuracy')
    plt.title('Predictive Power of Zodiac Systems (Sun Sign -> Profession)')
    plt.ylim(0, max(results.values()) + 0.1)

    # Add labels
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, h, f'{h:.1%}', ha='center', va='bottom')

    plt.savefig(OUTPUT_DIR / 'zodiac_comparison.png')
    print(f"Plot saved to {OUTPUT_DIR / 'zodiac_comparison.png'}")

if __name__ == "__main__":
    main()
