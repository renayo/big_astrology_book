#!/usr/bin/env python3
"""
Project 23: Birth Chart Career Similarity Analysis (Sign-Based)
===============================================================
Hypothesis: People in the same profession have similar planetary sign placements.
Method: 
1. Load data from PRIOR_24 list AND celebrity_data.py
2. Deduplicate people by name.
3. Calculate Planetary Sign (0-11) for Tropical and Vedic zodiacs.
4. One-Hot Encode the signs.
5. Compute Cosine Similarity between career groups.
6. Compare Within-Group similarity vs Between-Group similarity.
"""

import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
from datetime import datetime

# Import data
try:
    from celebrity_data import CELEBRITY_DATA
except ImportError:
    print("Warning: Could not import celebrity_data.py. Using internal data only.")
    CELEBRITY_DATA = []

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path('/usr/share/swisseph')

# --- PRIOR 24 DATASET ---
# Format: name, year, month, day, category
# Using user's specific categories: 'Tech', 'Music', 'Science'
PRIOR_24 = [
    # Tech Founders
    {'name': 'Steve Jobs', 'date': '1955-02-24', 'category': 'Tech'},
    {'name': 'Bill Gates', 'date': '1955-10-28', 'category': 'Tech'},
    {'name': 'Elon Musk', 'date': '1971-06-28', 'category': 'Tech'},
    {'name': 'Jeff Bezos', 'date': '1964-01-12', 'category': 'Tech'},
    {'name': 'Mark Zuckerberg', 'date': '1984-05-14', 'category': 'Tech'},
    {'name': 'Larry Page', 'date': '1973-03-26', 'category': 'Tech'},
    {'name': 'Sergey Brin', 'date': '1973-08-21', 'category': 'Tech'},
    {'name': 'Larry Ellison', 'date': '1944-08-17', 'category': 'Tech'},

    # Musicians
    {'name': 'Madonna', 'date': '1958-08-16', 'category': 'Music'},
    {'name': 'Prince', 'date': '1958-06-07', 'category': 'Music'},
    {'name': 'Michael Jackson', 'date': '1958-08-29', 'category': 'Music'},
    {'name': 'David Bowie', 'date': '1947-01-08', 'category': 'Music'},
    {'name': 'Beyonce', 'date': '1981-09-04', 'category': 'Music'},
    {'name': 'Freddie Mercury', 'date': '1946-09-05', 'category': 'Music'},
    {'name': 'Kurt Cobain', 'date': '1967-02-20', 'category': 'Music'},
    {'name': 'Lady Gaga', 'date': '1986-03-28', 'category': 'Music'},

    # Scientists
    {'name': 'Albert Einstein', 'date': '1879-03-14', 'category': 'Science'},
    {'name': 'Marie Curie', 'date': '1867-11-07', 'category': 'Science'},
    {'name': 'Stephen Hawking', 'date': '1942-01-08', 'category': 'Science'},
    {'name': 'Carl Sagan', 'date': '1934-11-09', 'category': 'Science'},
    {'name': 'Neil deGrasse Tyson', 'date': '1958-10-05', 'category': 'Science'},
    {'name': 'Isaac Newton', 'date': '1643-01-04', 'category': 'Science'},
    {'name': 'Charles Darwin', 'date': '1809-02-12', 'category': 'Science'},
    {'name': 'Nikola Tesla', 'date': '1856-07-10', 'category': 'Science'},
]

# --- MERGE AND DEDUPLICATE ---
def get_merged_dataset():
    # Start with PRIOR_24 (Master list)
    merged = list(PRIOR_24) # Copy
    seen_names = set(p['name'] for p in merged)

    # Add from CELEBRITY_DATA if new
    added_count = 0
    for person in CELEBRITY_DATA:
        if person['name'] not in seen_names:
            merged.append(person)
            seen_names.add(person['name'])
            added_count += 1

    print(f"Merged Data: Started with {len(PRIOR_24)} prior. Added {added_count} from external file. Total: {len(merged)}")
    return merged

FINAL_DATASET = get_merged_dataset()

PLANETS = [
    swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
    swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO, swe.TRUE_NODE
]

