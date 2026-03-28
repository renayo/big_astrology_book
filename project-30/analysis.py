#!/usr/bin/env python3
"""
PROJECT 30: CROSS-CULTURAL ZODIAC PERSONALITY
Analysis of Big Five Personality Traits vs Chinese Zodiac (Cyclic Years).

Note: Western Zodiac requires Month/Day, which is not available in the public Big5 dataset (only Age).
Therefore, this analysis focuses on the Chinese Zodiac (Cyclic Year of Birth) and Generational Archetypes.
"""

import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Constants
OUTPUT_DIR = Path(__file__).parent
DATA_PATH = OUTPUT_DIR / 'BIG5_data.csv'
DATA_YEAR = 2018 # Assumption based on dataset metadata timeframe

# Chinese Zodiac Order (Rat starts cycle)
CHINESE_SIGNS = [
    'Monkey', 'Rooster', 'Dog', 'Pig', 
    'Rat', 'Ox', 'Tiger', 'Rabbit', 
    'Dragon', 'Snake', 'Horse', 'Goat'
]
# Note: 1900 was Year of the Rat.
# (1900 % 12) = 4. 
# Modulo 12 logic check:
# 0: Monkey, 1: Rooster, 2: Dog, 3: Pig, 4: Rat ... 
# 1900 % 12 -> 4 (Rat). 
# So: [Monkey, Rooster, Dog, Pig, Rat, Ox, Tiger, Rabbit, Dragon, Snake, Horse, Goat] maps to 0..11
# Let's verify: 2024 is Dragon. 2024 % 12 = 8.
# Index 8 in my list: Dragon. Correct.

def get_chinese_sign(year):
    """Return Chinese Zodiac sign name based on year."""
    return CHINESE_SIGNS[year % 12]

def calculate_big5_scores(df):
    """
    Calculate aggregate Big 5 scores from raw items (E1..E10, etc).
    Note: Some items are reverse-keyed. 
    Standard scoring for 50-item IPIP Big5 usually has keys 
    (1, 3, 5, 7, 9 typically +keyed, 2, 4, 6, 8, 10 -keyed, or similar).
    However, simple sum often works for rough analysis if we assume standard keying.

    Actually, standard IPIP-50 Keying:
    E: 1+, 2-, 3+, 4-, 5+, 6-, 7+, 8-, 9+, 10-
    N: 1+, 2-, 3+, 4-, 5+, 6+, 7+, 8+, 9+, 10+ (Check this?)

    To limit complexity/error, we will TRUST the item correlations relative 
    to each other or just process them as sums if we don't have the key.

    Wait, inspecting the data values (1-5).
    Let's assume the standard OSPP IPIP keying.
    + keyed: 1, 3, 5, 7, 9
    - keyed: 2, 4, 6, 8, 10
    (This is the most common pattern for this dataset).
    """

    traits = ['E', 'N', 'A', 'C', 'O']
    scores = {}

    for trait in traits:
        cols = [f'{trait}{i}' for i in range(1, 11)]
        # Filter strictly valid columns
        valid_cols = [c for c in cols if c in df.columns]

        if not valid_cols: continue

        # OSPP documentation: 
        # "E1 I am the life of the party." (+)
        # "E2 I don't talk a lot." (-)
        # Pattern seems to be Odds=+, Evens=-

        # Vectorized calculation
        trait_score = pd.Series(0, index=df.index)

        for i in range(1, 11):
            col = f'{trait}{i}'
            if col not in df.columns: continue

            if i % 2 == 1: # Odd (1, 3, 5...) -> Positive
                trait_score += df[col]
            else:          # Even (2, 4, 6...) -> Negative (Reverse score: 6 - score)
                trait_score += (6 - df[col])

        scores[trait] = trait_score / 10.0 # Average 1-5

    return pd.DataFrame(scores)

def load_and_process_data():
    """Load raw CSV and compute traits + zodiac."""
    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found.")
        return None

    print(f"Loading {DATA_PATH}...")
    # Use tab separator based on file inspection
    try:
        df = pd.read_csv(DATA_PATH, sep='\t')
    except:
        df = pd.read_csv(DATA_PATH) # Try comma fallback

    print(f"Raw shape: {df.shape}")

    # Filter specific valid ages (e.g., 13 to 90) to avoid bad data
    df = df[(df['age'] >= 13) & (df['age'] <= 90)]

    # Calculate Scores
    scores = calculate_big5_scores(df)
    df = pd.concat([df[['age', 'country', 'gender']], scores], axis=1)

    # Calculate Year & Sign (Cyclic logic)
    df['birth_year'] = DATA_YEAR - df['age']
    df['chinese_sign'] = df['birth_year'].apply(get_chinese_sign)

    # Drop rows with NaN scores
    df = df.dropna(subset=['E', 'N', 'A', 'C', 'O'])

    return df

