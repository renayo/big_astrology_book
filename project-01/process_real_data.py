import pandas as pd
import swisseph as swe
from datetime import datetime
import os

# CONFIG
# ==============================================================================
PLANETS = {
    swe.MOON: 'Moon',
    swe.MARS: 'Mars',
    swe.JUPITER: 'Jupiter',
    swe.SATURN: 'Saturn'
}

SIGN_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
              'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

def get_positions(dt):
    # Noon UTC
    jd = swe.julday(dt.year, dt.month, dt.day, 12.0)
    pos = {}

    for pid, name in PLANETS.items():
        # Tropical
        res_trop = swe.calc_ut(jd, pid)[0][0]
        sign_trop = int(res_trop / 30) % 12
        pos[f"{name}_Trop"] = SIGN_NAMES[sign_trop]

        # Vedic (Lahiri)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        res_vedic = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL)[0][0]
        sign_vedic = int(res_vedic / 30) % 12
        pos[f"{name}_Vedic"] = SIGN_NAMES[sign_vedic]

    return pos

def load_and_merge_data():
    print("Loading real datasets...")

    # 1. 1969-1988 (CDC)
    # format: year,month,day,gender,births
    # Note: 1969 data exists, user wants Jan 1 1970 onwards.
    try:
        df1 = pd.read_csv("births_1969_1988.csv")
        df1 = df1.groupby(['year', 'month', 'day'])['births'].sum().reset_index()
        df1 = df1[df1['year'] >= 1970]
        print(f"Loaded 1970-1988 data: {len(df1)} days")
    except Exception as e:
        print(f"Error loading births_1969_1988.csv: {e}")
        df1 = pd.DataFrame()

    # 2. 1994-2003 (CDC NCHS)
    # format: year,month,date_of_month,day_of_week,births
    try:
        df2 = pd.read_csv("births_1994_2003.csv")
        df2 = df2.rename(columns={'date_of_month': 'day'})
        df2 = df2[['year', 'month', 'day', 'births']]
        print(f"Loaded 1994-2003 data: {len(df2)} days")
    except Exception as e:
        print(f"Error loading births_1994_2003.csv: {e}")
        df2 = pd.DataFrame()

    # 3. 2000-2014 (SSA)
    # format: year,month,date_of_month,day_of_week,births
    # USE ONLY 2004-2014 (since 1994-2003 covered by CDC, which is usually preferred)
    try:
        df3 = pd.read_csv("births_2000_2014.csv")
        df3 = df3.rename(columns={'date_of_month': 'day'})
        df3 = df3[['year', 'month', 'day', 'births']]
        df3 = df3[df3['year'] >= 2004]
        print(f"Loaded 2004-2014 data: {len(df3)} days")
    except Exception as e:
        print(f"Error loading births_2000_2014.csv: {e}")
        df3 = pd.DataFrame()

    # Merge
    full_df = pd.concat([df1, df2, df3], ignore_index=True)
    full_df = full_df.sort_values(['year', 'month', 'day'])

    # Ensure numeric
    full_df['year'] = pd.to_numeric(full_df['year'], errors='coerce')
    full_df['month'] = pd.to_numeric(full_df['month'], errors='coerce')
    full_df['day'] = pd.to_numeric(full_df['day'], errors='coerce')

    # Drop NaNs
    full_df = full_df.dropna(subset=['year', 'month', 'day'])

    # Filter insane values
    full_df = full_df[(full_df['month'] >= 1) & (full_df['month'] <= 12)]
    full_df = full_df[(full_df['day'] >= 1) & (full_df['day'] <= 31)]

    # Create datetime object, coerce errors (e.g. Feb 30)
    full_df['date'] = pd.to_datetime(full_df[['year', 'month', 'day']], errors='coerce')

    # Drop rows where date failed
    n_before = len(full_df)
    full_df = full_df.dropna(subset=['date'])
    n_after = len(full_df)
    if n_before != n_after:
        print(f"Dropped {n_before - n_after} rows with invalid dates (e.g. Feb 30 or 99)")

    print(f"Total Daily Records: {len(full_df)}")
    print(f"Date Range: {full_df['date'].min().date()} to {full_df['date'].max().date()}")
    print(f"Total Births: {full_df['births'].sum():,}")

    return full_df

def analyze():
    df = load_and_merge_data()

    if df.empty:
        print("No data found!")
        return

    print("Calculating planetary positions...")
    # Add columns for positions
    # Optimize: Precompute unique dates (positions only depend on date)
    unique_dates = df['date'].unique()
    pos_map = {pd.Timestamp(dt): get_positions(pd.Timestamp(dt)) for dt in unique_dates}

    # Expand dictionary into columns
    pos_df = pd.DataFrame.from_dict(pos_map, orient='index')

    # Merge back to main df
    df = df.merge(pos_df, left_on='date', right_index=True)

    results = []

    # Columns to analyze
    position_cols = [c for c in pos_df.columns] # e.g. Moon_Trop, Moon_Vedic...

    total_births_global = df['births'].sum()
    total_days_global = len(df)
    global_avg = total_births_global / total_days_global
    print(f"Global Average Births/Day: {global_avg:.2f}")

    for col in position_cols:
        system = "Tropical" if "Trop" in col else "Vedic"
        planet = col.split('_')[0]

        # Group by Sign
        groups = df.groupby(col)

        for sign, group in groups:
            n_days = len(group)
            total_b = group['births'].sum()
            avg_b = total_b / n_days

            deviance = (avg_b - global_avg) / global_avg * 100

            results.append({
                'System': system,
                'Planet': planet,
                'Sign': sign,
                'Avg_Births': avg_b,
                'Days_Count': n_days,
                'Deviance_Pct': deviance
            })

    # Save Results
    res_df = pd.DataFrame(results)
    res_df = res_df.sort_values(by='Deviance_Pct', ascending=False) # sort by deviation

    output_path = "01-temporal-pattern-birth-data/real_data_analysis_results.csv"
    res_df.to_csv(output_path, index=False)
    print(f"\nResults saved to {output_path}")

    print("\n--- TOP DEVIATIONS (Tropical) ---")
    print(res_df[res_df['System']=='Tropical'].head(10))
    print("\n--- MOON DEVIATIONS (Tropical) ---")
    print(res_df[(res_df['System']=='Tropical') & (res_df['Planet']=='Moon')].sort_values('Sign'))

    print("\n--- TOP DEVIATIONS (Vedic) ---")
    print(res_df[res_df['System']=='Vedic'].head(10))

if __name__ == "__main__":
    analyze()
