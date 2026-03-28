#!/usr/bin/env python3
"""
Project 7: Planetary Cycles & Personality (Cyclic Analysis)
===========================================================
Tests whether "Cyclic Age" (Planetary Phases) predicts personality
better than "Linear Age" (Maturation).

HYPOTHESIS:
User specifically requested: "compute age as measure of cyclicity... instead of age bands".
We test if planetary life-cycles (Saturn Return, Jupiter Return) correlate with Big 5 traits.

METHODOLOGY:
1. Load OSPP Big Five Data (N ~ 20,000).
2. Compute Cyclic Features from Age:
   - Saturn Phase (29.46 yr cycle)
   - Jupiter Phase (11.86 yr cycle)
   - Lunar Node Phase (18.6 yr cycle)
3. Encode as Sin/Cos components for ML.
4. Compare Models:
   - Model A (Linear Age Only): Trait ~ Age
   - Model B (Linear + Cyclic): Trait ~ Age + Saturn_Sin + Saturn_Cos...
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

OUTPUT_DIR = Path(__file__).parent
OUTPUT_DIR.mkdir(exist_ok=True)
DATA_FILE = OUTPUT_DIR / "BIG5_data.csv"

# Planetary Cycles (Years)
CYCLES = {
    'Sun': 1.000,       # 1 Year (Solar Return)
    'Moon': 0.0748,     # 27.3 Days (Sidereal) - Aliased in annual data
    'Mercury': 0.241,   # 88 Days
    'Venus': 0.615,     # 225 Days
    'Mars': 1.881,      # 687 Days
    'Jupiter': 11.862,
    'Saturn': 29.457,
    'Nodes': 18.61,  # Nodal Cycle
    'Uranus': 84.02
}

def load_data():
    if not DATA_FILE.exists():
        print("Data file not found. Running downloader...")
        # (Assuming the original analysis.py ran and downloaded it. If not, we'd need to re-implement download)
        raise FileNotFoundError(f"Please run the original analysis.py first to download {DATA_FILE}")

    print(f"Loading {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE, sep='\t')

    # Process Age
    df = df[df['age'].between(13, 90)] # Filter reasonable ages

    # Calculate Big 5 Scores (Summing items, handling reverse coding)
    # Reverse keys based on OSPP codebook
    reverse_keyed = {
        'E': [2, 4, 6, 8, 10], 'N': [2, 4], 'A': [1, 3, 5, 7], 
        'C': [2, 4, 6, 8], 'O': [2, 4, 6]
    }

    traits = ['E', 'N', 'A', 'C', 'O']
    for t in traits:
        items = [f'{t}{i}' for i in range(1, 11)]
        # Check if columns exist
        if not all(col in df.columns for col in items):
            continue

        # Compute score
        score = pd.Series(0, index=df.index)
        for i in range(1, 11):
            col = f'{t}{i}'
            val = df[col]
            if i in reverse_keyed[t]:
                val = 6 - val # Reverse 1-5 scale
            score += val

        df[f'Score_{t}'] = score

    return df.dropna(subset=[f'Score_{t}' for t in traits])

def add_cyclic_features(df):
    """Add Sin/Cos features for each planetary cycle."""
    for planet, period in CYCLES.items():
        # Phase (0 to 2pi)
        phase = (df['age'] / period * 2 * np.pi)

        df[f'{planet}_Sin'] = np.sin(phase)
        df[f'{planet}_Cos'] = np.cos(phase)

        # Also store raw phase (0-1) for plotting
        df[f'{planet}_Phase'] = (df['age'] % period) / period

    return df

def analyze_model_performance(df, trait):
    """Compare Linear vs Cyclic models."""
    X_linear = df[['age']].values

    # Cyclic features: Age + Sin/Cos of all planets
    cyclic_cols = ['age'] + [c for c in df.columns if '_Sin' in c or '_Cos' in c]
    X_cyclic = df[cyclic_cols].values

    y = df[trait].values

    # Cross Validation
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    # Using Random Forest to capture non-linear peaks (e.g. Mid-Life Crisis)
    # But Linear Regression is better to test "adding waves". 
    # Let's use Random Forest Regressor for general "Predictability"

    model = RandomForestRegressor(n_estimators=100, min_samples_leaf=50, random_state=42)

    score_linear = np.mean(cross_val_score(model, X_linear, y, cv=kf, scoring='r2'))
    score_cyclic = np.mean(cross_val_score(model, X_cyclic, y, cv=kf, scoring='r2'))

    return score_linear, score_cyclic

def plot_cycle_effect(df, trait, planet):
    """Plot Trait Score vs Phase of Planet."""
    plt.figure(figsize=(10, 6))

    # Bin by phase
    df['phase_bin'] = pd.cut(df[f'{planet}_Phase'], bins=20, labels=False)
    means = df.groupby('phase_bin')[trait].mean()
    sems = df.groupby('phase_bin')[trait].sem()

    # x-axis scaled to cycle years
    x_vals = np.linspace(0, CYCLES[planet], 20)

    plt.errorbar(x_vals, means, yerr=sems, fmt='o-', capsize=5)
    plt.title(f"{trait} vs {planet} Cycle ({CYCLES[planet]} yr)")
    plt.xlabel(f"Years into Cycle (0 to {CYCLES[planet]})")
    plt.ylabel(f"Mean {trait} Score")
    plt.grid(True, alpha=0.3)

    out_file = OUTPUT_DIR / f"cycle_{planet}_{trait}.png"
    plt.savefig(out_file)
    plt.close()

def main():
    print("Loading valid OSPP data...")
    try:
        df = load_data()
    except Exception as e:
        print(f"Error: {e}")
        return

    print(f"N={len(df)}")

    # Add features
    df = add_cyclic_features(df)

    print("\nCOMPARING MODELS (R-Squared): Linear Age vs Cyclic Age")
    print("-" * 60)
    print(f"{'Trait':<20} {'Linear Age':<15} {'Cyclic Age':<15} {'Improvement':<15}")
    print("-" * 60)

    traits = {
        'Score_E': 'Extraversion',
        'Score_N': 'Neuroticism',
        'Score_A': 'Agreeableness',
        'Score_C': 'Conscientiousness',
        'Score_O': 'Openness' 
    }

    results = []

    for col, name in traits.items():
        base, cyclic = analyze_model_performance(df, col)
        imp = cyclic - base
        print(f"{name:<20} {base:.4f}          {cyclic:.4f}          {imp:+.4f}")

        results.append({
            'Trait': name,
            'R2_Linear': base,
            'R2_Cyclic': cyclic,
            'Improvement': imp
        })

        # Plot Saturn for Conscientiousness (Saturn = Maturity/Discipline)
        if name == 'Conscientiousness':
            plot_cycle_effect(df, col, 'Saturn')

        # Plot Jupiter for Openness?
        if name == 'Openness':
            plot_cycle_effect(df, col, 'Jupiter')

        # Plot Mars for Extraversion (Mars = Energy)
        if name == 'Extraversion':
            plot_cycle_effect(df, col, 'Mars')

    pd.DataFrame(results).to_csv(OUTPUT_DIR / "age_cyclic_results.csv", index=False)
    print("\nanalysis saved to age_cyclic_results.csv")

if __name__ == "__main__":
    main()
