#!/usr/bin/env python3
"""
Project 7B: ML Classification of Profession using Chart Features
================================================================
Uses the Project 6 Celebrity Dataset (N=Real) to test if Machine Learning
can predict 'Profession' (Science vs Arts vs Politics) based on planetary positions.

This enables valid testing of INNER PLANETS (Sun, Moon, Mercury, Venus, Mars)
which was impossible with the Big Five (Year-only) dataset.

DATA:
- ~100 Verified Charts (Rodden AA/A)
- Categories: Science, Arts, Politics, Sports, Entertainment
- Features: Planetary Longitudes, Signs, Elements, Modalities

METHODOLOGY:
1. Feature Engineering:
   - Calculate Sign (0-11) for all bodies Sun-Pluto.
   - Calculate Elemental Balance (Fire/Earth/Air/Water counts).
   - Calculate Modalities (Cardinal/Fixed/Mutable).
2. ML Model:
   - Random Forest Classifier (multiclass).
   - Leave-One-Out Cross Validation (due to small sample size).
3. Baseline:
   - Compare accuracy to "Most Frequent" baseline.
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
from sklearn.dummy import DummyClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

# Import Data from Project 6
project6_path = Path(__file__).parent.parent / "06-harmonic-analysis-aspects"
if not project6_path.exists():
    print(f"Error: Project 6 folder not found at {project6_path}")
    sys.exit(1)

sys.path.insert(0, str(project6_path))
try:
    from celebrity_data import CELEBRITY_DATA
except ImportError as e:
    print(f"Error: Could not import celebrity_data.py from Project 6 folder.")
    print(f"Looked in: {project6_path}")
    print(f"Import error: {e}")
    sys.exit(1)

OUTPUT_DIR = Path(__file__).parent
OUTPUT_DIR.mkdir(exist_ok=True)
swe.set_ephe_path(None)

PLANETS = {
    swe.SUN: 'Sun', swe.MOON: 'Moon', swe.MERCURY: 'Mercury',
    swe.VENUS: 'Venus', swe.MARS: 'Mars', swe.JUPITER: 'Jupiter',
    swe.SATURN: 'Saturn', swe.URANUS: 'Uranus', swe.NEPTUNE: 'Neptune',
    swe.PLUTO: 'Pluto'
}

from datetime import datetime

def get_chart_features(entry):
    """Calculate comprehensive astrological features for a birth."""
    # Handle pre-1677 dates by avoiding pandas timestamp for old dates
    s_date = f"{entry['date']} {entry['time']}"
    try:
        dt = datetime.strptime(s_date, "%Y-%m-%d %H:%M")
    except ValueError:
        # Fallback for different formats if needed
        dt = datetime.strptime(s_date, "%Y-%m-%d %H:%M:%S")

    hour = dt.hour + dt.minute/60.0
    jd = swe.julday(dt.year, dt.month, dt.day, hour)

    features = {}

    # Elemental Counters
    elements = {'Fire': 0, 'Earth': 0, 'Air': 0, 'Water': 0}
    elem_map = {0:'Fire', 1:'Earth', 2:'Air', 3:'Water'}

    # Modality Counters
    modes = {'Cardinal': 0, 'Fixed': 0, 'Mutable': 0}
    mode_map = {0:'Cardinal', 1:'Fixed', 2:'Mutable'}

    # Planetary Data
    for pid, name in PLANETS.items():
        res = swe.calc_ut(jd, pid)[0][0] # Longitude
        sign = int(res / 30) % 12
        degree = res % 30

        # 1. Raw Sign (Categorical 0-11)
        # We will use Sin/Cos components to preserve circularity for ML
        # Sign = 0..11. 
        # Better: Longitude Sin/Cos
        rad = np.deg2rad(res)
        features[f'{name}_Sin'] = np.sin(rad)
        features[f'{name}_Cos'] = np.cos(rad)

        # 2. Element/Mode
        elem = elem_map[sign % 4]
        mode = mode_map[sign % 3]
        elements[elem] += 1
        modes[mode] += 1

    # Add Aggregate Features
    for k, v in elements.items(): features[f'Count_{k}'] = v
    for k, v in modes.items(): features[f'Count_{k}'] = v

    return features

def main():
    print("Preparing Dataset...")
    data = []
    labels = []

    for entry in CELEBRITY_DATA:
        if 'category' not in entry: continue

        feats = get_chart_features(entry)
        data.append(feats)
        labels.append(entry['category'])

    df = pd.DataFrame(data)
    y = np.array(labels)

    # Filter small classes
    counts = pd.Series(y).value_counts()
    valid_cats = counts[counts >= 5].index
    mask = pd.Series(y).isin(valid_cats)

    X = df[mask]
    y = y[mask]

    print(f"Dataset Size: {len(X)} samples")
    print(f"Classes: {np.unique(y)}")

    # ENCODER
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    # MODEL
    clf = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42)
    dummy = DummyClassifier(strategy='stratified', random_state=42)

    # EVALUATION (Leave One Out)
    print("\nRunning Leave-One-Out Cross Validation...")
    cv = LeaveOneOut()

    scores = cross_val_score(clf, X, y_enc, cv=cv, scoring='accuracy')
    baseline_scores = cross_val_score(dummy, X, y_enc, cv=cv, scoring='accuracy')

    print("-" * 40)
    print(f"ML Model Accuracy: {scores.mean():.4f}")
    print(f"Random Baseline:   {baseline_scores.mean():.4f}")
    print("-" * 40)

    # Feature Importance analysis (Train on full set)
    clf.fit(X, y_enc)
    importances = clf.feature_importances_

    feat_imp = pd.DataFrame({
        'Feature': X.columns,
        'Importance': importances
    }).sort_values('Importance', ascending=False)

    print("\nTop Predictive Features:")
    print(feat_imp.head(10))

    feat_imp.head(15).to_csv(OUTPUT_DIR / "feature_importance.csv", index=False)

    # Save Results
    with open(OUTPUT_DIR / "ml_profession_results.txt", "w") as f:
        f.write(f"Accuracy: {scores.mean()}\nBaseline: {baseline_scores.mean()}")

    # Visualization of Feature Importance
    plt.figure(figsize=(10, 8))
    sns.barplot(x='Importance', y='Feature', data=feat_imp.head(20))
    plt.title('Top 20 Chart Features for Profession Classification')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "ml_feature_importance.png")
    print(f"Plot saved to {OUTPUT_DIR / 'ml_feature_importance.png'}")

if __name__ == "__main__":
    main()
