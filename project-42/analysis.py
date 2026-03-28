#!/usr/bin/env python3
"""Project 42: Solar Cycles and Social Sentiment"""
import numpy as np
import pandas as pd
from scipy import stats
from datetime import datetime
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
DATA_PATH = OUTPUT_DIR / "solar_sentiment_data.csv"

def main():
    print("=" * 60)
    print("PROJECT 42: SOLAR CYCLES AND SOCIAL SENTIMENT (1960-2023)")
    print("=" * 60)
    
    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found.")
        return

    # Load Data
    df = pd.read_csv(DATA_PATH)
    # Handle optional missing values for earlier years if any
    df = df.dropna()
    df['Date(YYYY-MM)'] = pd.to_datetime(df['Date(YYYY-MM)'])
    df = df.sort_values('Date(YYYY-MM)').reset_index(drop=True)
    
    # Calculate rolling averages to see trends better over 60 years
    df['Sunspots_Smooth'] = df['Sunspots'].rolling(window=12, center=True).mean()
    df['Sentiment_Smooth'] = df['Sentiment'].rolling(window=12, center=True).mean()

    print(f"\nData points: {len(df)}")
    print(f"Period: {df['Date(YYYY-MM)'].iloc[0].strftime('%Y-%m')} to {df['Date(YYYY-MM)'].iloc[-1].strftime('%Y-%m')}")
    print(f"Sunspot range: {df['Sunspots'].min():.1f} - {df['Sunspots'].max():.1f}")
    print(f"Sentiment range: {df['Sentiment'].min():.1f} - {df['Sentiment'].max():.1f}")
    
    # Analysis
    corr, p_val = stats.pearsonr(df['Sunspots'], df['Sentiment'])
    print(f"\n--- Correlation Analysis ---")
    print(f"Sunspots vs Consumer Sentiment: r={corr:.3f}, p={p_val:.4g}")
    
    # Spearman rank correlation
    spearman_r, spearman_p = stats.spearmanr(df['Sunspots'], df['Sentiment'])
    print(f"Spearman correlation: ρ={spearman_r:.3f}, p={spearman_p:.4g}")
    
    # Lag analysis (-3 to +3 months)
    print("\n--- Cross-Correlation (Lag Analysis) ---")
    print("Positive lag = Solar Activity predictive of future Sentiment")
    lags = range(-6, 7)
    best_r = 0
    best_lag = 0
    
    for lag in lags:
        if lag == 0:
            r = corr
            p = p_val
        elif lag > 0:
            # Sunspots (earlier) vs Sentiment (later)
            r, p = stats.pearsonr(
                df['Sunspots'].iloc[:-lag],
                df['Sentiment'].iloc[lag:]
            )
        else:
            # Sunspots (later) vs Sentiment (earlier)
            r, p = stats.pearsonr(
                df['Sunspots'].iloc[-lag:],
                df['Sentiment'].iloc[:lag]
            )
        
        print(f"Lag {lag:2d} months: r={r:.3f} (p={p:.4f})")
        if abs(r) > abs(best_r):
            best_r = r
            best_lag = lag

    print(f"\nBest Lag: {best_lag} months (r={best_r:.3f})")
    
    # High vs low solar activity
    median_sunspots = df['Sunspots'].median()
    high_solar = df[df['Sunspots'] > median_sunspots]['Sentiment']
    low_solar = df[df['Sunspots'] <= median_sunspots]['Sentiment']
    
    t_stat, t_p = stats.ttest_ind(high_solar, low_solar)
    print(f"\n--- Group Comparison ---")
    print(f"High Solar (> {median_sunspots:.1f}) Mean Sentiment: {high_solar.mean():.1f} ± {high_solar.std():.1f}")
    print(f"Low Solar (<= {median_sunspots:.1f}) Mean Sentiment: {low_solar.mean():.1f} ± {low_solar.std():.1f}")
    print(f"T-test: t={t_stat:.3f}, p={t_p:.4g}")
    
    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    
    # Scatter plot
    axes[0].scatter(df['Sunspots'], df['Sentiment'], s=15, c='orange', alpha=0.4, edgecolors='none')
    
    # Regression line
    z = np.polyfit(df['Sunspots'], df['Sentiment'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df['Sunspots'].min(), df['Sunspots'].max(), 100)
    
    axes[0].plot(x_line, p(x_line), 'r--', linewidth=2, alpha=0.8, 
                 label=f'Fit: y={z[0]:.3f}x + {z[1]:.1f}')
    
    axes[0].set_xlabel('Monthly Mean Sunspot Number')
    axes[0].set_ylabel('Consumer Sentiment Index')
    axes[0].set_title(f'Solar Activity vs Sentiment\nPearson r={corr:.2f}, p={p_val:.4g}')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    
    # Time series (Dual Axis)
    ax2 = axes[1]
    ax3 = ax2.twinx()
    
    # Dates for x-axis
    dates = df['Date(YYYY-MM)']
    
    # Plot raw data faintly
    ax2.plot(dates, df['Sunspots'], 'tab:orange', linewidth=0.5, alpha=0.3)
    ax3.plot(dates, df['Sentiment'], 'tab:blue', linewidth=0.5, alpha=0.3)
    
    # Plot smoothed trends strongly
    l1 = ax2.plot(dates, df['Sunspots_Smooth'], 'tab:orange', linewidth=2, label='Sunspots (12mo Avg)')
    l2 = ax3.plot(dates, df['Sentiment_Smooth'], 'tab:blue', linewidth=2, label='Sentiment (12mo Avg)')
    
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Sunspot Number', color='tab:orange', fontweight='bold')
    ax3.set_ylabel('Sentiment Index', color='tab:blue', fontweight='bold')
    
    ax2.tick_params(axis='y', labelcolor='tab:orange')
    ax3.tick_params(axis='y', labelcolor='tab:blue')
    
    # Added grid
    ax2.grid(True, alpha=0.3)
    
    # Title
    axes[1].set_title('Time Series: 60 Years of Solar Cycles & Sentiment')
    
    # Combined Legend
    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax2.legend(lines, labels, loc='upper left')
    
    plt.tight_layout()
    output_img = OUTPUT_DIR / "solar_sentiment_analysis_1960_2023.png"
    plt.savefig(output_img)
    print(f"\nVisualization saved to {output_img}")
    
    # Save results to CSV
    results_df = pd.DataFrame([{
        'Correlation_r': corr,
        'P_Value': p_val,
        'Best_Lag': best_lag,
        'Best_Lag_r': best_r,
        'High_Solar_Mean': high_solar.mean(),
        'Low_Solar_Mean': low_solar.mean()
    }])
    results_df.to_csv(OUTPUT_DIR / "analysis_results.csv", index=False)

if __name__ == "__main__":
    main()

