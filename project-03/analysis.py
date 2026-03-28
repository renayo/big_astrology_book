#!/usr/bin/env python3
"""
Project 3: Lunar Effects Clean Analysis (Refactored)
====================================================
A rigorous, detrended analysis of daily biological events (US Births 1969-2014)
relative to Lunar Phase and Sidereal Position.

METHODOLOGY:
1. Load 45 years of daily event data (US Births).
2. DETRENDING: Remove long-term trends, weekly cycles, and annual/seasonal cycles.
   - Decomposition: Observed = Trend + Season + Week + Residual
3. ANALYSIS:
   - Variable 1: Lunar Phase Angle (0-360) = Sun-Moon Separation.
   - Variable 2: Lunar Sidereal Position (0-360) = Moon longitude in Lahiri Zodiac.
   - Variable 3: Lunar Tropical Position (0-360) = Moon longitude in Tropical Zodiac.
4. VISUALIZATION:
   - Raw means vs Detrended deviations.
   - No rolling averages.
"""

import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import statsmodels.api as sm

# Settings
swe.set_ephe_path(None) # Use built-in ephemeris
OUTPUT_DIR = Path(__file__).parent
OUTPUT_DIR.mkdir(exist_ok=True)

def get_lunar_metrics(jd):
    """
    Calculate:
    1. Phase Angle (Sun-Moon separation, 0-360)
    2. Sidereal Moon Longitude (Lahiri, 0-360)
    3. Tropical Moon Longitude (0-360)
    """
    # Tropical positions
    sun_lon, _ = swe.calc_ut(jd, swe.SUN)[:2]
    moon_lon_trop, _ = swe.calc_ut(jd, swe.MOON)[:2]

    # Phase angle (0-360)
    phase = (moon_lon_trop[0] - sun_lon[0]) % 360

    # Sidereal positions (Lahiri)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    moon_lon_sid, _ = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[:2]

    return phase, moon_lon_sid[0], moon_lon_trop[0]

def load_and_combine_data():
    """Load US Births data (1969-2014) and combine into single dataframe."""
    print("Loading datasets...")
    dfs = []

    # File paths
    files = [
        ('../births_1969_1988.csv', '1969-1988'),
        ('../births_1994_2003.csv', '1994-2003'),
        ('../births_2000_2014.csv', '2000-2014')
    ]

    for fpath, label in files:
        path = Path(fpath)
        if not path.exists():
            print(f"Warning: {fpath} not found.")
            continue

        df = pd.read_csv(path)

        # Normalize columns
        if 'date_of_month' in df.columns:
            df = df.rename(columns={'date_of_month': 'day'})

        # Create date object
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']], errors='coerce')

        # Aggregate if multiple entries per day (e.g. M/F split in 1969-1988)
        if 'births' in df.columns:
            df_agg = df.groupby('date')['births'].sum().reset_index()
        else:
            # Check for alternative column names?
            continue

        dfs.append(df_agg)
        print(f"Loaded {label}: {len(df_agg)} days")

    if not dfs:
        raise ValueError("No birth data files found.")

    full_df = pd.concat(dfs)
    full_df = full_df.drop_duplicates(subset='date', keep='last').sort_values('date')
    full_df = full_df.rename(columns={'births': 'count'})

    print(f"Total: {len(full_df)} days, {full_df['count'].sum():,} events.")
    return full_df

