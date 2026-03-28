import pandas as pd
import numpy as np
import scipy.stats as stats
import os
import glob

def run_stats():
    print("Initializing Statistical Verification...")

    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'daily-summaries-latest')
    astro_file = os.path.join(base_dir, 'astro_weather_features.csv')

    # Load Astro Data
    print("Loading astro features...")
    astro_df = pd.read_csv(astro_file)
    dates = astro_df['date'].values

    # Initialize Aggregation DF
    agg_df = pd.DataFrame(index=dates, columns=['sum_p', 'count_p']).fillna(0.0)

    # Scan Weather Files
    files = glob.glob(os.path.join(data_dir, "*.csv"))
    # Use 500 files for specific variance check (robust enough for T-test on daily means)
    sample_size = 500 
    files = files[:sample_size]
    print(f"Aggregating weather from {len(files)} stations...")

    processed = 0
    for f in files:
        try:
            df = pd.read_csv(f, usecols=['DATE', 'PRCP'])
            df = df.dropna(subset=['DATE', 'PRCP'])
            df = df[df['DATE'].isin(agg_df.index)]

            if df.empty: continue

            p_sums = df.set_index('DATE')['PRCP']
            # Align indices
            common_dates = p_sums.index.intersection(agg_df.index)
            if common_dates.empty: continue

            agg_df.loc[common_dates, 'sum_p'] += p_sums.loc[common_dates]
            agg_df.loc[common_dates, 'count_p'] += 1

            processed += 1
            if processed % 100 == 0:
                print(f"Processed {processed}...")
        except:
            continue

    # Calculate Mean Daily Prcp
    agg_df['avg_prcp'] = agg_df['sum_p'] / agg_df['count_p']
    weather_df = agg_df.reset_index().rename(columns={'index': 'date'}).dropna(subset=['avg_prcp'])

    print(f"Weather processed. Valid daily records: {len(weather_df)}")

    # Merge
    merged = pd.merge(weather_df, astro_df, on='date', how='inner')

    # --- TEST 1: Sun (Tropical) in Water ---
    print("\n--- TEST 1: SUN (TROPICAL) WATER SIGN EFFECT ---")
    water_signs = [3, 7, 11] # Cancer, Scorpio, Pisces

    sun_water_days = merged[merged['Sun_Trop_Sign'].isin(water_signs)]['avg_prcp']
    sun_non_water_days = merged[~merged['Sun_Trop_Sign'].isin(water_signs)]['avg_prcp']

    print(f"Water Days Count: {len(sun_water_days)}")
    print(f"Non-Water Days Count: {len(sun_non_water_days)}")
    print(f"Water Mean: {sun_water_days.mean():.2f}")
    print(f"Non-Water Mean: {sun_non_water_days.mean():.2f}")

    t_stat, p_val = stats.ttest_ind(sun_water_days, sun_non_water_days, equal_var=False)
    print(f"T-Statistic: {t_stat:.4f}")
    print(f"P-Value: {p_val:.4e}")
    if p_val < 0.05:
        print("RESULT: Statistically Significant (p < 0.05)")
    else:
        print("RESULT: Not Significant")

    # --- TEST 2: Moon (Tropical) in Water ---
    print("\n--- TEST 2: MOON (TROPICAL) WATER SIGN EFFECT ---")

    moon_water_days = merged[merged['Moon_Trop_Sign'].isin(water_signs)]['avg_prcp']
    moon_non_water_days = merged[~merged['Moon_Trop_Sign'].isin(water_signs)]['avg_prcp']

    print(f"Water Days Count: {len(moon_water_days)}")
    print(f"Non-Water Days Count: {len(moon_non_water_days)}")
    print(f"Water Mean: {moon_water_days.mean():.2f}")
    print(f"Non-Water Mean: {moon_non_water_days.mean():.2f}")

    t_stat_m, p_val_m = stats.ttest_ind(moon_water_days, moon_non_water_days, equal_var=False)
    print(f"T-Statistic: {t_stat_m:.4f}")
    print(f"P-Value: {p_val_m:.4f}")

if __name__ == "__main__":
    run_stats()
