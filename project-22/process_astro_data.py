import pandas as pd
import swisseph as swe
import numpy as np
from datetime import datetime, timedelta
import os

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEATHER_FILE = os.path.join(BASE_DIR, 'weather_data_full_checkpoint.csv')
OUTPUT_FILE = os.path.join(BASE_DIR, 'weather_with_astro_full.csv')

# Initialize Ephemeris
swe.set_ephe_path('/usr/share/swisseph') # Default or None often works if env var set

def get_julian_day(date_str):
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return swe.julday(dt.year, dt.month, dt.day, 12.0) # Noon

def get_zodiac_sign(lon):
    return int(lon / 30)

def get_element(sign_idx):
    # 0=Fire, 1=Earth, 2=Air, 3=Water
    # Aries(0)=Fire, Taurus(1)=Earth, Gemini(2)=Air, Cancer(3)=Water...
    elements = ['Fire', 'Earth', 'Air', 'Water']
    return elements[sign_idx % 4]

def normalize_angle(angle):
    return angle % 360

def calculate_astro_features(row):
    jd = get_julian_day(row['date'])

    # Planets to track
    planets = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mars': swe.MARS,
        'Venus': swe.VENUS,
        'Jupiter': swe.JUPITER,
        'Saturn': swe.SATURN,
        'Uranus': swe.URANUS,
        'Neptune': swe.NEPTUNE,
        'Pluto': swe.PLUTO,
        'Node': swe.MEAN_NODE
    }

    results = {}

    # --- TROPICAL ---
    swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY) # Reset/Standard Tropical? Actually standard is default.
    # To be safe for tropical, we don't set sid mode or we set 0? 
    # Standard swe_calc returns tropical by default unless specific flag used

    tropical_pos = {}
    for name, pid in planets.items():
        res = swe.calc_ut(jd, pid)
        tropical_pos[name] = res[0][0] # Longitude

        results[f'{name}_Tro_Lon'] = tropical_pos[name]
        sign_idx = get_zodiac_sign(tropical_pos[name])
        results[f'{name}_Tro_Sign'] = sign_idx
        results[f'{name}_Tro_Elem'] = get_element(sign_idx)

    # --- VEDIC (LAHIRI) ---
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    vedic_pos = {}
    for name, pid in planets.items():
        res = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL)
        vedic_pos[name] = res[0][0]

        results[f'{name}_Ved_Lon'] = vedic_pos[name]
        sign_idx = get_zodiac_sign(vedic_pos[name])
        results[f'{name}_Ved_Sign'] = sign_idx
        results[f'{name}_Ved_Elem'] = get_element(sign_idx)

    # --- ANGLES (0-360) ---
    # Sun-Moon Angle (Lunar Phase/Day)
    # Tithi Calculation: (Moon - Sun) / 12

    # Tropical Lunar Day
    diff_tro = normalize_angle(tropical_pos['Moon'] - tropical_pos['Sun'])
    results['Sun_Moon_Angle_Tro'] = diff_tro
    results['Lunar_Day_Tro'] = int(diff_tro / 12) + 1

    # Vedic Lunar Day
    diff_ved = normalize_angle(vedic_pos['Moon'] - vedic_pos['Sun'])
    results['Sun_Moon_Angle_Ved'] = diff_ved
    results['Lunar_Day_Ved'] = int(diff_ved / 12) + 1

    # Aspect Angles (0-360) for major pairs (requested "Angles from 1 to 360")
    # Doing primary pairs
    pairs = [('Sun', 'Mars'), ('Sun', 'Saturn'), ('Sun', 'Jupiter'), 
             ('Moon', 'Mars'), ('Moon', 'Saturn'), ('Venus', 'Mars')]

    for p1, p2 in pairs:
        # Tropical
        angle_tro = normalize_angle(tropical_pos[p2] - tropical_pos[p1])
        results[f'{p1}_{p2}_Angle_Tro'] = angle_tro

        # Vedic
        angle_ved = normalize_angle(vedic_pos[p2] - vedic_pos[p1])
        results[f'{p1}_{p2}_Angle_Ved'] = angle_ved

    return pd.Series(results)

def main():
    print("Loading weather data...")
    df = pd.read_csv(WEATHER_FILE)
    print(f"Loaded {len(df)} rows.")

    print("Calculating astrological features (this may take a moment)...")
    # Apply calculation (Pandas apply can be slow, but for 45k rows it's acceptable ~10-20s)
    astro_df = df.apply(calculate_astro_features, axis=1)

    # Merge back
    full_df = pd.concat([df, astro_df], axis=1)

    print(f"Saving to {OUTPUT_FILE}...")
    full_df.to_csv(OUTPUT_FILE, index=False)
    print("Done.")

if __name__ == "__main__":
    main()
