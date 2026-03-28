
import pandas as pd
import numpy as np
import swisseph as swe
from datetime import datetime
from sklearn.linear_model import LogisticRegressionCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Setup
OUTPUT_DIR = Path(__file__).parent
DATA_FILE = OUTPUT_DIR / "new_couples_wikidata.csv"
RESULTS_FILE = OUTPUT_DIR / "analysis_results.csv"
swe.set_ephe_path(None)

# 12 Celestial Features
PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO,
    'Node': swe.MEAN_NODE,
    'Lilith': swe.MEAN_APOG
}

def get_positions(date_str, time_str=None, sidereal=False):
    try:
        dt = datetime.strptime(str(date_str), "%Y-%m-%d")
        hour = 12.0 # Default to noon
        if time_str and not pd.isna(time_str):
            try:
                parts = str(time_str).split(':')
                hour = float(parts[0]) + float(parts[1])/60.0
            except:
                pass
        
        jd = swe.julday(dt.year, dt.month, dt.day, hour)
        
        if sidereal:
            swe.set_sid_mode(swe.SIDM_LAHIRI)
            flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
        else:
            swe.set_sid_mode(0)
            flags = swe.FLG_SWIEPH
            
        pos = {}
        for name, pid in PLANETS.items():
            res = swe.calc_ut(jd, pid, flags)
            # Use radians for easy cosine calc
            pos[name] = np.deg2rad(res[0][0])
            
        return pos
    except Exception as e:
        return None

def get_target(row):
    """
    1 = Divorced/Separated
    0 = Still Together or Widowed (Successful)
    """
    end = row['end_date']
    if pd.isna(end): return 0 # Still together
    
    try:
        end_dt = datetime.strptime(str(end), "%Y-%m-%d")
    except:
        return 0
    
    # Check if end was due to death
    for d in [row['p1_death_date'], row['p2_death_date']]:
         if not pd.isna(d):
              try:
                  death_dt = datetime.strptime(str(d), "%Y-%m-%d")
                  # If death occurred within 1 year of end date, count as widowed (Success)
                  if abs((end_dt - death_dt).days) < 365:
                       return 0 
              except:
                  pass
    return 1 # Divorce

def main():
    print("="*60)
    print("PROJECT 36: SYNASTRY HARMONICS (LOGISTIC REGRESSION)")
    print("="*60)
    print("Features: 12 Celestial Bodies x 12 Celestial Bodies (Cosine Angle Diff)")
    print("Systems: Tropical + Vedic (Sidereal)")
    print("------------------------------------------------------------")

    if not DATA_FILE.exists():
        print(f"Error: {DATA_FILE} not found.")
        return

    df = pd.read_csv(DATA_FILE)
    print(f"Loading {len(df)} couples from CSV...")
    
    data_list = []
    
    for _, row in df.iterrows():
        try:
            # Skip if birthdates are missing
            if pd.isna(row['p1_birth_date']) or pd.isna(row['p2_birth_date']): continue
            
            target = get_target(row)
            
            # --- TROPICAL ---
            p1_trop = get_positions(row['p1_birth_date'], row.get('p1_birth_time'), sidereal=False)
            p2_trop = get_positions(row['p2_birth_date'], row.get('p2_birth_time'), sidereal=False)
            
            # --- VEDIC ---
            p1_vedic = get_positions(row['p1_birth_date'], row.get('p1_birth_time'), sidereal=True)
            p2_vedic = get_positions(row['p2_birth_date'], row.get('p2_birth_time'), sidereal=True)
            
            if not (p1_trop and p2_trop and p1_vedic and p2_vedic): continue
            
            feat = {'is_divorced': target}
            
            planet_names = list(PLANETS.keys())
            
            # 1. Tropical Cross-Matrix
            for p1 in planet_names:
                for p2 in planet_names:
                    # Cosine of difference
                    # cos(a - b)
                    val = np.cos(p1_trop[p1] - p2_trop[p2])
                    feat[f"Trop_Cos_{p1}_{p2}"] = val
                    
            # 2. Vedic Cross-Matrix
            for p1 in planet_names:
                for p2 in planet_names:
                    val = np.cos(p1_vedic[p1] - p2_vedic[p2])
                    feat[f"Vedic_Cos_{p1}_{p2}"] = val
            
            data_list.append(feat)
            
        except Exception as e:
            continue
            
    if not data_list:
        print("No valid data generated.")
        return

    study_df = pd.DataFrame(data_list)
    
    total_samples = len(study_df)
    divorce_rate = study_df['is_divorced'].mean()
    print(f"Processed Dataset: {total_samples} couples")
    print(f"Divorce Rate: {divorce_rate:.1%}")
    
    # Train/Test
    X = study_df.drop(columns=['is_divorced'])
    y = study_df['is_divorced']
    feature_names = X.columns.tolist()
    
    print(f"Feature Count: {len(feature_names)} (144 Tropical + 144 Vedic)")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale features (StandardScaler is good practice for Logistic Regression regularization)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("Training Logistic Regression (L1 Reg / Lasso for Feature Selection)...")
    # LogisticRegressionCV automatically finds best C with Cross Validation
    model = LogisticRegressionCV(cv=5, penalty='l1', solver='liblinear', random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)
    
    # Evaluation
    preds = model.predict(X_test_scaled)
    probs = model.predict_proba(X_test_scaled)[:, 1]
    
    acc = accuracy_score(y_test, preds)
    roc = roc_auc_score(y_test, probs)
    
    print(f"\nResults:")
    print(f"Accuracy: {acc:.4f} (Baseline: {max(y.mean(), 1-y.mean()):.4f})")
    print(f"ROC AUC:  {roc:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, preds))
    
    # Feature Importance (Coefficients)
    coefs = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': model.coef_[0],
        'Abs_Coef': np.abs(model.coef_[0])
    })
    
    # Save coefficients
    coefs.sort_values(by='Abs_Coef', ascending=False, inplace=True)
    coefs.to_csv(OUTPUT_DIR / "analysis_results.csv", index=False)
    
    print("\nTop 10 Most Predictive Features:")
    print(coefs.head(10).to_string(index=False))
    
    # Plot top 20
    plt.figure(figsize=(10, 8))
    top_20 = coefs.head(20)
    sns.barplot(x='Coefficient', y='Feature', data=top_20, palette='RdBu')
    plt.title('Top 20 Synastry Factors (Logistic Regression Coefficients)')
    plt.axvline(0, color='black', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'logistic_coefficients.png')
    print(f"Saved plot to {OUTPUT_DIR / 'logistic_coefficients.png'}")

if __name__ == "__main__":
    main()

