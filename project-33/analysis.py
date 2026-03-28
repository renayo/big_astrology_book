#!/usr/bin/env python3
"""
Project 33: Planetary Dignities & Character
Does Essential Dignity (Domicile/Exaltation) correlate with Career Success/Field?
"""

import sys
import pandas as pd
import numpy as np
import swisseph as swe
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime

# Import the data extracted from Project 16
from source_data import CREATIVE_GENIUSES

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path(None)

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN
}

# Dignity Map (Sign Indices 0-11)
# Sign: 0=Ari, 1=Tau, 2=Gem, 3=Can, 4=Leo, 5=Vir, 6=Lib, 7=Sco, 8=Sag, 9=Cap, 10=Aqu, 11=Pis
DIGNITIES = {
    'Sun':    {'Dom': [4], 'Exalt': [0], 'Det': [10], 'Fall': [6]},
    'Moon':   {'Dom': [3], 'Exalt': [1], 'Det': [9], 'Fall': [7]},
    'Mercury':{'Dom': [2, 5], 'Exalt': [5], 'Det': [8, 11], 'Fall': [11]}, # Vir is Dom+Exalt
    'Venus':  {'Dom': [1, 6], 'Exalt': [11], 'Det': [0, 7], 'Fall': [5]},
    'Mars':   {'Dom': [0, 7], 'Exalt': [9], 'Det': [6, 1], 'Fall': [3]},
    'Jupiter':{'Dom': [8, 11], 'Exalt': [3], 'Det': [2, 5], 'Fall': [9]},
    'Saturn': {'Dom': [9, 10], 'Exalt': [6], 'Det': [3, 4], 'Fall': [0]},
}

def get_dignity_score(planet, sign_idx):
    """
    Calculate essential dignity score.
    Simple weighted model: 
    Domicile = +5
    Exaltation = +4
    Detriment = -5
    Fall = -4
    Peregrine = 0
    (Note: If sign is both Dom and Exalt (e.g. Mercury in Virgo), we sum them? 
    Tradition says Virgo is own domicile and exaltation. Usually considered very strong. 
    Let's sum them: 5+4=9.
    Same for debilities? Mercury in Pisces is Detriment and Fall. -5 + -4 = -9.)
    """
    rules = DIGNITIES[planet]
    score = 0

    if sign_idx in rules['Dom']: score += 5
    if sign_idx in rules['Exalt']: score += 4
    if sign_idx in rules['Det']: score -= 5
    if sign_idx in rules['Fall']: score -= 4

    return score

def get_dignity_label(planet, sign_idx):
    rules = DIGNITIES[planet]
    labels = []
    if sign_idx in rules['Dom']: labels.append("Domicile")
    if sign_idx in rules['Exalt']: labels.append("Exaltation")
    if sign_idx in rules['Det']: labels.append("Detriment")
    if sign_idx in rules['Fall']: labels.append("Fall")

    if not labels: return "Peregrine"
    return "/".join(labels)

def get_julian_day(date_str, time_str):
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        # Handle cases with seconds or weird formats if any
        try:
             dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
        except:
             # Fallback to noon
             dt = datetime.strptime(date_str, "%Y-%m-%d")
             dt = dt.replace(hour=12)

    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0)

def analyze_chart(name, date, time, field):
    jd = get_julian_day(date, time)

    row = {
        'name': name,
        'occupation': field,
    }

    total_score = 0

    for planet, pid in PLANETS.items():
        res = swe.calc_ut(jd, pid)[0][0]
        sign_idx = int(res / 30) % 12

        score = get_dignity_score(planet, sign_idx)
        label = get_dignity_label(planet, sign_idx)

        row[f'{planet}_Sign'] = SIGNS[sign_idx]
        row[f'{planet}_Score'] = score
        row[f'{planet}_Dignity'] = label

        total_score += score

    row['Total_Dignity'] = total_score
    return row