def get_sign_features(year, month, day, mode='tropical'):
    """
    Returns a One-Hot Encoded vector of planetary signs.
    """
    # Noon
    jd = swe.julday(year, month, day, 12.0)

    if mode == 'vedic':
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    else:
        swe.set_sid_mode(0)
        flags = swe.FLG_SWIEPH

    features = []

    for p in PLANETS:
        try:
            res = swe.calc_ut(jd, p, flags=flags)
            lon = res[0][0]
            sign_idx = int(lon / 30) # 0 to 11

            # One-Hot Encoding for this planet
            planet_vector = [0] * 12
            planet_vector[sign_idx] = 1
            features.extend(planet_vector)

        except swe.Error:
            features.extend([0]*12)

    return np.array(features)

def run_analysis(mode='tropical'):
    print(f"\n--- Running Analysis: {mode.upper()} ---")

    all_vectors = []
    all_labels = []
    all_names = []

    # Process merged data
    for person in FINAL_DATASET:
        try:
            # Handle date parsing
            dt = datetime.strptime(person['date'], '%Y-%m-%d')
            vec = get_sign_features(dt.year, dt.month, dt.day, mode=mode)

            all_vectors.append(vec)
            all_labels.append(person['category'])
            all_names.append(person['name'])
        except ValueError as e:
            print(f"Skipping {person['name']}: {e}")
            continue

    X = np.array(all_vectors) 

    # Compute Cosine Similarity Matrix
    sim_matrix = cosine_similarity(X)

    # Analyze Within-Group vs Between-Group
    within_scores = []
    between_scores = []

    n = len(all_labels)
    for i in range(n):
        for j in range(i + 1, n):
            score = sim_matrix[i, j]
            # Exact category match
            # Note: 'Tech' vs 'Science' will be considered DIFFERENT groups here,
            # which is what we want if we want to test the specific Tech hypothesis.
            if all_labels[i] == all_labels[j]:
                within_scores.append(score)
            else:
                between_scores.append(score)

    mean_within = np.mean(within_scores)
    mean_between = np.mean(between_scores)

    print(f"Within-Group Similarity (Mean): {mean_within:.4f}")
    print(f"Between-Group Similarity (Mean): {mean_between:.4f}")

    t_stat, p_val = stats.ttest_ind(within_scores, between_scores)
    print(f"T-test: t={t_stat:.3f}, p={p_val:.4f}")

    sig = "SIGNIFICANT" if p_val < 0.05 else "NOT Significant"
    print(f"Result: {sig}")

    results = {
        'Mode': mode,
        'Within_Mean': mean_within,
        'Between_Mean': mean_between,
        'p_value': p_val,
        'Conclusion': sig
    }

    # Visualize Heatmap (Ordered by Category)
    sorted_indices = np.argsort(all_labels)
    sorted_matrix = sim_matrix[sorted_indices][:, sorted_indices]
    sorted_labels = np.array(all_labels)[sorted_indices]

    plt.figure(figsize=(12, 10))
    sns.heatmap(sorted_matrix, 
                xticklabels=sorted_labels, 
                yticklabels=sorted_labels, 
                cmap='viridis',
                cbar_kws={'label': 'Cosine Similarity'})
    plt.title(f'Cluster Analysis by Profession ({mode.capitalize()})\n(Merged Dataset n={len(FINAL_DATASET)})')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'heatmap_{mode}.png')

    return results

def plot_comparison(df_res):
    """
    Generates a grouped bar chart comparing Within vs Between similarity
    for both Zodiac systems.
    """
    modes = df_res['Mode'].str.capitalize()
    within = df_res['Within_Mean']
    between = df_res['Between_Mean']

    x = np.arange(len(modes))
    width = 0.35

    plt.figure(figsize=(10, 6))
    fig, ax = plt.subplots(figsize=(10, 6))

    rects1 = ax.bar(x - width/2, within, width, label='Within Profession', color='#4c72b0')
    rects2 = ax.bar(x + width/2, between, width, label='Between Professions', color='#dd8452')

    ax.set_ylabel('Mean Cosine Similarity')
    ax.set_title('Career Similarity: Within vs Between Groups')
    ax.set_xticks(x)
    ax.set_xticklabels(modes)
    ax.legend()

    # Add p-values as text
    for i, p_val in enumerate(df_res['p_value']):
        sig_text = "p < 0.001" if p_val < 0.001 else f"p = {p_val:.3f}"
        color = 'green' if p_val < 0.05 else 'black'
        weight = 'bold' if p_val < 0.05 else 'normal'
        ax.text(x[i], max(within[i], between[i]) + 0.002, sig_text, 
                ha='center', va='bottom', color=color, fontweight=weight)

    ax.set_ylim(0, max(within.max(), between.max()) * 1.15)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'similarity_bar_chart.png')
    print(f"Saved bar chart visualization to {OUTPUT_DIR / 'similarity_bar_chart.png'}")

