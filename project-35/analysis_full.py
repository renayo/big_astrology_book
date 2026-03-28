#!/usr/bin/env python3
"""
Project 35: Unsupervised Clustering with ALL 12 Features
--------------------------------------------------------
Objectives:
1. Use ALL 12 celestial features (Sun, Moon, Mercury, Venus, Mars, 
   Jupiter, Saturn, Uranus, Neptune, Pluto, Node, Lilith).
2. Run PCA and Clustering (K-Means) separately for:
   a. Tropical Zodiac
   b. Vedic (Sidereal/Lahiri) Zodiac
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

# Import the massive list from the original file if possible, or define a loader
# Ideally we import from the existing analysis.py to avoid duplication
# But analysis.py has the data embedded. I will try to import it.

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path(None)

# 12 Features
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
    'Lilith': swe.MEAN_APOG # Mean Lilith based on previous correction
}

def get_positions(date_str, time_str, sidereal_mode=False):
    # Parse date
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except:
        try:
             # Fallback to noon if time is 12:00 or missing specific format
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
        
    positions = []
    for name, pid in PLANETS.items():
        pos = swe.calc_ut(jd, pid, flags)[0][0]
        # We use Cos/Sin components to handle circularity (0=360)
        # 12 bodies * 2 dimensions = 24 input features
        rad = np.deg2rad(pos)
        positions.append(np.sin(rad))
        positions.append(np.cos(rad))
        
    return positions

def run_analysis(data, mode_name, sidereal_mode):
    print(f"\n--- Running Analysis: {mode_name} ---")
    
    X = []
    y = []
    names = []
    
    for entry in data:
        # (Name, Date, Time, Profession)
        name, date, time, prof = entry
        features = get_positions(date, time, sidereal_mode)
        if features:
            X.append(features)
            y.append(prof)
            names.append(name)
            
    X = np.array(X)
    y = np.array(y)
    
    # Standardize?
    # Sin/Cos are already -1 to 1. Standardization is not strictly necessary but good practice.
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # PCA for Viz
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    # Clustering
    # We know the true labels, so let's see if K-Means matches them.
    n_clusters = len(np.unique(y))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    y_pred = kmeans.fit_predict(X_scaled)
    
    # Metrics
    ari = adjusted_rand_score(y, y_pred)
    sil = silhouette_score(X_scaled, y_pred)
    
    print(f"Stats for {mode_name}:")
    print(f"  Adjusted Rand Index (Alignment with Professions): {ari:.4f}")
    print(f"  Silhouette Score (Cluster Distinctness): {sil:.4f}")
    print(f"  Explained Variance (PCA 2D): {np.sum(pca.explained_variance_ratio_):.2f}")
    
    return X_pca, y, ari, sil

def main():
    # Import Data dynamically
    try:
        from analysis import PROFESSIONALS
    except ImportError:
        print("Could not import PROFESSIONALS from analysis.py")
        return

    print(f"Loaded {len(PROFESSIONALS)} professionals.")
    
    # 1. Tropical
    pca_trop, y_trop, ari_trop, sil_trop = run_analysis(PROFESSIONALS, "Tropical", False)
    
    # 2. Vedic
    pca_vedic, y_vedic, ari_vedic, sil_vedic = run_analysis(PROFESSIONALS, "Vedic (Sidereal)", True)
    
    # Visualization Comparison
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    unique_profs = np.unique(y_trop)
    colors = plt.cm.tab10(np.linspace(0, 1, len(unique_profs)))
    color_map = dict(zip(unique_profs, colors))
    
    # Plot Tropical
    for prof in unique_profs:
        mask = (y_trop == prof)
        axes[0].scatter(pca_trop[mask, 0], pca_trop[mask, 1], label=prof, alpha=0.6, s=15)
    axes[0].set_title(f"Tropical Clustering\nARI={ari_trop:.4f}")
    axes[0].legend()
    
    # Plot Vedic
    for prof in unique_profs:
        mask = (y_vedic == prof)
        axes[1].scatter(pca_vedic[mask, 0], pca_vedic[mask, 1], label=prof, alpha=0.6, s=15)
    axes[1].set_title(f"Vedic Clustering\nARI={ari_vedic:.4f}")
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'clustering_comparison_12features.png')
    
    # Report
    with open(OUTPUT_DIR / 'RESULTS_12FEATURES.md', 'w') as f:
        f.write("# Project 35: Unsupervised Clustering (12 Features)\n")
        f.write("## Methodology\n")
        f.write("- **Features**: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Node, Lilith.\n")
        f.write("- **Encoding**: Sin/Cos of Longitude (24 dimensions).\n")
        f.write("- **Algorithm**: K-Means Clustering (K=Number of Professions).\n")
        f.write(f"- **Sample**: {len(PROFESSIONALS)} Individuals.\n\n")
        
        f.write("## Results\n")
        f.write("| System | Adjusted Rand Index (ARI) | Silhouette Score | Interpretation |\n")
        f.write("|---|---|---|---|\n")
        f.write(f"| Tropical | {ari_trop:.4f} | {sil_trop:.4f} | {'Random Noise' if ari_trop < 0.05 else 'Structure Found'} |\n")
        f.write(f"| Vedic | {ari_vedic:.4f} | {sil_vedic:.4f} | {'Random Noise' if ari_vedic < 0.05 else 'Structure Found'} |\n")
        
        f.write("\n## Conclusion\n")
        if ari_trop < 0.05 and ari_vedic < 0.05:
            f.write("Both systems produced an ARI near 0, indicating that unsupervised machine learning on planetary positions **cannot distinguish professions**. The clusters formed by the algorithm have essentially zero overlap with the actual professional labels.")
        else:
             f.write("Some structure was found.")

if __name__ == "__main__":
    main()

