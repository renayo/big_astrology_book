#!/usr/bin/env python3
"""
Project 21: Eclipse Cycles and Collective Mood (Seattle 911 Analysis)
=====================================================================
Data Source: Seattle Real Time Fire 911 Calls (2013-2026)
Metric: Daily Call Volume (Detrended & Normalized)
Hypothesis: Eclipse days show higher chaos/distress (higher call volumes).
"""
import pandas as pd
import numpy as np
import swisseph as swe
from scipy import stats
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

OUTPUT_DIR = Path(__file__).parent
DATA_FILE = OUTPUT_DIR / 'seattle_fire_911.csv'

# Configure Swisseph
try:
    swe.set_ephe_path('/usr/share/swisseph')
except:
    pass

def get_julian_day(dt):
    return swe.julday(dt.year, dt.month, dt.day, 0.0)

def julian_day_to_date_obj(jd):
    year, month, day, hour = swe.revjul(jd)
    return datetime(year, month, day)

def find_all_eclipses(start_dt, end_dt):
    """
    Find all solar and lunar eclipses between start and end dates.
    """
    tjd_start = get_julian_day(start_dt)
    tjd_end = get_julian_day(end_dt)

    eclipses = []
    ERR = -1

    # --- Solar ---
    tjd = tjd_start
    while tjd < tjd_end:
        res = swe.sol_eclipse_when_glob(tjd)
        if res[0] == ERR: break
        tret = res[1] 
        tjd_eclipse = tret[0]
        if tjd_eclipse > tjd_end: break

        eclipses.append({
            'date': julian_day_to_date_obj(tjd_eclipse),
            'type': 'solar_eclipse',
            'category': 'solar'
        })
        tjd = tjd_eclipse + 20 

    # --- Lunar ---
    tjd = tjd_start
    while tjd < tjd_end:
        res = swe.lun_eclipse_when(tjd)
        if res[0] == ERR: break
        tret = res[1]
        tjd_eclipse = tret[0]
        if tjd_eclipse > tjd_end: break

        eclipses.append({
            'date': julian_day_to_date_obj(tjd_eclipse),
            'type': 'lunar_eclipse',
            'category': 'lunar'
        })
        tjd = tjd_eclipse + 20

    return sorted(eclipses, key=lambda x: x['date'])

def process_single_category(df_full, category_name, filter_str):
    """
    Process a single type of 911 call.
    filter_str: substring to match in 'type' column (None for ALL calls)
    """
    if filter_str:
        # Filter
        df = df_full[df_full['type'].str.contains(filter_str, case=False, na=False)].copy()
    else:
        df = df_full.copy()

    if len(df) < 1000: # Skip sparse categories
        return None

    # Aggregating to Daily Counts
    df['date'] = df['datetime'].dt.date
    daily = df.groupby('date').size().reset_index(name='count')
    daily['date'] = pd.to_datetime(daily['date'])
    daily = daily.sort_values('date')

    # Detrending & Normalization
    daily['log_count'] = np.log1p(daily['count'])

    # Remove Day-of-Week Seasonality
    daily['dow'] = daily['date'].dt.dayofweek
    dow_means = daily.groupby('dow')['log_count'].transform('mean')
    daily['deseasonalized'] = daily['log_count'] - dow_means

    # Remove Long-Term Trend
    daily['trend'] = daily['deseasonalized'].rolling(window=90, center=True, min_periods=30).median()
    daily['excess'] = daily['deseasonalized'] - daily['trend']

    # Z-Score
    std_dev = daily['excess'].std()
    daily['z_score'] = daily['excess'] / std_dev

    daily = daily.dropna()
    return daily