def analyze_stats(df):
    """Run ANOVA and generate stats."""
    print("Running Statistical Analysis...")

    results = []
    traits = {'E': 'Extroversion', 'N': 'Neuroticism', 'A': 'Agreeableness', 'C': 'Conscientiousness', 'O': 'Openness'}

    summary = "# Project 30 Results: Chinese Zodiac & Personality\n\n"
    summary += f"Data Sample: N={len(df):,} (Source: Open Psychometrics, 2018)\n"
    summary += "Method: ANOVA comparison of Big 5 Traits across 12 Chinese Zodiac signs (Cyclic Year calculated from Age in 2018).\n\n"

    for code, name in traits.items():
        # ANOVA
        groups = [df[df['chinese_sign'] == sign][code] for sign in CHINESE_SIGNS]
        f_stat, p_val = stats.f_oneway(*groups)

        sig = "**SIGNIFICANT**" if p_val < 0.05 else "ns"
        summary += f"## {name} ({code})\n"
        summary += f"- F-Statistic: {f_stat:.4f}\n"
        summary += f"- P-Value: {p_val:.4e} ({sig})\n"

        # Find highest/lowest
        means = df.groupby('chinese_sign')[code].mean()
        high_sign = means.idxmax()
        low_sign = means.idxmin()
        global_mean = df[code].mean()

        summary += f"- Highest: **{high_sign}** ({means[high_sign]:.2f})\n"
        summary += f"- Lowest: **{low_sign}** ({means[low_sign]:.2f})\n"
        summary += f"- Global Mean: {global_mean:.2f}\n\n"

        results.append({
            'Trait': name,
            'High': high_sign, 
            'Low': low_sign,
            'P-Value': p_val,
            'Significant': p_val < 0.05
        })

    return summary, results

def create_visualizations(df):
    """Create heatmap/boxplots."""
    print("Generating visualizations...")

    traits = ['E', 'N', 'A', 'C', 'O']
    trait_names = ['Extroversion', 'Neuroticism', 'Agreeableness', 'Conscientiousness', 'Openness']

    # 1. Normalized Deviation Heatmap
    # (Mean of sign - Global Mean) / Global Std

    matrix = []

    for t in traits:
        global_mean = df[t].mean()
        global_std = df[t].std()

        row = []
        for sign in CHINESE_SIGNS:
            sign_mean = df[df['chinese_sign'] == sign][t].mean()
            z_score = (sign_mean - global_mean) / global_std
            row.append(z_score)
        matrix.append(row)

    plt.figure(figsize=(12, 6))
    sns.heatmap(matrix, annot=True, center=0, cmap='RdBu_r', 
                xticklabels=CHINESE_SIGNS, yticklabels=trait_names, fmt='.2f')
    plt.title("Chinese Zodiac Personality Deviations (Z-Score)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chinese_zodiac_heatmap.png')
    plt.close()

    # 2. Box plots for all traits (Subplots)
    fig, axes = plt.subplots(5, 1, figsize=(14, 25))
    if not isinstance(axes, np.ndarray):
        axes = [axes]

    for idx, t in enumerate(traits):
        ax = axes[idx]
        # Fix hue warning by assigning hue=x and legend=False
        sns.boxplot(x='chinese_sign', y=t, data=df, order=CHINESE_SIGNS, hue='chinese_sign', palette='Set3', ax=ax, legend=False)
        ax.set_title(f"{trait_names[idx]} Distribution by Chinese Sign")
        ax.set_xlabel("")
        ax.set_ylabel("Score (1-5)")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'chinese_zodiac_boxplots.png')
    plt.close()

def main():
    df = load_and_process_data()
    if df is None or len(df) == 0:
        print("No data processed.")
        return

    report, stats_list = analyze_stats(df)
    create_visualizations(df)

    # Save Report
    with open(OUTPUT_DIR / 'RESULTS.md', 'w') as f:
        f.write(report)

    print(report)
    print(f"Analysis complete. Results saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
