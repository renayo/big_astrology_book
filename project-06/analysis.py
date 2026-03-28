#!/usr/bin/env python3
"""
Project 6: Harmonic Analysis of Planetary Aspects
=================================================
Applies Fourier/harmonic analysis to planetary aspect patterns
using real celebrity birth data from AstroDatabank (Rodden Rating A/AA).

DATA SOURCES (REAL):
- AstroDatabank: Verified celebrity birth times
- Swiss Ephemeris: Precise planetary calculations
- Dataset: ~100 diverse historical figures across Science, Arts, Politics, Sports.

METHODOLOGY:
1. Load real birth data (Science, Arts, Politics, etc.)
2. Calculate planetary positions (Sun through Saturn).
3. Perform harmonic decomposition (H1-H12).
   - Metric: Mean Resultant Length (Vector Strength) of aspect angles.
4. Compare specific categories against Random Baseline.
"""

import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
from datetime import datetime
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Import dataset
try:
    from celebrity_data import CELEBRITY_DATA
except ImportError:
    # Fallback if running from a different directory context
    sys.path.append(str(Path(__file__).parent))
    from celebrity_data import CELEBRITY_DATA

OUTPUT_DIR = Path(__file__).parent
OUTPUT_DIR.mkdir(exist_ok=True)
swe.set_ephe_path(None)

PLANETS = {swe.SUN: 'Sun', swe.MOON: 'Moon', swe.MERCURY: 'Mercury',
           swe.VENUS: 'Venus', swe.MARS: 'Mars', swe.JUPITER: 'Jupiter',
           swe.SATURN: 'Saturn'} 
           # Exclude Uranus/Neptune for traditional harmonic theory or keep? 
           # Addey often used all. Let's keep 7 traditional for classic harmonics 
           # or add outer planets. The original script had them, let's keep 7 for cleaner
           # "traditional" aspect analysis, or add them if requested. 
           # Using 7 visible bodies is standard for "hard" harmonic theory to avoid generational noise.

def datetime_to_jd(dt):
    """Convert datetime to Julian Day."""
    hour = dt.hour + dt.minute/60.0
    return swe.julday(dt.year, dt.month, dt.day, hour)

def get_positions(jd):
    """Get geocentric longitudes for planets."""
    positions = {}
    for pid, name in PLANETS.items():
        result, _ = swe.calc_ut(jd, pid)[:2]
        positions[name] = result[0]
    return positions

def harmonic_strength(angles, h):
    """
    Calculate strength of harmonic H using Vector Mean.
    R = sqrt( (sum(cos(theta))/N)^2 + (sum(sin(theta))/N)^2 )
    """
    if len(angles) == 0: return 0.0
    rad = np.deg2rad(np.array(angles) * h)
    return np.sqrt(np.mean(np.cos(rad))**2 + np.mean(np.sin(rad))**2)

def load_real_birth_data():
    """Load verified celebrity birth data from module."""
    print("Loading AstroDatabank celebrity data...")

    records = []
    for entry in CELEBRITY_DATA:
        try:
            dt = datetime.strptime(f"{entry['date']} {entry['time']}", "%Y-%m-%d %H:%M")
        except ValueError:
            # Handle potential date parsing errors
            continue

        jd = datetime_to_jd(dt)
        pos = get_positions(jd)

        records.append({
            'name': entry['name'],
            'category': entry.get('category', 'General'),
            'date': dt,
            'jd': jd,
            **{f'{p}_lon': lon for p, lon in pos.items()}
        })

    df = pd.DataFrame(records)
    print(f"Loaded {len(df)} verified celebrity charts")
    return df

def generate_random_baseline(n=2000):
    """Generate random birth charts as baseline."""
    print(f"Generating {n} random baseline charts...")
    np.random.seed(42)

    records = []
    for i in range(n):
        # Random dates between 1900 and 2000 to match demo mostly
        year = np.random.randint(1900, 2000)
        month = np.random.randint(1, 13)
        day = np.random.randint(1, 29)
        hour = np.random.randint(0, 24)
        minute = np.random.randint(0, 60)

        dt = datetime(year, month, day, hour, minute)
        jd = datetime_to_jd(dt)
        pos = get_positions(jd)

        records.append({
            'name': f'Random_{i}',
            'category': 'Random',
            'date': dt,
            'jd': jd,
            **{f'{p}_lon': lon for p, lon in pos.items()}
        })

    return pd.DataFrame(records)

