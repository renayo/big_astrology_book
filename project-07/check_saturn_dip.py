import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Setup paths
OUTPUT_DIR = Path(__file__).parent
DATA_FILE = OUTPUT_DIR / "BIG5_data.csv"

def load_and_analyze():
    print(f"Loading {DATA_FILE}...")
    try:
        df = pd.read_csv(DATA_FILE, sep='\t')
    except Exception as e:
        print(f"Error loading data: {e}. Trying default pandas read...")
        df = pd.read_csv(DATA_FILE) # Fallback

    # Filter reasonable ages
    df = df[df['age'].between(13, 90)]

    # Calculate Conscientiousness Score
    # Reverse keys for C: 2, 4, 6, 8 (based on code in analysis_cyclic.py)
    reverse_keyed_C = [2, 4, 6, 8]

    # Calculate score
    score = pd.Series(0, index=df.index)
    valid_cols = True
    for i in range(1, 11):
        col = f'C{i}'
        if col not in df.columns:
            print(f"Column {col} missing")
            valid_cols = False
            break
        val = df[col]
        if i in reverse_keyed_C:
            val = 6 - val # Reverse 1-5 scale
        score += val

    if not valid_cols:
        return

    df['Score_C'] = score

    # 1. Calculate Expected Score based on Age (Detrending)
    # Using a polynomial to capture the curved maturation process better than linear
    poly = PolynomialFeatures(degree=2)
    X_age = poly.fit_transform(df[['age']])
    model = LinearRegression().fit(X_age, df['Score_C'])
    df['Expected_C'] = model.predict(X_age)
    df['Residual_C'] = df['Score_C'] - df['Expected_C']

    # 2. Calculate Saturn Phase
    saturn_period = 29.457
    df['Saturn_Phase'] = (df['age'] % saturn_period) / saturn_period

    # 3. Bin the phases (20 bins = 0.05 width per bin)
    df['Phase_Bin'] = pd.cut(df['Saturn_Phase'], bins=20, labels=False)

    # 4. Analyze the bins
    results = df.groupby('Phase_Bin').agg({
        'Score_C': 'mean',
        'Expected_C': 'mean',
        'Residual_C': 'mean',
        'age': 'mean',
        'Score_C': ['mean', 'count', 'std']
    })

    # Flatten columns
    results.columns = ['_'.join(col).strip() for col in results.columns.values]
    results = results.reset_index()

    print("\n--- SATURN PHASE ANALYSIS (CONSCIENTIOUSNESS) ---")
    print(f"{'Bin':<5} | {'Phase Range':<12} | {'Mean Age':<8} | {'Raw Score':<10} | {'Residual':<10} | {'Count':<6}")
    print("-" * 75)

    for _, row in results.iterrows():
        bin_idx = int(row['Phase_Bin'])
        phase_center = (bin_idx * 0.05) + 0.025
        phase_start = bin_idx * 0.05
        phase_end = (bin_idx + 1) * 0.05

        # Determine if this is the "Opposition" region (0.45 - 0.55)
        marker = ""
        if 0.45 <= phase_center <= 0.55:
            marker = " <--- OPPOSITION (Halfway)"
        elif 0.0 <= phase_center <= 0.05 or 0.95 <= phase_center <= 1.0:
            marker = " <--- RETURN (Start/End)"

        # Note: Raw Score mean depends heavily on age, Residual is the key metric
        # We need to re-calculate residual mean manually here as agg above might have messed up col names?
        # Actually let's just use the dataframe mean for this bin from original df
        bin_mask = df['Phase_Bin'] == bin_idx
        res_mean = df.loc[bin_mask, 'Residual_C'].mean()
        raw_mean = df.loc[bin_mask, 'Score_C'].mean()
        age_mean = df.loc[bin_mask, 'age'].mean()
        count = df.loc[bin_mask, 'Score_C'].count()

        print(f"{bin_idx:<5} | {phase_start:.2f}-{phase_end:.2f}     | {age_mean:.1f}     | {raw_mean:.4f}     | {res_mean:+.4f}    | {count:<6}{marker}")

if __name__ == "__main__":
    load_and_analyze()
