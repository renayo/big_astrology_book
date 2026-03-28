import pandas as pd
import swisseph as swe
import numpy as np
import re

DATA_FILE = 'pantheon_with_birth_order.csv'
OUTPUT_FILE = 'pantheon_analysis_results.csv'
AYANAMSA_LAHIRI = swe.SIDM_LAHIRI
swe.set_sid_mode(AYANAMSA_LAHIRI)

def parse_date(date_str):
    """
    Parses dates like '1946-06-14' or '0566-04-08 BC'.
    Returns (year, month, day) or None.
    """
    if pd.isna(date_str):
        return None

    date_str = str(date_str).strip()
    is_bc = 'BC' in date_str

    # Remove ' BC' or other artifacts
    clean_str = date_str.replace(' BC', '').strip()

    parts = clean_str.split('-')
    if len(parts) != 3:
        return None

    try:
        y, m, d = int(parts[0]), int(parts[1]), int(parts[2])

        if is_bc:
            # Convert to astronomical year
            # Historical 1 BC = Astronomical 0
            # Historical 566 BC = 1 - 566 = -565
            y = 1 - y

        return (y, m, d)
    except:
        return None


def get_positions(y, m, d):
    try:
        jd = swe.julday(y, m, d, 12.0) # Noon

        # Tropical Positions
        flags_trop = swe.FLG_SWIEPH # Default is Tropical
        sun_trop = swe.calc_ut(jd, swe.SUN, flags_trop)[0][0]

        # Sidereal Positions
        flags_sid = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
        sun_sid = swe.calc_ut(jd, swe.SUN, flags_sid)[0][0]
        jup_sid = swe.calc_ut(jd, swe.JUPITER, flags_sid)[0][0]
        sat_sid = swe.calc_ut(jd, swe.SATURN, flags_sid)[0][0]

        return sun_trop, sun_sid, jup_sid, sat_sid
    except:
        return None, None, None, None

def get_sign_name(lon):
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
             'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    return signs[int(lon / 30) % 12]

def get_sign_element(lon):
    # Signs: 0=Aries (Fire), 1=Taurus (Earth), 2=Gemini (Air), 3=Cancer (Water)...
    sign_idx = int(lon / 30) % 12
    elements = ['Fire', 'Earth', 'Air', 'Water'] # Aries, Taurus, Gemini, Cancer...
    return elements[sign_idx % 4]

def get_aspect(p1, p2, orb=8):
    # Calculate shortest distance
    diff = abs(p1 - p2) % 360
    dist = min(diff, 360 - diff)

    if dist < orb: return 'Conjunction'
    if abs(dist - 180) < orb: return 'Opposition'
    if abs(dist - 120) < orb: return 'Trine'
    if abs(dist - 90) < orb: return 'Square'
    if abs(dist - 60) < orb: return 'Sextile'
    return 'None'

def analyze():
    print(f"Loading {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE)

    results = []

    print("Calculating planetary data...")
    for idx, row in df.iterrows():
        bdate = row['birthdate']
        y, m, d = 0,0,0
        parsed = parse_date(bdate)

        if not parsed:
            continue

        y, m, d = parsed
        sun_trop, sun_sid, jup_sid, sat_sid = get_positions(y, m, d)

        if sun_trop is None:
            continue

        sign_trop = get_sign_name(sun_trop)
        sign_sid = get_sign_name(sun_sid)
        element_sid = get_sign_element(sun_sid)
        # element_trop = get_sign_element(sun_trop) # Not strictly requested but good for debugging

        sat_aspect = get_aspect(sun_sid, sat_sid)
        jup_aspect = get_aspect(sun_sid, jup_sid)

        # Categorize birth order
        bo = row['birth_order']
        total = row['total_siblings'] # Note: this comes from wikidata count, might be incomplete

        cat = 'Middle'
        if bo == 1:
            if total == 1: cat = 'Only'
            else: cat = 'First'
        elif bo == total and total > 1:
            cat = 'Youngest'

        results.append({
            'name': row['name'],
            'birth_order': bo,
            'category': cat,
            'sun_sign_trop': sign_trop,
            'sun_sign_sid': sign_sid,
            'sun_element_sid': element_sid,
            'sun_saturn': sat_aspect,
            'sun_jupiter': jup_aspect
        })

    res_df = pd.DataFrame(results)

    # Filter for main categories
    main_cats = res_df[res_df['category'].isin(['First', 'Middle', 'Youngest'])]

    print("\n--- Tropical Sun Sign Distribution (%) ---")
    ct_trop = pd.crosstab(main_cats['category'], main_cats['sun_sign_trop'], normalize='index') * 100
    print(ct_trop.round(1))

    print("\n--- Vedic (Sidereal) Sun Sign Distribution (%) ---")
    ct_sid = pd.crosstab(main_cats['category'], main_cats['sun_sign_sid'], normalize='index') * 100
    print(ct_sid.round(1))

    print("\n--- Vedic Sun Element Distribution by Birth Order Category ---")
    ct = pd.crosstab(res_df['category'], res_df['sun_element_sid'], normalize='index') * 100
    print(ct.round(1))

    print("\n--- Sun-Saturn Aspects by Category (Vedic) ---")
    # Soft: Trine, Sextile. Hard: Square, Opposition, Conjunction
    def classify_aspect(asp):
        if asp == 'None': return 'None'
        if asp in ['Trine', 'Sextile']: return 'Soft'
        return 'Hard'

    res_df['sat_type'] = res_df['sun_saturn'].apply(classify_aspect)
    # Re-filter to include new column
    main_cats = res_df[res_df['category'].isin(['First', 'Middle', 'Youngest'])]

    ct_sat = pd.crosstab(main_cats['category'], main_cats['sat_type'], normalize='index') * 100
    print(ct_sat.round(1))

    print("\n--- Sun-Jupiter Aspects by Category (Vedic) ---")
    res_df['jup_type'] = res_df['sun_jupiter'].apply(classify_aspect)
    # Re-filter to include new column
    main_cats = res_df[res_df['category'].isin(['First', 'Middle', 'Youngest'])]

    ct_jup = pd.crosstab(main_cats['category'], main_cats['jup_type'], normalize='index') * 100
    print(ct_jup.round(1))

    # Save
    res_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nDetailed results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    analyze()
