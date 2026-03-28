import pandas as pd
import numpy as np
import swisseph as swe
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path

# Setup
OUTPUT_DIR = Path(__file__).parent
DATA_FILE = OUTPUT_DIR / "new_couples_wikidata.csv"
swe.set_ephe_path(None)

PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY, 'Venus': swe.VENUS, 
    'Mars': swe.MARS, 'Jupiter': swe.JUPITER, 'Saturn': swe.SATURN, 
    'Node': swe.MEAN_NODE, 'Lilith': swe.MEAN_APOG
}

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

def get_positions(date_str, time_str=None, sidereal=False):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        hour = 12.0
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

def run_check():
    df = pd.read_csv(DATA_FILE)
    processed_data = []
    original_rows = []

    for _, row in df.iterrows():
        try:
            target = get_target(row)
            if pd.isna(row['p1_birth_date']) or pd.isna(row['p2_birth_date']): continue
            
            p1_trop, p1_sign = get_positions(row['p1_birth_date'], row.get('p1_birth_time'), False)
            p2_trop, p2_sign = get_positions(row['p2_birth_date'], row.get('p2_birth_time'), False)
            p1_sid, p1_sid_s = get_positions(row['p1_birth_date'], row.get('p1_birth_time'), True)
            p2_sid, p2_sid_s = get_positions(row['p2_birth_date'], row.get('p2_birth_time'), True)
            
            if not p1_trop or not p2_trop: continue
                
            feat = {'divorced': target}
            planet_names = list(PLANETS.keys())
            for p1 in planet_names:
                for p2 in planet_names:
                    deg = p1_trop[p1] - p2_trop[p2]
                    feat[f"Angle_Cos_{p1}_{p2}"] = np.cos(deg)
            for p in planet_names:
                feat[f"Trop_P1_{p}_Sign"] = p1_sign[p]
                feat[f"Trop_P2_{p}_Sign"] = p2_sign[p]
                feat[f"Sid_P1_{p}_Sign"] = p1_sid_s[p]
                feat[f"Sid_P2_{p}_Sign"] = p2_sid_s[p]

            processed_data.append(feat)
            original_rows.append(row) # Keep track of original metadata
        except:
            continue
    
    study_df = pd.DataFrame(processed_data)
    study_df = pd.get_dummies(study_df, dtype=float)
    X = study_df.drop(columns=['divorced'])
    y = study_df['divorced']
    
    # Split using same seed
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    rf.fit(X_train_scaled, y_train)
    
    y_pred = rf.predict(X_test_scaled)
    
    print("\n--- Inspecting the Predictions ---")
    
    test_indices = X_test.index
    predicted_divorced_indices = test_indices[y_pred == 1]
    
    print(f"Total Predicted Divorced: {len(predicted_divorced_indices)}")
    
    # Retrieve original info
    print("\nBirth Years of Predicted Divorced Couples:")
    years = []
    for idx in predicted_divorced_indices:
        original = original_rows[idx]
        is_correct = (y[idx] == 1)
        p1_year = str(original['p1_birth_date'])[:4]
        print(f"Index {idx}: Born {p1_year}. Correct? {is_correct}")
        years.append(int(p1_year))

    print(f"\nAverage Birth Year of Predicted Divorced: {np.mean(years):.1f}")
    
    # Compare with False Negatives (Divorced but predicted Stayed)
    print("\nBirth Years of MISSED Divorces (False Negatives):")
    missed_indices = test_indices[(y_test == 1) & (y_pred == 0)]
    missed_years = []
    # Show first 10
    for idx in missed_indices[:10]:
        original = original_rows[idx]
        p1_year = str(original['p1_birth_date'])[:4]
        missed_years.append(int(p1_year))
    print(f"Average Birth Year of Sample Missed: {np.mean(missed_years):.1f}")

if __name__ == "__main__":
    run_check()

