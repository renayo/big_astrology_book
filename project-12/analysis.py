#!/usr/bin/env python3
"""
Project 12: Market Volatility and Planetary Harmonics
=====================================================
Tests whether planetary aspects correlate with market volatility using REAL data.
Updated Jan 2026: Added Vector Cosine Harmonic Analysis (Tropical vs Vedic).

DATA SOURCES (REAL):
- Yahoo Finance: VIX (CBOE Volatility Index) historical data
- Yahoo Finance: S&P 500 historical data
- Swiss Ephemeris: Exact planetary positions

METHODOLOGY:
1. Phase 1: Discrete Aspect Clusters (Original Hard/Soft Aspect Counts).
2. Phase 2: Continuous Harmonic Features (Cosine of Angle Vectors).
   - 12 Bodies (Sun-Pluto + Nodes).
   - Tropical vs Sidereal (Vedic) comparison.
   - Correlation of specific planetary pairs with VIX.
"""

import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path(None)

# Try to import yfinance
try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False
    print("Warning: yfinance not installed. Using embedded historical data.")

# -----------------------------------------------------------------------------
# CONSTANTS & CONFIG
# -----------------------------------------------------------------------------

PLANETS_12 = [
    (swe.SUN, 'Sun'), (swe.MOON, 'Moon'), (swe.MERCURY, 'Mercury'),
    (swe.VENUS, 'Venus'), (swe.MARS, 'Mars'), (swe.JUPITER, 'Jupiter'),
    (swe.SATURN, 'Saturn'), (swe.URANUS, 'Uranus'), (swe.NEPTUNE, 'Neptune'),
    (swe.PLUTO, 'Pluto'), (swe.MEAN_NODE, 'North Node')
]

# Embedded VIX monthly averages (real CBOE data 2015-2023)
VIX_MONTHLY_EMBEDDED = {
    '2015-01': 19.2, '2015-02': 15.3, '2015-03': 15.4, '2015-04': 13.2,
    '2015-05': 13.1, '2015-06': 14.0, '2015-07': 12.1, '2015-08': 22.5,
    '2015-09': 23.3, '2015-10': 16.3, '2015-11': 16.1, '2015-12': 18.2,
    '2016-01': 22.5, '2016-02': 22.0, '2016-03': 15.7, '2016-04': 14.4,
    '2016-05': 14.9, '2016-06': 17.2, '2016-07': 12.0, '2016-08': 12.1,
    '2016-09': 13.3, '2016-10': 15.0, '2016-11': 14.5, '2016-12': 12.9,
    '2017-01': 11.5, '2017-02': 11.5, '2017-03': 11.7, '2017-04': 11.7,
    '2017-05': 10.7, '2017-06': 10.9, '2017-07': 10.0, '2017-08': 12.2,
    '2017-09': 10.1, '2017-10': 10.0, '2017-11': 10.6, '2017-12': 9.9,
    '2018-01': 11.0, '2018-02': 21.5, '2018-03': 19.4, '2018-04': 17.0,
    '2018-05': 13.4, '2018-06': 13.0, '2018-07': 12.4, '2018-08': 12.8,
    '2018-09': 12.1, '2018-10': 19.5, '2018-11': 19.0, '2018-12': 23.4,
    '2019-01': 18.5, '2019-02': 15.0, '2019-03': 14.6, '2019-04': 13.1,
    '2019-05': 16.3, '2019-06': 14.3, '2019-07': 13.1, '2019-08': 18.5,
    '2019-09': 15.2, '2019-10': 14.3, '2019-11': 12.6, '2019-12': 13.3,
    '2020-01': 14.5, '2020-02': 19.2, '2020-03': 57.7, '2020-04': 40.8,
    '2020-05': 30.2, '2020-06': 30.5, '2020-07': 27.1, '2020-08': 23.1,
    '2020-09': 27.6, '2020-10': 27.6, '2020-11': 23.3, '2020-12': 22.8,
    '2021-01': 24.8, '2021-02': 22.1, '2021-03': 20.0, '2021-04': 17.7,
    '2021-05': 19.7, '2021-06': 16.9, '2021-07': 18.2, '2021-08': 17.2,
    '2021-09': 21.0, '2021-10': 17.2, '2021-11': 19.5, '2021-12': 19.5,
    '2022-01': 24.5, '2022-02': 27.6, '2022-03': 26.6, '2022-04': 26.1,
    '2022-05': 28.0, '2022-06': 28.7, '2022-07': 24.3, '2022-08': 23.0,
    '2022-09': 27.3, '2022-10': 29.2, '2022-11': 23.1, '2022-12': 22.3,
    '2023-01': 19.4, '2023-02': 20.7, '2023-03': 20.8, '2023-04': 16.8,
    '2023-05': 17.0, '2023-06': 14.0, '2023-07': 13.8, '2023-08': 15.0,
    '2023-09': 15.5, '2023-10': 18.1, '2023-11': 14.2, '2023-12': 13.0,
}


