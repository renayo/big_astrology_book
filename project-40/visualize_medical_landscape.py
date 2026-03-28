import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup
OUTPUT_DIR = Path(__file__).parent
DATA_FILE = OUTPUT_DIR / 'cosine_correlations.csv'

ORDERED_PLANETS = [
    'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 
    'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto',
    'Rahu', 'Ketu'
]

def main():
    if not DATA_FILE.exists():
        print("Data file not found. Run analysis_cosine.py first.")
        return

    df = pd.read_csv(DATA_FILE)
    
    # --- 1. Prepare Heatmap Data ---
    matrix = pd.DataFrame(index=ORDERED_PLANETS, columns=ORDERED_PLANETS, dtype=float)
    
    for _, row in df.iterrows():
        p1, p2 = row['Pair'].split('-')
        corr = row['Correlation']
        
        # Fill symmetric matrix
        if p1 in ORDERED_PLANETS and p2 in ORDERED_PLANETS:
            matrix.loc[p1, p2] = corr
            matrix.loc[p2, p1] = corr
            
    # Fill diagonal with 1.0 (self-correlation)
    np.fill_diagonal(matrix.values, 1.0)

    # --- 2. Visualization ---
    fig = plt.figure(figsize=(18, 8))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 0.8])
    
    # Plot A: Heatmap
    ax1 = fig.add_subplot(gs[0])
    
    # Mask upper triangle for cleaner look
    mask = np.triu(np.ones_like(matrix, dtype=bool))
    np.fill_diagonal(mask, False) # Keep diagonal?? No, standard correlation matrix usually hides upper or lower
    
    # For this, let's show full matrix or lower triangle
    mask = np.triu(np.ones_like(matrix, dtype=bool), k=1)
    
    sns.heatmap(matrix, annot=True, fmt=".2f", cmap='coolwarm', vmin=-0.5, vmax=0.5, 
                center=0, square=True, mask=mask, cbar_kws={"shrink": .8}, ax=ax1)
    
    ax1.set_title("The 'Cosmic Weather' Matrix\nCorrelation between Plantary Alignments & Illness Severity", fontsize=14, pad=20)
    
    # Plot B: Discovery vs Tradition
    ax2 = fig.add_subplot(gs[1])
    
    # Select traditional pairs
    trad_pairs = ['Moon-Mars', 'Moon-Saturn', 'Sun-Saturn', 'Mars-Saturn']
    trad_df = df[df['Pair'].isin(trad_pairs)].copy()
    trad_df['Type'] = 'Traditional Medical'
    
    # Select Top 3 strongest pairs (by Abs Correlation) avoiding those already in Trad
    top_df = df[~df['Pair'].isin(trad_pairs)].sort_values('Abs_Corr', ascending=False).head(5).copy()
    top_df['Type'] = 'Data Discovery'
    
    plot_df = pd.concat([top_df, trad_df]).sort_values('Abs_Corr', ascending=False)
    
    # Color palette based on correlation direction
    colors = ['crimson' if x > 0 else 'royalblue' for x in plot_df['Correlation']]
    
    sns.barplot(x='Correlation', y='Pair', data=plot_df, hue='Type', dodge=False, ax=ax2, palette='viridis')
    
    ax2.set_title("Discovery vs. Tradition\n(Strongest Predictors vs. Classic Theory)", fontsize=14)
    ax2.set_xlabel("Correlation with Admission Severity (r)")
    ax2.axvline(0, color='black', linewidth=1)
    ax2.grid(True, axis='x', alpha=0.3)
    
    # Annotate Top Bars
    for i, (idx, row) in enumerate(plot_df.iterrows()):
        ax2.text(row['Correlation'], i, f" {row['Correlation']:.2f}", va='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    output_path = OUTPUT_DIR / 'medical_astrology_landscape.png'
    plt.savefig(output_path, dpi=150)
    print(f"Saved visualization to {output_path}")

if __name__ == "__main__":
    main()

