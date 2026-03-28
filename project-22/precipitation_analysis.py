import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'weather_with_astro_full.csv')

def analyze_precipitation():
    print("Loading data for Precipitation Analysis...")
    if not os.path.exists(DATA_FILE):
        print(f"File {DATA_FILE} not found. Run process_astro_data.py first.")
        return

    df = pd.read_csv(DATA_FILE)

    # Ensure date is datetime
    df['date'] = pd.to_datetime(df['date'])

    # 1. Lunar Day Analysis (Tropical & Vedic)
    print("\nAnalyzing Precipitation by Lunar Day...")
    lunar_tro = df.groupby('Lunar_Day_Tro')['avg_prcp'].mean()
    lunar_ved = df.groupby('Lunar_Day_Ved')['avg_prcp'].mean()

    # 2. Element Analysis (Tropical)
    print("Analyzing Precipitation by Element (Tropical)...")
    elem_tro = df.groupby('Sun_Tro_Elem')['avg_prcp'].agg(['mean', 'count', 'std'])

    # 3. Element Analysis (Vedic)
    print("Analyzing Precipitation by Element (Vedic)...")
    elem_ved = df.groupby('Sun_Ved_Elem')['avg_prcp'].agg(['mean', 'count', 'std'])

    print("\n--- RESULTS: PRECIPITATION ---")
    print("\nBy Element (Tropical):")
    print(elem_tro)
    print("\nBy Element (Vedic):")
    print(elem_ved)

    # Save simple summary
    elem_tro.to_csv(os.path.join(BASE_DIR, 'precip_by_element_tropical.csv'))

if __name__ == "__main__":
    analyze_precipitation()
