
import pandas as pd
import numpy as np
from scipy.stats import chisquare, chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Config
current_dir = Path(__file__).parent
DATA_PATH = current_dir / "lunar_nodes_dataset.csv"
OUTPUT_DIR = current_dir / "results"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"{DATA_PATH} not found.")
    return pd.read_csv(DATA_PATH)

def analyze_distribution(df, category_col, value_col):
    """
    Compares the distribution of 'value_col' within 'category_col' subgroups
    against the background distribution of the entire dataset.
    """
    
    # 1. Background Probability (Expected Frequencies)
    # Count occurrences in the total population
    total_counts = df[value_col].value_counts(normalize=True).sort_index()
    all_possible_values = total_counts.index.tolist()
    
    results = []
    
    # Groups
    groups = df[category_col].unique()
    
    for group in groups:
        sub_df = df[df[category_col] == group]
        n_obs = len(sub_df)
        
        if n_obs < 10: # Skip small sample sizes
            continue
            
        # Observed Counts
        obs_counts = sub_df[value_col].value_counts().reindex(all_possible_values, fill_value=0).sort_index()
        
        # Expected Counts (based on background distribution)
        exp_counts = total_counts * n_obs
        
        # Chi-Square Test
        # We need to be careful with small expected counts, technically should bin them, 
        # but for this exploratory phase we will run it and note the warning.
        chi2, p_val = chisquare(f_obs=obs_counts, f_exp=exp_counts)
        
        # Calculate residuals (Enrichment)
        # > 1.0 means observed more than expected
        enrichment = obs_counts / exp_counts
        
        # Find strongest deviation
        max_enrichment = enrichment.max()
        max_elem = enrichment.idxmax()
        min_enrichment = enrichment.min()
        min_elem = enrichment.idxmin()
        
        results.append({
            'group': group,
            'n_samples': n_obs,
            'p_value': p_val,
            'stat': chi2,
            'max_enrichment': max_enrichment,
            'enriched_value': max_elem,
            'min_enrichment': min_enrichment,
            'depleted_value': min_elem,
            'enrichment_series': enrichment
        })
        
    return pd.DataFrame(results).sort_values('p_value')

def plot_enrichment_heatmap(results, title, filename):
    """
    Creates a heatmap of Observed/Expected ratios.
    """
    # Extract enrichment series into a DataFrame
    heatmap_data = pd.DataFrame()
    for _, row in results.iterrows():
        heatmap_data[row['group']] = row['enrichment_series']
        
    heatmap_data = heatmap_data.T # Professions as rows
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, center=1.0, cmap="RdBu_r", fmt=".2f", linewidths=.5)
    plt.title(f"Enrichment (Observed / Expected): {title}")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename)
    plt.close()

def plot_distributions(df, metric, title_prefix):
    """
    Plots the distribution of a metric for each profession vs background.
    """
    groups = df['profession'].unique()
    
    # Setup subplot grid
    n_groups = len(groups)
    cols = 2
    rows = (n_groups // cols) + (1 if n_groups % cols > 0 else 0)
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, 4 * rows))
    axes = axes.flatten()
    
    # Background params
    bg_counts = df[metric].value_counts(normalize=True).sort_index()
    
    for i, group in enumerate(groups):
        ax = axes[i]
        sub_df = df[df['profession'] == group]
        
        # Counts
        counts = sub_df[metric].value_counts(normalize=True).sort_index()
        
        # Align indices
        all_idx = bg_counts.index.union(counts.index).sort_values()
        bg_aligned = bg_counts.reindex(all_idx, fill_value=0)
        counts_aligned = counts.reindex(all_idx, fill_value=0)
        
        # Plot
        x = np.arange(len(all_idx))
        width = 0.35
        
        ax.bar(x - width/2, bg_aligned, width, label='All Professionals (Baseline)',  alpha=0.6, color='gray')
        ax.bar(x + width/2, counts_aligned, width, label=f'{group} (N={len(sub_df)})', alpha=0.8, color='tab:blue')
        
        ax.set_title(f"{group}: {title_prefix}")
        ax.set_xticks(x)
        ax.set_xticklabels(all_idx, rotation=45)
        ax.legend()
        
    # Hide empty subplots
    for j in range(i+1, len(axes)):
        axes[j].axis('off')
        
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f"dist_{metric}.png")
    plt.close()

def main():
    print("Loading data...")
    df = load_data()
    print(f"Loaded {len(df)} records.")
    
    metrics = [
        ('north_node_sign', 'North Node Sign'),
        ('nn_house_from_sun_equal', 'NN House from Sun (Equal)'),
        ('nn_house_from_moon_equal', 'NN House from Moon (Equal)'),
        ('nn_house_from_sun_whole', 'NN House from Sun (Whole)'),
        ('nn_house_from_moon_whole', 'NN House from Moon (Whole)')
    ]
    
    summary_text = "# Analysis Results: Lunar Nodes & Life Purpose\n\n"
    summary_text += f"Total Records: {len(df)}\n"
    summary_text += "Methodology: Chi-Square Goodness of Fit test comparing specific professions against the baseline distribution of the entire dataset. This controls for cohort bias (e.g. if 'Aquarius' is common in the dataset because many people were born in 1999, we expect Musicians to have that same Aquarius spike unless there is a specific astrological effect).\n\n"

    for col, name in metrics:
        print(f"Analyzing {name}...")
        results = analyze_distribution(df, 'profession', col)
        
        # Determine significance threshold (simple p < 0.05)
        sig_results = results[results['p_value'] < 0.05]
        
        summary_text += f"## {name}\n"
        if len(sig_results) > 0:
            summary_text += "### Significant Deviation found in:\n"
            for _, row in sig_results.iterrows():
                summary_text += f"- **{row['group']}** (p={row['p_value']:.4f}, N={row['n_samples']})\n"
                summary_text += f"  - Enriched: {row['enriched_value']} ({row['max_enrichment']:.2f}x expected)\n"
                summary_text += f"  - Depleted: {row['depleted_value']} ({row['min_enrichment']:.2f}x expected)\n"
        else:
            summary_text += "No statistically significant deviations (p < 0.05).\n"
            
        summary_text += "\n#### Top Trends (Non-Significant):\n"
        # Sort by p-value to find "least random" groups
        top_trends = results.sort_values('p_value').head(3)
        for _, row in top_trends.iterrows():
            summary_text += f"- **{row['group']}** (p={row['p_value']:.2f}): "
            summary_text += f"High in {row['enriched_value']} ({row['max_enrichment']:.2f}x), "
            summary_text += f"Low in {row['depleted_value']} ({row['min_enrichment']:.2f}x)\n"

        summary_text += "\n"
        
        # Plots
        plot_enrichment_heatmap(results, name, f"heatmap_{col}.png")
        plot_distributions(df, col, name)
        
    with open(OUTPUT_DIR / "ANALYSIS_SUMMARY.md", "w") as f:
        f.write(summary_text)
        
    print(f"Analysis complete. Results saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()

