import pandas as pd
import numpy as np
import swisseph as swe
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, f1_score, precision_score, recall_score, accuracy_score
from pathlib import Path
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Setup
OUTPUT_DIR = Path(__file__).parent
DATA_FILE = OUTPUT_DIR / "new_couples_wikidata.csv"
swe.set_ephe_path(None)

# 12 Celestial Features
PLANETS = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY, 'Venus': swe.VENUS, 
    'Mars': swe.MARS, 'Jupiter': swe.JUPITER, 'Saturn': swe.SATURN, 
    'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE, 'Pluto': swe.PLUTO, 
    'Node': swe.MEAN_NODE, 'Lilith': swe.MEAN_APOG
}

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

def get_positions(date_str, time_str=None, sidereal=False):
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
    print("Loading and processing data...")
    if not DATA_FILE.exists():
        print(f"Error: {DATA_FILE} not found.")
        return None, None

    df = pd.read_csv(DATA_FILE)
    data_list = []
    
    for _, row in df.iterrows():
        try:
            target = get_target(row)
            if pd.isna(row['p1_birth_date']) or pd.isna(row['p2_birth_date']): continue
            
            p1_trop_pos, p1_trop_signs = get_positions(row['p1_birth_date'], row.get('p1_birth_time'), False)
            p2_trop_pos, p2_trop_signs = get_positions(row['p2_birth_date'], row.get('p2_birth_time'), False)
            
            p1_sid_pos, p1_sid_signs = get_positions(row['p1_birth_date'], row.get('p1_birth_time'), True)
            p2_sid_pos, p2_sid_signs = get_positions(row['p2_birth_date'], row.get('p2_birth_time'), True)

            if not p1_trop_pos or not p2_trop_pos: continue
                
            feat = {'divorced': target}
            planet_names = list(PLANETS.keys())
            
            # Angles (Tropical)
            for p1 in planet_names:
                for p2 in planet_names:
                    angle = p1_trop_pos[p1] - p2_trop_pos[p2]
                    feat[f"Angle_Cos_{p1}_{p2}"] = np.cos(angle)
            
            # Signs (Both)
            for p in planet_names:
                feat[f"Trop_P1_{p}_Sign"] = p1_trop_signs[p]
                feat[f"Trop_P2_{p}_Sign"] = p2_trop_signs[p]
                feat[f"Sid_P1_{p}_Sign"] = p1_sid_signs[p]
                feat[f"Sid_P2_{p}_Sign"] = p2_sid_signs[p]

            data_list.append(feat)
        except:
            continue
            
    study_df = pd.DataFrame(data_list)
    print(f"Processed {len(study_df)} couples.")
    
    study_df = pd.get_dummies(study_df, dtype=float)
    X = study_df.drop(columns=['divorced'])
    y = study_df['divorced']
    
    return X, y

def main():
    X, y = load_and_process_data()
    if X is None: return

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Models to Test
    models = {
        "Logistic Regression (Baseline)": None, # Already ran, but good for comparison
        "Random Forest (100 Trees)": RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42),
        "Gradient Boosting (GBM)": GradientBoostingClassifier(n_estimators=100, random_state=42),
        "SVM (RBF Kernel)": SVC(class_weight='balanced', random_state=42),
        "Neural Network (MLP)": MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
    }
    
    print("\n--- Model Comparison ---")
    print(f"{'Model':<30} | {'Accuracy':<10} | {'F1 (Divorce)':<12} | {'Precision':<10} | {'Recall':<10}")
    print("-" * 85)
    
    baseline_acc = 1 - y_test.mean()
    print(f"{'Majority Class Baseline':<30} | {baseline_acc:.2%}      | 0.00         | 0.00       | 0.00")

    for name, model in models.items():
        if model is None: continue
        
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, pos_label=1)
        prec = precision_score(y_test, y_pred, pos_label=1)
        rec = recall_score(y_test, y_pred, pos_label=1)
        
        print(f"{name:<30} | {acc:.2%}      | {f1:.4f}       | {prec:.4f}     | {rec:.4f}")

if __name__ == "__main__":
    main()

