#!/usr/bin/env python3
"""
Project 14: Celestial Mechanics - Ancient Techniques
====================================================
Comparing Essential Dignities in Tropical vs. Sidereal (Vedic) Systems.

METHODOLOGY:
1. Load Celebrity Dataset (211 records from Project 13).
2. Calculate Planetary Positions (Sun-Saturn) for:
   - Tropical Zodiac
   - Sidereal Zodiac (Lahiri Ayanamsa)
3. Calculate Essential Dignity Scores (Ptolemaic/Parashari simplified):
   - Domicile: +5
   - Exaltation: +4
   - Detriment: -5
   - Fall: -4
   - Peregrine: 0
4. Compare Dignity Scores between systems and across professions.
"""

import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path(None)

# --- CELEBRITY DATA (Imported from Project 13) ---
CELEBRITY_DATA = [
     # PERFORMERS
    ('Marilyn Monroe', '1926-06-01', 'performer'), ('Elvis Presley', '1935-01-08', 'performer'),
    ('Michael Jackson', '1958-08-29', 'performer'), ('Prince', '1958-06-07', 'performer'),
    ('David Bowie', '1947-01-08', 'performer'), ('Freddie Mercury', '1946-09-05', 'performer'),
    ('Whitney Houston', '1963-08-09', 'performer'), ('Amy Winehouse', '1983-09-14', 'performer'),
    ('Kurt Cobain', '1967-02-20', 'performer'), ('Jimi Hendrix', '1942-11-27', 'performer'),
    ('Janis Joplin', '1943-01-19', 'performer'), ('Jim Morrison', '1943-12-08', 'performer'),
    ('John Lennon', '1940-10-09', 'performer'), ('George Harrison', '1943-02-25', 'performer'),
    ('Frank Sinatra', '1915-12-12', 'performer'), ('Dean Martin', '1917-06-07', 'performer'),
    ('Sammy Davis Jr', '1925-12-08', 'performer'), ('Lucille Ball', '1911-08-06', 'performer'),
    ('Robin Williams', '1951-07-21', 'performer'), ('John Belushi', '1949-01-24', 'performer'),
    ('Richard Pryor', '1940-12-01', 'performer'), ('George Carlin', '1937-05-12', 'performer'),
    ('Madonna', '1958-08-16', 'performer'), ('Lady Gaga', '1986-03-28', 'performer'),
    ('Beyonce', '1981-09-04', 'performer'), ('Taylor Swift', '1989-12-13', 'performer'),
    ('Kanye West', '1977-06-08', 'performer'), ('Eminem', '1972-10-17', 'performer'),
    ('Tupac Shakur', '1971-06-16', 'performer'), ('Notorious BIG', '1972-05-21', 'performer'),
    ('Bob Dylan', '1941-05-24', 'performer'), ('Paul McCartney', '1942-06-18', 'performer'),

    # SCIENTISTS
    ('Albert Einstein', '1879-03-14', 'scientist'), ('Isaac Newton', '1643-01-04', 'scientist'),
    ('Charles Darwin', '1809-02-12', 'scientist'), ('Marie Curie', '1867-11-07', 'scientist'),
    ('Nikola Tesla', '1856-07-10', 'scientist'), ('Thomas Edison', '1847-02-11', 'scientist'),
    ('Stephen Hawking', '1942-01-08', 'scientist'), ('Richard Feynman', '1918-05-11', 'scientist'),
    ('Carl Sagan', '1934-11-09', 'scientist'), ('Alan Turing', '1912-06-23', 'scientist'),
    ('Galileo Galilei', '1564-02-15', 'scientist'), ('Johannes Kepler', '1571-12-27', 'scientist'),
    ('Niels Bohr', '1885-10-07', 'scientist'), ('Werner Heisenberg', '1901-12-05', 'scientist'),
    ('Erwin Schrodinger', '1887-08-12', 'scientist'), ('Max Planck', '1858-04-23', 'scientist'),
    ('Louis Pasteur', '1822-12-27', 'scientist'), ('Sigmund Freud', '1856-05-06', 'scientist'),
    ('Carl Jung', '1875-07-26', 'scientist'), ('John von Neumann', '1903-12-28', 'scientist')
]

# --- ESSENTIAL DIGNITIES MAP ---
SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

DIGNITIES = {
    'Sun': {'domicile': ['Leo'], 'exaltation': 'Aries', 'detriment': ['Aquarius'], 'fall': 'Libra'},
    'Moon': {'domicile': ['Cancer'], 'exaltation': 'Taurus', 'detriment': ['Capricorn'], 'fall': 'Scorpio'},
    'Mercury': {'domicile': ['Gemini', 'Virgo'], 'exaltation': 'Virgo', 'detriment': ['Sagittarius', 'Pisces'], 'fall': 'Pisces'},
    'Venus': {'domicile': ['Taurus', 'Libra'], 'exaltation': 'Pisces', 'detriment': ['Scorpio', 'Aries'], 'fall': 'Virgo'},
    'Mars': {'domicile': ['Aries', 'Scorpio'], 'exaltation': 'Capricorn', 'detriment': ['Libra', 'Taurus'], 'fall': 'Cancer'},
    'Jupiter': {'domicile': ['Sagittarius', 'Pisces'], 'exaltation': 'Cancer', 'detriment': ['Gemini', 'Virgo'], 'fall': 'Capricorn'},
    'Saturn': {'domicile': ['Capricorn', 'Aquarius'], 'exaltation': 'Libra', 'detriment': ['Cancer', 'Leo'], 'fall': 'Aries'},
}

