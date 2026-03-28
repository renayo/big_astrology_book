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
    'Moon': swe.MOON,  # Including Moon for this visualization (assuming noon is roughly okay for general distrib)
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN
}
# Note: Moon moves ~13 deg/day. Noon position has +/- 6.5 deg error. 
# For broad distribution analysis (KDE) of thousands of couples, this noise might flatten the curve 
# but shouldn't shift the mean significantly if random. 

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
    print("Loading data for KDE Visualization...")
    if not DATA_FILE.exists():
        print("Data file not found.")
        return

    df = pd.read_csv(DATA_FILE)

    data_list = []

    print(f"Processing {len(df)} couples...")
    for _, row in df.iterrows():
        try:
            start_str = str(row['start_date'])
            end_str = str(row['end_date'])

            if start_str == 'nan': continue

            start_dt = datetime.strptime(start_str, "%Y-%m-%d")

            # Determine duration and status
            if end_str != 'nan':
                end_dt = datetime.strptime(end_str, "%Y-%m-%d")
                duration = (end_dt - start_dt).days / 365.25
                status = 'Ended'
            else:
                # For ongoing, we can use current duration, but for "Success/Fail" comparison,
                # we usually want to compare Completed Short vs Completed Long, or Completed vs Ongoing Long.
                duration = (datetime.now() - start_dt).days / 365.25
                status = 'Ongoing'

            if duration < 0.1 or duration > 80: continue

            # Synastry
            p1_pos = get_positions(row['p1_birth_date'])
            p2_pos = get_positions(row['p2_birth_date'])

            if not p1_pos or not p2_pos: continue

            feat = {
                'duration': duration,
                'status': status
            }

            # Key pairs for visualization
            pairs_to_calc = [
                ('Sun', 'Moon'), 
                ('Venus', 'Mars'), 
                ('Mars', 'Mars'), 
                ('Sun', 'Sun'),
                ('Venus', 'Saturn') # Classic "Glue" aspect?
            ]

            for p1, p2 in pairs_to_calc:
                angle = p1_pos[p1] - p2_pos[p2]
                feat[f"{p1}-{p2}"] = np.cos(angle)

            data_list.append(feat)
        except:
            continue

    res_df = pd.DataFrame(data_list)
    print(f"Processed {len(res_df)} couples.")

    # Define Long vs Short Term
    # We will use Quartiles of the entire dataset to show extremes
    q_high = res_df['duration'].quantile(0.75)
    q_low = res_df['duration'].quantile(0.25)

    long_term = res_df[res_df['duration'] > q_high].copy()
    short_term = res_df[res_df['duration'] < q_low].copy()

    long_term['Group'] = 'Long Term'
    short_term['Group'] = 'Short Term'

    combined = pd.concat([long_term, short_term])

    print(f"Long Term (> {q_high:.1f}y): {len(long_term)}")
    print(f"Short Term (< {q_low:.1f}y): {len(short_term)}")

    # Plotting
    key_aspects = ['Sun-Moon', 'Venus-Mars', 'Mars-Mars', 'Sun-Sun']

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for i, aspect in enumerate(key_aspects):
        ax = axes[i]
        sns.kdeplot(data=combined, x=aspect, hue='Group', fill=True, ax=ax, 
                   common_norm=False, palette={'Long Term': 'green', 'Short Term': 'red'}, alpha=0.3)

        ax.set_title(f"Distribution of {aspect} Synastry")
        ax.set_xlabel("Cosine Similarity (-1=Opp, +1=Conj)")
        ax.set_ylabel("Density")
        ax.axvline(0, color='gray', linestyle='--', alpha=0.5)
        ax.set_xlim(-1.1, 1.1)

    plt.suptitle("Synastry Distributions: Long Term vs Short Term Relationships\n(Are 'Good' Aspects more common in Long marriages?)", fontsize=16)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'aspect_distributions_kde.png')
    print("Saved aspect_distributions_kde.png")

if __name__ == "__main__":
    main()
