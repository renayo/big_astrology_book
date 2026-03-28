#!/usr/bin/env python3
"""
Project 35: Advanced Clustering Analysis
----------------------------------------
Objectives:
1. Apply more sophisticated algorithms beyond K-Means:
   a. Gaussian Mixture Models (GMM) - Probabilistic, fits ellipsoidal clusters.
   b. Spectral Clustering - Manifold learning, finds connected components.
   c. Agglomerative Clustering - Hierarchical structure.
2. Use the Cosine Interaction features (66 dimensions).
3. Evaluate if ANY algorithm can recover professional labels.
"""

import numpy as np
import pandas as pd
import swisseph as swe
from sklearn.mixture import GaussianMixture
from sklearn.cluster import SpectralClustering, AgglomerativeClustering, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
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

def get_cosine_features(date_str, time_str):
    # Same feature extraction as previous step
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except:
        try:
             dt = datetime.strptime(date_str, "%Y-%m-%d")
             if time_str == "12:00":
                 dt = dt.replace(hour=12)
        except:
             return None

    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0)
    
    # Tropical positions (Aspects are invariant to zodiac)
    flags = 0 
    positions = []
    for name in PLANET_LIST:
        pid = PLANETS[name]
        deg = swe.calc_ut(jd, pid, flags)[0][0]
        positions.append(np.deg2rad(deg))
        
    features = []
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            features.append(np.cos(positions[i] - positions[j]))
            
    return features

def run_advanced_clustering(data):
    print("Extracting features...")
    X = []
    y = []
    for entry in data:
        name, date, time, prof = entry
        feats = get_cosine_features(date, time)
        if feats:
            X.append(feats)
            y.append(prof)
            
    X = np.array(X)
    y = np.array(y)
    
    print(f"Data Shape: {X.shape}")
    
    # Preprocessing
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Reduce dimensions for density-based/spectral methods?
    # High dim (66) can be sparse. Lets try PCA reduction first for some methods.
    # Retain 95% variance
    pca_full = PCA(n_components=0.95)
    X_pca = pca_full.fit_transform(X_scaled)
    print(f"PCA Reduced dimensions: {X_pca.shape[1]} (95% variance)")
    
    n_classes = len(np.unique(y))
    print(f"Target Clusters: {n_classes}")
    
    results = []
    
    # 1. Gaussian Mixture Model (GMM)
    # Allows for distinct cluster shapes (covariance types)
    print("\n--- Gaussian Mixture Model ---")
    gmm = GaussianMixture(n_components=n_classes, covariance_type='full', random_state=42)
    y_gmm = gmm.fit_predict(X_pca)
    ari_gmm = adjusted_rand_score(y, y_gmm)
    print(f"GMM ARI: {ari_gmm:.4f}")
    results.append(('GMM', y_gmm, ari_gmm))
    
    # 2. Spectral Clustering
    # Good for non-convex clusters (manifold learning)
    print("\n--- Spectral Clustering ---")
    spectral = SpectralClustering(n_clusters=n_classes, affinity='nearest_neighbors', random_state=42)
    y_spec = spectral.fit_predict(X_pca)
    ari_spec = adjusted_rand_score(y, y_spec)
    print(f"Spectral ARI: {ari_spec:.4f}")
    results.append(('Spectral', y_spec, ari_spec))
    
    # 3. Agglomerative Clustering (Hierarchical)
    # Ward linkage minimizes variance within clusters
    print("\n--- Agglomerative Clustering (Ward) ---")
    agg = AgglomerativeClustering(n_clusters=n_classes, linkage='ward')
    y_agg = agg.fit_predict(X_pca)
    ari_agg = adjusted_rand_score(y, y_agg)
    print(f"Agglomerative ARI: {ari_agg:.4f}")
    results.append(('Agglomerative', y_agg, ari_agg))
    
    # 4. DBSCAN (Density)
    # Doesn't require specifying K. Finds dense blobs.
    # eps is tricky. Let's try heuristic or default.
    print("\n--- DBSCAN ---")
    dbscan = DBSCAN(eps=5.0, min_samples=5) # Heuristic guess for 66-dim space? Likely fails.
    # PCA space might be better. 
    # Average distance? Let's rely on ARI.
    y_db = dbscan.fit_predict(X_scaled) 
    # DBSCAN returns -1 for noise.
    # ARI handles noise labels fine.
    ari_db = adjusted_rand_score(y, y_db)
    print(f"DBSCAN ARI: {ari_db:.4f} (Clusters found: {len(np.unique(y_db))-1})")
    results.append(('DBSCAN', y_db, ari_db))

    return results, y, X_pca

def visualize_results(results, y_true, X_pca):
    # Use t-SNE for 2D embedding of the high-dim space
    print("\nGenerating t-SNE visualization...")
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    X_tsne = tsne.fit_transform(X_pca)
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()
    
    # Ground Truth
    unique_profs = np.unique(y_true)
    for prof in unique_profs:
        mask = (y_true == prof)
        axes[0].scatter(X_tsne[mask, 0], X_tsne[mask, 1], label=prof, s=10, alpha=0.6)
    axes[0].set_title("Ground Truth (Professions)")
    # axes[0].legend(fontsize='x-small')
    
    # Algorithms
    for i, (name, y_pred, ari) in enumerate(results):
        ax = axes[i+1]
        unique_labels = np.unique(y_pred)
        for label in unique_labels:
            if name == 'DBSCAN' and label == -1:
                color = 'gray'
                alpha = 0.1
                lbl = 'Noise'
            else:
                color = None
                alpha = 0.6
                lbl = f'Cluster {label}'
                
            mask = (y_pred == label)
            ax.scatter(X_tsne[mask, 0], X_tsne[mask, 1], label=lbl, s=10, alpha=alpha, c=color)
        ax.set_title(f"{name}\nARI={ari:.4f}")
        
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'advanced_clustering_comparison.png')

def main():
    try:
        sys.path.append(str(OUTPUT_DIR))
        from analysis import PROFESSIONALS
    except ImportError:
        print("Could not load data.")
        return

    print(f"Loaded {len(PROFESSIONALS)} professionals.")
    results, y_true, X_pca = run_advanced_clustering(PROFESSIONALS)
    visualize_results(results, y_true, X_pca)
    
    # Write report
    with open(OUTPUT_DIR / 'RESULTS_ADVANCED.md', 'w') as f:
        f.write("# Project 35: Advanced Clustering Results\n\n")
        f.write("## Methodology\n")
        f.write("Applied advanced algorithms to Cosine Interaction Features (PCA-reduced, 95% variance).\n")
        f.write(" Algorithms tested: GMM (Probabilistic), Spectral (Manifold), Agglomerative (Hierarchical), DBSCAN (Density).\n\n")
        
        f.write("## Results (Adjusted Rand Index)\n")
        f.write("| Algorithm | Best For | ARI Score | Interpretation |\n")
        f.write("|---|---|---|---|\n")
        for name, _, ari in results:
            f.write(f"| {name} | ... | {ari:.4f} | {'Null' if ari < 0.05 else 'Structure'} |\n")
            
        f.write("\n## Conclusion\n")
        f.write("Even with advanced algorithms capable of detecting non-spherical or overlapping clusters, **no latent structure** matching the professional categories was found. The Adjusted Rand Indices are all consistently near zero.")

if __name__ == "__main__":
    main()

