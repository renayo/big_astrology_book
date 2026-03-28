import pandas as pd
import numpy as np
import os

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_HITS = os.path.join(SCRIPT_DIR, 'detailed_conjunctions.csv')
INPUT_FILE_PEOPLE = os.path.join(SCRIPT_DIR, 'celebrity_data.csv')
OUTPUT_FILE_STATS = os.path.join(SCRIPT_DIR, 'permutation_test_results.csv')
N_PERMUTATIONS = 1000

def run_permutation_test():
    print("Loading data...")
    if not os.path.exists(INPUT_FILE_HITS) or not os.path.exists(INPUT_FILE_PEOPLE):
        print("Error: Input files not found. Run analysis.py first.")
        return

    # 1. Load Data
    hits_df = pd.read_csv(INPUT_FILE_HITS)
    people_df = pd.read_csv(INPUT_FILE_PEOPLE)

    # Clean people data
    # Ensure 'category' column exists (mapped from 'cause')
    if 'cause' in people_df.columns and 'category' not in people_df.columns:
        people_df['category'] = people_df['cause']

    # Filter for valid categories
    people_df = people_df[people_df['category'].notna()]

    # Drop duplicates by name to prevent reindexing errors
    people_df = people_df.drop_duplicates(subset='name')

    unique_categories = people_df['category'].unique()

    # Map Names to Categories (The Ground Truth)
    # We use a dictionary for fast lookup during permutation? 
    # Actually, we can just shuffle the 'category' column in people_df.

    # 2. Build the Intensity Matrix (People x Stars)
    # Rows: Name, Cols: Star, Values: Sum of Cosine Similarity (Total Intensity for that person-star pair)
    # Note: A person might have Sun conjunct Sirius AND Venus conjunct Sirius. We sum these intensities.
    intensity_matrix = hits_df.groupby(['name', 'star'])['cosine'].sum().unstack(fill_value=0)

    # Align with people_df
    # Ensure all people in people_df are in the matrix (even if they have 0 hits)
    # content of people_df['name'] might overlap with intensity_matrix.index
    # We want to preserve the people_df list because that's our population N.

    people_names = people_df['name'].unique()

    # Reindex matrix to include all people (fill 0 for those with no hits)
    intensity_matrix = intensity_matrix.reindex(people_names, fill_value=0)

    # Now we have:
    # X: Matrix (N_people x N_stars) of intensities.
    # y: Vector (N_people) of categories.

    print(f"Data prepared: {len(people_names)} people, {intensity_matrix.shape[1]} stars.")

    # 3. Calculate Observed Statistics
    # Mean Intensity per Category-Star pair

    # Helper to calculate stats
    def calculate_group_means(matrix, categories_series):
        # Add category column temporarily
        df = matrix.copy()
        df['current_category'] = categories_series.values
        return df.groupby('current_category').mean()

    print("Calculating observed statistics...")
    # Ensure the order of categories_series matches the matrix index (names)
    # people_df needs to be sorted/aligned by name to match intensity_matrix
    people_df = people_df.set_index('name').reindex(intensity_matrix.index)

    observed_means = calculate_group_means(intensity_matrix, people_df['category'])

    # 4. Permutation Test
    print(f"Running {N_PERMUTATIONS} permutations...")

    # Store aggregated permutation results
    # We need to build a distribution for every (Category, Star) cell.
    # Shape of observed_means is (N_Categories, N_Stars).
    # We can perform vectorised updates.

    # Initialize accumulators for mean and variance calculation (Welford's algorithm or just sum/sq_sum)
    # Or just store all? 1000 * 15 * 12 is small (180k floats). We can store all.

    results_storage = {cat: {star: [] for star in intensity_matrix.columns} for cat in unique_categories}

    categories_array = people_df['category'].values

    for i in range(N_PERMUTATIONS):
        if i % 100 == 0:
            print(f"Permutation {i}/{N_PERMUTATIONS}")

        # Shuffle categories
        shuffled_categories = np.random.permutation(categories_array)

        # Calculate means
        # Construct a temporary DF is slow in loop.
        # Use pandas groupby on the matrix values directly? Or numpy?
        # Numpy is faster.

        # Convert matrix to numpy
        X = intensity_matrix.values
        # grouped means:
        # iterate unique categories
        for cat in unique_categories:
            # mask for this category
            mask = (shuffled_categories == cat)
            if np.sum(mask) > 0:
                cat_means = np.mean(X[mask], axis=0)

                # Store
                for star_idx, star in enumerate(intensity_matrix.columns):
                    results_storage[cat][star].append(cat_means[star_idx])

    # 5. Calculate Z-Scores and P-Values
    print("Computing Z-Scores...")
    final_results = []

    for cat in unique_categories:
        for star in intensity_matrix.columns:
            obs = observed_means.loc[cat, star]
            perm_dist = np.array(results_storage[cat][star])

            if len(perm_dist) == 0:
                continue

            mu = np.mean(perm_dist)
            sigma = np.std(perm_dist)

            # Avoid divide by zero
            if sigma == 0:
                z_score = 0
            else:
                z_score = (obs - mu) / sigma

            # P-value (Two-sided? Or one-sided? "Significance" usually implies extreme)
            # Let's do two-sided
            # Count how many permuted values are as extreme as observed
            # Actually, standard interpretation for "Effect":
            # If obs > mu, how many perms > obs?
            # If obs < mu, how many perms < obs?

            # Simple percentile rank / p-value
            n_greater = np.sum(perm_dist >= obs)
            n_less = np.sum(perm_dist <= obs)
            p_val = min(n_greater, n_less) / N_PERMUTATIONS * 2 # Two-tailed approximation

            final_results.append({
                'Category': cat,
                'Star': star,
                'Observed_Intensity_Mean': obs,
                'Baseline_Mean': mu,
                'Std_Dev': sigma,
                'Z_Score': z_score,
                'P_Value': p_val,
                'N_Category': len(people_df[people_df['category'] == cat])
            })

    # 6. Save Results
    results_df = pd.DataFrame(final_results)

    # Sort by absolute Z-Score descending
    results_df['Abs_Z'] = results_df['Z_Score'].abs()
    results_df = results_df.sort_values('Abs_Z', ascending=False)
    results_df = results_df.drop(columns=['Abs_Z'])

    results_df.to_csv(OUTPUT_FILE_STATS, index=False)
    print(f"Saved results to {OUTPUT_FILE_STATS}")

    # Print Top 5
    print("\nTop 5 Significant Associations:")
    print(results_df.head(5).to_string())

if __name__ == "__main__":
    run_permutation_test()
