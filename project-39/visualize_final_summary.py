import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

OUTPUT_DIR = Path("39-retrograde-market-volatility")
SP500_FILE = OUTPUT_DIR / "retrograde_analysis_summary_long_term.csv"

def main():
    # Load Data
    sp500_df = pd.read_csv(SP500_FILE)

    # Plot Setup
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")

    # Colors
    palette = {"Mercury": "gray", "Venus": "crimson", "Mars": "royalblue"}

    # Plot: S&P 500 Realized Volatility
    ax = sns.barplot(
        x="Planet", 
        y="Diff", 
        data=sp500_df, 
        palette=palette,
        edgecolor="black",
        hue="Planet",
        legend=False
    )
    
    plt.title("Impact of Retrograde Cycles on Market Volatility\n(S&P 500, 1950 - Present)", fontsize=16, pad=20)
    plt.ylabel("Change in Annualized Volatility (%)", fontsize=12)
    plt.axhline(0, color="black", linewidth=1)

    # Annotate significance
    for i, row in sp500_df.iterrows():
        sig = "n.s."
        p_val = row['P_Value']
        if p_val < 0.05: sig = "*"
        if p_val < 0.01: sig = "**"
        if p_val < 0.001: sig = "***"
        
        # Position label above or below bar
        offset = 0.05 if row['Diff'] > 0 else -0.15
        y_pos = row['Diff'] + offset
        
        label_text = f"{row['Diff']:+.2f}%\n({sig})"
        plt.text(i, y_pos, label_text, ha='center', color='black', fontweight='bold', fontsize=12)

    # Caption
    plt.figtext(0.5, -0.02, 
                "Based on 19,106 trading days (1950-2026). Realized Volatility = 30-day Rolling Std Dev.\n"
                "Significance: *** p<0.001. Venus significantly increases risk; Mars significantly reduces it.",
                ha="center", fontsize=11, bbox={"facecolor": "orange", "alpha": 0.1, "pad": 5})

    plt.tight_layout()
    output_path = OUTPUT_DIR / "retrograde_effect_final.png"
    plt.savefig(output_path, bbox_inches='tight')
    print(f"Saved plot to {output_path}")

if __name__ == "__main__":
    main()

