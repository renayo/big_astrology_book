#!/usr/bin/env python3
"""Project 40: Medical Astrology Decumbiture Analysis (NYC Data)"""
import pandas as pd
import numpy as np
import swisseph as swe
from scipy import stats
import matplotlib.pyplot as plt
from pathlib import Path

# Setup
OUTPUT_DIR = Path(__file__).parent
DATA_FILE = Path(__file__).parent.parent / "temp_nyc_data.csv"
swe.set_ephe_path(None)

def get_moon_condition(date_str):
    """
    Calculates Moon's condition at Noon EST (17:00 UT) for the date.
    Returns: {malefic_aspect: bool, benefic_aspect: bool, moon_phase: float}
    """
    try:
        dt = pd.to_datetime(date_str)
        # Noon EST roughly
        jd = swe.julday(dt.year, dt.month, dt.day, 17.0)
        
        moon = swe.calc_ut(jd, swe.MOON)[0][0]
        mars = swe.calc_ut(jd, swe.MARS)[0][0]
        saturn = swe.calc_ut(jd, swe.SATURN)[0][0]
        jupiter = swe.calc_ut(jd, swe.JUPITER)[0][0]
        sun = swe.calc_ut(jd, swe.SUN)[0][0]
        
        # Helper for aspect calculation
        def check_aspect(p1, p2, aspect_list, orb=6):
            diff = abs(p1 - p2) % 360
            if diff > 180: diff = 360 - diff
            for asp in aspect_list:
                if abs(diff - asp) <= orb:
                    return True
            return False

        # Malefic: Conjunction (0), Square (90), Opposition (180) to Mars/Saturn
        is_malefic = (check_aspect(moon, mars, [0, 90, 180]) or 
                      check_aspect(moon, saturn, [0, 90, 180]))
                      
        # Benefic: Trine (120), Sextile (60) to Jupiter/Sun
        is_benefic = (check_aspect(moon, jupiter, [60, 120]) or 
                      check_aspect(moon, sun, [60, 120]))
        
        return is_malefic, is_benefic
        
    except:
        return np.nan, np.nan

def main():
    print("=" * 60)
    print("PROJECT 40: NYC EMERGENCY DATA ANALYSIS")
    print("=" * 60)

    if not DATA_FILE.exists():
        print(f"Error: Data file {DATA_FILE} not found.")
        return

    print("Loading NYC Data...")
    df = pd.read_csv(DATA_FILE)
    
    # Filter for valid dates and sufficient data
    df = df.dropna(subset=['date', 'total_ed_visits', 'ili_pne_admissions'])
    # Only keep records with at least 1 visit to avoid divide by zero
    df = df[df['total_ed_visits'] > 0]
    
    # Calculate Severity Ratio: Admissions / Visits
    # Logic: If many people are visiting but few admitted, severity is low.
    # If high % are admitted, the illness is severe.
    df['severity_ratio'] = df['ili_pne_admissions'] / df['total_ed_visits']
    
    print(f"Loaded {len(df)} records.")
    
    # Aggregate by DATE to speed up astrology (assigning same astro to all zips on that day)
    # We want to test if the DAY has higher severity generally.
    daily_stats = df.groupby('date')['severity_ratio'].mean().reset_index()
    print(f"Aggregated to {len(daily_stats)} unique days.")
    
    print("Calculating Planetary Aspects...")
    conditions = daily_stats['date'].apply(get_moon_condition)
    daily_stats['malefic_moon'] = [x[0] for x in conditions]
    daily_stats['benefic_moon'] = [x[1] for x in conditions]
    
    daily_stats = daily_stats.dropna()
    
    # Convert booleans
    daily_stats['malefic_moon'] = daily_stats['malefic_moon'].astype(bool)
    daily_stats['benefic_moon'] = daily_stats['benefic_moon'].astype(bool)

    # --- ANALYSIS ---
    
    # 1. Malefic Days Trend
    malefic_days = daily_stats[daily_stats['malefic_moon']]
    normal_days = daily_stats[~daily_stats['malefic_moon']]
    
    mean_malefic = malefic_days['severity_ratio'].mean()
    mean_normal = normal_days['severity_ratio'].mean()
    
    t_stat, p_val = stats.ttest_ind(malefic_days['severity_ratio'], normal_days['severity_ratio'], equal_var=False)
    
    print("\n--- Results: Moon-Malefic Aspects (Mars/Saturn) ---")
    print(f"Malefic Days (N={len(malefic_days)}): Mean Severity = {mean_malefic:.4f}")
    print(f"Normal Days  (N={len(normal_days)}): Mean Severity = {mean_normal:.4f}")
    print(f"Diff: {(mean_malefic - mean_normal)*100:.3f}% pts")
    print(f"T-Test p-value: {p_val:.4f}")
    
    # 2. Results to CSV
    results = pd.DataFrame([{
        'Hypothesis': 'Moon-Malefic -> High Severity',
        'Malefic_Mean': mean_malefic,
        'Normal_Mean': mean_normal,
        'P_Value': p_val,
        'Significant': p_val < 0.05
    }])
    results.to_csv(OUTPUT_DIR / 'analysis_results.csv', index=False)
    
    # 3. Visualization
    plt.figure(figsize=(10, 6))
    
    bp = plt.boxplot([malefic_days['severity_ratio'], normal_days['severity_ratio']], 
                     labels=['Moon Afflicted\n(Square/Opp Mars/Saturn)', 'Moon Unafflicted'],
                     patch_artist=True)
    
    colors = ['#ff9999', '#99ff99']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        
    plt.title(f'Illness Severity Ratio on Astrological Critical Days\n(N={len(daily_stats)} Days, NYC ED Data)', fontsize=14)
    plt.ylabel('Admission Severity Ratio (Admissions / Visits)')
    plt.grid(axis='y', alpha=0.3)
    
    # Add annotation
    sig_text = "SIGNIFICANT" if p_val < 0.05 else "NOT SIGNIFICANT"
    plt.figtext(0.5, 0.02, f"P-Value: {p_val:.4f} ({sig_text})", ha="center", fontsize=12, fontweight='bold')
    
    plt.savefig(OUTPUT_DIR / 'decumbiture_analysis_nyc.png')
    print(f"Plot saved to {OUTPUT_DIR / 'decumbiture_analysis_nyc.png'}")

if __name__ == "__main__":
    main()

