#!/usr/bin/env python3
"""
Project 44: ML Chart Rectification - Data Generator
===================================================
Generates SYNTHETIC data to train and validate the ML model.

Problem:
Real rectification data (exact birth time + exact event dates) is distinct 
from standard datasets. Most public data has birth time but only 'Year' for events,
or precise events but no birth time.

Solution:
To prove the ML *methodology*, we first generate a synthetic dataset where
events are DERIVED from the birth chart using standard astrological rules.
If the ML cannot rectify these charts (where the link is mathematical), 
it generally cannot rectify real charts (where the link is weaker).

Synthetic Rules (The "Ground Truth" for the AI to learn):
1. Marriage: Jupiter transiting the 7th House Cusp (Descendant)
2. Career Peak: Saturn transiting the Midheaven (MC)
3. Sudden Change: Uranus transiting the Ascendant
4. Children: Jupiter transiting the 5th House Cusp
"""

import numpy as np
import pandas as pd
import swisseph as swe
import random
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path(None)

EVENT_TYPES = ['marriage', 'career', 'shock', 'child']
START_YEAR = 1960
END_YEAR = 2000

def get_julian_day(dt):
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0)

def jd_to_date(jd):
    y, m, d, h = swe.revjul(jd)
    return datetime(y, m, d) + timedelta(hours=h)

def find_transit_events(birth_jd, asc, mc, houses):
    """
    Generate synthetic events based on transits to angles/houses.
    Returns list of (date_string, event_type)
    """
    events = []
    
    # Define rules: (Planet, Target_Angle/Cusp, Event_Type)
    # Houses: 1=Asc, 10=MC, 7=Dsc, 4=IC. 
    # swe.houses returns (cusps, ascmc). cusps is 1-based index (0 is dummy)
    
    # 7th House Cusp (Descendant) = (Asc + 180) in some systems, but use calculated cusp
    descendant = houses[7]
    fifth_cusp = houses[5]
    
    rules = [
        (swe.JUPITER, descendant, 'marriage'), # Jupiter to Dsc
        (swe.SATURN, mc, 'career'),            # Saturn to MC
        (swe.URANUS, asc, 'shock'),            # Uranus to Asc
        (swe.JUPITER, fifth_cusp, 'child')     # Jupiter to 5th
    ]
    
    # Scan next 60 years
    search_days = 21900 
    step_days = 10 # Check every 10 days for speed (transits are slow)
    
    # Optimization: Pre-calculate approximate positions to skip huge loops?
    # No, simple loop for 5000 people might be slow in Python.
    # 5000 people * 2000 steps = 10,000,000 calculations. Might take a few minutes. Acceptable.
    
    for day_offset in range(0, search_days, step_days):
        current_jd = birth_jd + day_offset
        
        for planet, target_deg, event_type in rules:
            # Calculate planet position
            pos = swe.calc_ut(current_jd, planet)[0][0]
            
            # Check for conjunction (Orb 2 degrees)
            # Handle 360 wrap
            diff = abs(pos - target_deg)
            if diff > 180: diff = 360 - diff
            
            if diff < 2.0:
                # Add some randomness to the exact date (simulate imperfection)
                # Random +/- 30 days
                noise = random.randint(-30, 30)
                event_jd = current_jd + noise
                
                # Probability of event happening (not every transit = event)
                if random.random() < 0.4: 
                    # Date string
                    evt_date = jd_to_date(event_jd)
                    events.append((evt_date.strftime('%Y-%m-%d'), event_type))
    
    # Clean duplicates (simple)
    unique_events = {}
    for date, etype in events:
        year = date[:4]
        key = f"{year}-{etype}"
        if key not in unique_events:
            unique_events[key] = (date, etype)
    
    return list(unique_events.values())

def get_positions_vector(jd):
    """Get positions of 12 celestial bodies."""
    bodies = [
        swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS, 
        swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO,
        swe.TRUE_NODE, swe.CHIRON
    ]
    positions = []
    for b in bodies:
        try:
            pos = swe.calc_ut(jd, b)[0][0]
            positions.append(pos)
        except:
            positions.append(0.0)
    return positions

