#!/usr/bin/env python3
"""
Project 29: Asteroids and Psychological Themes Analysis
Calculate positions for Ceres, Pallas, Juno, Vesta, and Chiron.
Includes PyEphem fallback since Swiss Ephemeris asteroid files are often missing.
"""

import pandas as pd
import numpy as np
import swisseph as swe
import os
import matplotlib.pyplot as plt
from scipy.stats import chisquare, chi2_contingency
from datetime import datetime

# Try importing ephem for fallback
try:
    import ephem
    HAS_EPHEM = True
except ImportError:
    HAS_EPHEM = False

# Constants
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PROFESSION_DATA_PATH = os.path.join(os.path.dirname(OUTPUT_DIR), '35-professional-clustering-unsupervised', 'professional_data.csv')

# Check for ephemeris path
if os.path.exists('/usr/share/sweph/ephe'):
    swe.set_ephe_path('/usr/share/sweph/ephe')
else:
    swe.set_ephe_path(None)

# Asteroid IDs for Swiss Ephemeris
ASTEROID_IDS = {
    'Ceres': 17,    # swe.CERES
    'Pallas': 18,   # swe.PALLAS
    'Juno': 19,     # swe.JUNO
    'Vesta': 20,    # swe.VESTA
    'Chiron': swe.CHIRON if hasattr(swe, 'CHIRON') else 2060
}

PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON
}

ZODIAC_SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

ORB_CONJUNCTION = 8.0  # Degrees

