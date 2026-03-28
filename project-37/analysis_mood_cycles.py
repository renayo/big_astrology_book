import pandas as pd
import numpy as np
import swisseph as swe
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup
swe.set_ephe_path(None) # Use built-in or default ephemeris
DATA_FILE = Path("37-planetary-cycles-mood-surveys/synthetic_mood_1950_2025.csv")
OUTPUT_DIR = Path("37-planetary-cycles-mood-surveys")

def get_astro_features(date_str):
    try:
        # Parse date
        dt = datetime.strptime(str(date_str)[:10], "%Y-%m-%d")
        jd = swe.julday(dt.year, dt.month, dt.day, 12.0) # Noon
        
        # 1. Vedic / Sidereal
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        flags_sid = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
        
        # Sun & Moon Sidereal
        sun_sid = swe.calc_ut(jd, swe.SUN, flags_sid)[0][0]
        moon_sid = swe.calc_ut(jd, swe.MOON, flags_sid)[0][0]
        merc_sid_res = swe.calc_ut(jd, swe.MERCURY, flags_sid)
        merc_sid = merc_sid_res[0][0]
        merc_speed = merc_sid_res[0][3]
        
        # 2. Tropical
        swe.set_sid_mode(0)
        flags_trop = swe.FLG_SWIEPH
        sun_trop = swe.calc_ut(jd, swe.SUN, flags_trop)[0][0]
        moon_trop = swe.calc_ut(jd, swe.MOON, flags_trop)[0][0]
        
        # 3. Features
        
        # Tithi (Vedic Lunar Day) - Distance between Moon and Sun
        # Ensure positive angle 0-360
        diff = (moon_sid - sun_sid) % 360
        tithi_num = int(diff / 12) + 1 # 1-30
        
        # Paksha (Fortnight)
        paksha = "Shukla" if tithi_num <= 15 else "Krishna"
        
        # Zodiac Signs (0=Aries)
        sid_sun_sign = int(sun_sid / 30)
        sid_moon_sign = int(moon_sid / 30)
        trop_sun_sign = int(sun_trop / 30)
        trop_moon_sign = int(moon_trop / 30)
        
        # Retrograde
        is_merc_rx = 1 if merc_speed < 0 else 0
        
        return {
            'tithi': tithi_num,
            'paksha': paksha,
            'sid_sun_sign': sid_sun_sign,
            'sid_moon_sign': sid_moon_sign,
            'trop_sun_sign': trop_sun_sign,
            'trop_moon_sign': trop_moon_sign,
            'merc_rx': is_merc_rx,
            'sun_sid_deg': sun_sid,
            'moon_sid_deg': moon_sid
        }
    except Exception as e:
        # print(e)
        return None

def main():
    print("Loading Mood Data...")
    df = pd.read_csv(DATA_FILE)
    print(f"Loaded {len(df)} records. Calculating Astrology features...")
    
    # Process in chunks or direct apply (apply might be slow for 27k rows but acceptable)
    astro_data = df['date'].apply(get_astro_features)
    astro_df = pd.DataFrame(list(astro_data))
    
    # Combine
    full_df = pd.concat([df, astro_df], axis=1)
    
    print("Analyzing Patterns...")
    
    # 1. Tithi Analysis
    tithi_group = full_df.groupby('tithi')['mood_index'].mean()
    print("\n--- Average Mood by Tithi (1-30) ---")
    print(tithi_group)
    
    # 2. Moon Sign Analysis (Tropical vs Vedic)
    print("\n--- Tropical Moon Sign Effect ---")
    print(full_df.groupby('trop_moon_sign')['mood_index'].mean())
    
    print("\n--- Vedic Moon Sign Effect ---")
    print(full_df.groupby('sid_moon_sign')['mood_index'].mean())
    
    # 3. Mercury Retrograde
    print("\n--- Mercury Retrograde Effect ---")
    print(full_df.groupby('merc_rx')['mood_index'].mean())
    
    # Visualization: Tithi
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=full_df, x='tithi', y='mood_index', estimator='mean', errorbar='ci')
    plt.title("Average Mood Index by Tithi (Vedic Lunar Day)")
    plt.xlabel("Tithi (1-15 Shukla, 16-30 Krishna)")
    plt.ylabel("Mood Index")
    plt.grid(True)
    plt.savefig(OUTPUT_DIR / "tithi_mood_analysis.png")
    print("Saved plot to tithi_mood_analysis.png")
    
    # Statistical Test (ANOVA)
    from scipy.stats import f_oneway
    
    print("\n--- Statistical Significance (ANOVA) ---")
    tithi_groups = [group['mood_index'].values for name, group in full_df.groupby('tithi')]
    f_stat, p_val = f_oneway(*tithi_groups)
    print(f"Tithi: F={f_stat:.2f}, p={p_val:.4f}")
    
    trop_groups = [group['mood_index'].values for name, group in full_df.groupby('trop_moon_sign')]
    f_stat, p_val = f_oneway(*trop_groups)
    print(f"Tropical Moon: F={f_stat:.2f}, p={p_val:.4f}")
    
    sid_groups = [group['mood_index'].values for name, group in full_df.groupby('sid_moon_sign')]
    f_stat, p_val = f_oneway(*sid_groups)
    print(f"Vedic Moon: F={f_stat:.2f}, p={p_val:.4f}")

if __name__ == "__main__":
    main()

