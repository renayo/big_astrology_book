import pandas as pd
import swisseph as swe
import numpy as np
import os

# Settings
DATA_FILE = 'birth_order_real_data.csv'
OUTPUT_FILE = 'analysis_results.csv'
SIDEREAL_MODE = True  # Variable for Lahiri
AYANAMSA_LAHIRI = swe.SIDM_LAHIRI

# Planets to analyze (Slow moving + Nodes)
# Saturn, Uranus, Neptune, Pluto, Rahu, Ketu.
PLANETS = {
    'Saturn': swe.SATURN,
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO,
    'Rahu': swe.MEAN_NODE # North Node
}

def get_positions(year, sidereal=False):
    # Mid-year approximation: July 2nd, Noon
    jd = swe.julday(year, 7, 2, 12.0)

    if sidereal:
        swe.set_sid_mode(AYANAMSA_LAHIRI)
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    else:
        flags = swe.FLG_SWIEPH

    positions = {}
    for name, pid in PLANETS.items():
        xx, ret = swe.calc_ut(jd, pid, flags)
        positions[name] = xx[0] # Longitude

    # Calculate Ketu (Opposite Rahu)
    positions['Ketu'] = (positions['Rahu'] + 180) % 360

    return positions

def analyze():
    print(f"Loading {DATA_FILE}...")
    if not os.path.exists(DATA_FILE):
        print("Data file not found!")
        return

    df = pd.read_csv(DATA_FILE)

    # Filter for reasonable years
    df = df[(df['birth_year'] >= 1900) & (df['birth_year'] <= 2000)]

    print("Calculating planetary positions (Sidereal Lahiri)...")

    # Pre-calculate positions for each unique year to save time
    unique_years = df['birth_year'].unique()
    year_map = {}
    for y in unique_years:
        year_map[y] = get_positions(y, sidereal=SIDEREAL_MODE)

    # Apply to dataframe
    for planet in list(PLANETS.keys()) + ['Ketu']:
        df[f'{planet}_deg'] = df['birth_year'].map(lambda y: year_map[y][planet])

    # 1. Circular Mean for each Birth Order
    results = []

    # Group by Birth Order (1-5+)
    df['order_bin'] = df['birth_order'].apply(lambda x: str(x) if x < 5 else '5+')

    print("Analyzing angular distributions...")

    for planet in list(PLANETS.keys()) + ['Ketu']:
        col = f'{planet}_deg'
        rads = np.deg2rad(df[col])
        df[f'{planet}_cos'] = np.cos(rads)
        df[f'{planet}_sin'] = np.sin(rads)

        stats = df.groupby('order_bin')[col].agg(['count', 'mean', 'std'])
        # Circular mean
        stats['sin_mean'] = df.groupby('order_bin')[f'{planet}_sin'].mean()
        stats['cos_mean'] = df.groupby('order_bin')[f'{planet}_cos'].mean()
        stats['circ_mean'] = np.rad2deg(np.arctan2(stats['sin_mean'], stats['cos_mean'])) % 360
        stats['R'] = np.sqrt(stats['sin_mean']**2 + stats['cos_mean']**2)

        print(f"\n--- {planet} ---")
        print(stats[['count', 'circ_mean', 'R']])

        for idx, row in stats.iterrows():
            results.append({
                'Planet': planet,
                'Birth_Order': idx,
                'N': row['count'],
                'J2000_Mean_Deg': row['circ_mean'],
                'Concentration_R': row['R']
            })

    # Save results
    res_df = pd.DataFrame(results)
    res_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Results saved to {OUTPUT_FILE}")

    # Correlations
    print("\nCorrelation (Person's Coefficient) between Birth Order and Planetary Longitude Components:")
    corrs = {}
    for planet in list(PLANETS.keys()) + ['Ketu']:
        r_cos = df['birth_order'].corr(df[f'{planet}_cos'])
        r_sin = df['birth_order'].corr(df[f'{planet}_sin'])
        corrs[planet] = (r_cos, r_sin)
        print(f"{planet}: Cos_corr={r_cos:.3f}, Sin_corr={r_sin:.3f}")

if __name__ == "__main__":
    analyze()
