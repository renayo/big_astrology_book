#!/usr/bin/env python3
"""
Project 31: Planetary Patterns and Disease Outbreaks
Comparative analysis of outer planetary cycles during major historical epidemics 
vs. non-epidemic years (full century control group).
"""

import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns

OUTPUT_DIR = Path(__file__).parent
if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir()

# Ensure ephemeris is available or set to None (moshier fallback)
# Using standard path usually available or None
swe.set_ephe_path(None)

# --- Configuration ---
START_YEAR = 1900
END_YEAR = 2025

# List of major 20th/21st century pandemics/epidemics
# Source: WHO, CDC historical records
# Format: Name, Start Year
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

# Planets to analyze
PLANETS = {
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO
}

# Aspects to check (Harmonic 1, 2, 4 mainly for "Hard" aspects)
# Orbs are wide for mundane astrology (often 6-8 degrees, sometimes 10)
ASPECTS = {
    'Conjunction': {'angle': 0, 'orb': 8},
    'Opposition': {'angle': 180, 'orb': 8},
    'Square': {'angle': 90, 'orb': 8},
}

def get_planet_positions(year):
    """Calculate positions for mid-year (July 1st)."""
    # Using mid-year as proxy for the "Year's Quality"
    jd = swe.julday(year, 7, 1, 12.0)

    positions = {}
    for name, pid in PLANETS.items():
        res = swe.calc_ut(jd, pid)
        positions[name] = res[0][0] # Longitude
    return positions

def get_angular_separation(pos1, pos2):
    """Calculate shortest distance between two points on circle."""
    diff = abs(pos1 - pos2)
    if diff > 180:
        diff = 360 - diff
    return diff

def check_aspect(angle, aspect_def):
    """Check if angle is within orb of aspect."""
    target = aspect_def['angle']
    orb = aspect_def['orb']
    return abs(angle - target) <= orb

def analyze_year(year):
    """Analyze planetary data for a specific year."""
    pos = get_planet_positions(year)

    # Calculate all pairs
    planet_names = list(PLANETS.keys())
    data = {
        'year': year,
        'is_outbreak': year in OUTBREAKS,
        'outbreak_name': OUTBREAKS.get(year, "None"),
        'hard_aspect_count': 0
    }

    pairs = []
    for i in range(len(planet_names)):
        for j in range(i + 1, len(planet_names)):
            p1 = planet_names[i]
            p2 = planet_names[j]
            pair_name = f"{p1}-{p2}"

            angle = get_angular_separation(pos[p1], pos[p2])
            data[f"{pair_name}_angle"] = angle

            # Check for hard aspects
            is_hard = False
            aspect_type = "None"

            for asp_name, asp_params in ASPECTS.items():
                if check_aspect(angle, asp_params):
                    is_hard = True
                    aspect_type = asp_name
                    break

            data[f"{pair_name}_aspect"] = aspect_type
            if is_hard:
                data['hard_aspect_count'] += 1

    return data

def main():
    print("Project 31: Analyzing Planetary-Pandemic Correlations...")

    records = []
    for year in range(START_YEAR, END_YEAR + 1):
        records.append(analyze_year(year))

    df = pd.DataFrame(records)

    # --- Statistical Analysis ---

    # 1. Compare Hard Aspect Counts
    outbreak_mean = df[df['is_outbreak']]['hard_aspect_count'].mean()
    control_mean = df[~df['is_outbreak']]['hard_aspect_count'].mean()

    t_stat, p_val = stats.ttest_ind(
        df[df['is_outbreak']]['hard_aspect_count'],
        df[~df['is_outbreak']]['hard_aspect_count']
    )

    print("\n--- Hard Aspect Frequencies (Outer Planets) ---")
    print(f"Outbreak Years (N={df['is_outbreak'].sum()}): Mean = {outbreak_mean:.2f} aspects")
    print(f"Control Years  (N={(~df['is_outbreak']).sum()}): Mean = {control_mean:.2f} aspects")
    print(f"T-Test: t={t_stat:.2f}, p={p_val:.4f}")

    # 2. Specific Pair Analysis using Chi-Square
    print("\n--- Specific Pair Correlations (Hard Aspects) ---")
    pairs = [c.replace('_aspect', '') for c in df.columns if c.endswith('_aspect')]

    significance_results = []

    for pair in pairs:
        # Create contingency table
        #           Aspect  NoAspect
        # Outbreak    A       B
        # Control     C       D

        has_aspect = df[f"{pair}_aspect"] != "None"

        # Build 2x2 manually to avoid crosstab missing row/col issues
        # Row 1: Outbreak=True,  Col 1: Aspect=True
        a = len(df[(df['is_outbreak'] == True) & (has_aspect == True)])
        # Row 1: Outbreak=True,  Col 0: Aspect=False
        b = len(df[(df['is_outbreak'] == True) & (has_aspect == False)])
        # Row 0: Outbreak=False, Col 1: Aspect=True
        c = len(df[(df['is_outbreak'] == False) & (has_aspect == True)])
        # Row 0: Outbreak=False, Col 0: Aspect=False
        d = len(df[(df['is_outbreak'] == False) & (has_aspect == False)])

        obs = np.array([[a, b], [c, d]])

        try:
            # Check for zero rows/cols which break chi2_contingency if expectations are 0
            # If any row or col sum is 0, we can't do chi2 properly.
            if obs.sum(axis=0).min() == 0 or obs.sum(axis=1).min() == 0:
                 # Degenerate case
                 p = 1.0
            else:
                 chi2, p, dof, ex = stats.chi2_contingency(obs)

            # Rate calc
            o_rate = a / (a + b) if (a + b) > 0 else 0
            c_rate = c / (c + d) if (c + d) > 0 else 0

            ratio = o_rate / c_rate if c_rate > 0 else 0

            sig = "**SIGNIFICANT**" if p < 0.10 else "ns" # Using 0.10 for exploratory
            print(f"{pair:<15}: Ratio={ratio:.2f}x, p={p:.4f} {sig}")

            significance_results.append({
                'Pair': pair,
                'Outbreak_Rate': o_rate,
                'Control_Rate': c_rate,
                'P_Value': p
            })

        except Exception as e:
            print(f"{pair}: Error {e}")
            significance_results.append({
                'Pair': pair,
                'Outbreak_Rate': 0,
                'Control_Rate': 0,
                'P_Value': 1.0
            })

    # --- Visualization ---
    create_plots(df, significance_results)

    # Save Data
    df.to_csv(OUTPUT_DIR / 'analysis_data_full_century.csv', index=False)

    # Generate Report
    generate_report(df, significance_results, outbreak_mean, control_mean, p_val)