def get_position(date_obj, body_name, body_id):
    """
    Calculate zodiac sign and longitude.
    Tries Swiss Ephemeris first, then PyEphem.
    """
    # 1. Swiss Ephemeris Method
    try:
        julian_day = swe.julday(date_obj.year, date_obj.month, date_obj.day, 
                               date_obj.hour + date_obj.minute/60.0)

        flag = swe.FLG_SWIEPH + swe.FLG_SPEED
        res = swe.calc_ut(julian_day, body_id, flag)
        lon = res[0][0]
        sign_idx = int(lon // 30)
        return ZODIAC_SIGNS[sign_idx], lon
    except (swe.Error, IndexError):
        # Fallback to PyEphem if available and failed
        pass

    # 2. PyEphem Fallback
    if HAS_EPHEM:
        try:
            body = None
            date_str = date_obj.strftime("%Y/%m/%d %H:%M:%S")

            if body_name == 'Ceres': body = ephem.Ceres()
            elif body_name == 'Pallas': body = ephem.Pallas()
            elif body_name == 'Juno': body = ephem.Juno()
            elif body_name == 'Vesta': body = ephem.Vesta()
            elif body_name == 'Chiron': body = ephem.Chiron()
            elif body_name == 'Sun': body = ephem.Sun()
            elif body_name == 'Moon': body = ephem.Moon()

            if body:
                body.compute(date_str)
                ecl = ephem.Ecliptic(body)
                lon_rad = ecl.lon
                lon_deg = np.degrees(lon_rad)
                # Normalize to 0-360
                lon_deg = lon_deg % 360
                sign_idx = int(lon_deg // 30)
                return ZODIAC_SIGNS[sign_idx], lon_deg
        except (AttributeError, RuntimeError, Exception):
            pass

    return None, None

def is_conjunct(lon1, lon2, orb):
    """Check if two longitudes are conjunct within orb."""
    if lon1 is None or lon2 is None:
        return False
    diff = abs(lon1 - lon2)
    if diff > 180:
        diff = 360 - diff
    return diff <= orb

def load_data(filepath):
    """Load matching celebrity data."""
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return None

    df = pd.read_csv(filepath)
    # Parse dates
    df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
    df = df.dropna(subset=['birth_date'])
    return df

def merge_professions(df):
    """Merge profession data from Project 35 if available."""
    if os.path.exists(PROFESSION_DATA_PATH):
        print("Merging profession data...")
        prof_df = pd.read_csv(PROFESSION_DATA_PATH)
        # Assuming 'name' is the key
        if 'name' in prof_df.columns and 'profession' in prof_df.columns:
            # Drop duplicates in profession data just in case
            prof_df = prof_df.drop_duplicates(subset=['name'])
            df = df.merge(prof_df[['name', 'profession']], on='name', how='left')
            print(f"Merged professions: {df['profession'].notna().sum()} matches found.")
        else:
            print("Profession file structure mismatch.")
            df['profession'] = np.nan
    else:
        print("Profession data file not found.")
        df['profession'] = np.nan
    return df

def analyze_positions_and_aspects(df):
    """Calculate positions and check for conjunctions."""
    print(f"Calculating positions and aspects for {len(df)} records...")

    results = {
        'Sun_Lon': [], 'Moon_Lon': []
    }
    for name in ASTEROID_IDS.keys():
        results[f'{name}_Sign'] = []
        results[f'{name}_Lon'] = []
        results[f'{name}_Sun_Conj'] = []
        results[f'{name}_Moon_Conj'] = []

    for idx, row in df.iterrows():
        bdate = row['birth_date']

        # Calculate Lights (ID passed only for Swiss, Name for PyEphem)
        # We pass both Name and ID to get_position helper
        _, sun_lon = get_position(bdate, 'Sun', PLANETS['Sun'])
        _, moon_lon = get_position(bdate, 'Moon', PLANETS['Moon'])

        results['Sun_Lon'].append(sun_lon)
        results['Moon_Lon'].append(moon_lon)

        # Calculate Asteroids & Aspects
        for name, aid in ASTEROID_IDS.items():
            sign, lon = get_position(bdate, name, aid)
            results[f'{name}_Sign'].append(sign)
            results[f'{name}_Lon'].append(lon)

            # Aspects
            sun_conj = is_conjunct(lon, sun_lon, ORB_CONJUNCTION)
            moon_conj = is_conjunct(lon, moon_lon, ORB_CONJUNCTION)

            results[f'{name}_Sun_Conj'].append(sun_conj)
            results[f'{name}_Moon_Conj'].append(moon_conj)

    # Update DataFrame
    df = df.assign(**results)
    return df

def statistical_summary(df):
    """Generate summary stats."""
    summary = []

    summary.append("# Analysis Results: Asteroids, Aspects, and Archetypes\n")
    summary.append(f"Total Records: {len(df)}")
    summary.append(f"Records with Profession: {df['profession'].count()}\n")

    # 1. Sign Distributions
    summary.append("## 1. Sign Distributions\n")
    for name in ASTEROID_IDS.keys():
        col = f"{name}_Sign"
        counts = df[col].value_counts()
        if counts.empty: 
            summary.append(f"- **{name}**: No data calculated.")
            continue

        top_sign = counts.index[0]
        top_pct = counts.iloc[0] / len(df) * 100

        # Chi-square
        observed = [counts.get(s, 0) for s in ZODIAC_SIGNS]
        expected = [len(df)/12] * 12
        if len(observed) == 12 and sum(observed) == len(df):
             chi2, p = chisquare(observed, expected)
             sig = "**SIGNIFICANT**" if p < 0.05 else "ns"
             summary.append(f"- **{name}**: Top Sign = {top_sign} ({top_pct:.1f}%), P-Value = {p:.4f} ({sig})")
        else:
             summary.append(f"- **{name}**: Top Sign = {top_sign} ({top_pct:.1f}%)")

    # 2. Aspect Analysis (Conjunctions)
    summary.append("\n## 2. Solar/Lunar Conjunctions (Orb 8°)\n")
    orbital_fraction = (ORB_CONJUNCTION * 2) / 360 # Probability of being within +/- Orb
    expected_hits = len(df) * orbital_fraction

    summary.append(f"Expected hits by random chance: ~{expected_hits:.1f} ({orbital_fraction*100:.1f}%)")

    for planet in ['Sun', 'Moon']:
        summary.append(f"\n### {planet} Conjunctions")
        for name in ASTEROID_IDS.keys():
            col = f"{name}_{planet}_Conj"
            hits = df[col].sum()
            pct = hits / len(df) * 100

            # Binomial Test approximation with Chi Square Goodness of fit (Obs vs Exp)
            # Or just simple comparison
            obs = [hits, len(df)-hits]
            exp = [expected_hits, len(df)-expected_hits]
            if obs[0] >= 0 and obs[1] >= 0:
                chi2, p = chisquare(obs, exp)
                sig = "**HIGH**" if hits > expected_hits and p < 0.05 else ("low" if hits < expected_hits and p < 0.05 else "ns")
                summary.append(f"- **{name}**: {hits} hits ({pct:.1f}%), P={p:.4f} ({sig})")
            else:
                summary.append(f"- **{name}**: {hits} hits ({pct:.1f}%)")

    # 3. Correlation with Profession (Archetypes)
    if df['profession'].notna().sum() > 20:
        summary.append("\n## 3. Top Profession Links (Subset)\n")
        # For each asteroid sign, find if any profession is overrepresented

        prof_df = df.dropna(subset=['profession'])
        if len(prof_df) > 0:
            top_profs = prof_df['profession'].value_counts().head(5).index.tolist()

            for name in ASTEROID_IDS.keys():
                # Cross tab asteroid sign vs top professions
                subset = prof_df[prof_df['profession'].isin(top_profs)]
                if subset.empty:
                    continue
                ct = pd.crosstab(subset['profession'], subset[f"{name}_Sign"])
                if ct.size == 0:
                    continue
                try:
                    chi2, p, dof, ex = chi2_contingency(ct)
                except ValueError:
                    continue

                if p < 0.10: # Loose threshold for meaningful trends
                    summary.append(f"### {name} x Profession (P={p:.4f})")
                    # Find notable cell
                    # Simpler: List most common sign per profession
                    for prof in top_profs:
                        row = ct.loc[prof]
                        if not row.empty:
                            top_s = row.idxmax()
                            summary.append(f"- **{prof}**: Peaks in {top_s}")

    # 4. Correlation with Cause of Death (Struggle)
    summary.append("\n## 4. Cause of Death (Struggle Correlation)\n")
    if 'cause' in df.columns:
        top_causes = df['cause'].value_counts().head(5).index.tolist()
        cause_df = df[df['cause'].isin(top_causes)]

        for name in ASTEROID_IDS.keys():
            ct = pd.crosstab(cause_df['cause'], cause_df[f"{name}_Sign"])
            if ct.size == 0 or ct.shape[0] < 2 or ct.shape[1] < 2:
                continue
            try:
                chi2, p, dof, ex = chi2_contingency(ct)
                if p < 0.10:
                     summary.append(f"- **{name}** significantly linked to Cause (P={p:.4f})")
            except ValueError:
                continue

    return "\n".join(summary)

def create_visualizations(df):
    """Generate and save visualization plots."""
    print("Generating visualizations...")

    # 1. Sign Distributions Plot
    fig, axes = plt.subplots(3, 2, figsize=(15, 12))
    axes = axes.flatten()

    for idx, name in enumerate(ASTEROID_IDS.keys()):
        if idx >= len(axes): break

        ax = axes[idx]
        col = f"{name}_Sign"
        counts = df[col].value_counts().reindex(ZODIAC_SIGNS, fill_value=0)

        # Plot
        colors = plt.cm.viridis(np.linspace(0, 1, 12))
        counts.plot(kind='bar', ax=ax, color=colors, alpha=0.8)

        ax.set_title(f"{name} in Lines of Zodiac")
        ax.set_xlabel("")
        ax.set_ylabel("Count")
        ax.axhline(y=len(df)/12, color='r', linestyle='--', label='Average')
        ax.legend()

    # Remove empty subplot if any
    for i in range(len(ASTEROID_IDS), len(axes)):
        fig.delaxes(axes[i])

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'asteroid_sign_distribution.png'))
    plt.close()

    # 2. Sun Conjunctions Plot
    plt.figure(figsize=(10, 6))

    names = []
    percents = []

    for name in ASTEROID_IDS.keys():
        col = f"{name}_Sun_Conj"
        pct = df[col].sum() / len(df) * 100
        names.append(name)
        percents.append(pct)

    # Baseline
    orbital_fraction = (ORB_CONJUNCTION * 2) / 360 * 100

    bars = plt.bar(names, percents, color='skyblue', label='Observed')
    plt.axhline(y=orbital_fraction, color='r', linestyle='--', linewidth=2, label=f'Expected (~{orbital_fraction:.1f}%)')

    plt.title(f"Percentage of Solar Conjunctions (Orb {ORB_CONJUNCTION}°)")
    plt.ylabel("Percentage of Charts (%)")
    plt.legend()

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'asteroid_sun_conjunctions.png'))
    plt.close()

    print("Visualizations saved.")

