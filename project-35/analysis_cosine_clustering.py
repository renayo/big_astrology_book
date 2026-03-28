#!/usr/bin/env python3
"""
Project 35: Unsupervised Clustering with Cosine Interactions
------------------------------------------------------------
Objectives:
1. Use ALL 66 Pairwise Interactions between the 12 celestial features.
   Metric: Cosine of the angle difference (Cos(A-B)).
   +1 = Conjunction, -1 = Opposition.
2. Run PCA and Clustering (K-Means) to see if professionals cluster
   based on their "Aspect Structure" rather than absolute signs.
3. Determine if clustering occurs by profession.
"""

import numpy as np
import pandas as pd
import swisseph as swe
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, silhouette_score
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Constants
OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path(None)

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
PLANET_LIST = list(PLANETS.keys())

def get_cosine_features(date_str, time_str, sidereal_mode=False):
    # Parse date
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except:
        try:
             dt = datetime.strptime(date_str, "%Y-%m-%d")
             if time_str == "12:00":
                 dt = dt.replace(hour=12)
        except:
             return None

    # Calculate JD
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0)
    
    # Set Zodiac Mode
    if sidereal_mode:
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
        flags = swe.FLG_SIDEREAL
    else:
        flags = 0
        
    # Get Positions in Radians
    positions = []
    for name in PLANET_LIST:
        pid = PLANETS[name]
        deg = swe.calc_ut(jd, pid, flags)[0][0]
        positions.append(np.deg2rad(deg))
        
    # Calculate 66 Pairwise Cosines
    features = []
    # Loop i from 0 to 11
    # Loop j from i+1 to 11
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            # Angle difference
            diff = positions[i] - positions[j]
            # Cosine
            features.append(np.cos(diff))
            
    return features

def run_analysis(data, mode_name, sidereal_mode):
    print(f"\n--- Running Cosine Analysis: {mode_name} ---")
    
    X = []
    y = []
    names = []
    
    for entry in data:
        # (Name, Date, Time, Profession)
        name, date, time, prof = entry
        features = get_cosine_features(date, time, sidereal_mode)
        if features:
            X.append(features)
            y.append(prof)
            names.append(name)
            
    X = np.array(X)
    y = np.array(y)
    
    print(f"Feature Vector Shape: {X.shape}") 
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # PCA for Viz
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    # Clustering (K-Means)
    n_clusters = len(np.unique(y))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    y_pred = kmeans.fit_predict(X_scaled)
    
    # Metrics
    ari = adjusted_rand_score(y, y_pred)
    sil = silhouette_score(X_scaled, y_pred)
    
    print(f"Stats for {mode_name}:")
    print(f"  Adjusted Rand Index (ARI): {ari:.4f}")
    print(f"  Silhouette Score: {sil:.4f}")
    print(f"  Explained Variance (PCA 2D): {np.sum(pca.explained_variance_ratio_):.2f}")
    
    return X_pca, y, ari, sil

def main():
    # Import Data dynamically from the original analysis file to keep data consistent
    try:
        from analysis import PROFESSIONALS
    except ImportError:
        # Fallback or path manipulation if needed
        sys.path.append(str(OUTPUT_DIR))
        from analysis import PROFESSIONALS

    print(f"Loaded {len(PROFESSIONALS)} professionals.")
    
    # 1. Tropical Cosines
    pca_trop, y_trop, ari_trop, sil_trop = run_analysis(PROFESSIONALS, "Tropical", False)
    
    # 2. Vedic Cosines
    # Theoretically, Cos(A-B) is invariant to rotation, so these should be identical
    # unless there is some subtle difference in calculation flags or Ayanamsa effects on specific bodies?
    # Let's verify.
    pca_vedic, y_vedic, ari_vedic, sil_vedic = run_analysis(PROFESSIONALS, "Vedic (Sidereal)", True)
    
    # Visualization Comparison
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    unique_profs = np.unique(y_trop)
    
    # Plot Tropical
    for prof in unique_profs:
        mask = (y_trop == prof)
        axes[0].scatter(pca_trop[mask, 0], pca_trop[mask, 1], label=prof, alpha=0.6, s=15)
    axes[0].set_title(f"Tropical Cosines\nARI={ari_trop:.4f}")
    axes[0].legend()
    
    # Plot Vedic
    for prof in unique_profs:
        mask = (y_vedic == prof)
        axes[1].scatter(pca_vedic[mask, 0], pca_vedic[mask, 1], label=prof, alpha=0.6, s=15)
    axes[1].set_title(f"Vedic Cosines\nARI={ari_vedic:.4f}")
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'clustering_cosine_comparison.png')
    
    # Report
    with open(OUTPUT_DIR / 'RESULTS_COSINE_CLUSTERING.md', 'w') as f:
        f.write("# Project 35: Unsupervised Clustering (Cosine Interactions)\n")
        f.write("## Methodology\n")
        f.write("- **Features**: 66 Pairwise Cosines (Sun-Moon, Sun-Mercury... Node-Lilith).\n")
        f.write("- **Logic**: Are professionals grouped by their 'Aspect Structure' geometry?\n")
        f.write("- **Algorithm**: K-Means Clustering (K=Number of Professions).\n")
        f.write(f"- **Sample**: {len(PROFESSIONALS)} Individuals.\n\n")
        
        f.write("## Results\n")
        f.write("| System | Adjusted Rand Index (ARI) | Silhouette Score | Interpretation |\n")
        f.write("|---|---|---|---|\n")
        f.write(f"| Tropical | {ari_trop:.4f} | {sil_trop:.4f} | {'Null Result' if ari_trop < 0.05 else 'Structure Found'} |\n")
        f.write(f"| Vedic | {ari_vedic:.4f} | {sil_vedic:.4f} | {'Null Result' if ari_vedic < 0.05 else 'Structure Found'} |\n")
        
        f.write("\n## Conclusion\n")
        if ari_trop < 0.05 :
             f.write("Switching to 'Cosine Interactions' (Aspects) did **not** uncover hidden professional clusters. The ARI remains near zero. The data suggests that while specific aspects might be statistically more frequent in certain groups (as seen in Project 34), these signals are not strong enough to force charts into clearly defined professional clusters in high-dimensional space.")
        else:
             f.write("Using interaction terms improved the clustering significantly!")

if __name__ == "__main__":
    main()

