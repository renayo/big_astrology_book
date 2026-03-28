import os
import pandas as pd
from pathlib import Path

DATA_DIR = Path("/home/rko/Astrology Projects/Big Book of Astrology Research/22-astro-weather-meteorological/daily-summaries-latest")

def get_station_info(file_path):
    try:
        # Read just the first row to get lat/lon
        df = pd.read_csv(file_path, nrows=1)
        if 'LATITUDE' in df.columns:
            return df['LATITUDE'].iloc[0], file_path.stat().st_size
    except:
        pass
    return None, 0

def select_stations():
    north_files = []
    south_files = []

    # 1. Get Top North Files
    # (We know the largest ones are North, so this is easy)
    all_files = sorted(DATA_DIR.glob("*.csv"), key=lambda x: x.stat().st_size, reverse=True)

    print("Selecting North Stations...")
    for file_path in all_files:
        lat, size = get_station_info(file_path)
        if lat is not None and lat > 20:
            north_files.append((file_path, size, lat))
            if len(north_files) >= 5:
                break

    # 2. Get Top South Files
    # Look for specific prefixes first for efficiency: ZA (South Africa), AR (Argentina), AS (Australia)
    # The list showed ZA, ZI, UY.
    print("Selecting South Stations...")
    south_candidates = list(DATA_DIR.glob("ZA*.csv")) + list(DATA_DIR.glob("ZI*.csv")) + list(DATA_DIR.glob("UY*.csv")) + list(DATA_DIR.glob("AS*.csv")) + list(DATA_DIR.glob("WA*.csv"))

    # Sort candidates by size
    south_candidates.sort(key=lambda x: x.stat().st_size, reverse=True)

    for file_path in south_candidates:
        lat, size = get_station_info(file_path)
        if lat is not None and lat < -10: # South of Equator (tropics included if needed, user said South Hemisphere)
             # User said "southern hemisphere". Let's use < 0.
             if lat < 0:
                south_files.append((file_path, size, lat))
                if len(south_files) >= 5:
                    break

    print("Selected North Stations:")
    for f in north_files[:3]:
        print(f"{f[0].name} (Size: {f[1]/1024:.1f}KB, Lat: {f[2]})")

    print("\nSelected South Stations:")
    for f in south_files[:3]:
        print(f"{f[0].name} (Size: {f[1]/1024:.1f}KB, Lat: {f[2]})")

    # Save selection to a file for use
    with open(DATA_DIR.parent / "selected_stations.txt", "w") as f:
        for item in north_files[:3] + south_files[:3]:
            f.write(str(item[0]) + "\n")

if __name__ == "__main__":
    select_stations()
