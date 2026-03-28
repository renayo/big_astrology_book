#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "detailed_conjunctions.csv"
OUTPUT_DIR = BASE_DIR

def main():
    if not DATA_FILE.exists():
        print(f"Error: {DATA_FILE} not found. Run analysis.py first.")
        return

    print("Loading data...")
    df = pd.read_csv(DATA_FILE)

    # Set style
    sns.set_theme(style="whitegrid")

    # 1. Heatmap: Fixed Star vs Planet Intensity (Sum of Cosines)
    print("Generating Star vs Planet Heatmap...")
    plt.figure(figsize=(14, 10))
    pivot_planet = pd.crosstab(
        index=df['star'], 
        columns=df['planet'], 
        values=df['cosine'], 
        aggfunc='sum'
    ).fillna(0)

    sns.heatmap(pivot_planet, annot=True, fmt=".1f", cmap="YlOrRd", linewidths=.5)
    plt.title("Fixed Star Conjunction Intensity (Sum of Cosines) by Planet", fontsize=16)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "heatmap_star_planet.png", dpi=150)
    plt.close()

    # 2. Heatmap: Category vs Star Intensity
    print("Generating Category vs Star Heatmap...")
    # Filter for top stars and top categories to keep heatmap readable
    top_categories = df['category'].value_counts().nlargest(15).index
    top_stars = df['star'].value_counts().nlargest(12).index

    df_filtered = df[df['category'].isin(top_categories) & df['star'].isin(top_stars)]

    if not df_filtered.empty:
        plt.figure(figsize=(16, 10))
        pivot_category = pd.crosstab(
            index=df_filtered['category'], 
            columns=df_filtered['star'], 
            values=df_filtered['cosine'], 
            aggfunc='sum'
        ).fillna(0)

        sns.heatmap(pivot_category, annot=True, fmt=".1f", cmap="viridis", linewidths=.5)
        plt.title("Fixed Star Intensity by Category (Top 15 Categories)", fontsize=16)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "heatmap_category_star.png", dpi=150)
        plt.close()

    # 3. Bar Chart: Average 'Tightness' (Mean Cosine) per Star
    print("Generating Star Tightness Chart...")
    plt.figure(figsize=(12, 6))
    avg_cosine = df.groupby('star')['cosine'].mean().sort_values(ascending=False)

    # Convert cosine to approximate degrees for easier reading labels
    # acos(val) in radians -> degrees
    import numpy as np
    avg_degrees = np.degrees(np.arccos(avg_cosine))

    ax = avg_degrees.plot(kind='bar', color='teal', alpha=0.7)
    plt.title("Average Conjunction Orb (Degrees) by Star (Lower is Tighter)", fontsize=16)
    plt.ylabel("Average Orb (Degrees)")
    plt.xlabel("Fixed Star")

    # Add values on top
    for i, v in enumerate(avg_degrees):
        ax.text(i, v + 0.05, f"{v:.2f}°", ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "star_orb_tightness.png", dpi=150)
    plt.close()

    print(f"Visualizations saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