def main():
    print("Project 33: Planetary Dignities Analysis")
    print("-" * 50)

    data = []
    for entry in CREATIVE_GENIUSES:
        # Entry: (Name, Date, Time, Field, Achievement)
        data.append(analyze_chart(entry[0], entry[1], entry[2], entry[3]))

    df = pd.DataFrame(data)

    # Save processed data
    df.to_csv(OUTPUT_DIR / 'dignities_analyzed.csv', index=False)
    print(f"Analyzed {len(df)} charts.")

    # --- Statistical Analysis ---

    # Hypotheses:
    # 1. Scientists have strong Saturn or Mercury?
    # 2. Artists have strong Venus?
    # 3. Writers have strong Mercury?
    # 4. Leaders/Filmmakers have strong Sun?

    print("\n--- Average Dignity Scores by Occupation ---")
    score_cols = [f'{p}_Score' for p in PLANETS.keys()]
    grouped = df.groupby('occupation')[score_cols].mean()
    print(grouped.round(2))

    # Test Significance
    print("\n--- Significance Tests (T-Test vs Rest of Population) ---")
    results = []

    occupations = df['occupation'].unique()
    for occ in occupations:
        occ_df = df[df['occupation'] == occ]
        rest_df = df[df['occupation'] != occ]

        print(f"\nOccupation: {occ.upper()} (n={len(occ_df)})")

        for planet in PLANETS.keys():
            col = f'{planet}_Score'
            t_stat, p_val = stats.ttest_ind(occ_df[col], rest_df[col], equal_var=False)

            diff = occ_df[col].mean() - rest_df[col].mean()
            if p_val < 0.10: # Loose threshold for initial scan
                sig = "**" if p_val < 0.05 else "*"
                print(f"  {planet}: Diff={diff:+.2f}, p={p_val:.4f} {sig}")

                results.append({
                    'Occupation': occ,
                    'Planet': planet,
                    'Mean_Occ': occ_df[col].mean(),
                    'Mean_Rest': rest_df[col].mean(),
                    'Diff': diff,
                    'P_Value': p_val
                })

    # --- Visualization ---
    create_plots(df, results)

    # --- Generate Report ---
    generate_report(df, results)

def create_plots(df, results_list):
    # 1. Heatmap of Average Scores
    score_cols = [f'{p}_Score' for p in PLANETS.keys()]
    global_mean = df[score_cols].mean()

    # Calculate difference from global mean for each occupation
    grouped = df.groupby('occupation')[score_cols].mean()
    diff_matrix = grouped - global_mean

    plt.figure(figsize=(10, 6))
    sns.heatmap(diff_matrix, cmap='RdBu_r', center=0, annot=True, fmt='.2f')
    plt.title('Dignity Score Deviation by Occupation\n(Positive = Higher Dignity than Average)')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'dignity_heatmap.png')
    plt.close()

    # 2. Distro of Total Dignity
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df, x='Total_Dignity', hue='occupation', fill=False)
    plt.title('Distribution of Total Chart Dignity by Occupation')
    plt.savefig(OUTPUT_DIR / 'total_dignity_dist.png')
    plt.close()

def generate_report(df, results):
    with open(OUTPUT_DIR / 'RESULTS.md', 'w') as f:
        f.write("# Project 33: Planetary Dignities & Character\n\n")
        f.write("## Overview\n")
        f.write(f"Analyzed **{len(df)}** charts of historical figures for Essential Dignity (Domicile/Exaltation vs Detriment/Fall).\n")
        f.write("Does the 'strength' of a planet correlate with career choice?\n\n")

        f.write("## Scoring System\n")
        f.write("- **Domicile**: +5\n")
        f.write("- **Exaltation**: +4\n")
        f.write("- **Peregrine**: 0\n")
        f.write("- **Detriment**: -5\n")
        f.write("- **Fall**: -4\n\n")

        f.write("## Significant Findings (P < 0.10)\n")
        f.write("| Occupation | Planet | Mean Score | Vs Rest | Diff | P-Value |\n")
        f.write("|---|---|---|---|---|---|\n")

        results.sort(key=lambda x: x['P_Value'])
        for r in results:
            sig = "**" if r['P_Value'] < 0.05 else ""
            f.write(f"| {r['Occupation']} | {r['Planet']} | {r['Mean_Occ']:.2f} | {r['Mean_Rest']:.2f} | {r['Diff']:+.2f} | {sig}{r['P_Value']:.4f}{sig} |\n")

        f.write("\n## Interpretation\n")
        # Add dynamic interpretation
        strongest = results[0] if results else None
        if strongest and strongest['P_Value'] < 0.05:
            f.write(f"The most significant finding is **{strongest['Occupation']} and {strongest['Planet']}** (Diff: {strongest['Diff']:.2f}). ")
            if strongest['Diff'] > 0:
                f.write(f"This group has significantly stronger {strongest['Planet']} placement than average.\n")
            else:
                f.write(f"This group actually has WEAKER {strongest['Planet']} placement than average (Debility?).\n")
        else:
            f.write("No extremely strong correlations (p<0.05) were found, suggesting that classical dignity scores alone may not determine career field.\n")

if __name__ == "__main__":
    main()
