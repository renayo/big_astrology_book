import pandas as pd
import numpy as np
import swisseph as swe
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from pathlib import Path
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Setup
OUTPUT_DIR = Path(__file__).parent
DATA_FILE = OUTPUT_DIR / "new_couples_wikidata.csv"
swe.set_ephe_path(None)

# REMOVED OUTER PLANETS
PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY, 'Venus': swe.VENUS, 
    'Mars': swe.MARS, 'Jupiter': swe.JUPITER, 'Saturn': swe.SATURN, 
    # 'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE, 'Pluto': swe.PLUTO, 
    'Node': swe.MEAN_NODE, 'Lilith': swe.MEAN_APOG
}

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

def get_positions(date_str, time_str=None, sidereal=False):
    # (Same implementation)
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        hour = 12.0
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
        signs = {}
        
        for name, pid in PLANETS.items():
            res = swe.calc_ut(jd, pid, flags)
            deg = res[0][0]
            pos[name] = np.deg2rad(deg)
            signs[name] = SIGNS[int(deg / 30) % 12]
            
        return pos, signs
    except:
        return None, None

def get_target(row):
    end = row['end_date']
    if pd.isna(end): return 0
    try:
        end_dt = datetime.strptime(str(end), "%Y-%m-%d")
    except:
        return 0
    
    # Check Death
    for d in [row['p1_death_date'], row['p2_death_date']]:
         if not pd.isna(d):
              try:
                  death_dt = datetime.strptime(str(d), "%Y-%m-%d")
                  if abs((end_dt - death_dt).days) < 365:
                       return 0 
              except:
                  pass
    return 1

def load_and_process_data():
    print("Loading and processing data (NO OUTER PLANETS)...")
    if not DATA_FILE.exists():
        print(f"Error: {DATA_FILE} not found.")
        return None, None

    df = pd.read_csv(DATA_FILE)
    data_list = []
    
    for _, row in df.iterrows():
        try:
            get_target(row) 
            if pd.isna(row['p1_birth_date']) or pd.isna(row['p2_birth_date']): continue
            
            p1_trop_pos, p1_trop_signs = get_positions(row['p1_birth_date'], row.get('p1_birth_time'), False)
            p2_trop_pos, p2_trop_signs = get_positions(row['p2_birth_date'], row.get('p2_birth_time'), False)
            p1_sid_pos, p1_sid_signs = get_positions(row['p1_birth_date'], row.get('p1_birth_time'), True)
            p2_sid_pos, p2_sid_signs = get_positions(row['p2_birth_date'], row.get('p2_birth_time'), True)
            
            if not p1_trop_pos or not p2_trop_pos: continue
                
            target = get_target(row)
            feat = {'divorced': target}
            planet_names = list(PLANETS.keys())
            
            # Angles (Tropical)
            for p1 in planet_names:
                for p2 in planet_names:
                    angle = p1_trop_pos[p1] - p2_trop_pos[p2]
                    feat[f"Angle_Cos_{p1}_{p2}"] = np.cos(angle)
            
            # Signs
            for p in planet_names:
                feat[f"Trop_P1_{p}_Sign"] = p1_trop_signs[p]
                feat[f"Trop_P2_{p}_Sign"] = p2_trop_signs[p]
                feat[f"Sid_P1_{p}_Sign"] = p1_sid_signs[p]
                feat[f"Sid_P2_{p}_Sign"] = p2_sid_signs[p]

            data_list.append(feat)
        except:
            continue
            
    study_df = pd.DataFrame(data_list)
    study_df = pd.get_dummies(study_df, dtype=float)
    X = study_df.drop(columns=['divorced'])
    y = study_df['divorced']
    return X, y

def main():
    X, y = load_and_process_data()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Random Forest Focus
    rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    rf.fit(X_train_scaled, y_train)
    
    y_pred = rf.predict(X_test_scaled)
    
    print("\n--- Random Forest Results (NO OUTER PLANETS) ---")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Feature Importance
    importances = rf.feature_importances_
    feature_names = X.columns
    indices = np.argsort(importances)[::-1]

    print("\n--- Top 20 Most Important Features ---")
    for f in range(20):
        print(f"{f+1}. {feature_names[indices[f]]}: {importances[indices[f]]:.4f}")

if __name__ == "__main__":
    main()