def datetime_to_jd(dt):
    # Noon UTC
    return swe.julday(dt.year, dt.month, dt.day, 12.0)


def get_outer_planet_positions(jd):
    """Old Phase 1 function for outer planets."""
    planets = {
        swe.JUPITER: 'Jupiter',
        swe.SATURN: 'Saturn', 
        swe.URANUS: 'Uranus',
        swe.NEPTUNE: 'Neptune',
        swe.PLUTO: 'Pluto'
    }
    positions = {}
    for pid, name in planets.items():
        result = swe.calc_ut(jd, pid)[0]
        positions[name] = result[0]
    return positions


def get_all_positions(jd, sidereal=False):
    """New Phase 2 function for all 12 bodies."""
    if sidereal:
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
        flags = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL
    else:
        flags = swe.FLG_SWIEPH | swe.FLG_SPEED

    positions = {}
    for pid, name in PLANETS_12:
        pos, _ = swe.calc_ut(jd, pid, flags)[:2]
        positions[name] = pos[0]

    # Add South Node
    positions['South Node'] = (positions['North Node'] + 180) % 360
    return positions


def get_harmonic_interactions(positions):
    """Calculate Cosine of angle difference for all unique pairs."""
    interactions = {}
    names = list(positions.keys())

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            p1, p2 = names[i], names[j]
            diff = (positions[p1] - positions[p2]) % 360
            # Cosine: +1 (0 deg, conj), -1 (180 deg, opp), 0 (90 deg, square)
            interactions[f"{p1}_{p2}"] = np.cos(np.radians(diff))

    return interactions


def calculate_aspects(positions):
    """Phase 1: Counts hard/soft aspects."""
    aspects = {
        'conjunctions': 0, 'squares': 0, 'oppositions': 0,
        'trines': 0, 'sextiles': 0,
        'hard_aspects': 0, 'soft_aspects': 0
    }
    planets = list(positions.keys())
    for i, p1 in enumerate(planets):
        for p2 in planets[i+1:]:
            angle = abs(positions[p1] - positions[p2]) % 360
            if angle > 180: angle = 360 - angle

            if angle < 8:
                aspects['conjunctions'] += 1
                aspects['hard_aspects'] += 1
            elif abs(angle - 60) < 5:
                aspects['sextiles'] += 1
                aspects['soft_aspects'] += 1
            elif abs(angle - 90) < 6:
                aspects['squares'] += 1
                aspects['hard_aspects'] += 1
            elif abs(angle - 120) < 6:
                aspects['trines'] += 1
                aspects['soft_aspects'] += 1
            elif abs(angle - 180) < 8:
                aspects['oppositions'] += 1
                aspects['hard_aspects'] += 1
    return aspects


def fetch_market_data():
    """Fetch real VIX and market data."""
    if HAS_YFINANCE:
        print("Fetching VIX data from Yahoo Finance...")
        try:
            vix = yf.download('^VIX', start='2015-01-01', end='2024-01-01', progress=False)
            if len(vix) > 100:
                vix = vix.reset_index()
                # Handle multi-index columns from yfinance
                if isinstance(vix.columns[0], tuple):
                    vix.columns = [c[0] if isinstance(c, tuple) else c for c in vix.columns]
                return vix[['Date', 'Close']]
        except Exception as e:
            print(f"Yahoo Finance error: {e}")

    # Use embedded data
    print("Using embedded VIX data...")
    dates = []
    values = []
    for month_str, vix_val in VIX_MONTHLY_EMBEDDED.items():
        date = datetime.strptime(month_str + '-15', '%Y-%m-%d')
        dates.append(date)
        values.append(vix_val)
    return pd.DataFrame({'Date': dates, 'Close': values})


def analyze_aspect_volatility():
    """Phase 1: Discrete Aspect Analysis (Outer Planets)."""
    print("=" * 60)
    print("PHASE 1: DISCRETE ASPECT COUNTS")
    print("=" * 60)

    vix_data = fetch_market_data()
    print(f"VIX data points: {len(vix_data)}")

    records = []

    for _, row in vix_data.iterrows():
        date = pd.to_datetime(row['Date'])
        vix_val = float(row['Close'])

        jd = datetime_to_jd(date)
        positions = get_outer_planet_positions(jd)
        aspects = calculate_aspects(positions)

        records.append({
            'date': date,
            'vix': vix_val,
            **aspects
        })

    df = pd.DataFrame(records)
    return df


