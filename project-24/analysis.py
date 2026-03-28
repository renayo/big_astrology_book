"""
Project 24: Large Scale IPO & Electional Astrology Analysis
===========================================================
Objective: Test astrological election rules on ~10,000+ publicly traded companies.
Data Source: Yahoo Finance (yfinance).
"""

import yfinance as yf
import pandas as pd
import numpy as np
import swisseph as swe
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
import concurrent.futures
import sys
import math
import itertools
import itertools
import requests_cache
session = requests_cache.CachedSession('yfinance.cache')

warnings.filterwarnings('ignore')

session.headers['User-agent'] = 'my-program/1.0'

from pathlib import Path

warnings.filterwarnings('ignore')

OUTPUT_DIR = Path(__file__).parent
OUTPUT_FILE = OUTPUT_DIR / 'large_scale_ipo_results.csv'

# Configure Swisseph
try:
    swe.set_ephe_path('/usr/share/sweph/ephe')
except:
    pass


def get_julian_day(dt):
    """Convert datetime to Julian Day."""
    return swe.julday(dt.year, dt.month, dt.day, 12.0) # Noon
# --- NEW ASTROLOGICAL LOGIC ---

PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY, 
    'Venus': swe.VENUS, 'Mars': swe.MARS, 'Jupiter': swe.JUPITER, 
    'Saturn': swe.SATURN, 'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE, 
    'Pluto': swe.PLUTO, 'NorthNode': swe.MEAN_NODE, 'Chiron': swe.CHIRON
}
# ...existing code...
def get_full_astro_profile(dt):
    """
    Calculates:
    1. Positions (0-360) for 12 bodies.
    2. Tithi (1-30).
    3. Cosine of angular distinct between all pairs (harmonic resonance).
    """
    jd = get_julian_day(dt)
    data = {}

    # Flag to use Moshier ephemeris if files are missing (slower but works without files)
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED

    # 1. Get Positions
    positions = {}
    for name, pid in PLANETS.items():
        try:
            # Try efficient Swiss Ephemeris first
            res = swe.calc_ut(jd, pid, flags)[0]
        except swe.Error:
            # Fallback to Moshier (analytic) if file missing
            res = swe.calc_ut(jd, pid, swe.FLG_MOSEPH | swe.FLG_SPEED)[0]

        positions[name] = res[0] # Longitude
        data[f'{name}_lon'] = res[0]

    # 2. Key Special Features
    # Tithi: (Moon - Sun) / 12 degrees. 1-30 scale.
    diff = (positions['Moon'] - positions['Sun']) % 360
    tithi = int(diff / 12) + 1
    data['Tithi'] = tithi

    # Moon Phase (Standard labels for grouping)
    if diff < 15 or diff > 345: phase_label = 'New Moon'
    elif 165 < diff < 195: phase_label = 'Full Moon'
    else: phase_label = 'Waxing' if diff < 180 else 'Waning'
    data['moon_phase_label'] = phase_label

    # 3. Cosine Interaction Matrix
    # Calculates cos(A - B). 
    keys = list(PLANETS.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            p1 = keys[i]
            p2 = keys[j]

            angle_1 = positions[p1]
            angle_2 = positions[p2]

            # Angle difference in radians
            delta_rad = math.radians(angle_1 - angle_2)
            cosine_interaction = math.cos(delta_rad)

            data[f'cos_{p1}_{p2}'] = cosine_interaction

    return data

def get_retrogrades(jd):
    """Check if Mercury or Venus are retrograde."""
    # Speed is index 3 in results
    # Use fallback flags here as well to be safe
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    fallback = swe.FLG_MOSEPH | swe.FLG_SPEED

    def get_speed(planet):
        try:
            return swe.calc_ut(jd, planet, flags)[0][3]
        except swe.Error:
            return swe.calc_ut(jd, planet, fallback)[0][3]

    merc_speed = get_speed(swe.MERCURY)
    venus_speed = get_speed(swe.VENUS)
    mars_speed = get_speed(swe.MARS)

    return {
        'mercury_rx': merc_speed < 0,
        'venus_rx': venus_speed < 0,
        'mars_rx': mars_speed < 0
    }

def fetch_ticker_data(ticker):
    """Fetches IPO date and 1-year performance."""
    try:
        t = yf.Ticker(ticker)
        # Fetching max history
        hist = t.history(period="max")

        if hist.empty:
            return None

        start_date = hist.index[0]
        start_price = hist['Close'].iloc[0]

        # Calculate 1-year performance
        target_date = start_date + timedelta(days=365)

        # If company is less than 1 year old, skip
        if hist.index[-1] < target_date:
            return None

        # Get price at 1 year (using nearest index)
        idx_1yr = np.abs(hist.index - target_date).argmin()
        end_price_1yr = hist['Close'].iloc[idx_1yr]

        pct_change = (end_price_1yr - start_price) / start_price

        return {
            'ticker': ticker,
            'ipo_date': start_date.to_pydatetime(),
            'start_price': start_price,
            'price_1yr': end_price_1yr,
            'pct_change_1yr': pct_change
        }
    except Exception:
        return None

def main():
    print("Generating Massive Ticker List (10,000+)...")
    tickers = []

    try:
        # Use a stable GitHub raw file for NASDAQ/NYSE tickers
        url = "https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/all/all_tickers.txt"

        # FIX: Robust downloading and parsing manually
        import requests
        resp = requests.get(url)
        if resp.status_code == 200:
            # Split by newlines and clean whitespace
            raw_tickers = resp.text.splitlines()
            tickers = [t.strip() for t in raw_tickers if t.strip()]
            print(f"Loaded {len(tickers)} tickers from GitHub source.")
            print(f"Sample tickers: {tickers[:5]}")
        else:
            raise Exception(f"GitHub download failed with status {resp.status_code}")

    except Exception as e:
        print(f"Could not load large list: {e}. Using S&P 500 fallback.")
        try:
             # Backup: Just manual list if Wiki fails
            tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'JNJ', 'K', 'L', 'M', 'N', 'O', 'P']
        except:
            pass

    # Clean tickers
    tickers = [str(t).replace('.', '-') for t in tickers if isinstance(t, str)]

    # LIMIT FOR API SAFETY (Optional: Remove slicing to do ALL 12,000)
    # yfinance might throttle after 2-3k. 
    # tickers = tickers[:5000] 

    print(f"Starting data fetch for {len(tickers)} companies...")

    results = []

    # Reduce concurrent workers if scaling up to prevent IP ban
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ticker = {executor.submit(fetch_ticker_data, t): t for t in tickers}

        count = 0
        total = len(tickers)
        for future in concurrent.futures.as_completed(future_to_ticker):
            res = future.result()
            if res:
                results.append(res)
            count += 1
            if count % 20 == 0:
                sys.stdout.write(f"\rProcessed {count}/{total} entities ({len(results)} successful)")
                sys.stdout.flush()

    df = pd.DataFrame(results)
    if len(df) == 0:
        print("\nNo data collected.")
        return

    print(f"\nSuccessfully collected data for {len(df)} companies.")
    print("Calculating Extended Astrological Features...")

    astro_rows = []

    for _, row in df.iterrows():
        ipo_date = row['ipo_date']
        # Use new comprehensive function
        astro_data = get_full_astro_profile(ipo_date)
        astro_rows.append(astro_data)

    astro_df = pd.DataFrame(astro_rows)
    final_df = pd.concat([df.reset_index(drop=True), astro_df], axis=1)

    # --- Analysis ---

    print("\n" + "="*50)
    print(f"RESULTS: {len(final_df)} COMPANIES PROCESSED")
    print("="*50)

    # 1. Moon Phase / Tithi Analysis
    print("\n--- Tithi (Lunar Day 1-30) Performance ---")
    # Group by Tithi to see if specific lunar days are luckier
    tithi_group = final_df.groupby('Tithi')['pct_change_1yr'].mean()
    print(tithi_group.sort_values(ascending=False).head(5))

    # --- Visualization ---
    plt.figure(figsize=(15, 10))

    # Subplot 1: Tithis
    plt.subplot(2, 2, 1)
    plt.bar(tithi_group.index, tithi_group.values, color='purple', alpha=0.7)
    plt.title("Avg 1-Year Return by Tithi (1-30)")
    plt.xlabel("Tithi")
    plt.axhline(0, color='black')

    # Subplot 2: Moon Phase Label
    plt.subplot(2, 2, 2)
    phase_gb = final_df.groupby('moon_phase_label')['pct_change_1yr'].mean()
    plt.bar(phase_gb.index, phase_gb.values, color='orange')
    plt.title("Avg Return by Phase Category")
    plt.axhline(0, color='black')

    # Subplot 3: Sun-Jupiter Cosine Interaction (Optimism Aspect)
    # +1 = Conjunction, -1 = Opposition
    plt.subplot(2, 2, 3)
    plt.scatter(final_df['cos_Sun_Jupiter'], final_df['pct_change_1yr'], s=2, alpha=0.3)
    plt.title("Sun-Jupiter Cosine vs Return")
    plt.xlabel("Cosine (1=Conj, -1=Opp)")
    plt.ylabel("Return")
    plt.ylim(-1, 5) # Clip

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'large_scale_astro_analysis.png')

    final_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved massive dataset to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
