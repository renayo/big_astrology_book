#!/usr/bin/env python3
"""Project 20b: Genetic Algorithms for Rule Discovery"""
import numpy as np
import pandas as pd
import swisseph as swe
from datetime import datetime
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path(None)

def load_celebrity_data(csv_path):
    df = pd.read_csv(csv_path)
    people = []
    for idx, row in df.iterrows():
        name = row['Name']
        birthdate = row['Birthdate']
        category = row['Category'] if 'Category' in row else 'Unknown'
        if not birthdate or pd.isna(birthdate):
            continue
        birthtime = row['Time'] if 'Time' in row and not pd.isna(row['Time']) else '12:00'
        people.append((name, birthdate, birthtime, category))
    return people

CELEBRITIES = load_celebrity_data(OUTPUT_DIR / 'celebrity_data.csv')

def datetime_to_jd(dt):
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0)

def get_chart_features_tropical(jd):
    """Get signs for all major planets and nodes."""
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
        'Rahu': swe.MEAN_NODE
    }

    positions = {}
    for name, pid in bodies.items():
        res = swe.calc_ut(jd, pid)[0]
        sign = int(res[0] / 30)
        positions[name] = sign

    # Calculate Ketu (opposite Rahu)
    ketu_deg = (swe.calc_ut(jd, swe.MEAN_NODE)[0][0] + 180) % 360
    positions['Ketu'] = int(ketu_deg / 30)

    return positions

def get_chart_features_vedic(jd):
    """Get Sidereal Lahiri signs for all major planets and nodes."""
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
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
        'Rahu': swe.MEAN_NODE
    }

    flags = swe.FLG_SIDEREAL | swe.FLG_SWIEPH | swe.FLG_SPEED
    positions = {}

    for name, pid in bodies.items():
        res = swe.calc_ut(jd, pid, flags=flags)[0]
        sign = int(res[0] / 30)
        positions[name] = sign

    # Calculate Ketu (opposite Rahu)
    rahu_deg = swe.calc_ut(jd, swe.MEAN_NODE, flags=flags)[0][0]
    ketu_deg = (rahu_deg + 180) % 360
    positions['Ketu'] = int(ketu_deg / 30)

    return positions

def fitness(rule, data):
    """Evaluate rule fitness. Rule is dict like {'planet': 'Sun', 'sign': 0}"""
    target_planet = rule['planet']
    target_sign = rule['sign']
    matches = sum(1 for d in data if d.get(target_planet) == target_sign)
    return matches / len(data)

def analyze_dataset(data, system_name):
    """Run exhaustive search for all single-factor rules."""
    planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Rahu', 'Ketu']
    signs = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis']

    all_results = []

    for planet in planets:
        best_for_planet = {'fitness': -1}

        for sign_idx in range(12):
            rule = {'planet': planet, 'sign': sign_idx}
            fit = fitness(rule, data)

            result = {
                'planet': planet,
                'sign': signs[sign_idx],
                'fitness': fit,
                'n': int(fit * len(data))
            }
            all_results.append(result)

            if fit > best_for_planet['fitness']:
                best_for_planet = result

    # Sort by fitness descending
    all_results.sort(key=lambda x: x['fitness'], reverse=True)

    print(f"\n[{system_name}] TOP 10 RULES FOUND:")
    print(f"{'Planet':<10} {'Sign':<5} {'Fitness':<8} {'Count':<5}")
    print("-" * 35)
    for r in all_results[:10]:
        print(f"{r['planet']:<10} {r['sign']:<5} {r['fitness']:.3f}    {r['n']:<5}")

    return all_results

def main():
    print("=" * 60)
    print("PROJECT 20b: GENETIC ALGORITHM RULE DISCOVERY (EXTENDED)")
    print(f"Dataset Size: {len(CELEBRITIES)} High-Profile Individuals")
    print("=" * 60)

    # 1. Tropical Analysis
    data_tropical = []
    for name, bd, bt, category in CELEBRITIES:
        try:
            dt = datetime.strptime(f"{bd} {bt}", "%Y-%m-%d %H:%M")
            features = get_chart_features_tropical(datetime_to_jd(dt))
            features['category'] = category
            data_tropical.append(features)
        except Exception:
            continue

    if data_tropical:
        results_trop = analyze_dataset(data_tropical, "TROPICAL")
        pd.DataFrame(results_trop).to_csv(OUTPUT_DIR / 'analysis_results_tropical_extended.csv', index=False)

    # 2. Vedic Analysis
    data_vedic = []
    for name, bd, bt, category in CELEBRITIES:
        try:
            dt = datetime.strptime(f"{bd} {bt}", "%Y-%m-%d %H:%M")
            features = get_chart_features_vedic(datetime_to_jd(dt))
            features['category'] = category
            data_vedic.append(features)
        except Exception:
            continue

    if data_vedic:
        results_vedic = analyze_dataset(data_vedic, "VEDIC (LAHIRI)")
        pd.DataFrame(results_vedic).to_csv(OUTPUT_DIR / 'analysis_results_vedic_extended.csv', index=False)

    print(f"\nExtended results saved to {OUTPUT_DIR}")

if __name__ == '__main__':
    main()
