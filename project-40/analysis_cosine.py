#!/usr/bin/env python3
"""Project 40: Medical Astrology Decumbiture Analysis (NYC Data)"""
import pandas as pd
import numpy as np
import swisseph as swe
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup
OUTPUT_DIR = Path(__file__).parent
DATA_FILE = Path(__file__).parent.parent / "temp_nyc_data.csv"
swe.set_ephe_path(None)

PLANETS = {
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
    'Rahu': swe.TRUE_NODE
}

def get_planetary_cosines(date_str):
    """
    Calculates cosine of angle differences for all planetary pairs.
    Returns: dict of pair_name -> cosine_value
    """
    try:
        dt = pd.to_datetime(date_str)
        # Noon EST roughly (17:00 UT)
        jd = swe.julday(dt.year, dt.month, dt.day, 17.0)
        
        # Get positions
        positions = {}
        for name, pid in PLANETS.items():
            positions[name] = swe.calc_ut(jd, pid)[0][0]
            
        # Add Ketu (South Node) explicitly
        positions['Ketu'] = (positions['Rahu'] + 180.0) % 360.0
            
        # Calculate pair cosines
        results = {}
        p_names = list(positions.keys()) # Includes Ketu now
        
        for i in range(len(p_names)):
            for j in range(i + 1, len(p_names)):
                p1 = p_names[i]
                p2 = p_names[j]
                
                deg1 = positions[p1]
                deg2 = positions[p2]
                
                # Minimum angle difference
                diff = abs(deg1 - deg2) % 360
                # We want the cyclical diff (0-360 mapped to cosine 0 at 0, -1 at 180)
                # Cosine(diff_radians). 
                # Conjunction (0) -> 1.0
                # Opposition (180) -> -1.0
                # Square (90) -> 0.0
                
                rads = np.radians(diff)
                results[f"{p1}-{p2}"] = np.cos(rads)
                
        return results
        
    except Exception as e:
        return None

def main():
    print("=" * 60)
    print("PROJECT 40: NYC EMERGENCY DATA ANALYSIS (Continuous Cosines)")
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
    df['severity_ratio'] = df['ili_pne_admissions'] / df['total_ed_visits']
    
    print(f"Loaded {len(df)} records.")
    
    # Aggregate by DATE
    daily_stats = df.groupby('date')['severity_ratio'].mean().reset_index()
    print(f"Aggregated to {len(daily_stats)} unique days.")
    
    print("Calculating Planetary Pair Cosines...")
    # Apply calculation
    astro_data = daily_stats['date'].apply(get_planetary_cosines)
    
    # Expand dict results into columns
    astro_df = pd.DataFrame(astro_data.tolist())
    
    # Combine
    full_df = pd.concat([daily_stats, astro_df], axis=1).dropna()
    print(f"Final N={len(full_df)} days.")

    # --- ANALYSIS ---
    correlation_results = []
    feature_cols = [c for c in full_df.columns if '-' in c] # Pair columns
    
    print(f"Testing {len(feature_cols)} planetary pairs...")
    
    for pair in feature_cols:
        r, p = stats.pearsonr(full_df[pair], full_df['severity_ratio'])
        correlation_results.append({
            'Pair': pair,
            'Correlation': r,
            'P_Value': p,
            'Abs_Corr': abs(r)
        })
        
    results_df = pd.DataFrame(correlation_results).sort_values('P_Value')
    
    # Top 10 Significant Results
    print("\n--- Top Correlations with Severity Ratio ---")
    print(results_df.head(10).to_string(index=False))
    
    # Save Results
    results_df.to_csv(OUTPUT_DIR / 'cosine_correlations.csv', index=False)
    
    # Visualization: Scatter of Top Result
    top_pair = results_df.iloc[0]
    pair_name = top_pair['Pair']
    
    plt.figure(figsize=(10, 6))
    sns.regplot(x=pair_name, y='severity_ratio', data=full_df, 
                scatter_kws={'alpha':0.3}, line_kws={'color':'red'})
    
    plt.title(f"Impact of {pair_name} Alignment on Illness Severity\n(r={top_pair['Correlation']:.3f}, p={top_pair['P_Value']:.4f})")
    plt.xlabel(f"{pair_name} Cosine Similarity\n(+1.0 = Conjunct, -1.0 = Opposite)")
    plt.ylabel("Admission Severity Ratio")
    plt.grid(True, alpha=0.3)
    
    plt.savefig(OUTPUT_DIR / 'decumbiture_cosine_analysis.png')
    print(f"\nPlot saved to {OUTPUT_DIR / 'decumbiture_cosine_analysis.png'}")
    
    # Analyze Specific Medical Pairs (Moon-Mars, Moon-Saturn) regardless of rank
    print("\n--- Traditional Medical Pairs ---")
    medical_pairs = ['Moon-Mars', 'Moon-Saturn', 'Sun-Saturn', 'Mars-Saturn']
    print(results_df[results_df['Pair'].isin(medical_pairs)].to_string(index=False))

if __name__ == "__main__":
    main()

