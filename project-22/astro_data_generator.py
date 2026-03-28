import swisseph as swe
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def get_planet_positions(jd, mode='tropical'):
    """
    Returns a dict of planet longitudes for a given Julian Day.
    mode: 'tropical' or 'vedic'
    """

    if mode == 'vedic':
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    else:
        swe.set_sid_mode(0) # Reset to tropical just in case
        flags = swe.FLG_SWIEPH

    bodies = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mercury': swe.MERCURY,
        'Venus': swe.VENUS,
        'Mars': swe.MARS,
        'Jupiter': swe.JUPITER,
        'Saturn': swe.SATURN,
        'Uranus': swe.URANUS,
        'Neptune': swe.NEPTUNE,
        'Pluto': swe.PLUTO,
        'NorthNode': swe.TRUE_NODE
    }

    positions = {}
    for name, pid in bodies.items():
        try:
            res = swe.calc_ut(jd, pid, flags)
            positions[name] = res[0][0] # Longitude
        except swe.Error as e:
            print(f"Error calculating {name}: {e}")
            positions[name] = 0.0

    # South Node is strictly opposite North Node
    positions['SouthNode'] = (positions['NorthNode'] + 180.0) % 360.0

    return positions

def calculate_astro_data(start_year, end_year):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    days = (end_date - start_date).days + 1

    data_rows = []

    print(f"Calculating full astro metrics for {days} days between {start_year} and {end_year}...")

    for i in range(days):
        current_date = start_date + timedelta(days=i)
        date_str = current_date.strftime('%Y-%m-%d')

        # Noon UTC
        jd = swe.julday(current_date.year, current_date.month, current_date.day, 12.0)

        # Tropical
        trop_pos = get_planet_positions(jd, mode='tropical')
        # Vedic
        vedic_pos = get_planet_positions(jd, mode='vedic')

        row = {'date': date_str}

        # Store Tropical
        for body, lon in trop_pos.items():
            row[f'{body}_Trop_Lon'] = lon
            row[f'{body}_Trop_Sign'] = int(lon / 30)

        # Store Vedic
        for body, lon in vedic_pos.items():
            row[f'{body}_Vedic_Lon'] = lon
            row[f'{body}_Vedic_Sign'] = int(lon / 30)

        # Reuse Phase/Tithi from Tropical logic (Standard definition uses tropical difference usually, 
        # but Tithi is often Sidereal in Indian context? 
        # Actually Tithi is Phase based. Phase is independent of Zodiac (Moon - Sun). 
        # Let's verify: (Moon_Trop - Sun_Trop) == (Moon_Sid - Sun_Sid) mathematically.
        # So we just calculate it once.

        phase_angle = (trop_pos['Moon'] - trop_pos['Sun']) % 360
        row['Phase_Angle'] = phase_angle
        row['Tithi'] = int(phase_angle / 12) + 1

        data_rows.append(row)

        if i % 10000 == 0:
            print(f"Processed {i}/{days} days...")

    df = pd.DataFrame(data_rows)
    return df

if __name__ == "__main__":
    # Generate for 1900 to 2024 to match full weather dataset scope
    df = calculate_astro_data(1900, 2024)

    output_path = os.path.join(os.path.dirname(__file__), 'astro_weather_features.csv')
    df.to_csv(output_path, index=False)
    print(f"Saved full astro data to {output_path}")
