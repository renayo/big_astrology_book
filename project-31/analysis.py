#!/usr/bin/env python3
"""
Project 31: Planetary Patterns and Disease Outbreaks
Metric: Cosine of Planetary Angle Differences (12 Bodies)
Bodies: Sun, Moon, Rahu, Ketu, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto
"""

import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
import math

OUTPUT_DIR = Path(__file__).parent
if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir()

# Ensure ephemeris is available or set to None (moshier fallback)
swe.set_ephe_path(None)

# --- Configuration ---
START_YEAR = 1900
END_YEAR = 2025

# List of major 20th/21st century pandemics/epidemics
OUTBREAKS = {
    1918: "Spanish Flu",
    1919: "Spanish Flu (Cont)",
    1957: "Asian Flu",
    1968: "Hong Kong Flu",
    1981: "HIV/AIDS Emergence",
    2002: "SARS (Early)",
    2003: "SARS",
    2009: "Swine Flu (H1N1)",
    2014: "Ebola (West Africa)",
    2019: "COVID-19 (Start)",
    2020: "COVID-19 (Peak)",
    2021: "COVID-19 (Delta/Omicron)",
    1920: "Cholera (Major)", 
}

# 12 Bodies as requested
BODY_IDS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO,
    'Rahu': swe.MEAN_NODE,
    # Ketu is derived
}

ORDERED_BODIES = [
    'Sun', 'Moon', 'Rahu', 'Ketu', 'Mercury', 'Venus', 
    'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto'
]

def get_planet_positions(year):
    """
    Calculate positions for mid-year (July 1st).
    Note: Fast moving bodies (Moon, Sun, Mercury...) will use the Noon position on July 1st.
    """
    jd = swe.julday(year, 7, 1, 12.0)

    positions = {}
    for name, pid in BODY_IDS.items():
        res = swe.calc_ut(jd, pid)
        positions[name] = res[0][0] # Longitude

    # Calculate Ketu (Rahu + 180)
    positions['Ketu'] = (positions['Rahu'] + 180.0) % 360.0

    return positions

def get_angular_cosine(pos1, pos2):
    """
    Calculate cosine of angular difference.
    Range: [-1, 1]
    1 = Conjunction, 0 = Square, -1 = Opposition
    """
    diff = abs(pos1 - pos2)
    rad = math.radians(diff)
    return math.cos(rad)

def analyze_year(year):
    """Analyze planetary data for a specific year."""
    pos = get_planet_positions(year)

    data = {
        'year': year,
        'is_outbreak': year in OUTBREAKS,
        'outbreak_name': OUTBREAKS.get(year, "None"),
    }

    # Calculate all pairs of the 12 bodies
    for i in range(len(ORDERED_BODIES)):
        for j in range(i + 1, len(ORDERED_BODIES)):
            p1 = ORDERED_BODIES[i]
            p2 = ORDERED_BODIES[j]
            pair_name = f"{p1}-{p2}"

            val = get_angular_cosine(pos[p1], pos[p2])
            data[f"{pair_name}_cos"] = val

    return data

def main():
    print("Project 31: Analyzing Planetary-Pandemic Correlations (12-Body Cosine)...")

    records = []
    for year in range(START_YEAR, END_YEAR + 1):
        records.append(analyze_year(year))

    df = pd.DataFrame(records)

    # --- Statistical Analysis ---
    pair_cols = [c for c in df.columns if c.endswith('_cos')]
    results = []

    print(f"\nAnalyzing {len(pair_cols)} planetary pairs...")
    print(f"{'Pair':<20} | {'Outbreak Mean':<10} | {'Control Mean':<10} | {'P-Value':<8}")
    print("-" * 65)

    for col in pair_cols:
        pair = col.replace('_cos', '')

        # Split groups
        out_vals = df[df['is_outbreak']][col]
        ctrl_vals = df[~df['is_outbreak']][col]

        # T-Test (Independent samples)
        # H0: Means are equal
        t_stat, p_val = stats.ttest_ind(out_vals, ctrl_vals, equal_var=False)

        # Filter for printing to reduce noise? No, print significant ones.
        if p_val < 0.10:
            print(f"{pair:<20} | {out_vals.mean():.4f}     | {ctrl_vals.mean():.4f}     | {p_val:.4f} *")

        results.append({
            'Pair': pair,
            'Outbreak_Mean': out_vals.mean(),
            'Control_Mean': ctrl_vals.mean(),
            'Diff': out_vals.mean() - ctrl_vals.mean(), # Positive = More Conjunct during outbreaks
            'P_Value': p_val,
            'T_Stat': t_stat
        })

    # --- Visualization ---
    create_visualization(df, results)

    # Save Data
    df.to_csv(OUTPUT_DIR / 'analysis_data_12body_cosine.csv', index=False)

    # Report
    generate_report(df, results)

