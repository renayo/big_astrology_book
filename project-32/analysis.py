#!/usr/bin/env python3
"""
Project 32: Historical Predictions Evaluation
Statistical analysis of famous astrological predictions vs outcomes.
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
DATA_FILE = OUTPUT_DIR / 'predictions_data.csv'

def main():
    print("Project 32: Historical Predictions Analysis")
    print("-" * 50)

    # Load Data
    if not DATA_FILE.exists():
        print("Error: predictions_data.csv not found.")
        return

    df = pd.read_csv(DATA_FILE)
    df['Result_Bool'] = df['Result'] == 'Success'

    total_n = len(df)
    success_n = df['Result_Bool'].sum()
    accuracy = success_n / total_n

    print(f"Total Predictions: {total_n}")
    print(f"Successful: {success_n}")
    print(f"Accuracy Rate: {accuracy:.2%}")

    # 1. Binomial Test vs Random Chance (50/50)
    # H0: p <= 0.5
    # H1: p > 0.5
    binom_res = stats.binomtest(success_n, total_n, p=0.5, alternative='greater')
    print(f"Binomial Test P-Value: {binom_res.pvalue:.4f}")
    if binom_res.pvalue < 0.05:
        print(">> Result is statistically significant (Better than chance).")
    else:
        print(">> Result is NOT statistically significant (Indistinguishable from chance).")

    # 2. Accuracy by Category
    print("\n--- Accuracy by Category ---")
    cat_acc = df.groupby('Category')['Result_Bool'].agg(['count', 'mean'])
    cat_acc = cat_acc.sort_values('mean', ascending=False)
    print(cat_acc)

    # 3. Accuracy by Time Delta (Buckets)
    print("\n--- Accuracy by Time Horizon ---")
    df['Horizon'] = pd.cut(df['Time_Delta_Years'], 
                           bins=[-1, 1, 10, 500], 
                           labels=['Short Term (<2y)', 'Medium (2-10y)', 'Long Term (>10y)'])

    time_acc = df.groupby('Horizon', observed=False)['Result_Bool'].agg(['count', 'mean'])
    print(time_acc)

    # --- Visualizations ---
    create_plots(df, cat_acc, time_acc)

    # --- Generate Report ---
    generate_report(df, accuracy, binom_res.pvalue, cat_acc, time_acc)

def create_plots(df, cat_acc, time_acc):
    sns.set_theme(style="whitegrid")

    # 1. Bar Chart: Accuracy by Category
    plt.figure(figsize=(10, 6))
    ax1 = sns.barplot(x=cat_acc.index, y=cat_acc['mean'], palette='viridis')
    plt.title('Prediction Accuracy by Category')
    plt.ylabel('Success Rate')
    plt.ylim(0, 1)
    plt.axhline(0.5, color='red', linestyle='--', label='Chance (50%)')
    plt.legend()
    # Add count labels
    for i, p in enumerate(ax1.patches):
        count = cat_acc['count'].iloc[i]
        ax1.annotate(f'n={count}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 9), 
                    textcoords = 'offset points')
    plt.savefig(OUTPUT_DIR / 'accuracy_by_category.png')
    plt.close()

    # 2. Scatter/Swarm: Horizon vs Result
    plt.figure(figsize=(10, 6))
    # Add jitter
    sns.stripplot(data=df, x='Result', y='Time_Delta_Years', hue='Category', 
                  size=10, jitter=0.2, alpha=0.8, palette='deep')
    plt.yscale('log') # Log scale because Nostradamus 200y outliers
    plt.title('Prediction Horizon vs Outcome (Log Scale)')
    plt.ylabel('Years in Advance (Log Scale)')
    plt.savefig(OUTPUT_DIR / 'horizon_vs_outcome.png')
    plt.close()

def generate_report(df, acc, p_val, cat_df, time_df):
    with open(OUTPUT_DIR / 'RESULTS.md', 'w') as f:
        f.write("# Project 32: Historical Predictions Evaluation\n\n")
        f.write("## Overview\n")
        f.write(f"This analysis evaluated **{len(df)}** famous astrological predictions from 1555 to 2022.\n\n")

        f.write("## Key Findings\n")
        f.write(f"- **Overall Accuracy**: {acc:.1%}\n")
        f.write(f"- **Statistical Significance**: p={p_val:.4f}\n")

        sig_text = "significantly better than random chance." if p_val < 0.05 else "not statistically distinguishable from a coin flip."
        f.write(f"The aggregate performance of these historical predictions is **{sig_text}**\n\n")

        f.write("## Performance by Category\n")
        f.write("| Category | N | Accuracy |\n")
        f.write("|----------|---|----------|\n")
        for cat, row in cat_df.iterrows():
            f.write(f"| {cat} | {row['count']} | {row['mean']:.1%} |\n")

        f.write("\n## Performance by Time Horizon\n")
        f.write("| Horizon | N | Accuracy |\n")
        f.write("|---------|---|----------|\n")
        for hor, row in time_df.iterrows():
            f.write(f"| {hor} | {row['count']} | {row['mean']:.1%} |\n")

        f.write("\n## The Dataset\n")
        f.write(df[['Source', 'Year_Made', 'Target_Year', 'Event_Description', 'Result']].to_markdown(index=False))

if __name__ == "__main__":
    main()
