import pandas as pd
import numpy as np
import swisseph as swe
from datetime import datetime
from sklearn.linear_model import ElasticNetCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup
OUTPUT_DIR = Path(__file__).parent
DATA_FILE = OUTPUT_DIR / "new_couples_wikidata.csv"
swe.set_ephe_path(None)

# Planets
PLANETS = {
    'Sun': swe.SUN,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Node': swe.MEAN_NODE
}
PLANET_LIST = list(PLANETS.keys())

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

def get_positions(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        jd = swe.julday(dt.year, dt.month, dt.day, 12.0)
        pos = {}
        for name, pid in PLANETS.items():
            deg = swe.calc_ut(jd, pid)[0][0]
            pos[name] = np.deg2rad(deg)
        return pos
    except:
        return None

def main():
    print("Loading data for Multilinear Regression...")
    df = pd.read_csv(DATA_FILE)

    data_list = []

    # Preprocessing
    for _, row in df.iterrows():
        try:
            # We can only regress on COMPLETED relationships (Death or Divorce).
            # 'Ongoing' relationships are censored; we don't know their final duration.
            end_str = str(row['end_date'])
            if end_str == 'nan': continue 

            start_str = str(row['start_date'])
            if start_str == 'nan': continue

            start_dt = datetime.strptime(start_str, "%Y-%m-%d")
            end_dt = datetime.strptime(end_str, "%Y-%m-%d")

            duration_years = (end_dt - start_dt).days / 365.25

            # Sanity filters
            if duration_years < 0.1 or duration_years > 80: continue

            # Synastry Features
            p1_pos = get_positions(row['p1_birth_date'])
            p2_pos = get_positions(row['p2_birth_date'])

            if not p1_pos or not p2_pos: continue

            feat = {'duration': duration_years}

            # P1 Zodiac Signs (Categorical)
            for p_name, rad in p1_pos.items():
                deg = np.degrees(rad)
                idx = int(deg / 30) % 12
                feat[f"P1_{p_name}_Sign"] = SIGNS[idx]

            # Calculate all pairwise cosines
            for p1 in PLANET_LIST:
                for p2 in PLANET_LIST:
                    angle = p1_pos[p1] - p2_pos[p2]
                    # Agnostic Cosine: +1 (Conj), -1 (Opp)
                    feat[f"{p1}-{p2}"] = np.cos(angle)

            data_list.append(feat)

        except Exception:
            continue

    study_df = pd.DataFrame(data_list)
    print(f"Dataset: {len(study_df)} completed relationships/marriages.")

    # One-Hot Encode Signs
    study_df = pd.get_dummies(study_df, columns=[c for c in study_df.columns if '_Sign' in c], dtype=float)

    if len(study_df) < 50:
        print("Not enough data for regression.")
        return

    # Prepare X (Features) and y (Target)
    feature_cols = [c for c in study_df.columns if c != 'duration']
    X = study_df[feature_cols]
    y = study_df['duration']

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standard Scaling (Crucial for Regularization)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("\n--- Running ElasticNet Regression ---")
    print("Finding the optimal combination of features...")

    # ElasticNetCV automatically finds best alpha (regularization strength) and l1_ratio
    # It tends to zero-out irrelevant features (Feature Selection).
    model = ElasticNetCV(cv=5, random_state=42, max_iter=10000, n_jobs=-1)
    model.fit(X_train_scaled, y_train)

    # Evaluation
    r2_train = model.score(X_train_scaled, y_train)
    r2_test = model.score(X_test_scaled, y_test)
    y_pred = model.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"\nModel Performance:")
    print(f"R² (Test Set): {r2_test:.4f}")
    print(f"Mean Absolute Error: {mae:.2f} years")
    print(f"Baseline (Mean) Error: {mean_absolute_error(y_test, [y_train.mean()]*len(y_test)):.2f} years")

    # Analysis of Coefficients
    coefs = pd.Series(model.coef_, index=feature_cols)
    non_zero = coefs[coefs != 0].sort_values(ascending=False) # Sort by magnitude

    print(f"\nTotal Features: {len(feature_cols)}")
    print(f"Selected Features (Non-Zero): {len(non_zero)}")

    print("\n--- THE FORMULA ---")
    print(f"Duration (Years) = {model.intercept_:.2f}")
    print("Terms (Scaled Coefficients):")

    print(non_zero)

    # Visualization
    if len(non_zero) > 0:
        plt.figure(figsize=(10, len(non_zero)*0.3 + 4))
        sns.barplot(x=non_zero.values, y=non_zero.index, palette='vlag')
        plt.title('Best Multilinear Regression Formula\n(ElasticNet Coefficients)')
        plt.xlabel('Impact on Duration (Years per StdDev)')
        plt.axvline(0, color='black', linewidth=1)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / 'regression_formula_coeffs.png')
        print("Saved regression_formula_coeffs.png")
    else:
        print("Model shrunk all coefficients to zero. Best predictor is just the Mean Duration.")

if __name__ == "__main__":
    main()
