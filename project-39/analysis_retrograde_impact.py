import pandas as pd
import numpy as np
import swisseph as swe
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy.stats import ttest_ind, mannwhitneyu

# Setup
swe.set_ephe_path(None)
DATA_FILE = Path("39-retrograde-market-volatility/vix_data.csv")
OUTPUT_DIR = Path("39-retrograde-market-volatility")

PLANETS = {
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS
}

def get_retrograde_status(date_series):
    """
    Calculates Retrograde status for Mercury, Venus, Mars for a list of dates.
    Returns a DataFrame with boolean columns.
    """
    results = []
    print(f"Calculating planetary positions for {len(date_series)} days...")
    
    # Pre-cache commonly used constants
    flg = swe.FLG_SWIEPH | swe.FLG_SPEED
    
    for i, date_val in enumerate(date_series):
        try:
            dt = pd.to_datetime(date_val)
            jd = swe.julday(dt.year, dt.month, dt.day, 12.0) # Noon
            
            row = {}
            for name, pid in PLANETS.items():
                res = swe.calc_ut(jd, pid, flg)
                # res[0][3] is speed in longitude
                speed = res[0][3]
                row[f"{name}_Rx"] = 1 if speed < 0 else 0
            
            results.append(row)
        except Exception as e:
            # Handle potential bad dates
            results.append({k: 0 for k in list(PLANETS.keys()) + ["_Rx"]})

    return pd.DataFrame(results)

def analyze_vix(df):
    results_summary = []
    
    print("\n--- Market Volatility (VIX) Analysis ---")
    
    # Baseline
    baseline_vix = df['VIXCLS'].mean()
    print(f"Baseline Mean VIX (N={len(df)}): {baseline_vix:.2f}")
    
    # 1. Individual Planet Analysis
    for planet in PLANETS.keys():
        rx_col = f"{planet}_Rx"
        
        rx_data = df[df[rx_col] == 1]['VIXCLS']
        direct_data = df[df[rx_col] == 0]['VIXCLS']
        
        mean_rx = rx_data.mean()
        mean_dir = direct_data.mean()
        
        # T-Test (assuming independence, though time series has auto-correlation)
        t_stat, p_val = ttest_ind(rx_data, direct_data, equal_var=False)
        
        # Mann-Whitney U (Robust to non-normality)
        u_stat, p_u = mannwhitneyu(rx_data, direct_data)
        
        print(f"\n{planet} Retrograde:")
        print(f"  Rx Days: {len(rx_data)} ({len(rx_data)/len(df):.1%})")
        print(f"  Mean VIX (Rx):     {mean_rx:.2f}")
        print(f"  Mean VIX (Direct): {mean_dir:.2f}")
        print(f"  Difference:        {mean_rx - mean_dir:.2f}")
        print(f"  T-test p-value:    {p_val:.4f}")
        print(f"  Mann-Whitney p:    {p_u:.4f}")
        
        results_summary.append({
            'Planet': planet,
            'Rx_Mean': mean_rx,
            'Direct_Mean': mean_dir,
            'Diff': mean_rx - mean_dir,
            'P_Value': p_val
        })

    # Visualization
    plt.figure(figsize=(12, 6))
    
    # Prepare data for boxplot
    plot_data = []
    for planet in PLANETS.keys():
        rx_col = f"{planet}_Rx"
        temp = df.copy()
        temp['Status'] = np.where(temp[rx_col] == 1, 'Retrograde', 'Direct')
        temp['Planet'] = planet
        plot_data.append(temp[['VIXCLS', 'Status', 'Planet']])
    
    viz_df = pd.concat(plot_data)
    
    sns.boxplot(x='Planet', y='VIXCLS', hue='Status', data=viz_df, showfliers=False)
    plt.title("VIX Volatility during Planetary Retrogrades (1990-2025)")
    plt.ylabel("VIX Index (Outliers Removed)")
    plt.grid(True, axis='y', alpha=0.3)
    
    output_path = OUTPUT_DIR / "retrograde_impact_v2.png"
    plt.savefig(output_path)
    print(f"\nPlot saved to {output_path}")
    
    return pd.DataFrame(results_summary)

def main():
    print("Loading VIX Data...")
    if not DATA_FILE.exists():
        print("Data file not found.")
        return

    df = pd.read_csv(DATA_FILE, na_values='.')
    df = df.dropna(subset=['VIXCLS']) # Drop days where market was closed or data missing
    df['VIXCLS'] = pd.to_numeric(df['VIXCLS'])
    
    print(f"Loaded {len(df)} trading days.")
    
    # Calculate Retrogrades
    retro_df = get_retrograde_status(df['observation_date'])
    
    # Merge
    full_df = pd.concat([df.reset_index(drop=True), retro_df.reset_index(drop=True)], axis=1)
    
    # Analyze
    summary = analyze_vix(full_df)
    
    # Save Results
    summary.to_csv(OUTPUT_DIR / "retrograde_analysis_summary.csv", index=False)
    full_df.to_csv(OUTPUT_DIR / "vix_with_retrogrades.csv", index=False)

if __name__ == "__main__":
    main()