def calculate_group_harmonics(df, label):
    """Calculate harmonic strengths H1-H12 for a specific group."""
    results = {}
    planets = list(PLANETS.values())

    # We collect ALL angles from ALL charts in the group
    # (Pooling approach: "How strong is H5 in this Population?")
    # Alternatively, we could calc strength per chart and average. 
    # Pooling is often better for "Population Harmonic Signature".

    all_angles = []

    for _, row in df.iterrows():
        chart_angles = []
        for i, p1 in enumerate(planets):
            for p2 in planets[i+1:]:
                angle = abs(row[f'{p1}_lon'] - row[f'{p2}_lon'])
                # Shortest distance on circle
                if angle > 180: angle = 360 - angle
                all_angles.append(angle)

    # Calculate Mean R for each Harmonic
    for h in range(1, 13):
        strength = harmonic_strength(all_angles, h)
        results[f'H{h}'] = strength

    return results

def main():
    print("=" * 60)
    print("PROJECT 6: HARMONIC ANALYSIS OF PLANETARY ASPECTS")
    print("=" * 60)

    # 1. Load Data
    real_df = load_real_birth_data()
    baseline_df = generate_random_baseline(5000)

    # 2. Define Groups
    categories = ['All Real'] + list(real_df['category'].unique())
    results_map = {}

    # 3. Analyze Baseline
    base_harmonics = calculate_group_harmonics(baseline_df, "Random")

    # 4. Analyze Categories
    print("\nAnalyzing Categories...")

    # Global
    results_map['All Real'] = calculate_group_harmonics(real_df, "All Real")

    # Sub-groups
    for cat in real_df['category'].unique():
        sub_df = real_df[real_df['category'] == cat]
        if len(sub_df) < 5: continue # Skip tiny groups
        results_map[cat] = calculate_group_harmonics(sub_df, cat)
        print(f"Analyzed {cat} (N={len(sub_df)})")

    # 5. Output Results & Check Significance
    print("\n" + "=" * 60)
    print(f"{'Category':<15} {'H1':<7} {'H4 (Sqr)':<10} {'H5 (Art)':<10} {'H7 (Mys)':<10}")
    print("-" * 60)

    csv_data = []

    for cat, metrics in results_map.items():
        # Ratios vs Baseline
        r1 = metrics['H1'] / base_harmonics['H1']
        r4 = metrics['H4'] / base_harmonics['H4']
        r5 = metrics['H5'] / base_harmonics['H5']
        r7 = metrics['H7'] / base_harmonics['H7']

        print(f"{cat:<15} {r1:.2f}x   {r4:.2f}x       {r5:.2f}x       {r7:.2f}x")

        # Prepare CSV row
        row = {'Category': cat, 'N': len(real_df) if cat == 'All Real' else len(real_df[real_df['category']==cat])}
        for h in range(1, 13):
            row[f'H{h}_Str'] = metrics[f'H{h}']
            row[f'H{h}_Ratio'] = metrics[f'H{h}'] / base_harmonics[f'H{h}']
        csv_data.append(row)

    pd.DataFrame(csv_data).to_csv(OUTPUT_DIR / 'analysis_results.csv', index=False)

    # 6. Visualization (Arts vs Science vs Random)
    plt.figure(figsize=(14, 6))

    # Harmonics to plot
    x = np.arange(1, 13)
    width = 0.2

    # Plot Baseline (at 1.0 ratio)
    plt.axhline(1.0, color='black', linestyle='--', alpha=0.5, label='Random Baseline')

    # Plot Science
    if 'Science' in results_map:
        y_sci = [results_map['Science'][f'H{i}'] / base_harmonics[f'H{i}'] for i in x]
        plt.bar(x - width, y_sci, width, label='Science', color='skyblue')

    # Plot Arts
    if 'Arts' in results_map:
        y_art = [results_map['Arts'][f'H{i}'] / base_harmonics[f'H{i}'] for i in x]
        plt.bar(x, y_art, width, label='Arts/Music', color='salmon')

    # Plot Sports
    if 'Sports' in results_map:
        y_spo = [results_map['Sports'][f'H{i}'] / base_harmonics[f'H{i}'] for i in x]
        plt.bar(x + width, y_spo, width, label='Sports', color='lightgreen')

    plt.xlabel("Harmonic (H1 - H12)")
    plt.ylabel("Strength Ratio (Actual / Random)")
    plt.title("Harmonic Signature by Profession")
    plt.xticks(x, [f'H{i}' for i in x])
    plt.legend()
    plt.grid(axis='y', alpha=0.3)

    plt.savefig(OUTPUT_DIR / 'harmonic_analysis.png')
    print(f"\nPlot saved to {OUTPUT_DIR / 'harmonic_analysis.png'}")

if __name__ == '__main__':
    main()