def analyze_all_categories():
    print("Loading Seattle 911 Data...")
    if not DATA_FILE.exists():
        print("Data file not found.")
        return

    # Load data once
    df_full = pd.read_csv(DATA_FILE, usecols=['datetime', 'type'])
    df_full['datetime'] = pd.to_datetime(df_full['datetime'])

    min_date = df_full['datetime'].min()
    max_date = df_full['datetime'].max()
    print(f"Data Range: {min_date.date()} to {max_date.date()}")

    # Eclipses
    eclipses = find_all_eclipses(min_date, max_date)
    eclipse_dates = set([e['date'].date() for e in eclipses])
    print(f"Eclipses: {len(eclipses)}")

    # Categories to analyze
    categories = {
        'AID RESPONSE': 'Aid Response',
        'MEDIC RESPONSE': 'Medic Response',
        'AUTO FIRE ALARM': 'Auto Fire Alarm',
        'TRANS TO AMR': 'Trans to AMR',
        'TRIAGED INCIDENT': 'Triaged Incident',
        'MOTOR VEHICLE (MVI)': 'MVI',
        'RESCUE ELEVATOR': 'Rescue Elevator',
        'TOTAL CALLS': None # None means no filter
    }

    results = []

    print("\nStarting Categorical Analysis...")
    print("-" * 80)
    print(f"{'Category':<20} | {'N_Calls':<8} | {'Ec_Mean':<8} | {'Ctrl_Mean':<8} | {'T-Stat':<8} | {'P-Value':<8}")
    print("-" * 80)

    mvi_df = None # Store MVI data for detailed plotting

    for name, filter_str in categories.items():
        daily_df = process_single_category(df_full, name, filter_str)

        if daily_df is None:
            continue

        # Add Eclipse Flag
        eclipse_mask = pd.Series(False, index=daily_df.index)
        for e_date in eclipse_dates:
            mask = (daily_df['date'] == pd.Timestamp(e_date))
            eclipse_mask = eclipse_mask | mask

        daily_df['is_eclipse'] = eclipse_mask

        # Store MVI for later
        if name == 'MOTOR VEHICLE (MVI)':
            mvi_df = daily_df.copy()

        e_vals = daily_df[daily_df['is_eclipse']]['z_score']
        c_vals = daily_df[~daily_df['is_eclipse']]['z_score']

        t_stat, p_val = stats.ttest_ind(e_vals, c_vals, equal_var=False)

        # Original call count for context (approx)
        if filter_str:
            n_raw = len(df_full[df_full['type'].str.contains(filter_str, case=False, na=False)])
        else:
            n_raw = len(df_full)

        print(f"{name:<20} | {n_raw:<8} | {e_vals.mean():.4f}   | {c_vals.mean():.4f}   | {t_stat:.3f}    | {p_val:.4f} {'*' if p_val < 0.05 else ''}")

        results.append({
            'Category': name,
            'N_Calls': n_raw,
            'Eclipse_Mean_Z': e_vals.mean(),
            'Control_Mean_Z': c_vals.mean(),
            'T_Stat': t_stat,
            'P_Value': p_val
        })

    # Save Summary
    res_df = pd.DataFrame(results)
    res_df.to_csv(OUTPUT_DIR / 'categorical_analysis_results.csv', index=False)

    # Plotting P-values
    plt.figure(figsize=(12, 6))
    bars = plt.bar(res_df['Category'], res_df['P_Value'], color=['red' if p < 0.05 else 'gray' for p in res_df['P_Value']])
    plt.axhline(0.05, color='black', linestyle='--', label='p=0.05 Significance')
    plt.ylabel('P-Value (T-test)')
    plt.title('Eclipse Impact Significance by 911 Call Category')
    plt.xticks(rotation=45)
    plt.ylim(0, 1.0)

    # Add labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'categorical_significance.png')
    plt.close()

    # --- NEW VIZ 1: Effect Size (Mean Difference) ---
    res_df['Mean_Diff'] = res_df['Eclipse_Mean_Z'] - res_df['Control_Mean_Z']

    plt.figure(figsize=(12, 6))
    colors = ['green' if x > 0 else 'red' for x in res_df['Mean_Diff']]
    bars = plt.bar(res_df['Category'], res_df['Mean_Diff'], color=colors)
    plt.axhline(0, color='black', linestyle='-', linewidth=1)

    plt.ylabel('Mean Z-Score Difference (Eclipse - Control)')
    plt.title('Eclipse Effect Direction (Positive = More Calls, Negative = Fewer Calls)')
    plt.xticks(rotation=45)

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        y_pos = height if height > 0 else height
        va = 'bottom' if height > 0 else 'top'
        plt.text(bar.get_x() + bar.get_width()/2., y_pos,
                f'{height:.3f}', ha='center', va=va, fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'categorical_effect_size.png')
    plt.close()

    # --- NEW VIZ 2: MVI Distribution Plot ---
    if mvi_df is not None:
        plt.figure(figsize=(10, 6))

        # Separate data
        eclipse_mvi = mvi_df[mvi_df['is_eclipse']]['z_score']
        control_mvi = mvi_df[~mvi_df['is_eclipse']]['z_score']

        # Plot KDEs
        try:
            eclipse_mvi.plot(kind='kde', color='red', label=f'Eclipse Days (n={len(eclipse_mvi)})', linewidth=2)
            control_mvi.plot(kind='kde', color='blue', label=f'Control Days (n={len(control_mvi)})', linestyle='--', linewidth=1)

            plt.title('Distribution of Motor Vehicle Incidents (MVI) Volume\nEclipse vs. Non-Eclipse Days')
            plt.xlabel('Daily Volume Z-Score (0 = Average)')
            plt.ylabel('Density')
            plt.legend()
            plt.grid(alpha=0.3)
            plt.xlim(-3, 3) # Limit to relevant Z-score range

            plt.tight_layout()
            plt.savefig(OUTPUT_DIR / 'mvi_distribution.png')
            plt.close()
            print("Saved mvi_distribution.png")
        except Exception as e:
            print(f"Could not plot MVI distribution: {e}")

    print("-" * 80)
    print("Saved categorical_analysis_results.csv, categorical_significance.png, categorical_effect_size.png")

if __name__ == "__main__":
    analyze_all_categories()
