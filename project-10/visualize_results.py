#!/usr/bin/env python3
import pandas as pd
import numpy as np
import swisseph as swe
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup
OUTPUT_DIR = Path(__file__).parent
DATA_FILE = OUTPUT_DIR / "new_couples_wikidata.csv"
swe.set_ephe_path(None)

# Planets
PLANETS = {
    'Sun': swe.SUN,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO,
    'Node': swe.MEAN_NODE
}
PLANET_LIST = list(PLANETS.keys())

def get_positions(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        jd = swe.julday(dt.year, dt.month, dt.day, 12.0)
        pos = {}
        for name, pid in PLANETS.items():
            deg = swe.calc_ut(jd, pid)[0][0]
            pos[name] = np.deg2rad(deg)
        return pos
    except:
        return None

def main():
    print("Loading data...")
    df = pd.read_csv(DATA_FILE)

    results = []
    print(f"Processing {len(df)} couples...")

    for _, row in df.iterrows():
        try:
            # Duration Calc
            start = str(row['start_date'])
            end = str(row['end_date'])
            if start == 'nan': continue

            start_dt = datetime.strptime(start, "%Y-%m-%d")

            if end != 'nan':
                end_dt = datetime.strptime(end, "%Y-%m-%d")
                duration = (end_dt - start_dt).days / 365.25
                status = 'Ended'
            else:
                duration = (datetime.now() - start_dt).days / 365.25
                status = 'Ongoing'

            if duration < 0: continue

            # Synastry Calc
            p1_pos = get_positions(row['p1_birth_date'])
            p2_pos = get_positions(row['p2_birth_date'])

            if not p1_pos or not p2_pos: continue

            feat = {'duration': duration, 'status': status}

            for p1 in PLANET_LIST:
                for p2 in PLANET_LIST:
                    angle = p1_pos[p1] - p2_pos[p2]
                    # Agnostic Cosine: +1 Conj, -1 Opp
                    feat[f"{p1}-{p2}"] = np.cos(angle)

            results.append(feat)

        except Exception:
            continue

    res_df = pd.DataFrame(results)
    print(f"Computed features for {len(res_df)} couples.")

    # Filter for Completed Relationships for Stats
    ended_df = res_df[res_df['status'] == 'Ended']

    # Define Long vs Short Term (Quartiles)
    # Using all data (including ongoing) for quartiles might be biased towards short ongoing ones?
    # Better to use distribution of ALL to determine thresholds, or just ENDED?
    # The previous analysis likely used ALL. Let's stick to ALL for quartiles to match earlier method,
    # or refine to Ended if that's more rigorous. 
    # Let's simple use 25% top/bottom of ALL valid durations.
    q_high = res_df['duration'].quantile(0.75)
    q_low = res_df['duration'].quantile(0.25)

    long_term = res_df[res_df['duration'] > q_high]
    short_term = res_df[res_df['duration'] < q_low]

    print(f"Long Term > {q_high:.1f}y (n={len(long_term)})")
    print(f"Short Term < {q_low:.1f}y (n={len(short_term)})")

    # --- Plot 1: The Mars Effect (Distribution) ---
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=long_term, x='Mars-Mars', label='Long Term', fill=True, color='green', alpha=0.3)
    sns.kdeplot(data=short_term, x='Mars-Mars', label='Short Term', fill=True, color='red', alpha=0.3)
    plt.title('Distribution of Mars-Mars Synastry\n(Long vs Short Relationships)')
    plt.xlabel('Cosine Similarity (+1=Conjunction, -1=Opposition)')
    plt.legend()
    plt.xlim(-1.1, 1.1)
    plt.grid(True, alpha=0.3)
    plt.savefig(OUTPUT_DIR / 'viz_mars_mars_dist.png')
    print("Saved viz_mars_mars_dist.png")

    # --- Plot 2: Top factors Bar Chart (Mean Difference) ---
    # Calculate Mean Diff for all pairs
    diffs = []
    pairs = [c for c in res_df.columns if '-' in c]
    for col in pairs:
        # T-test
        t, p = stats.ttest_ind(long_term[col], short_term[col], equal_var=False)
        mean_diff = long_term[col].mean() - short_term[col].mean()
        diffs.append({'pair': col, 'diff': mean_diff, 'p': p})

    diff_df = pd.DataFrame(diffs).sort_values('diff', ascending=False)

    # Top 5 Positive (Conjunction Helps) & Top 5 Negative (Opposition Helps)
    top_pos = diff_df.head(5)
    top_neg = diff_df.tail(5)

    viz_df = pd.concat([top_pos, top_neg])

    plt.figure(figsize=(12, 8))
    colors = ['green' if x > 0 else 'red' for x in viz_df['diff']]
    sns.barplot(data=viz_df, x='diff', y='pair', palette=colors)
    plt.title('Top Synastry Factors Differentiating Long vs Short Relationships\n(Mean Difference in Cosine)')
    plt.xlabel('Difference (Long Mean - Short Mean)\nPositive = Conjunction Favors Longevity')
    plt.axvline(0, color='black', linewidth=1)
    plt.savefig(OUTPUT_DIR / 'viz_top_factors.png')
    print("Saved viz_top_factors.png")

    # --- Plot 3: Personal Planet Heatmap (Correlation with Duration) ---
    # Only Personal Planets: Sun, Moon (Excluded), Mercury, Venus, Mars
    personal_planets = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']

    # Init matrix
    matrix = pd.DataFrame(index=personal_planets, columns=personal_planets, dtype=float)

    for p1 in personal_planets:
        for p2 in personal_planets:
            key = f"{p1}-{p2}"
            if key in res_df.columns:
                # Correlation with Duration (Ended only)
                corr = ended_df[key].corr(ended_df['duration'])
                matrix.loc[p1, p2] = corr

    plt.figure(figsize=(8, 6))
    sns.heatmap(matrix.astype(float), annot=True, cmap='RdBu_r', center=0, fmt='.3f')
    plt.title('Correlation with Longevity (Personal Planets)\nRed=Conjunction Good, Blue=Opposition Good')
    plt.savefig(OUTPUT_DIR / 'viz_personal_heatmap.png')
    print("Saved viz_personal_heatmap.png")

    # --- Plot 4: Age Artifact Demo (Pluto-Pluto) ---
    plt.figure(figsize=(10, 6))
    sns.regplot(data=ended_df, x='Pluto-Pluto', y='duration', scatter_kws={'alpha':0.1}, line_kws={'color':'red'})
    plt.title('The Age Artifact: Pluto-Pluto Conjunction vs Longevity\n(Partners of same generation live longer together)')
    plt.xlabel('Pluto-Pluto Cosine')
    plt.ylabel('Duration (Years)')
    plt.savefig(OUTPUT_DIR / 'viz_age_artifact.png')
    print("Saved viz_age_artifact.png")

if __name__ == "__main__":
    from scipy import stats # Ensure stats is available
    main()
