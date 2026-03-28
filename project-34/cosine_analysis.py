#!/usr/bin/env python3
"""
Project 34: Solar Return Annual Predictions (Cosine Analysis)
-------------------------------------------------------------
Objective: Be agnostic. Use cosines of angle differences of pairs from the 
12 celestial features (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, 
Uranus, Neptune, Pluto, Mean Node, Lilith).

Methodology:
1. Load event data from solar_return_data.csv.
2. For each event year:
   a. Calculate Solar Return chart (assuming 12:00 birth time if unknown).
   b. Calculate positions of 12 bodies.
   c. Calculate 66 pair-wise Cosines (cos(A-B)).
3. Statistical Analysis:
   a. For each Event Type (Death, Marriage, etc.), compare pair means to the rest of the dataset.
   b. Identify significant deviations.
"""

import pandas as pd
import numpy as np
import swisseph as swe
from datetime import datetime, timedelta
from pathlib import Path
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Constants
PLANETS = {
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
    'Node': swe.MEAN_NODE,  # Mean Node
    'Lilith': swe.MEAN_APOG # Mean Lilith (Black Moon)
}

PLANET_LIST = list(PLANETS.keys())
OUTPUT_DIR = Path(__file__).parent
DATA_FILE = OUTPUT_DIR / 'solar_return_data.csv'

# Setup Swiss Ephemeris
swe.set_ephe_path(None)

def get_solar_return_date(birth_date_str, target_year):
    """
    Calculate the JD of the Solar Return for the target year.
    Assumes Birth Time is 12:00:00 UTC.
    """
    # Parse Birth Date
    try:
        bd = datetime.strptime(birth_date_str, "%Y-%m-%d")
    except ValueError:
        return None

    # Calculate Natal Sun
    # Assuming 12:00 UTC
    jd_birth = swe.julday(bd.year, bd.month, bd.day, 12.0)
    natal_sun = swe.calc_ut(jd_birth, swe.SUN)[0][0]

    # Estimate Return Date (Same Month/Day, Target Year)
    # Start search around the birthday in target year
    # Need to handle leap years carefully, but swe.julday handles dates fine.
    # Solar return is usually within +/- 1 day of birthday.

    jd_approx = swe.julday(target_year, bd.month, bd.day, 12.0)

    # Iterative search for exact return
    jd_iter = jd_approx
    for _ in range(10): # 10 iterations is plenty for high precision
        sun_pos = swe.calc_ut(jd_iter, swe.SUN)[0][0]

        # Calculate difference (accounting for 360 wrap)
        diff = natal_sun - sun_pos
        while diff > 180: diff -= 360
        while diff < -180: diff += 360

        if abs(diff) < 0.00001: # ~0.03 seconds of arc
            break

        # Sun moves ~1 degree per day (roughly)
        # correction = diff / 1.0
        jd_iter += diff

    return jd_iter

def analyze_chart_cosines(jd):
    """
    Calculate positions of 12 bodies and returns 66 cosine features.
    Feature Name: "Sun-Moon", Value: cos(Sun - Moon)
    """
    positions = {}
    for name, pid in PLANETS.items():
        pos = swe.calc_ut(jd, pid)[0][0]
        positions[name] = np.deg2rad(pos) # Convert to radians for cosine

    features = {}

    # Generate Pairs
    for i in range(len(PLANET_LIST)):
        for j in range(i + 1, len(PLANET_LIST)):
            p1 = PLANET_LIST[i]
            p2 = PLANET_LIST[j]

            # Cosine of angle difference
            # cos(a - b)
            angle_diff = positions[p1] - positions[p2]
            cosine_val = np.cos(angle_diff)

            features[f"{p1}-{p2}"] = cosine_val

    return features

