#!/usr/bin/env python3
"""
Project 10 (v4): Cosine Synastry Analysis
=========================================
Instead of discrete aspect buckets (Conjunction, Trine, Square...),
we use a CONTINUOUS measure: cos(angle_difference).

This is agnostic to traditional orbs and captures "closeness" as:
- cos(0°) = +1.0 (Conjunction - maximum alignment)
- cos(90°) = 0.0 (Square - orthogonal)
- cos(180°) = -1.0 (Opposition - maximum tension)

We calculate this for ALL planet pairs (11x11 = 121 features) and use
them to predict the binary Married/Divorced state via Logistic Regression.
"""

import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
from datetime import datetime
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import random

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path(None)

# Import celebrity data from the main analysis file
from analysis import CELEBRITY_BIRTHS, CELEBRITY_RELATIONSHIPS, generate_extended_couples

# Planets to analyze (including Nodes)
PLANETS = {
    swe.SUN: 'Sun',
    swe.MOON: 'Moon', 
    swe.MERCURY: 'Mercury',
    swe.VENUS: 'Venus',
    swe.MARS: 'Mars',
    swe.JUPITER: 'Jupiter',
    swe.SATURN: 'Saturn',
    swe.URANUS: 'Uranus',
    swe.NEPTUNE: 'Neptune',
    swe.PLUTO: 'Pluto',
    swe.MEAN_NODE: 'Rahu'  # North Node
}

def get_full_positions(jd):
    """Get positions (0-360°) for all planets including Rahu/Ketu."""
    pos = {}
    for pid, name in PLANETS.items():
        result = swe.calc_ut(jd, pid)[0][0]
        pos[name] = result

        # Ketu is opposite Rahu
        if name == 'Rahu':
            pos['Ketu'] = (result + 180) % 360

    return pos

def datetime_to_jd(dt):
    hour = dt.hour + dt.minute/60.0 if hasattr(dt, 'hour') else 12.0
    return swe.julday(dt.year, dt.month, dt.day, hour)

def calculate_cosine_features(pos1, pos2):
    """
    Calculate cos(angle_diff) for each planet pair.
    Returns dict with feature names like 'cos_Sun_Moon', 'cos_Venus_Mars', etc.
    """
    features = {}

    planet_names = list(pos1.keys())  # Sun, Moon, Mercury... Rahu, Ketu

    for p1 in planet_names:
        for p2 in planet_names:
            # Angle difference (shortest arc)
            diff = pos1[p1] - pos2[p2]

            # Cosine of the angle difference (in radians)
            cos_val = np.cos(np.deg2rad(diff))

            features[f'cos_{p1}_{p2}'] = cos_val

    return features

def prepare_dataset():
    """Build the dataset with cosine features."""
    print("Building Cosine Feature Dataset...")

    # Get all relationships
    extended = generate_extended_couples()
    all_relationships = list(CELEBRITY_RELATIONSHIPS) + extended

    records = []
    skipped = 0

    for rel in all_relationships:
        p1_name, p2_name, married_year, status, duration = rel

        # Get birth data
        if p1_name not in CELEBRITY_BIRTHS or p2_name not in CELEBRITY_BIRTHS:
            skipped += 1
            continue

        b1 = CELEBRITY_BIRTHS[p1_name]
        b2 = CELEBRITY_BIRTHS[p2_name]

        try:
            dt1 = datetime.strptime(f"{b1[0]} {b1[1]}", "%Y-%m-%d %H:%M")
            dt2 = datetime.strptime(f"{b2[0]} {b2[1]}", "%Y-%m-%d %H:%M")
        except:
            skipped += 1
            continue

        jd1 = datetime_to_jd(dt1)
        jd2 = datetime_to_jd(dt2)

        pos1 = get_full_positions(jd1)
        pos2 = get_full_positions(jd2)

        cos_features = calculate_cosine_features(pos1, pos2)

        # Binary outcome
        is_married = 1 if status in ['married', 'together', 'engaged'] else 0

        records.append({
            'couple': f"{p1_name} & {p2_name}",
            'is_married': is_married,
            'duration': duration,
            **cos_features
        })

    print(f"Generated {len(records)} records ({skipped} skipped)")
    return pd.DataFrame(records)

