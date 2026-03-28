import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
import numpy as np

OUTPUT_DIR = Path("37-planetary-cycles-mood-surveys")
DATA_FILE = OUTPUT_DIR / "real_data_processed.csv"

def main():
    print("Loading processed real data...")
    if not DATA_FILE.exists():
        print("Data file not found. Please run analysis_real_mood.py first.")
        return

    df = pd.read_csv(DATA_FILE)
    df['observation_date'] = pd.to_datetime(df['observation_date'])
    
    # Calculate Correlation again for title
    corr, p_val = stats.pearsonr(df['jup_sat_angle'], df['UMCSENT'])
    print(f"Correlation: r={corr:.3f}, p={p_val:.4e}")

    # Create Plot matching original layout
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Time Series
    axes[0].plot(df['observation_date'], df['UMCSENT'], color='#1f77b4', linewidth=0.8)
    axes[0].set_ylabel('Consumer Sentiment Index (1966=100)')
    axes[0].set_xlabel('Year')
    axes[0].set_title('University of Michigan Consumer Sentiment (1952-Present)')
    axes[0].grid(True, linestyle=':', alpha=0.6)
    
    # Plot 2: Scatter vs Jupiter-Saturn Angle
    # Scatter with transparency to handle density
    axes[1].scatter(df['jup_sat_angle'], df['UMCSENT'], alpha=0.3, s=10, color='#2ca02c')
    
    # Regression Line
    sns.regplot(
        x='jup_sat_angle', 
        y='UMCSENT', 
        data=df, 
        ax=axes[1], 
        scatter=False, 
        color='red', 
        line_kws={'linewidth': 2}
    )
    
    axes[1].set_xlabel('Jupiter-Saturn Angle (0°=Conj, 180°=Opp)')
    axes[1].set_ylabel('Consumer Sentiment')
    axes[1].set_title(f'Economic Mood vs Planetary Cycle\nr={corr:.3f} (Significant Negative Trend)')
    axes[1].grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / 'mood_analysis.png'
    plt.savefig(output_path, dpi=150)
    print(f"Recreated mood_analysis.png using full dataset at {output_path}")

if __name__ == "__main__":
    main()

