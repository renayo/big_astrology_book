import ast
import pandas as pd
import swisseph as swe
from pathlib import Path
from datetime import datetime
import sys

# Setup
PROJECT_35_PATH = Path(__file__).parent.parent / "35-professional-clustering-unsupervised/analysis.py"
OUTPUT_FILE = Path(__file__).parent / "lunar_nodes_dataset.csv"
swe.set_ephe_path(None)

def get_planetary_data(date_str, time_str):
    try:
        # Parse datetime
        dt_str = f"{date_str} {time_str}"
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        
        # UT conversion 
        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0)
        
        # Calculate Positions
        # True Node
        node_res = swe.calc_ut(jd, swe.TRUE_NODE)
        north_node_lon = node_res[0][0]
        
        # Sun
        sun_res = swe.calc_ut(jd, swe.SUN)
        sun_lon = sun_res[0][0]
        
        # Moon
        moon_res = swe.calc_ut(jd, swe.MOON)
        moon_lon = moon_res[0][0]
        
        # Sign (0=Aries, 1=Taurus...)
        nn_sign_num = int(north_node_lon / 30)
        
        return north_node_lon, sun_lon, moon_lon, nn_sign_num
    except Exception as e:
        return None, None, None, None

def main():
    if not PROJECT_35_PATH.exists():
        print(f"Error: Could not find {PROJECT_35_PATH}")
        return

    print("Reading data from Project 35 analysis script...")
    
    # Import the file dynamically to get the list safely
    import importlib.util
    spec = importlib.util.spec_from_file_location("project35_source", PROJECT_35_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["project35_source"] = module
    
    try:
        spec.loader.exec_module(module)
        professionals_data = module.PROFESSIONALS
    except Exception as importerror:
        print(f"Import failed: {importerror}")
        return

    print(f"Extracted {len(professionals_data)} professionals.")

    # Process Data
    processed_rows = []
    
    SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
             'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

    for entry in professionals_data:
        name, date, time, category = entry
        
        nn_lon, sun_lon, moon_lon, nn_sign_id = get_planetary_data(date, time)
        
        if nn_lon is not None:
            # --- 1. Equal House Calculation (Degree based) ---
            # House 1 = 0-30 deg difference, House 2 = 30-60 deg difference, etc.
            
            # Relative to Sun
            diff_sun = (nn_lon - sun_lon) % 360
            nn_house_from_sun_equal = int(diff_sun / 30) + 1
            
            # Relative to Moon
            diff_moon = (nn_lon - moon_lon) % 360
            nn_house_from_moon_equal = int(diff_moon / 30) + 1

            # Ketu (South Node) is exactly opposite North Node
            sn_lon = (nn_lon + 180) % 360
            
            # Ketu relative to Sun
            diff_sun_k = (sn_lon - sun_lon) % 360
            sn_house_from_sun_equal = int(diff_sun_k / 30) + 1
            
            # Ketu relative to Moon
            diff_moon_k = (sn_lon - moon_lon) % 360
            sn_house_from_moon_equal = int(diff_moon_k / 30) + 1
            
            # --- 2. Whole Sign Calculation (Sign based) ---
            sun_sign_id = int(sun_lon / 30)
            moon_sign_id = int(moon_lon / 30)
            sn_sign_id = int(sn_lon / 30)
            
            # North Node Whole Sign
            nn_house_from_sun_whole = ((nn_sign_id - sun_sign_id) % 12) + 1
            nn_house_from_moon_whole = ((nn_sign_id - moon_sign_id) % 12) + 1
            
            # South Node Whole Sign
            sn_house_from_sun_whole = ((sn_sign_id - sun_sign_id) % 12) + 1
            sn_house_from_moon_whole = ((sn_sign_id - moon_sign_id) % 12) + 1

            processed_rows.append({
                'name': name,
                'profession': category,
                'north_node_lon': nn_lon,
                'south_node_lon': sn_lon,
                'sun_lon': sun_lon,
                'moon_lon': moon_lon,
                'north_node_sign': SIGNS[nn_sign_id],
                'north_node_sign_id': nn_sign_id,
                # Equal House Columns
                'nn_house_from_sun_equal': nn_house_from_sun_equal,
                'nn_house_from_moon_equal': nn_house_from_moon_equal,
                'sn_house_from_sun_equal': sn_house_from_sun_equal,
                'sn_house_from_moon_equal': sn_house_from_moon_equal,
                # Whole Sign Columns
                'nn_house_from_sun_whole': nn_house_from_sun_whole,
                'nn_house_from_moon_whole': nn_house_from_moon_whole,
                'sn_house_from_sun_whole': sn_house_from_sun_whole,
                'sn_house_from_moon_whole': sn_house_from_moon_whole
            })

    df = pd.DataFrame(processed_rows)
    
    # Remove duplicates by name
    initial_count = len(df)
    df = df.drop_duplicates(subset=['name'])
    deduped_count = len(df)
    print(f"Calculated Planetary Positions for {initial_count} records. Removed {initial_count - deduped_count} duplicates.")
    
    # Save
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