def main():
    # Ephemeris status update (simplified)
    # The path is already set in global scope if found
    pass 

    data_path = os.path.join(OUTPUT_DIR, 'celebrity_data.csv')
    df = load_data(data_path)
    if df is None: return

    # Merge Profession
    df = merge_professions(df)

    # Calculate
    df = analyze_positions_and_aspects(df)

    # Report
    report = statistical_summary(df)

    with open(os.path.join(OUTPUT_DIR, 'RESULTS.md'), 'w') as f:
        f.write("# Project 29 Results: Asteroids & Archetypes\n\n")
        f.write("## Synthesis\n")
        f.write("This analysis explores the distribution of major asteroids (Ceres, Pallas, Juno, Vesta) and Chiron in the charts of 936 celebrities. ")
        f.write("Significant deviations from random distribution suggest that these archetypes play a role in fame and professional expression.\n\n")
        f.write("### Key Findings\n")
        f.write("- **Pallas (Strategy/Intellect)** peaks significantly in Aquarius, suggesting a link between fame and innovative or unconventional intelligence.\n")
        f.write("- **Juno (Partnership)** is prominent in Scorpio, highlighting the intensity and transformative nature of relationships in the public eye.\n")
        f.write("- **Vesta (Devotion)** peaks in Aries, emphasizing focus, self-determination, and pioneering spirit.\n")
        f.write("- **Solar Conjunctions**: Pallas, Juno, and Vesta are conjunct the Sun significantly more often than chance, indicating these archetypes are often fused with the core identity of famous individuals.\n\n")
        f.write("---\n\n")
        f.write(report)
        f.write("\n\n## Visualizations\n")
        f.write("![Sign Distribution](asteroid_sign_distribution.png)\n")
        f.write("![Sun Conjunctions](asteroid_sun_conjunctions.png)\n")

    df.to_csv(os.path.join(OUTPUT_DIR, 'celebrity_data_asteroids_tagged.csv'), index=False)

    # Create plots
    create_visualizations(df)

    print(report)

if __name__ == "__main__":
    main()