def visualize_archetype_distributions(dataset, mode):
    """
    Creates Planet vs Sign heatmaps for each career archetype.
    Each cell represents the percentage of people in that category 
    having that planet in that sign.
    """
    # 1. Group data by category
    groups = {}
    for person in dataset:
        cat = person['category']
        if cat not in groups:
            groups[cat] = []

        try:
            # Re-calculating here is slightly inefficient but safe
            dt = datetime.strptime(person['date'], '%Y-%m-%d')
            vec = get_sign_features(dt.year, dt.month, dt.day, mode=mode)
            groups[cat].append(vec)
        except ValueError:
            continue

    # Signs and Planets for labels
    signs = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aq', 'Pis']
    planet_names = ['Sun', 'Moon', 'Mer', 'Ven', 'Mar', 'Jup', 'Sat', 'Ura', 'Nep', 'Plu', 'NNode']

    print(f"\nGeneratring Archetype Heatmaps ({mode})...")

    for cat, vectors in groups.items():
        if not vectors:
            continue

        n_people = len(vectors)
        if n_people < 3: # Skip small groups
            continue

        mat = np.array(vectors) # Shape (N_people, 132)
        # Sum across people
        counts = np.sum(mat, axis=0) # Shape (132,)

        # Reshape to (11 Planets, 12 Signs)
        # The vector construction order in get_sign_features is:
        # P1_S1..S12, P2_S1..S12
        heatmap_data = counts.reshape(len(PLANETS), 12)

        # Normalize to percentage (0.0 to 1.0)
        heatmap_data_pct = heatmap_data / n_people

        # Plot
        plt.figure(figsize=(12, 8))
        sns.heatmap(heatmap_data_pct, annot=True, fmt='.0%', 
                    xticklabels=signs, yticklabels=planet_names, 
                    cmap='RdPu', cbar_kws={'label': 'Frequency (%)'},
                    vmin=0, vmax=0.5) # Cap colormap at 50% for visibility

        plt.title(f'Archetype Signature: {cat} ({mode.capitalize()})\n(n={n_people})')
        plt.tight_layout()

        filename = f'archetype_heatmap_{mode}_{cat.replace(" ", "_").lower()}.png'
        plt.savefig(OUTPUT_DIR / filename)
        plt.close()
        print(f"  Saved {filename}")

def main():
    res_trop = run_analysis('tropical')
    res_vedic = run_analysis('vedic')

    # Generate Archetype Heatmaps
    visualize_archetype_distributions(FINAL_DATASET, 'tropical')
    visualize_archetype_distributions(FINAL_DATASET, 'vedic')

    # Save Summary
    df_res = pd.DataFrame([res_trop, res_vedic])
    print("\n--- SUMMARY ---")
    print(df_res.to_string(index=False))
    df_res.to_csv(OUTPUT_DIR / 'analysis_comparative_results.csv', index=False)

    # Generate Comparison Plot
    plot_comparison(df_res)

    # Update RESULTS.md
    with open(OUTPUT_DIR / 'RESULTS.md', 'w') as f:
        f.write("# Project 23: Birth Chart Career Similarity (Sign-Based)\n\n")
        f.write("## Methodology\n")
        f.write("- **Features**: Planetary Signs (Sun through Node), One-Hot Encoded.\n")
        f.write("- **Metric**: Cosine Similarity between feature vectors.\n")
        f.write("- **Zodiacs**: Tropical and Vedic (Lahiri).\n")
        f.write(f"- **Sample**: {len(FINAL_DATASET)} celebrities (Merged Dataset: Manual + scraped).\n")
        f.write("- **Data Merging**: Prior 24 manually selected celebrities (Tech/Music/Science) + additional non-duplicates from .\n")
        f.write("- **Categories**: Tech, Music, Science, Arts, Politics, Sports.\n\n")

        f.write("## Findings\n")
        f.write("\n")
        f.write(df_res.to_string(index=False))
        f.write("\n\n")
        f.write("### Interpretation\n")
        if res_trop['p_value'] > 0.05 and res_vedic['p_value'] > 0.05:
            f.write("No statistically significant similarity found within professions in either zodiac.\n")
            f.write("Planetary signs alone do not appear to cluster strongly by career choice in this larger, merged dataset.\n")
        else:
             f.write("Some significant clustering observed.\n")

if __name__ == "__main__":
    main()
