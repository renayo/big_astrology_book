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
    print("Loading data for Heatmap...")
    df = pd.read_csv(DATA_FILE)

    data_list = []

    for _, row in df.iterrows():
        try:
            # Use only completed relationships for valid duration correlation
            if str(row['end_date']) == 'nan': continue

            start_str = str(row['start_date'])
            end_str = str(row['end_date'])

            if start_str == 'nan': continue

            start_dt = datetime.strptime(start_str, "%Y-%m-%d")
            end_dt = datetime.strptime(end_str, "%Y-%m-%d")

            duration_years = (end_dt - start_dt).days / 365.25

            if duration_years < 0.1 or duration_years > 80: continue

            p1_pos = get_positions(row['p1_birth_date'])
            p2_pos = get_positions(row['p2_birth_date'])

            if not p1_pos or not p2_pos: continue

            feat = {'duration': duration_years}

            for p1 in PLANET_LIST:
                for p2 in PLANET_LIST:
                    angle = p1_pos[p1] - p2_pos[p2]
                    feat[f"{p1}-{p2}"] = np.cos(angle)

            data_list.append(feat)
        except:
            continue

    study_df = pd.DataFrame(data_list)
    print(f"Dataset: {len(study_df)} completed relationships.")

    # Create 10x10 Correlation Matrix
    # Cell (i, j) = Correlation( Cosine(P1_i - P2_j), Duration )

    corr_matrix = pd.DataFrame(index=PLANET_LIST, columns=PLANET_LIST, dtype=float)

    for p1 in PLANET_LIST:
        for p2 in PLANET_LIST:
            col_name = f"{p1}-{p2}"
            corr = study_df[col_name].corr(study_df['duration'])
            corr_matrix.loc[p1, p2] = corr

    # Plotting
    plt.figure(figsize=(12, 10))

    # Mask diagonal if needed, but here P1-P2 is different persons, so diagonal is meaningful (Sun-Sun).

    sns.heatmap(corr_matrix, annot=True, center=0, cmap='RdBu_r', fmt='.3f',
                cbar_kws={'label': 'Correlation Coefficient (r)'})

    plt.title('Synastry Correlation Heatmap (N=1687)\nCorrelation between Aspect Cosine and Marriage Duration\n(Red = Conjunction favors longevity, Blue = Opposition favors longevity)')
    plt.xlabel('Partner 2 Planet')
    plt.ylabel('Partner 1 Planet')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'synastry_correlation_heatmap.png')
    print("Saved synastry_correlation_heatmap.png")

if __name__ == "__main__":
    main()