def analyze_continuous_harmonics(vix_df):
    """Phase 2: Continuous Harmonic Analysis (12 Planets, Trop/Sid)."""
    print("\n" + "=" * 60)
    print("PHASE 2: CONTINUOUS HARMONIC ANALYSIS")
    print("=" * 60)

    records = []

    for _, row in vix_df.iterrows():
        date = pd.to_datetime(row['date'])
        vix_val = row['vix']

        jd = datetime_to_jd(date)

        # Tropical
        trop_pos = get_all_positions(jd, sidereal=False)
        trop_har = get_harmonic_interactions(trop_pos)

        # Sidereal
        sid_pos = get_all_positions(jd, sidereal=True)
        sid_har = get_harmonic_interactions(sid_pos)

        rec = {'date': date, 'vix': vix_val}
        for k, v in trop_har.items(): rec[f'Trop_{k}'] = v
        for k, v in sid_har.items(): rec[f'Sid_{k}'] = v

        records.append(rec)

    df = pd.DataFrame(records)
    print(f"Calculated vectors for {len(df)} days.")

    results = {}

    # Analyze Correlations
    print("\nTop 5 Correlated Harmonics (Tropical):")
    cols = [c for c in df.columns if c.startswith('Trop_')]
    corrs = []
    for c in cols:
        r, p = stats.pearsonr(df[c], df['vix'])
        corrs.append((c, r, p))

    corrs.sort(key=lambda x: abs(x[1]), reverse=True)
    for c, r, p in corrs[:5]:
        print(f"  {c:<30}: r={r:.4f}, p={p:.4f}")
        results[c] = (r, p)

    print("\nTop 5 Correlated Harmonics (Sidereal/Vedic):")
    cols = [c for c in df.columns if c.startswith('Sid_')]
    corrs_sid = []
    for c in cols:
        r, p = stats.pearsonr(df[c], df['vix'])
        corrs_sid.append((c, r, p))

    corrs_sid.sort(key=lambda x: abs(x[1]), reverse=True)
    for c, r, p in corrs_sid[:5]:
        print(f"  {c:<30}: r={r:.4f}, p={p:.4f}")
        results[c] = (r, p)

    return results


def statistical_analysis(df):
    """Phase 1 Stats."""
    print("\n--- Phase 1 Stats ---")
    results = {}
    corr_hard, p_hard = stats.pearsonr(df['hard_aspects'], df['vix'])
    results['hard_aspects_vix_corr'] = corr_hard
    results['hard_aspects_vix_p'] = p_hard
    print(f"Hard Aspects Correlation: r = {corr_hard:.4f} (p={p_hard:.4f})")

    # Bootstrap
    observed_corr = abs(corr_hard)
    null_corrs = []
    for _ in range(200): # Reduced for speed
        shuffled_vix = df['vix'].sample(frac=1, replace=False).values
        null_corr, _ = stats.pearsonr(df['hard_aspects'], shuffled_vix)
        null_corrs.append(abs(null_corr))

    bootstrap_p = np.mean([c >= observed_corr for c in null_corrs])
    results['bootstrap_p'] = bootstrap_p
    return results


def main():
    print("=" * 70)
    print("PROJECT 12: MARKET VOLATILITY AND PLANETARY HARMONICS")
    print("Real VIX Data Analysis")
    print("=" * 70)

    # Phase 1
    df = analyze_aspect_volatility()
    stats1 = statistical_analysis(df)

    # Phase 2
    stats2 = analyze_continuous_harmonics(df[['date', 'vix']])

    # Save Results
    with open(OUTPUT_DIR / 'RESULTS.md', 'a') as f:
        f.write("\n\n## Phase 2: Continuous Harmonic Modeling (Update)\n")
        f.write("Following the methodology for high-dimensional analysis:\n")
        f.write("- **Approach**: Tested 12 planetary bodies (Sun-Pluto + Nodes) using Cosine Similarity ($cos(\\theta)$) as a continuous feature.\n")
        f.write("- **Comparison**: Tropical vs Vedic (Sidereal) Zodiacs.\n\n")

        f.write("### Top Correlations (Tropical)\n")
        f.write("| Harmonic Pair | Correlation (r) | P-value |\n|---|---|---|\n")
        count = 0
        sorted_trop = sorted([(k, v) for k, v in stats2.items() if 'Trop' in k], key=lambda x: abs(x[1][0]), reverse=True)
        for k, (r, p) in sorted_trop[:5]:
            f.write(f"| {k.replace('Trop_', '')} | {r:.4f} | {p:.4f} |\n")

        f.write("\n### Top Correlations (Sidereal/Vedic)\n")
        f.write("| Harmonic Pair | Correlation (r) | P-value |\n|---|---|---|\n")
        sorted_sid = sorted([(k, v) for k, v in stats2.items() if 'Sid' in k], key=lambda x: abs(x[1][0]), reverse=True)
        for k, (r, p) in sorted_sid[:5]:
            f.write(f"| {k.replace('Sid_', '')} | {r:.4f} | {p:.4f} |\n")

        f.write("\n### Observation\n")
        f.write("Comparing Tropical and Sidereal interaction frames shows that angular relationships (aspects) are largely independent of the coordinate system origin, producing identical cosine values for planet-to-planet pairs. Differences only emerge if referencing fixed stars or signs specifically.\n")

    print(f"\nResults appended to {OUTPUT_DIR / 'RESULTS.md'}")


if __name__ == '__main__':
    main()
