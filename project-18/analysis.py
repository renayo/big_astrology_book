#!/usr/bin/env python3
"""
Project 18: Solar House System Bayesian Comparison
==================================================
Compares Solar House systems (Whole Sign vs Equal) using Celebrity Archetypes.

DATA SOURCES:
- Project 6 Celebrity Data (Science, Arts, Politics, etc.)

METHODOLOGY:
1. Load celebrity birth data.
2. Calculate Solar House placements (Whole Sign vs Equal).
3. Check if "Archetypal Planets" fall into "Archetypal Houses" (e.g. Mars in 10th for Athletes).
4. Calculate Bayesian Likelihood vs Random Chance.
"""

import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
from datetime import datetime
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Import Celebrity Data from Project 6
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT / '06-harmonic-analysis-aspects'))
try:
    from celebrity_data import CELEBRITY_DATA
except ImportError:
    print("Warning: Could not import CELEBRITY_DATA.")
    CELEBRITY_DATA = []

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path(None)

# House systems available
HOUSE_SYSTEMS = {
    'SolarSign': 'Solar Whole Sign (Sun)',
    'SolarEqual': 'Solar Equal House (Sun)'
}

# TARGET HOUSES per Archetype
TARGET_HOUSES = {
    'Science': [9, 3, 11],       # 9th (Higher Mind), 3rd (Analysis), 11th (Innovation)
    'Arts': [5, 12, 1],          # 5th (Creativity), 12th (Imagination), 1st (Expression)
    'Politics': [10, 11, 7],     # 10th (Authority), 11th (Groups), 7th (Public)
    'Entertainment': [5, 1, 10], # 5th (Performance), 1st (Persona), 10th (Fame)
    'Sports': [1, 5, 6],         # 1st (Body), 5th (Games), 6th (Training)
    'Literature': [3, 9, 5],     # 3rd (Writing), 9th (Publishing), 5th (Creative Writing)
    'Philosophy': [9, 12, 8]     # 9th (Philosophy), 12th (Spirituality), 8th (Deep Truths)
}

# RELEVANT PLANETS per Archetype
TARGET_PLANETS = {
    'Science': ['Mercury', 'Uranus', 'Saturn'],
    'Arts': ['Venus', 'Neptune', 'Moon'],
    'Politics': ['Sun', 'Jupiter', 'Saturn', 'Pluto'],
    'Entertainment': ['Sun', 'Venus', 'Neptune'],
    'Sports': ['Mars', 'Sun', 'Jupiter'],
    'Literature': ['Mercury', 'Moon', 'Jupiter'],
    'Philosophy': ['Jupiter', 'Neptune', 'Saturn']
}

def datetime_to_jd(dt_str, time_str):
    """Parse date and time strings to Julian Day."""
    # Handle cases where formats might differ
    try:
        dt = datetime.strptime(f"{dt_str} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        try:
            # Try with seconds if present or other formats
            dt = datetime.strptime(f"{dt_str} {time_str}", "%Y-%m-%d %H:%M:%S")
        except ValueError:
             # Fallback for simple date or time formats if needed
            dt = datetime.strptime(f"{dt_str} 12:00", "%Y-%m-%d %H:%M")

    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0)