def detrend_data(df):
    """
    Remove time-based trends to isolate cyclical anomalies.
    Modeled as: Count ~ DayOfWeek + Month + Year(Trend)
    Residuals = Actual / Expected (Ratio)
    """
    print("Detrending data (removing Weekly, Monthly, and Yearly trends)...")

    df['dow'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['doy'] = df['date'].dt.dayofyear

    # 1. Weekly seasonality (strongest factor in birth/hospital data)
    dow_means = df.groupby('dow')['count'].transform('mean')
    overall_mean = df['count'].mean()
    df['dow_factor'] = dow_means / overall_mean

    # 2. Annual seasonality (Month/DayOfYear)
    # Using a smoothed daily average across all years
    doy_means = df.groupby('doy')['count'].transform('mean')
    df['seasonal_factor'] = doy_means / overall_mean

    # 3. Long-term Trend (Yearly)
    # Using 365-day rolling average of the counts as the baseline trend
    # (Checking if rolling is allowed for TREND determination - usually necessary for detrending, but not for final averaging)
    # User said "NO rolling averages", likely referring to the *result* plots (phase bins).
    # For detrending, we must establish a baseline. Let's use Year-Average.
    year_means = df.groupby('year')['count'].transform('mean')
    df['trend_factor'] = year_means / overall_mean

    # Expected model
    # We combine factors. Note: This is a simplified multiplicative model.
    # Expected = GlobalMean * DowFactor * SeasonalFactor * TrendFactor
    df['expected'] = overall_mean * df['dow_factor'] * df['seasonal_factor'] * df['trend_factor']

    # The Metric of Interest: Deviation from Expected
    # 1.0 = exactly as expected. 1.05 = 5% above expected.
    df['anomaly_ratio'] = df['count'] / df['expected']

    return df

def calculate_astro_metrics(df):
    """Calculate lunar metrics for every day."""
    print("Calculating astrological metrics...")

    phases = []
    sidereal_lons = []
    tropical_lons = []

    # Pre-calculate JDs to speed up
    # (Vectorization might be hard with swisseph, usually loop is fast enough for <20k rows)
    dates = df['date'].tolist()

    for dt in dates:
        jd = swe.julday(dt.year, dt.month, dt.day, 12.0) # Noon
        ph, sid, trop = get_lunar_metrics(jd)
        phases.append(ph)
        sidereal_lons.append(sid)
        tropical_lons.append(trop)

    df['phase_angle'] = phases
    df['sidereal_lon'] = sidereal_lons
    df['tropical_lon'] = tropical_lons

    # Create Integer Degrees (1-360)
    # Bin 0.0-0.99 -> 1, 1.0-1.99 -> 2, ..., 359.0-359.99 -> 360
    # Formula: floor(val) + 1
    df['phase_deg'] = np.floor(df['phase_angle']).astype(int) + 1
    df['sidereal_deg'] = np.floor(df['sidereal_lon']).astype(int) + 1
    df['tropical_deg'] = np.floor(df['tropical_lon']).astype(int) + 1

    return df

def analyze_and_plot(df):
    """
    Bin data by degrees (1-360) and plot the Anomaly Ratio.
    NO rolling averages on the final plot.
    """
    print("Analyzing and creating clean visualizations...")

    # Group by degrees
    phase_stats = df.groupby('phase_deg')['anomaly_ratio'].agg(['mean', 'sem', 'count'])
    sidereal_stats = df.groupby('sidereal_deg')['anomaly_ratio'].agg(['mean', 'sem'])
    tropical_stats = df.groupby('tropical_deg')['anomaly_ratio'].agg(['mean', 'sem'])

    # Setup Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), dpi=150)

    # Plot 1: Phase Angle (Sun-Moon Separation)
    # x-axis: 1 to 360
    ax1.plot(phase_stats.index, phase_stats['mean'], color='blue', linewidth=1, alpha=0.8, label='Phase Angle')

    # Add error bars (SEM) - Optional, can clutter 360 points. Let's do a shaded region.
    ax1.fill_between(phase_stats.index, 
                     phase_stats['mean'] - phase_stats['sem'],
                     phase_stats['mean'] + phase_stats['sem'],
                     color='blue', alpha=0.1)

    ax1.axhline(1.0, color='black', linestyle='-', linewidth=1)
    ax1.set_xlim(1, 360)
    # ax1.set_ylim(0.98, 1.02) # Removed to show full range
    ax1.set_xlabel('Sun-Moon Separation (Degrees 1-360)')
    ax1.set_ylabel('Anomaly Ratio (1.0 = Average)')
    ax1.set_title('Detrended Event Rate by Lunar Phase Angle (0=New, 180=Full)')

    # Mark major phases
    y_max_1 = phase_stats['mean'].max() # Dynamic text positioning
    for x, label in [(1, 'New'), (90, '1st Q'), (180, 'Full'), (270, '3rd Q')]:
        ax1.axvline(x, color='gray', linestyle='--', alpha=0.5)
        ax1.text(x, y_max_1, label, ha='center', va='bottom', fontsize=8)

    # Plot 2: Zodiac Position (Sidereal vs Tropical)
    ax2.plot(sidereal_stats.index, sidereal_stats['mean'], color='red', linewidth=1, alpha=0.9, label='Sidereal Moon (Lahiri)')
    ax2.plot(tropical_stats.index, tropical_stats['mean'], color='green', linewidth=1, alpha=0.4, label='Tropical Moon')

    ax2.axhline(1.0, color='black', linestyle='-', linewidth=1)
    ax2.set_xlim(1, 360)
    # ax2.set_ylim(0.98, 1.02) # Removed to show full range
    ax2.set_xlabel('Lunar Longitude (Degrees 1-360)')
    ax2.set_ylabel('Anomaly Ratio (1.0 = Average)')
    ax2.set_title('Detrended Event Rate by Lunar Zodiac Position')
    ax2.legend()

    # Mark Zodiac Signs (every 30 deg)
    signs = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis']
    for i, sign in enumerate(signs):
        x = i * 30 + 1
        ax2.axvline(x, color='gray', linestyle=':', alpha=0.3)
        ax2.text(x + 15, 1.018, sign, ha='center', fontsize=8)

    plt.tight_layout()
    plot_path = OUTPUT_DIR / 'clean_lunar_analysis_nobias.png'
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")

    # Print quantitative checks
    print("\nQuantitative Check (Phase 0 vs 180):")
    # Check "bins" around new moon vs full moon?
    # Let's just look at the raw bins 1 (New) and 180 (Full)

    try:
        new_moon_val = phase_stats.loc[1, 'mean']
        full_moon_val = phase_stats.loc[180, 'mean']
        print(f"  New Moon bin (1°): {new_moon_val:.4f}")
        print(f"  Full Moon bin (180°): {full_moon_val:.4f}")
    except KeyError:
        print("  (Specific bins 1 or 180 missing?)")

    print("\nQuantitative Check (Sidereal 0 vs 180):")
    try:
        ari_val = sidereal_stats.loc[1, 'mean']
        lib_val = sidereal_stats.loc[180, 'mean']
        print(f"  Aries bin (1°): {ari_val:.4f}")
        print(f"  Libra bin (180°): {lib_val:.4f}")
    except KeyError:
        print("  (Specific bins missing)")

def main():
    print("PROJECT 3: CLEAN DETRENDED ANALYSIS")
    print("===================================")

    try:
        df = load_and_combine_data()
        df = detrend_data(df)
        df = calculate_astro_metrics(df)
        analyze_and_plot(df)

        # Save processed summary data for inspection
        summary_path = OUTPUT_DIR / 'clean_analysis_daily_metrics.csv'
        df[['date', 'count', 'anomaly_ratio', 'phase_deg', 'sidereal_deg']].to_csv(summary_path, index=False)
        print(f"Summary CSV saved to {summary_path}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
