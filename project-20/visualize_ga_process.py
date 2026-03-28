import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent

def create_fitness_landscape(csv_path, title, filename):
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
        return

    # Pivot data into a grid: Planets x Signs
    pivot_table = df.pivot(index='planet', columns='sign', values='fitness')

    # Reorder indices for logical flow
    planet_order = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Rahu', 'Ketu']
    sign_order = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis']

    # Filter to ensure only existing items are used
    planet_order = [p for p in planet_order if p in pivot_table.index]
    sign_order = [s for s in sign_order if s in pivot_table.columns]

    pivot_table = pivot_table.reindex(index=planet_order, columns=sign_order)

    plt.figure(figsize=(12, 8))

    # Create Heatmap
    sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="viridis", cbar_kws={'label': 'Fitness (Frequency)'})

    plt.title(f"GA Optimization Landscape: {title}\n(High Brightness = Optimal Rule Found)", fontsize=14)
    plt.xlabel("Gene 2: Zodiac Sign", fontsize=12)
    plt.ylabel("Gene 1: Planetary Body", fontsize=12)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=150)
    print(f"Saved {filename}")
    plt.close()

def main():
    print("Generating GA Visualization...")
    create_fitness_landscape(
        OUTPUT_DIR / 'analysis_results_tropical_extended.csv', 
        "Tropical Zodiac Search Space", 
        "ga_fitness_landscape_tropical.png"
    )
    create_fitness_landscape(
        OUTPUT_DIR / 'analysis_results_vedic_extended.csv', 
        "Vedic (Lahiri) Search Space", 
        "ga_fitness_landscape_vedic.png"
    )

if __name__ == "__main__":
    main()