def create_plots(df, sig_results):
    print("Generating visualizations...")

    # 1. Hard Aspect Count Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='hard_aspect_count', hue='is_outbreak', 
                 element="step", stat="density", common_norm=False, palette=['blue', 'red'])
    plt.title('Distribution of Outer Planet Hard Aspects: Outbreak vs Control Years')
    plt.xlabel('Number of Simultaneous Hard Aspects')
    plt.savefig(OUTPUT_DIR / 'hard_aspect_distribution.png')
    plt.close()

    # 2. Pair Significance
    sig_df = pd.DataFrame(sig_results).sort_values('P_Value')
    plt.figure(figsize=(12, 8))

    # Melt for grouped bar chart
    plot_data = sig_df.melt(id_vars=['Pair', 'P_Value'], 
                           value_vars=['Outbreak_Rate', 'Control_Rate'],
                           var_name='Group', value_name='Rate')

    sns.barplot(data=plot_data, x='Rate', y='Pair', hue='Group', palette=['red', 'blue'])
    plt.title('Frequency of Hard Aspects by Planetary Pair')
    plt.axvline(x=0.05, color='gray', linestyle='--', alpha=0.5) 
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'pair_significance.png')
    plt.close()

    # 3. Timeline of Aspect Index vs Outbreaks
    plt.figure(figsize=(15, 6))
    plt.plot(df['year'], df['hard_aspect_count'], color='gray', alpha=0.5, label='Aspect Count')

    # Highlight outbreaks
    outbreaks = df[df['is_outbreak']]
    plt.scatter(outbreaks['year'], outbreaks['hard_aspect_count'], color='red', zorder=5, label='Outbreak')

    plt.title('Timeline: Outer Planet Hard Aspect Density (1900-2025)')
    plt.xlabel('Year')
    plt.ylabel('Count of Hard Aspects')
    plt.legend()
    plt.savefig(OUTPUT_DIR / 'timeline_aspects.png')
    plt.close()

def generate_report(df, sig_results, out_mean, ctrl_mean, t_p):
    with open(OUTPUT_DIR / 'RESULTS.md', 'w') as f:
        f.write("# Project 31: Planetary Patterns & Outbreaks\n\n")
        f.write(f"**Analysis Window**: {START_YEAR}-{END_YEAR}\n")
        f.write(f"**Total Years Analyzed**: {len(df)}\n")
        f.write(f"**Outbreak Years**: {df['is_outbreak'].sum()}\n")
        f.write(f"**Control Years**: {(~df['is_outbreak']).sum()}\n\n")

        f.write("## 1. Global Intensity Hypothesis\n")
        f.write("Do outbreak years have a higher density of hard outer planet aspects (Conj/Sqr/Opp)?\n\n")
        f.write(f"- **Outbreak Mean**: {out_mean:.2f}\n")
        f.write(f"- **Control Mean**: {ctrl_mean:.2f}\n")
        f.write(f"- **Statistical Significance**: p = {t_p:.4f}\n")
        if t_p < 0.05:
            f.write("**CONCLUSION**: There is a statistically significant difference in planetary tension.\n\n")
        else:
            f.write("**CONCLUSION**: No global difference in aspect count found.\n\n")

        f.write("## 2. Specific Planetary Pairs\n")
        f.write("Which pairs are most active during outbreaks?\n\n| Pair | Outbreak Freq | Control Freq | P-Value |\n|---|---|---|---|\n")

        sig_results.sort(key=lambda x: x['P_Value'])
        for res in sig_results:
            bold = "**" if res['P_Value'] < 0.10 else ""
            f.write(f"| {res['Pair']} | {res['Outbreak_Rate']:.1%} | {res['Control_Rate']:.1%} | {bold}{res['P_Value']:.4f}{bold} |\n")

        f.write("\n\n## 3. Notable Outbreak Configurations\n")
        outbreaks = df[df['is_outbreak']]
        for _, row in outbreaks.iterrows():
            aspects = []
            for col in df.columns:
                if col.endswith('_aspect') and row[col] != 'None':
                    planet = col.replace('_aspect', '')
                    aspects.append(f"{planet} ({row[col]})")

            aspect_str = ", ".join(aspects) if aspects else "None"
            f.write(f"- **{row['year']} ({row['outbreak_name']})**: {aspect_str}\n")

if __name__ == "__main__":
    main()
