import pandas as pd
import numpy as np
import swisseph as swe
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy.stats import pearsonr

# Setup
swe.set_ephe_path(None)
DATA_FILE = Path("38-composite-charts-group-dynamics/bands_data.csv")
OUTPUT_DIR = Path("38-composite-charts-group-dynamics")

PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY, 'Venus': swe.VENUS, 
    'Mars': swe.MARS, 'Jupiter': swe.JUPITER, 'Saturn': swe.SATURN, 
    'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE, 'Pluto': swe.PLUTO, 
    'Node': swe.MEAN_NODE, 'Lilith': swe.MEAN_APOG
}

def get_positions(date_str):
    try:
        dt = datetime.strptime(str(date_str), "%Y-%m-%d")
        jd = swe.julday(dt.year, dt.month, dt.day, 12.0)
        
        pos = {}
        for name, pid in PLANETS.items():
            res = swe.calc_ut(jd, pid, swe.FLG_SWIEPH)
            pos[name] = np.deg2rad(res[0][0]) # Radians for cosine calc
        return pos
    except:
        return None

def calculate_group_metrics(members_df):
    # Determine positions for all members
    member_positions = []
    
    # Deduplicate members (Wiki data might have duplicates)
    members = members_df[['member_name', 'birth_date']].drop_duplicates()
    
    if len(members) < 2: return None
    
    for _, m in members.iterrows():
        pos = get_positions(m['birth_date'])
        if pos: 
            member_positions.append(pos)
    
    if len(member_positions) < 2: return None
    
    n = len(member_positions)
    metrics = {}
    
    # Calculate Mean Angular Cosine Differences for each Planet (Cohesion)
    # 1.0 = All Conjunct
    # -1.0 = All Opposite
    # 0.0 = Random or Squared
    
    for p in PLANETS.keys():
        cos_sum = 0
        pair_count = 0
        
        # All pairs
        for i in range(n):
            for j in range(i+1, n):
                angle_diff = member_positions[i][p] - member_positions[j][p]
                cos_sum += np.cos(angle_diff)
                pair_count += 1
        
        avg_cos = cos_sum / pair_count if pair_count > 0 else 0
        metrics[f"Cohesion_{p}"] = avg_cos
        
    # Aggregate "Inner Planet Cohesion" (Sun, Moon, Merc, Venus, Mars)
    inner_keys = [f"Cohesion_{p}" for p in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars']]
    metrics['Inner_Cohesion'] = np.mean([metrics[k] for k in inner_keys])
    
    # Aggregate "Outer Planet Cohesion" (Generational check)
    outer_keys = [f"Cohesion_{p}" for p in ['Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']]
    metrics['Outer_Cohesion'] = np.mean([metrics[k] for k in outer_keys])
    
    return metrics

def main():
    print("Loading Band Data...")
    if not DATA_FILE.exists():
        print("Data file not found.")
        return

    df = pd.read_csv(DATA_FILE)
    
    results = []
    
    # Group by Band
    unique_bands = df['band_name'].unique()
    print(f"Processing {len(unique_bands)} bands...")
    
    for band in unique_bands:
        band_subset = df[df['band_name'] == band]
        
        # Calculate Lifespan
        start = band_subset['start_year'].iloc[0]
        end = band_subset['end_year'].iloc[0]
        lifespan = end - start
        
        # Calculate Metrics
        metrics = calculate_group_metrics(band_subset)
        
        if metrics:
            row = {'band': band, 'lifespan': lifespan, 'members': len(band_subset['member_name'].unique())}
            row.update(metrics)
            results.append(row)
            
    results_df = pd.DataFrame(results)
    print(f"Calculated metrics for {len(results_df)} valid bands.")
    
    if len(results_df) > 2:
        # Correlations
        print("\n--- Correlation with Band Lifespan ---")
        corrs = {}
        for col in results_df.columns:
            if 'Cohesion' in col:
                r, p = pearsonr(results_df[col], results_df['lifespan'])
                corrs[col] = (r, p)
                print(f"{col}: r={r:.3f}, p={p:.3f}")
        
        # Visualization
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Inner_Cohesion', y='lifespan', data=results_df, size='members', sizes=(50, 200))
        plt.title("Band Inner Planet Cohesion vs Lifespan")
        plt.xlabel("Inner Planet Cohesion (1=Conjunct, -1=Opposed)")
        plt.ylabel("Years Active")
        plt.grid(True)
        plt.savefig(OUTPUT_DIR / "band_cohesion.png")
        
        # Save results
        results_df.to_csv(OUTPUT_DIR / "band_analysis_results.csv", index=False)
    else:
        print("Not enough data for correlation.")

if __name__ == "__main__":
    main()