def main():
    print("Loading data...")
    if not DATA_FILE.exists():
        print(f"Error: {DATA_FILE} not found. Please run the data generation step first or locate the file.")
        return

    df = pd.read_csv(DATA_FILE)
    print(f"Loaded {len(df)} events.")

    results = []

    print("Calculating Solar Returns and Cosine Features...")
    for idx, row in df.iterrows():
        name = row['name']
        bdate = row['birth_date']
        year = row['year']
        event = row['event_type']

        try:
            jd_return = get_solar_return_date(bdate, year)
            if jd_return is None: continue

            features = analyze_chart_cosines(jd_return)
            features['event_type'] = event
            features['year'] = year
            features['name'] = name

            results.append(features)
        except Exception as e:
            print(f"Error processing {name} {year}: {e}")

    results_df = pd.DataFrame(results)
    print(f"Processed {len(results_df)} valid charts.")

    # --- Analysis ---

    # Normalize Event Types
    # Group rare events? 
    print("\nEvent Counts:")
    print(results_df['event_type'].value_counts())

    main_events = ['death', 'marriage', 'award', 'crisis', 'divorce']

    output_lines = []
    output_lines.append("# Project 34: Solar Return Cosine Analysis Results")
    output_lines.append("\n## Methodology")
    output_lines.append("Analyzing **cosine similarity** (+1 Conj, -1 Opp) for 66 planetary pairs in Solar Return charts.")
    output_lines.append(f"Dataset: {len(results_df)} events.")
    output_lines.append("\n## Top Correlations by Event Type")
    output_lines.append("| Event | Pair | Mean Diff | P-Value | Interpretation |")
    output_lines.append("|---|---|---|---|---|")

    significant_findings = []

    for event in main_events:
        print(f"\nAnalyzing: {event.upper()}")
        event_df = results_df[results_df['event_type'] == event]
        rest_df = results_df[results_df['event_type'] != event]

        if len(event_df) < 5:
            print("  Not enough data.")
            continue

        # Check all 66 pairs
        pair_cols = [c for c in results_df.columns if '-' in c and c not in ['birth-date', 'event-type']] # robust filter?
        # Actually columns are strictly "P1-P2".
        pair_cols = [f"{PLANET_LIST[i]}-{PLANET_LIST[j]}" for i in range(len(PLANET_LIST)) for j in range(i+1, len(PLANET_LIST))]

        local_results = []
        for pair in pair_cols:
            t_stat, p_val = stats.ttest_ind(event_df[pair], rest_df[pair], equal_var=False)
            diff = event_df[pair].mean() - rest_df[pair].mean()

            local_results.append({
                'pair': pair,
                'diff': diff,
                'p': p_val,
                'mean_event': event_df[pair].mean(),
                'mean_rest': rest_df[pair].mean()
            })

        # Sort by significance
        local_results.sort(key=lambda x: x['p'])

        # Report top 3
        for r in local_results[:3]:
            sig = "**" if r['p'] < 0.05 else ""
            print(f"  {r['pair']}: Diff={r['diff']:+.2f}, p={r['p']:.4f} {sig}")

            if r['p'] < 0.10: # Significance filter
                interp = "Conjunction" if r['mean_event'] > r['mean_rest'] else "Opposition"
                output_lines.append(f"| {event} | {r['pair']} | {r['diff']:+.2f} | {sig}{r['p']:.4f}{sig} | {interp} tendency |")
                significant_findings.append({'event': event, 'pair': r['pair'], 'p': r['p'], 'diff': r['diff']})

    # Save Results
    with open(OUTPUT_DIR / 'RESULTS_COSINE.md', 'w') as f:
        f.write("\n".join(output_lines))

    # Visualize top finding
    if significant_findings:
        top = sorted(significant_findings, key=lambda x: x['p'])[0]
        plot_pair_distribution(results_df, top['event'], top['pair'])

def plot_pair_distribution(df, target_event, pair):
    plt.figure(figsize=(10, 6))

    # Plot target event
    sns.kdeplot(df[df['event_type'] == target_event][pair], label=f'{target_event} (n={len(df[df["event_type"]==target_event])})', fill=True)

    # Plot rest
    sns.kdeplot(df[df['event_type'] != target_event][pair], label=f'Rest (n={len(df[df["event_type"]!=target_event])})', fill=True, alpha=0.3)

    plt.title(f'Solar Return {pair} Cosine Distribution: {target_event.title()}')
    plt.xlabel(f'{pair} Cosine (+1=Conj, -1=Opp)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(OUTPUT_DIR / 'cosine_analysis_plot.png')
    print(f"Saved plot for {pair} ({target_event})")

if __name__ == "__main__":
    main()
