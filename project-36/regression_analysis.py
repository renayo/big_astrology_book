import pandas as pd
import numpy as np
import swisseph as swe
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression, ElasticNetCV, RidgeCV, LassoCV
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
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO,
    'Node': swe.MEAN_NODE
}
PLANET_LIST = list(PLANETS.keys())

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
    print("Loading data...")
    df = pd.read_csv(DATA_FILE)
    
    data_list = []
    
    print(f"Processing {len(df)} raw entries...")
    for _, row in df.iterrows():
        try:
            # 1. Filter for ENDED relationships only (for regression)
            if str(row['end_date']) == 'nan':
                continue # Skip ongoing relationships
            
            start_str = str(row['start_date'])
            end_str = str(row['end_date'])
            
            if start_str == 'nan': continue
            
            start_dt = datetime.strptime(start_str, "%Y-%m-%d")
            end_dt = datetime.strptime(end_str, "%Y-%m-%d")
            
            duration_years = (end_dt - start_dt).days / 365.25
            
            if duration_years < 0.1 or duration_years > 80: continue
            
            # 2. Calculate Synastry Features
            p1_pos = get_positions(row['p1_birth_date'])
            p2_pos = get_positions(row['p2_birth_date'])
            
            if not p1_pos or not p2_pos: continue
            
            feat = {'duration': duration_years}
            
            # P1 Planet vs P2 Planet
            for p1 in PLANET_LIST:
                for p2 in PLANET_LIST:
                    angle = p1_pos[p1] - p2_pos[p2]
                    # Feature: Cosine (+1 Conj, -1 Opp)
                    feat[f"{p1}-{p2}"] = np.cos(angle)
            
            data_list.append(feat)
            
        except Exception:
            continue
            
    study_df = pd.DataFrame(data_list)
    print(f"Final Dataset: {len(study_df)} completed marriages/relationships.")
    
    # Prepare X and y
    feature_cols = [c for c in study_df.columns if '-' in c]
    X = study_df[feature_cols]
    y = study_df['duration']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features (important for regularization interpretation)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("\n--- Training ElasticNet Regression (Optimizing Alpha/L1) ---")
    # ElasticNet combines Lasso (Selection) and Ridge (Stability)
    model = ElasticNetCV(cv=5, random_state=42, max_iter=10000)
    model.fit(X_train_scaled, y_train)
    
    r2_train = model.score(X_train_scaled, y_train)
    r2_test = model.score(X_test_scaled, y_test)
    
    print(f"R² (Train): {r2_train:.4f}")
    print(f"R² (Test):  {r2_test:.4f}")
    print(f"MAE (Test): {mean_absolute_error(y_test, model.predict(X_test_scaled)):.2f} years")
    
    # Extract Coefficients
    coefs = pd.Series(model.coef_, index=feature_cols)
    non_zero = coefs[coefs != 0].sort_values(ascending=False)
    
    print("\n--- Best Multilinear Formula (Non-Zero Coefficients) ---")
    print(f"Interceptor (Base Duration): {model.intercept_:.2f} years")
    print("\nTop Positive Influences (Increases Duration):")
    print(non_zero.head(10))
    
    print("\nTop Negative Influences (Decreases Duration):")
    print(non_zero.tail(10))
    
    # Visualization of Coefficients
    if len(non_zero) > 0:
        plt.figure(figsize=(12, 10))
        top_plot = pd.concat([non_zero.head(10), non_zero.tail(10)])
        sns.barplot(x=top_plot.values, y=top_plot.index, palette='RdBu_r')
        plt.title('Regression Coefficients (Standardized)\nChecking for Signal in Noise')
        plt.xlabel('Impact on Duration (Std Devs)')
        plt.axvline(0, color='black')
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / 'regression_coefficients.png')
        print("Saved regression_coefficients.png")
    else:
        print("Model shrunk all coefficients to zero. No signal found.")

    # Save Results
    with open(OUTPUT_DIR / 'regression_formula.txt', 'w') as f:
        f.write(f"Base Duration: {model.intercept_:.4f}\n")
        f.write(non_zero.to_string())

if __name__ == "__main__":
    main()

