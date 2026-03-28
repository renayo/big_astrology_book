#!/usr/bin/env python3
"""
Project 44: ML Chart Rectification
===================================
Uses ML to test if life events can predict birth time (Ascendant).
Now updated to use the 'Expanded' dataset with 144 Geometric Cosine Features.

DATA SOURCES:
- rectification_dataset_expanded.csv (5000 individuals, 83k events)

METHODOLOGY:
1. Load expanded dataset with pre-calculated cosine differences.
   (Features = cos(Transit_Planet - Natal_Noon_Planet))
2. Train Random Forest to predict 'birth_hour_true'.
3. Evaluate MAE vs Baseline.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import mean_absolute_error
from pathlib import Path

# Paths
OUTPUT_DIR = Path(__file__).parent

def load_dataset():
    """Load from CSV or fallback."""
    # Prioritize the expanded dataset
    csv_path = OUTPUT_DIR / 'rectification_dataset_expanded.csv'
    
    if csv_path.exists():
        print(f"Loading expanded synthetic dataset from {csv_path}...")
        df = pd.read_csv(csv_path)
        return df
    
    # Fallback to older generation logic (deprecated)
    csv_path = OUTPUT_DIR / 'rectification_data.csv'
    if csv_path.exists():
        print(f"Loading basic synthetic dataset from {csv_path}...")
        return pd.read_csv(csv_path) 
        
    print("Warning: CSV not found.")
    return None

def main():
    print("=" * 60)
    print("PROJECT 44: ML CHART RECTIFICATION (GEOMETRIC FEATURES)")
    print("=" * 60)
    
    # 1. Load Data
    df = load_dataset()
    if df is None: return
    
    print(f"Loaded {len(df)} event samples.")
    
    # Check if this is the expanded dataset (contains 'cos_' cols)
    is_expanded = 'cos_Sun_nSun' in df.columns
    
    if is_expanded:
        print("Detected expanded feature set (Celestial Pairs).")
        # All columns starting with 'cos_' are features
        feature_cols = [c for c in df.columns if c.startswith('cos_')]
        
        # We also need simple event type encoding
        if 'event_type' in df.columns:
            dummies = pd.get_dummies(df['event_type'], prefix='evt')
            df = pd.concat([df, dummies], axis=1)
            feature_cols_extra = [c for c in dummies.columns] + ['age_at_event']
        else:
            feature_cols_extra = ['age_at_event']

        X_cols = feature_cols + feature_cols_extra
        
        # Target
        y = df['birth_hour_true']
        X = df[X_cols]
        
    else:
        print("Error: Dataset format not recognized as 'Expanded'. Please run generate_data.py first.")
        return

    print(f"\nTraining Random Forest on {len(X)} samples with {len(X_cols)} features...")
    
    # Use fewer trees if dataset is huge to save time, or use n_jobs
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1, max_depth=20)
    
    # Split for holdout test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Fitting model...")
    model.fit(X_train, y_train)
    
    print("Evaluating...")
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    
    print(f"Mean Absolute Error (Birth Time): {mae:.2f} hours")
    
    dummy_mae = np.mean(np.abs(y_test - y_train.mean()))
    print(f"Baseline MAE (Mean Guess): {dummy_mae:.2f} hours")
    
    improvement = dummy_mae - mae
    print(f"Improvement: {improvement:.2f} hours (+{(improvement/dummy_mae)*100:.1f}%)")
    
    # 4. Feature Importance
    importances = model.feature_importances_
    
    print("\nTop 10 Predictors:")
    indices = np.argsort(importances)[::-1]
    for i in range(10):
        if i < len(indices):
            print(f"  {X_cols[indices[i]]}: {importances[indices[i]]:.4f}")
            
    # 5. Visualization
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    ax1 = axes[0]
    # Downsample for scatter plot if too big
    if len(y_test) > 2000:
        idx_plot = np.random.choice(len(y_test), size=2000, replace=False)
        y_plot = y_test.iloc[idx_plot]
        pred_plot = predictions[idx_plot]
    else:
        y_plot = y_test
        pred_plot = predictions
        
    ax1.scatter(y_plot, pred_plot, alpha=0.3, s=10, color='purple')
    ax1.plot([0, 24], [0, 24], 'r--', lw=2)
    ax1.set_xlabel('True Birth Hour')
    ax1.set_ylabel('Predicted Birth Hour')
    ax1.set_title(f'ML Rectification Performance (MAE={mae:.2f}h)')
    ax1.grid(True, alpha=0.3)
    
    ax2 = axes[1]
    # Plot top 15 features
    top_n = 15
    top_indices = indices[:top_n]
    ax2.barh([X_cols[i] for i in top_indices][::-1], importances[top_indices][::-1], color='teal')
    ax2.set_xlabel('Relative Importance')
    ax2.set_title('Top Features for Rectification')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'rectification_analysis.png')
    print(f"Saved plot to {OUTPUT_DIR / 'rectification_analysis.png'}")
    
    results_df = pd.DataFrame({
        'Metric': ['MAE', 'Baseline', 'Improvement_Pct'],
        'Value': [mae, dummy_mae, (improvement/dummy_mae)*100]
    })
    results_df.to_csv(OUTPUT_DIR / 'analysis_results.csv', index=False)

if __name__ == "__main__":
    main()

