#!/usr/bin/env python3
"""
Project 28: Solar House & Sign Emphasis by Life Domain
"""
import pandas as pd
import numpy as np
import swisseph as swe
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from data_source import CELEBRITY_DATA

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path('/usr/share/libswe/ephe') # Try standard path, or None

PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO
}

SIGNS = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis']

def get_positions(date_str, time_str):
    year, month, day = map(int, date_str.split('-'))
    hour, minute = map(int, time_str.split(':'))
    ut = hour + minute/60.0

    jd = swe.julday(year, month, day, ut)

    positions = {}
    for p_name, p_id in PLANETS.items():
        res = swe.calc_ut(jd, p_id)
        positions[p_name] = res[0][0] # Longitude

    return positions

def analyze():
    records = []

    for person in CELEBRITY_DATA:
        try:
            pos = get_positions(person['date'], person['time'])
            sun_lon = pos['Sun']

            for p_name, lon in pos.items():
                if p_name == 'Sun': continue # Sun is always in 1st Solar House relative to itself

                # 1. Zodiac Sign (0-11)
                sign_idx = int(lon / 30)

                # 2. Solar House (0-11, where 0 = Sun's position)
                # Normalize difference to 0-360
                diff = (lon - sun_lon) % 360
                solar_house_idx = int(diff / 30) + 1 # 1-12

                records.append({
                    'Category': person['category'],
                    'Name': person['name'],
                    'Planet': p_name,
                    'Sign': SIGNS[sign_idx],
                    'Solar_House': solar_house_idx
                })

        except Exception as e:
            print(f"Error processing {person['name']}: {e}")

    df = pd.DataFrame(records)

    # --- Analysis 1: Solar House Distribution by Category ---
    # We want to see: For 'Politics', which Solar Houses are most populated?

    # Normalize by category size
    # Count(Cat, House) / Total_Planets(Cat)
    house_counts = df.groupby(['Category', 'Solar_House']).size().unstack(fill_value=0)
    # Convert to percentages per category
    house_pct = house_counts.div(house_counts.sum(axis=1), axis=0)

    print("\n--- Solar House Emphasis (Percentage of Planets) ---")
    print(house_pct.round(3))

    # Plot Heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(house_pct, annot=True, fmt='.1%', cmap='viridis')
    plt.title('Solar House Emphasis by Profession (Sun = 1st House)')
    plt.xlabel('Solar House (Distance from Sun)')
    plt.ylabel('Profession Category')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'solar_house_heatmap.png')
    print("Saved solar_house_heatmap.png")

    # --- Analysis 2: Sign Element Emphasis ---
    # Map signs to elements
    elements = {
        'Ari': 'Fire', 'Leo': 'Fire', 'Sag': 'Fire',
        'Tau': 'Earth', 'Vir': 'Earth', 'Cap': 'Earth',
        'Gem': 'Air', 'Lib': 'Air', 'Aqu': 'Air',
        'Can': 'Water', 'Sco': 'Water', 'Pis': 'Water'
    }
    df['Element'] = df['Sign'].map(elements)

    element_counts = df.groupby(['Category', 'Element']).size().unstack(fill_value=0)
    element_pct = element_counts.div(element_counts.sum(axis=1), axis=0)

    print("\n--- Element Emphasis (Percentage of Planets) ---")
    print(element_pct.round(3))

    # Plot Element Heatmap
    plt.figure(figsize=(8, 5))
    sns.heatmap(element_pct, annot=True, fmt='.1%', cmap='coolwarm')
    plt.title('Elemental Emphasis by Profession')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'element_heatmap.png')
    print("Saved element_heatmap.png")

    # Save Data
    df.to_csv(OUTPUT_DIR / 'solar_houses_processed.csv', index=False)

if __name__ == '__main__':
    analyze()