def get_positions(jd, sidereal=False):
    """
    Get sign placement for Sun-Saturn.
    """
    if sidereal:
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    else:
        flags = swe.FLG_SWIEPH

    planets = [
        (swe.SUN, 'Sun'), (swe.MOON, 'Moon'), (swe.MERCURY, 'Mercury'),
        (swe.VENUS, 'Venus'), (swe.MARS, 'Mars'), (swe.JUPITER, 'Jupiter'),
        (swe.SATURN, 'Saturn')
    ]

    positions = {}
    for pid, name in planets:
        # Longitude
        lon = swe.calc_ut(jd, pid, flags)[0][0]
        sign_idx = int(lon / 30)
        positions[name] = SIGNS[sign_idx]

    return positions

def calculate_score(positions):
    """
    Calculate simple essential dignity score.
    """
    score = 0
    breakdown = {}

    for planet, sign in positions.items():
        p_score = 0
        rule = DIGNITIES.get(planet)

        if sign in rule['domicile']:
            p_score = 5
        elif sign == rule['exaltation']:
            p_score = 4
        elif sign in rule['detriment']:
            p_score = -5
        elif sign == rule['fall']:
            p_score = -4
        else:
            p_score = 0 # Peregrine (simplified)

        score += p_score
        breakdown[planet] = p_score

    return score, breakdown

def run_analysis():
    print("Project 14: Tropical vs Vedic Dignity Analysis")
    print("-" * 50)

    results = []

    for name, date_str, profession in CELEBRITY_DATA:
        try:
            # Noon birth time default
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            jd = swe.julday(dt.year, dt.month, dt.day, 12.0)

            # Tropical
            trop_pos = get_positions(jd, sidereal=False)
            trop_score, trop_breakdown = calculate_score(trop_pos)

            # Sidereal
            sid_pos = get_positions(jd, sidereal=True)
            sid_score, sid_breakdown = calculate_score(sid_pos)

            row = {
                'name': name,
                'profession': profession,
                'Trop_Score': trop_score,
                'Sid_Score': sid_score,
                'Delta': sid_score - trop_score
            }
            # Add planet scores
            for p in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
                row[f'Trop_{p}'] = trop_breakdown[p]
                row[f'Sid_{p}'] = sid_breakdown[p]

            results.append(row)

        except Exception as e:
            print(f"Error {name}: {e}")

    df = pd.DataFrame(results)

    # OUTPUT RESULTS
    with open(OUTPUT_DIR / 'RESULTS.md', 'w') as f:
        f.write("# Project 14 Results: Ancient Dignities & Celestial Mechanics\n\n")

        f.write("## 1. Overall Dignity Score Comparison\n")
        f.write("Comparing the sum of Essential Dignities (Sun-Saturn) in Tropical vs. Sidereal.\n\n")
        f.write("| Metric | Tropical Mean | Sidereal Mean | Diff |\n|---|---|---|---|\n")
        t_mean = df['Trop_Score'].mean()
        s_mean = df['Sid_Score'].mean()
        f.write(f"| All Celebrities | {t_mean:.2f} | {s_mean:.2f} | {s_mean - t_mean:.2f} |\n")

        f.write("\n## 2. Scores by Profession\n")
        f.write("| Profession | Tropical Mean | Sidereal Mean | T-Test (p) |\n|---|---|---|---|\n")

        for prof in df['profession'].unique():
            sub = df[df['profession'] == prof]
            t = sub['Trop_Score'].mean()
            s = sub['Sid_Score'].mean()

            # Simple t-test between systems for this group
            # (Paired t-test as it's the same people)
            stat, p = stats.ttest_rel(sub['Trop_Score'], sub['Sid_Score'])

            f.write(f"| {prof.capitalize()} | {t:.2f} | {s:.2f} | {p:.4f} |\n")

        f.write("\n## 3. Top Dignified Celebrities (Tropical)\n")
        f.write("| Name | Profession | Score |\n|---|---|---|\n")
        for i, r in df.sort_values('Trop_Score', ascending=False).head(5).iterrows():
            f.write(f"| {r['name']} | {r['profession']} | {r['Trop_Score']} |\n")

        f.write("\n## 4. Top Dignified Celebrities (Sidereal/Vedic)\n")
        f.write("| Name | Profession | Score |\n|---|---|---|\n")
        for i, r in df.sort_values('Sid_Score', ascending=False).head(5).iterrows():
            f.write(f"| {r['name']} | {r['profession']} | {r['Sid_Score']} |\n")

        f.write("\n## 5. Most Interesting Shifts (Largest Delta)\n")
        f.write("Celebrities whose astrological 'strength' changes drastically between systems.\n\n")
        f.write("| Name | Tropical Score | Sidereal Score | Change |\n|---|---|---|---|\n")
        # Largest absolute change
        df['Abs_Delta'] = df['Delta'].abs()
        for i, r in df.sort_values('Abs_Delta', ascending=False).head(10).iterrows():
             f.write(f"| {r['name']} | {r['Trop_Score']} | {r['Sid_Score']} | {r['Delta']} |\n")

    print("Results generated.")

if __name__ == "__main__":
    run_analysis()