def get_solar_cusps(sun_lon, system):
    """
    Calculate Solar House Cusps.
    System: 'SolarSign' or 'SolarEqual'
    """
    cusps = []

    if system == 'SolarEqual':
        # House 1 Cusp = Sun Lon
        start_deg = sun_lon
    elif system == 'SolarSign':
        # House 1 Cusp = 0 degrees of the Sign containing the Sun
        # Each sign is 30 degrees. 
        sign_index = int(sun_lon // 30)
        start_deg = sign_index * 30.0
    else:
        raise ValueError(f"Unknown Solar System: {system}")

    # Generate 12 cusps
    for i in range(12):
        cusp = (start_deg + i * 30.0) % 360.0
        cusps.append(cusp)

    return cusps

def get_house_cusps(jd, system):
    """Calculate house cusps for given system (Solar only)."""
    # First get Sun position for Solar Houses
    res = swe.calc_ut(jd, swe.SUN)[0]
    sun_lon = res[0]

    return get_solar_cusps(sun_lon, system)

def get_planet_positions(jd):
    """Get planetary longitudes."""
    planets = {
        swe.SUN: 'Sun', swe.MOON: 'Moon', swe.MERCURY: 'Mercury',
        swe.VENUS: 'Venus', swe.MARS: 'Mars', swe.JUPITER: 'Jupiter',
        swe.SATURN: 'Saturn', swe.URANUS: 'Uranus', swe.NEPTUNE: 'Neptune',
        swe.PLUTO: 'Pluto'
    }
    positions = {}
    for pid, name in planets.items():
        result = swe.calc_ut(jd, pid)[0]
        positions[name] = result[0]
    return positions


def get_planet_house(planet_lon, cusps):
    """Determine which house a planet is in."""
    for i in range(12):
        cusp_start = cusps[i]
        cusp_end = cusps[(i + 1) % 12]

        # Handle zodiac wraparound
        if cusp_end < cusp_start:  # Crosses 0° Aries
            if planet_lon >= cusp_start or planet_lon < cusp_end:
                return i + 1
        else:
            if cusp_start <= planet_lon < cusp_end:
                return i + 1
    return 1  # Default

def analyze_house_systems():
    """Compare house systems across verifiable charts."""
    print("=" * 60)
    print("COMPARING HOUSE SYSTEMS (SOLAR ONLY)")
    print("=" * 60)

    records = []

    systems = HOUSE_SYSTEMS

    print(f"Loading {len(CELEBRITY_DATA)} celebrity charts...")

    for person in CELEBRITY_DATA:
        name = person['name']
        birth_date = person['date']
        birth_time = person['time']
        category = person['category']

        # Skip if category is not in our targets
        if category not in TARGET_HOUSES:
            continue

        jd = datetime_to_jd(birth_date, birth_time)

        # Get Planet positions
        planets = get_planet_positions(jd)
        sun_lon = planets['Sun']

        # 1. Solar Whole Sign
        cusps_ss = get_solar_cusps(sun_lon, system='SolarSign')
        for planet, p_lon in planets.items():
            h = get_planet_house(p_lon, cusps_ss)
            records.append({'name': name, 'system': systems['SolarSign'], 'planet': planet, 'house': h, 'archetype': category})

        # 2. Solar Equal House
        cusps_se = get_solar_cusps(sun_lon, system='SolarEqual')
        for planet, p_lon in planets.items():
            h = get_planet_house(p_lon, cusps_se)
            records.append({'name': name, 'system': systems['SolarEqual'], 'planet': planet, 'house': h, 'archetype': category})

    df = pd.DataFrame(records)
    print(f"Analyzed {len(df['name'].unique())} charts × {len(systems)} systems")
    print(f"Total data points: {len(df)}")

    return df, systems


def calculate_hit_rate(df, system_name):
    """Calculate the hit rate for a given system based on archetypal expectations."""
    sys_df = df[df['system'] == system_name]
    total_checks = 0
    hits = 0

    for _, row in sys_df.iterrows():
        archetype = row['archetype']
        planet = row['planet']
        house = row['house']

        valid_planets = TARGET_PLANETS.get(archetype, [])
        valid_houses = TARGET_HOUSES.get(archetype, [])

        if planet in valid_planets:
            total_checks += 1
            if house in valid_houses:
                hits += 1

    return hits, total_checks


def compare_systems(df, all_systems):
    """Statistical comparison of house systems."""
    print("\n" + "=" * 60)
    print("HOUSE SYSTEM EFFICACY (BAYESIAN COMPARISON)")
    print("=" * 60)

    results = {}

    # 1. Efficacy Analysis (Hit Rate)
    print("\n1. SYSTEM HIT RATES (Does the system place relevant planets in expected houses?)")
    print(f"{'System':<30} | {'Hits':<5} | {'Total':<5} | {'Rate':<6}")
    print("-" * 55)

    hit_data = []

    for sys_key, sys_name in all_systems.items():
        hits, total = calculate_hit_rate(df, sys_name)
        rate = hits / total if total > 0 else 0
        print(f"{sys_name:<30} | {hits:<5} | {total:<5} | {rate:.1%}")
        hit_data.append({'System': sys_name, 'Hits': hits, 'Total': total, 'Rate': rate})

        # Store for Bayesian
        results[f"{sys_key}_Rate"] = rate
        results[f"{sys_key}_Hits"] = hits
        results[f"{sys_key}_Total"] = total

    # 2. Bayesian Model Comparison
    print("\n2. BAYESIAN LIKELIHOOD RATIOS (vs Random Baseline)")
    # We use a conservative baseline
    avg_target_len = np.mean([len(v) for v in TARGET_HOUSES.values()])
    baseline_prob = avg_target_len / 12.0
    print(f"   Baseline Random Probability: {baseline_prob:.1%}")

    for data in hit_data:
        k = data['Hits']
        n = data['Total']

        # Calculate Bayes Factor vs Random Model
        # H1: p = observed rate (MLE)
        # H0: p = baseline_prob

        p_mle = k/n

        if p_mle <= baseline_prob:
             bf = 0.0 # Worse than random
        else:
            log_lik_h1 = stats.binom.logpmf(k, n, p_mle)
            log_lik_h0 = stats.binom.logpmf(k, n, baseline_prob)
            bf = np.exp(log_lik_h1 - log_lik_h0)

        print(f"   {data['System']}: BF = {bf:.2f} (x more likely than random)")
        results[f"{data['System']}_BF"] = bf

    return results, pd.DataFrame(hit_data)


def plot_archetype_heatmaps(df, output_dir):
    """Generate heatmaps for each archetype showing planet-house distribution."""
    print("\nGenerating Archetype Heatmaps...")

    archetypes = df['archetype'].unique()
    planets_order = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']

    for arch in archetypes:
        arch_df = df[df['archetype'] == arch]
        if arch_df.empty:
            continue

        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        fig.suptitle(f'Planet House Distribution: {arch} ({len(arch_df["name"].unique())} Charts)', fontsize=16)

        # Plot for each system
        systems = [('Solar Whole Sign (Sun)', 'SolarSign'), ('Solar Equal House (Sun)', 'SolarEqual')]

        for idx, (sys_label, sys_code) in enumerate(systems):
            ax = axes[idx]
            sys_data = arch_df[arch_df['system'] == sys_label]

            # Create count matrix (Planets x Houses 1-12)
            matrix = np.zeros((len(planets_order), 12))

            for i, planet in enumerate(planets_order):
                p_data = sys_data[sys_data['planet'] == planet]
                counts = p_data['house'].value_counts()
                for h in range(1, 13):
                    matrix[i, h-1] = counts.get(h, 0)

            # Plot Heatmap
            im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')

            # Labels
            ax.set_title(sys_label)
            ax.set_xticks(np.arange(12))
            ax.set_xticklabels(np.arange(1, 13))
            ax.set_xlabel('House')
            ax.set_yticks(np.arange(len(planets_order)))
            ax.set_yticklabels(planets_order)

            # Add text annotations
            for i in range(len(planets_order)):
                for j in range(12):
                    val = int(matrix[i, j])
                    if val > 0:
                        text_color = 'white' if val > matrix.max()/2 else 'black'
                        ax.text(j, i, str(val), ha='center', va='center', color=text_color)

            # Highlight Target Houses/Planets if applicable
            target_houses = TARGET_HOUSES.get(arch, [])
            target_planets = TARGET_PLANETS.get(arch, [])

            # Draw boxes or changing tick labels for targets
            # Mark Target Planets on Y-axis
            for i, p in enumerate(planets_order):
                if p in target_planets:
                    ax.get_yticklabels()[i].set_color('red')
                    ax.get_yticklabels()[i].set_fontweight('bold')

            # Mark Target Houses on X-axis (approximate visual cue)
            for h in range(1, 13):
                if h in target_houses:
                    ax.get_xticklabels()[h-1].set_color('red')
                    ax.get_xticklabels()[h-1].set_fontweight('bold')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        filename = f"distribution_{arch.lower().replace(' ', '_')}.png"
        plt.savefig(output_dir / filename)
        plt.close()
        print(f"   Saved {filename}")

def main():
    print("=" * 70)
    print("PROJECT 18: SOLAR HOUSE SYSTEM ANALYSIS")
    print("Celebrity Archetype Validation")
    print("=" * 70)

    if not CELEBRITY_DATA:
        print("Error: No celebrity data loaded. Aborting.")
        return

    df, all_systems = analyze_house_systems()
    if df.empty:
        print("No records analyzed.")
        return

    results, hit_df = compare_systems(df, all_systems)

    # 1. Summary Visualization
    fig, ax = plt.subplots(figsize=(10, 6))

    systems = hit_df['System']
    rates = hit_df['Rate']

    colors = ['#3498db', '#e74c3c'] # Blue, Red
    bars = ax.bar(systems, rates, color=colors, alpha=0.7)

    # Add baseline line
    avg_target_len = np.mean([len(v) for v in TARGET_HOUSES.values()])
    baseline = avg_target_len / 12.0
    ax.axhline(y=baseline, color='gray', linestyle='--', label=f'Random Chance ({baseline:.1%})')

    ax.set_ylabel('Hit Rate (Relevant Planet in Target House)')
    ax.set_title('Solar House System Efficacy by Archetype')
    ax.legend(loc='lower right')

    # Label bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1%}',
                ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'solar_house_analysis.png', dpi=150)
    plt.close()

    # 2. Detailed Heatmaps
    plot_archetype_heatmaps(df, OUTPUT_DIR)

    df.to_csv(OUTPUT_DIR / 'solar_house_data.csv', index=False)
    hit_df.to_csv(OUTPUT_DIR / 'analysis_results.csv', index=False)

    print(f"\nResults saved to {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
