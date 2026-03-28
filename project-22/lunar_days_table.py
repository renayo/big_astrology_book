import swisseph as swe
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def calculate_lunar_days(start_year, end_year):
    """
    Generates a DataFrame with Date, Sun_Lon, Moon_Lon, Phase_Angle, Tithi (1-30), Moon_Sign (0-11).
    """

    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    days = (end_date - start_date).days + 1

    dates = []
    tithis = []
    phases = []
    moon_signs = []
    sun_signs = []

    print(f"Calculating lunar metrics for {days} days between {start_year} and {end_year}...")

    for i in range(days):
        current_date = start_date + timedelta(days=i)
        dates.append(current_date.strftime('%Y-%m-%d'))

        # Noon UTC
        jd = swe.julday(current_date.year, current_date.month, current_date.day, 12.0)

        # Calculate Sun and Moon positions
        sun_res = swe.calc_ut(jd, swe.SUN)
        moon_res = swe.calc_ut(jd, swe.MOON)

        sun_lon = sun_res[0][0]
        moon_lon = moon_res[0][0]

        # Calculate Phase Angle (0-360) where 0 is New Moon
        phase_angle = (moon_lon - sun_lon) % 360
        phases.append(phase_angle)

        # Calculate Tithi (1-30)
        tithi = int(phase_angle / 12) + 1
        tithis.append(tithi)

        # Calculate Signs (0 = Aries, 1 = Taurus, ...)
        moon_sign = int(moon_lon / 30)
        sun_sign = int(sun_lon / 30)

        moon_signs.append(moon_sign)
        sun_signs.append(sun_sign)

    df = pd.DataFrame({
        'date': dates,
        'phase_angle': phases,
        'tithi': tithis,
        'moon_sign': moon_signs,
        'sun_sign': sun_signs
    })

    return df

if __name__ == "__main__":
    # Generate for a wide range to cover historical weather data if needed
    df = calculate_lunar_days(1900, 2024)

    output_path = os.path.join(os.path.dirname(__file__), 'lunar_data.csv')
    df.to_csv(output_path, index=False)
    print(f"Saved lunar data to {output_path}")