def generate_synthetic_person(id):
    """Create a random person and derived events."""
    EVENT_TYPES = ['marriage', 'career', 'shock', 'child']
    
    # 1. Random Birth Date (1960-1990)
    year = random.randint(1960, 1990)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    
    birth_dt = datetime(year, month, day, hour, minute)
    birth_jd = get_julian_day(birth_dt)
    
    # 2. Calculate Chart (Assume Lat/Lon for NYC for simplicity)
    lat = 40.71
    lon = -74.00
    
    # Houses: 'P' = Placidus
    cusps, ascmc = swe.houses(birth_jd, lat, lon, b'P')
    asc = ascmc[0]
    mc = ascmc[1]
    
    # 3. Generate Events based on this chart
    events = find_transit_events(birth_jd, asc, mc, cusps)
    
    # 4. Add Random Noise Events (False Herrings)
    # ML needs to distinguish signal from noise
    num_noise = random.randint(1, 4)
    for _ in range(num_noise):
        noise_year = year + random.randint(15, 60)
        noise_month = random.randint(1, 12)
        noise_day = random.randint(1, 28)
        noise_type = random.choice(EVENT_TYPES)
        events.append((f"{noise_year}-{noise_month:02d}-{noise_day:02d}", noise_type))
    
    # Sort events
    events.sort()
    
    # Format for CSV
    # Need to serialize events list
    # Format: "YYYY-MM-DD:type|YYYY-MM-DD:type"
    event_str = "|".join([f"{d}:{t}" for d, t in events])
    
    return {
        'id': id,
        'birth_date': birth_dt.strftime('%Y-%m-%d'),
        'birth_time': birth_dt.strftime('%H:%M'),
        'latitude': lat,
        'longitude': lon,
        'asc_true': asc,
        'events': event_str
    }

def main():
    print("Generating comprehensive synthetic dataset (5000 records)...")
    
    # Prepare CSV header
    # Features: 12 bodies (Transit) x 12 bodies (Natal) = 144 cosine differences
    bodies_names = ['Sun', 'Moon', 'Merc', 'Ven', 'Mars', 'Jup', 'Sat', 'Ura', 'Nep', 'Plu', 'Node', 'Chi']
    feature_cols = []
    for t_name in bodies_names:
        for n_name in bodies_names:
            feature_cols.append(f"cos_{t_name}_n{n_name}")
            
    header = ['id', 'birth_hour_true', 'event_type', 'age_at_event'] + feature_cols
    
    output_path = OUTPUT_DIR / 'rectification_dataset_expanded.csv'
    
    # Open file for incremental writing
    import csv
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        count = 0
        total_people = 5000
        
        for i in range(1, total_people + 1):
            if i % 100 == 0:
                print(f"  Processed {i}/{total_people} individuals...")
                
            person = generate_synthetic_person(i)
            
            # If no events, skip
            if not person['events']:
                continue
                
            # Parse events back from string (since we reused the helper)
            # or refactor helper. Let's just parse.
            # Format: "YYYY-MM-DD:type|..."
            event_strs = person['events'].split('|')
            
            # Calculate Natal Positions (Noon Chart for "Unknown Time" simulation)
            bd_str = person['birth_date']
            birth_noon_dt = datetime.strptime(f"{bd_str} 12:00", "%Y-%m-%d %H:%M")
            birth_noon_jd = get_julian_day(birth_noon_dt)
            natal_pos = get_positions_vector(birth_noon_jd)
            
            # True Birth Time (Target) - Convert HH:MM to float
            bt_parts = person['birth_time'].split(':')
            birth_hour = float(bt_parts[0]) + float(bt_parts[1])/60.0
            
            # For each event, generate row
            for evt_str in event_strs:
                if ':' not in evt_str: continue
                d_str, t_type = evt_str.split(':')
                
                evt_dt = datetime.strptime(d_str, "%Y-%m-%d")
                evt_jd = get_julian_day(evt_dt)
                
                # Transit Positions
                trans_pos = get_positions_vector(evt_jd)
                
                # Calculate Features: Cosine differences
                row_features = []
                for t_val in trans_pos:
                    for n_val in natal_pos:
                        # Angle difference
                        diff = abs(t_val - n_val)
                        # Cosine (deg to rad)
                        row_features.append(np.cos(np.deg2rad(diff)))
                
                # Age
                age = (evt_jd - birth_noon_jd) / 365.25
                
                # Write Row
                # Encode event type? Or keep valid string
                # We'll calculate embeddings later or One-Hot. For CSV, keep string.
                row = [person['id'], birth_hour, t_type, age] + row_features
                writer.writerow(row)
                
                count += 1
                
    print(f"Done. Generated {count} event samples.")

if __name__ == "__main__":
    main()