def run_classification(df):
    """Run classification using cosine features."""
    print("\n" + "=" * 70)
    print("COSINE SYNASTRY CLASSIFICATION: Married vs Divorced")
    print("=" * 70)

    # Features are all cos_* columns
    feature_cols = [c for c in df.columns if c.startswith('cos_')]
    X = df[feature_cols].values
    y = df['is_married'].values

    print(f"Features: {len(feature_cols)} (11x11 planet pairs)")
    print(f"Samples: {len(y)} (Married: {y.sum()}, Divorced: {len(y) - y.sum()})")

    # Baseline
    baseline = max(y.mean(), 1 - y.mean())
    print(f"\nBaseline Accuracy (Always guess majority): {baseline:.1%}")

    # Model 1: Logistic Regression
    print("\n--- LOGISTIC REGRESSION ---")
    clf_lr = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(max_iter=1000, random_state=42))
    ])

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores_lr = cross_val_score(clf_lr, X, y, cv=cv, scoring='accuracy')
    print(f"CV Accuracy: {scores_lr.mean():.1%} ± {scores_lr.std():.1%}")

    # Model 2: Random Forest
    print("\n--- RANDOM FOREST ---")
    clf_rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
    scores_rf = cross_val_score(clf_rf, X, y, cv=cv, scoring='accuracy')
    print(f"CV Accuracy: {scores_rf.mean():.1%} ± {scores_rf.std():.1%}")

    # Feature Importance (from full fit)
    clf_rf.fit(X, y)
    importances = clf_rf.feature_importances_

    # Top 20 features
    top_idx = np.argsort(importances)[::-1][:20]

    print("\n--- TOP 20 PREDICTIVE FEATURES ---")
    print(f"{'Feature':<25} | {'Importance':<10}")
    print("-" * 40)
    for idx in top_idx:
        print(f"{feature_cols[idx]:<25} | {importances[idx]:.4f}")

    # Correlation Analysis: Which cosine features correlate with staying married?
    print("\n--- CORRELATION WITH MARRIAGE SURVIVAL ---")
    print(f"{'Feature':<25} | {'Correlation':<10} | {'P-Value':<10}")
    print("-" * 55)

    correlations = []
    for col in feature_cols:
        r, p = stats.pearsonr(df[col], df['is_married'])
        correlations.append((col, r, p))

    # Sort by absolute correlation
    correlations.sort(key=lambda x: abs(x[1]), reverse=True)

    for col, r, p in correlations[:20]:
        sig = "*" if p < 0.05 else ""
        print(f"{col:<25} | {r:+.4f}     | {p:.4f} {sig}")

    return scores_lr, scores_rf, correlations

def main():
    df = prepare_dataset()

    # Save the dataset
    df.to_csv(OUTPUT_DIR / 'cosine_synastry_data.csv', index=False)

    # Run classification
    scores_lr, scores_rf, correlations = run_classification(df)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Logistic Regression: {np.mean(scores_lr):.1%}")
    print(f"Random Forest: {np.mean(scores_rf):.1%}")
    print(f"Baseline: {max(df['is_married'].mean(), 1-df['is_married'].mean()):.1%}")

    # Find any significant correlations
    sig_corrs = [(c, r, p) for c, r, p in correlations if p < 0.05]
    print(f"\nSignificant Correlations (p<0.05): {len(sig_corrs)}")

    if sig_corrs:
        print("Top 5 Significant:")
        for c, r, p in sig_corrs[:5]:
            direction = "LONGER" if r > 0 else "SHORTER"
            print(f"  {c}: r={r:+.4f} (couples with high cosine stay {direction})")

if __name__ == "__main__":
    main()
