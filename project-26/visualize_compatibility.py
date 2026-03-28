import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, 'compatibility_data_processed.csv')

def load_data():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Processed data file not found at {INPUT_FILE}")
        return None
    return pd.read_csv(INPUT_FILE)

def plot_correlation_heatmap(df):
    """
    Plots the correlation of each planetary aspect with the 'Success' binary outcome.
    """
    print("Generating Correlation Heatmap...")

    # Select only numeric aspect columns + Success
    # Filter columns that look like 'Planet_Planet'
    aspect_cols = [c for c in df.columns if '_' in c and c not in ['Couple', 'Status']]

    # Calculate correlation with Success
    correlations = df[aspect_cols].apply(lambda x: x.corr(df['Success']))

    # Reshape into matrix
    # We assume keys are in the format "Planet1_Planet2"
    planets = sorted(list(set([c.split('_')[0] for c in aspect_cols])))
    corr_matrix = pd.DataFrame(index=planets, columns=planets, dtype=float)

    for col in aspect_cols:
        p1, p2 = col.split('_')
        corr_matrix.loc[p1, p2] = correlations[col]

    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f', vmin=-0.3, vmax=0.3)
    plt.title("Correlation of Synastry Aspects with Relationship Success\n(Positive = Conjunctions favor Success, Negative = Oppositions favor Success)")
    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, 'correlation_heatmap.png'))
    plt.close()

def plot_aspect_distributions(df):
    """
    Plots KDE distributions for key aspects to see the difference between Success/Fail.
    """
    print("Generating KDE Plots...")

    key_aspects = ['Sun_Moon', 'Venus_Mars', 'Moon_Saturn', 'Sun_Sun']

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for i, aspect in enumerate(key_aspects):
        if aspect not in df.columns:
            continue

        ax = axes[i]
        sns.kdeplot(data=df, x=aspect, hue='Status', fill=True, ax=ax, common_norm=False, palette='husl')
        ax.set_title(f"Distribution of {aspect} Similarity")
        ax.set_xlabel("Cosine Similarity (-1=Opp, 1=Conj)")
        ax.axvline(0, color='k', linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, 'aspect_distributions_kde.png'))
    plt.close()

def plot_aggregate_score_vs_duration(df):
    """
    Creates a simple 'Compatibility Score' (Sum of all cosines) and plots vs Duration.
    """
    print("Generating Duration Scatter Plot...")

    aspect_cols = [c for c in df.columns if '_' in c and c not in ['Couple', 'Status']]

    # Calculate a naive "Harmonic Score" (Sum of cosines)
    # Note: This assumes Conjunctions (1.0) are good and Oppositions (-1.0) are bad.
    df['total_harmony'] = df[aspect_cols].sum(axis=1)

    plt.figure(figsize=(10, 6))

    # Color by Success status
    sns.scatterplot(data=df, x='total_harmony', y='Duration', hue='Status', style='Status', s=100, palette='viridis')

    # Add trendline
    sns.regplot(data=df, x='total_harmony', y='Duration', scatter=False, color='black', line_kws={'alpha':0.5})

    plt.title("Total Harmonic Score (Sum of Cosines) vs Relationship Duration")
    plt.xlabel("Total Harmony (Sum of all Planetary Cosine Similarities)")
    plt.ylabel("Duration (Years)")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, 'harmony_vs_duration.png'))
    plt.close()

def main():
    df = load_data()
    if df is not None:
        plot_correlation_heatmap(df)
        plot_aspect_distributions(df)
        plot_aggregate_score_vs_duration(df)
        print("Visualizations created in project folder.")

if __name__ == "__main__":
    main()
