import pandas as pd
import swisseph as swe
from datetime import datetime
import os

# CONFIG
# ==============================================================================
# REMOVE PLANETARY EXPLORATIONS: ONLY Moon
PLANETS_TO_ANALYZE = {
    swe.MOON: 'Moon'
}

SIGN_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
              'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

def get_positions(dt):
    # Noon UTC
    jd = swe.julday(dt.year, dt.month, dt.day, 12.0)
    pos = {}

    # 1. MOON (Tropical & Vedic)
    # Tropical
    moon_trop_deg = swe.calc_ut(jd, swe.MOON)[0][0]
    moon_sign_trop = int(moon_trop_deg / 30) % 12
    pos["Moon_Tropical"] = SIGN_NAMES[moon_sign_trop]

    # Vedic (Lahiri)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    moon_vedic_deg = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]
    moon_sign_vedic = int(moon_vedic_deg / 30) % 12
    pos["Moon_Vedic"] = SIGN_NAMES[moon_sign_vedic]

    # 2. SUN (Tropical)
    sun_trop_deg = swe.calc_ut(jd, swe.SUN)[0][0]
    sun_sign_trop = int(sun_trop_deg / 30) % 12
    pos["Sun_Tropical"] = SIGN_NAMES[sun_sign_trop]

    # 3. TITHI (Vedic Lunar Day)
    sun_trop_deg = swe.calc_ut(jd, swe.SUN)[0][0]

    diff = (moon_trop_deg - sun_trop_deg) % 360
    tithi_num = int(diff / 12) + 1  # 1 to 30

    if tithi_num <= 15:
        paksha = "Shukla"  # Waxing
        day = tithi_num
    else:
        paksha = "Krishna"  # Waning
        day = tithi_num - 15

    tithi_name = f"{paksha} {day:02d}"
    if tithi_num == 15: tithi_name = "Purnima (Full)"
    if tithi_num == 30: tithi_name = "Amavasya (New)"

    pos["Tithi"] = tithi_name

    return pos

def load_and_merge_data():
    print("Loading real datasets...")

    try:
        df1 = pd.read_csv("births_1969_1988.csv")
        df1 = df1.groupby(['year', 'month', 'day'])['births'].sum().reset_index()
        df1 = df1[df1['year'] >= 1970]
        print(f"Loaded 1970-1988 data: {len(df1)} days")
    except Exception as e:
        print(f"Error loading births_1969_1988.csv: {e}")
        df1 = pd.DataFrame()

    try:
        df2 = pd.read_csv("births_1994_2003.csv")
        df2 = df2.rename(columns={'date_of_month': 'day'})
        df2 = df2[['year', 'month', 'day', 'births']]
        print(f"Loaded 1994-2003 data: {len(df2)} days")
    except Exception as e:
        print(f"Error loading births_1994_2003.csv: {e}")
        df2 = pd.DataFrame()

    try:
        df3 = pd.read_csv("births_2000_2014.csv")
        df3 = df3.rename(columns={'date_of_month': 'day'})
        df3 = df3[['year', 'month', 'day', 'births']]
        df3 = df3[df3['year'] >= 2004]
        print(f"Loaded 2004-2014 data: {len(df3)} days")
    except Exception as e:
        print(f"Error loading births_2000_2014.csv: {e}")
        df3 = pd.DataFrame()

    full_df = pd.concat([df1, df2, df3], ignore_index=True)
    full_df = full_df.sort_values(['year', 'month', 'day'])

    full_df['year'] = pd.to_numeric(full_df['year'], errors='coerce')
    full_df['month'] = pd.to_numeric(full_df['month'], errors='coerce')
    full_df['day'] = pd.to_numeric(full_df['day'], errors='coerce')

    full_df = full_df.dropna(subset=['year', 'month', 'day'])
    full_df = full_df[(full_df['month'] >= 1) & (full_df['month'] <= 12)]
    full_df = full_df[(full_df['day'] >= 1) & (full_df['day'] <= 31)]

    full_df['date'] = pd.to_datetime(full_df[['year', 'month', 'day']], errors='coerce')

    n_before = len(full_df)
    full_df = full_df.dropna(subset=['date'])
    n_after = len(full_df)
    if n_before != n_after:
        print(f"Dropped {n_before - n_after} rows with invalid dates")

    print(f"Total Daily Records: {len(full_df)}")
    print(f"Date Range: {full_df['date'].min().date()} to {full_df['date'].max().date()}")
    print(f"Total Births: {full_df['births'].sum():,}")

    return full_df

def analyze():
    df = load_and_merge_data()

    if df.empty:
        print("No data found!")
        return

    print("Calculating Moon Positions & Tithis...")
    unique_dates = df['date'].unique()
    pos_map = {pd.Timestamp(dt): get_positions(pd.Timestamp(dt)) for dt in unique_dates}

    pos_df = pd.DataFrame.from_dict(pos_map, orient='index')

    df = df.merge(pos_df, left_on='date', right_index=True)

    results = []

    position_cols = ["Moon_Tropical", "Moon_Vedic", "Tithi", "Sun_Tropical"]

    total_births_global = df['births'].sum()
    total_days_global = len(df)
    global_avg = total_births_global / total_days_global
    print(f"Global Average Births/Day: {global_avg:.2f}")

    for col in position_cols:
        if "Sun" in col: category = "Sun Sign (Tropical)"
        elif "Tropical" in col: category = "Moon Sign (Tropical)"
        elif "Vedic" in col: category = "Moon Sign (Vedic)"
        else: category = "Tithi (Lunar Day)"

        groups = df.groupby(col)

        for name, group in groups:
            n_days = len(group)
            total_b = group['births'].sum()
            avg_b = total_b / n_days

            deviance = (avg_b - global_avg) / global_avg * 100

            results.append({
                'Category': category,
                'Value': name,
                'Avg_Births': avg_b,
                'Days_Count': n_days,
                'Deviance_Pct': deviance
            })

    res_df = pd.DataFrame(results)
    res_df = res_df.sort_values(by='Deviance_Pct', ascending=False)

    output_path = "01-temporal-pattern-birth-data/real_data_moon_tithi_results.csv"
    res_df.to_csv(output_path, index=False)
    print(f"\nResults saved to {output_path}")

if __name__ == "__main__":
    analyze()