def create_visualization(df, results):
    print("Generating visualizations...")
    results.sort(key=lambda x: x['P_Value'])

    # 1. Top 20 Most Significant Deviations
    top_20 = results[:20]
    res_df = pd.DataFrame(top_20)

    plt.figure(figsize=(12, 10))
    sns.barplot(data=res_df, x='Diff', y='Pair', palette='vlag')
    plt.title('Top 20 Cosine Differences (Outbreak - Control)\nLeft (Blue) = More Opposed | Right (Red) = More Conjunct')
    plt.axvline(0, color='black', linewidth=1)
    plt.xlabel('Difference in Mean Cosine')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'cosine_diff_top20.png')
    plt.close()

    # 2. Heatmap of Outbreak Years for Significant Pairs (P < 0.10)
    sig_pairs = [r['Pair'] for r in results if r['P_Value'] < 0.10]
    if sig_pairs:
        # Limit to top 30 to prevent clutter if many are significant
        sig_pairs = sig_pairs[:30]
        cols = [f"{p}_cos" for p in sig_pairs]

        outbreak_df = df[df['is_outbreak']].set_index('year')

        plt.figure(figsize=(14, 10))
        sns.heatmap(outbreak_df[cols], cmap='coolwarm', center=0, vmin=-1, vmax=1,
                   cbar_kws={'label': 'Cosine (1=Conj, -1=Opp)'})
        plt.title('Heatmap: Significant Pairs during Outbreak Years')
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / 'outbreak_sig_heatmap.png')
        plt.close()

def generate_report(df, results):
    with open(OUTPUT_DIR / 'RESULTS_COSINE.md', 'w') as f:
        f.write("# Project 31: 12-Body Cosine Analysis Results\n\n")
        f.write("## Methodology\n")
        f.write("Calculated the cosine of the angular difference for all pairs of the following 12 bodies:\n")
        f.write(", ".join(ORDERED_BODIES) + "\n\n")
        f.write("- **Analysis Type**: Full Century Control (1900-2025)\n")
        f.write(f"- **Outbreak Years**: {df['is_outbreak'].sum()}\n")
        f.write(f"- **Control Years**: {(~df['is_outbreak']).sum()}\n\n")

        f.write("## Statistical Significance (T-Test)\n")
        f.write("Pairs with P-Value < 0.10:\n\n")
        f.write("| Pair | Outbreak Mean | Control Mean | Diff | P-Value |\n")
        f.write("|---|---|---|---|---|\n")

        # Sort by P-Value
        results.sort(key=lambda x: x['P_Value'])

        count_sig = 0
        for res in results:
            if res['P_Value'] < 0.10:
                count_sig += 1
                sig_mark = "**" if res['P_Value'] < 0.05 else ""
                f.write(f"| {res['Pair']} | {res['Outbreak_Mean']:.3f} | {res['Control_Mean']:.3f} | {res['Diff']:+.3f} | {sig_mark}{res['P_Value']:.4f}{sig_mark} |\n")

        if count_sig == 0:
            f.write("| None | - | - | - | - |\n")

        f.write(f"\nTotal Pairs Analyzed: {len(results)}\n")

if __name__ == "__main__":
    main()
