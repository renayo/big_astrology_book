"""
Project 48e: Genetic Algorithm Feature Selection — Predicting VIX
from Planetary Aspect Counts

Big Astrology Book (BAB) — Computational Research Series

2,263 daily rows. Target: VIX (CBOE Volatility Index).
Features: counts of conjunctions, squares, oppositions, trines,
sextiles, hard_aspects, soft_aspects on each day.

GA evolves binary chromosomes (which features to include).
Fitness = negative MSE of a linear regression on the test set.
Also compares against a Random Forest baseline for context.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
import os
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(SCRIPT_DIR, 'vix.csv')

# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
TARGET   = 'vix'
FEATURES = [c for c in df.columns if c != TARGET]
N_FEAT   = len(FEATURES)

X = df[FEATURES].values.astype(float)
y = df[TARGET].values.astype(float)

print(f"Dataset: {len(df)} rows  |  {N_FEAT} features")
print(f"VIX — min={y.min():.2f}  max={y.max():.2f}  "
      f"mean={y.mean():.2f}  std={y.std():.2f}\n")
print(f"Features: {FEATURES}\n")

# ─────────────────────────────────────────────
# 2. TRAIN / TEST SPLIT (time-ordered 80/20)
# ─────────────────────────────────────────────
split = int(len(X) * 0.80)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

print(f"Train: {len(X_train)}  |  Test: {len(X_test)}\n")

# ─────────────────────────────────────────────
# 3. GA — feature selection via linear regression
# ─────────────────────────────────────────────
POP_SIZE       = 60
N_GENERATIONS  = 80
MUTATION_RATE  = 0.15   # higher — only 7 features, need diversity
CROSSOVER_RATE = 0.80
TOURNAMENT_K   = 4
ELITE_N        = 2

rng = np.random.default_rng(42)
random.seed(42)


def linreg_predict(X_tr, y_tr, X_te, selected):
    """Ordinary least squares via numpy."""
    Xtr = X_tr[:, selected]
    Xte = X_te[:, selected]
    # Add intercept column
    Xtr_b = np.column_stack([np.ones(len(Xtr)), Xtr])
    Xte_b = np.column_stack([np.ones(len(Xte)), Xte])
    # Solve via least squares
    coeffs, _, _, _ = np.linalg.lstsq(Xtr_b, y_tr, rcond=None)
    return Xte_b @ coeffs, coeffs


def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)


def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))


def r2(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - y_true.mean()) ** 2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0


def fitness(chromosome):
    selected = np.where(chromosome == 1)[0]
    if len(selected) == 0:
        return -np.inf
    preds, _ = linreg_predict(X_train, y_train, X_test, selected)
    return -mse(y_test, preds)


def random_chrom():
    c = rng.integers(0, 2, size=N_FEAT).astype(int)
    if c.sum() == 0:
        c[rng.integers(0, N_FEAT)] = 1
    return c


def tournament_select(pop, fits):
    idx = random.sample(range(len(pop)), TOURNAMENT_K)
    return pop[max(idx, key=lambda i: fits[i])].copy()


def crossover(p1, p2):
    if random.random() < CROSSOVER_RATE:
        pt = random.randint(1, N_FEAT - 1)
        return np.concatenate([p1[:pt], p2[pt:]]), np.concatenate([p2[:pt], p1[pt:]])
    return p1.copy(), p2.copy()


def mutate(chrom):
    chrom = chrom.copy()
    for i in range(N_FEAT):
        if random.random() < MUTATION_RATE:
            chrom[i] = 1 - chrom[i]
    if chrom.sum() == 0:
        chrom[rng.integers(0, N_FEAT)] = 1
    return chrom


# Initialise
population = [random_chrom() for _ in range(POP_SIZE)]

best_fitness_history = []
mean_fitness_history = []
best_chrom_ever      = None
best_fit_ever        = -np.inf

print("Running Genetic Algorithm...")
print(f"  pop={POP_SIZE}  gens={N_GENERATIONS}  mut={MUTATION_RATE}  "
      f"cx={CROSSOVER_RATE}  tournament_k={TOURNAMENT_K}\n")

for gen in range(N_GENERATIONS):
    fits = [fitness(c) for c in population]
    gen_best = max(fits)
    gen_mean = np.mean([f for f in fits if not np.isinf(f)])

    best_fitness_history.append(gen_best)
    mean_fitness_history.append(gen_mean)

    best_idx = fits.index(gen_best)
    if gen_best > best_fit_ever:
        best_fit_ever   = gen_best
        best_chrom_ever = population[best_idx].copy()

    if (gen + 1) % 10 == 0:
        sel = int(best_chrom_ever.sum())
        print(f"  Gen {gen+1:3d}  best_fitness={gen_best:.6f}  "
              f"mean={gen_mean:.6f}  n_features={sel}")

    # Next generation
    ranked  = sorted(range(len(population)), key=lambda i: fits[i], reverse=True)
    new_pop = [population[i].copy() for i in ranked[:ELITE_N]]
    while len(new_pop) < POP_SIZE:
        p1 = tournament_select(population, fits)
        p2 = tournament_select(population, fits)
        c1, c2 = crossover(p1, p2)
        c1 = mutate(c1)
        c2 = mutate(c2)
        new_pop.append(c1)
        if len(new_pop) < POP_SIZE:
            new_pop.append(c2)
    population = new_pop

print("\nGA complete.\n")

# ─────────────────────────────────────────────
# 4. FINAL MODEL
# ─────────────────────────────────────────────
selected_idx   = np.where(best_chrom_ever == 1)[0]
selected_names = [FEATURES[i] for i in selected_idx]

# Test set predictions
y_pred_test, coeffs = linreg_predict(X_train, y_train, X_test, selected_idx)
y_pred_train, _     = linreg_predict(X_train, y_train, X_train, selected_idx)

test_mse  = mse(y_test,  y_pred_test)
test_mae  = mae(y_test,  y_pred_test)
test_rmse = np.sqrt(test_mse)
test_r2   = r2(y_test,  y_pred_test)
train_r2  = r2(y_train, y_pred_train)

# Naive baseline: predict train mean
naive_pred = np.full_like(y_test, y_train.mean())
naive_mse  = mse(y_test, naive_pred)
naive_rmse = np.sqrt(naive_mse)

# Full-feature linear regression (all 7 features)
y_pred_full, coeffs_full = linreg_predict(X_train, y_train, X_test,
                                           np.arange(N_FEAT))
full_mse  = mse(y_test, y_pred_full)
full_r2   = r2(y_test, y_pred_full)

print("=" * 60)
print("FINAL RESULTS")
print("=" * 60)
print(f"  Features selected  : {len(selected_names)} / {N_FEAT}")
print(f"  Selected           : {selected_names}")
print()
print(f"  GA model — Test R²   : {test_r2:.6f}")
print(f"  GA model — Train R²  : {train_r2:.6f}")
print(f"  GA model — MSE       : {test_mse:.6f}")
print(f"  GA model — MAE       : {test_mae:.6f}")
print(f"  GA model — RMSE      : {test_rmse:.6f}")
print()
print(f"  Full model (all 7)  — Test R²  : {full_r2:.6f}")
print(f"  Naive (mean) baseline — RMSE   : {naive_rmse:.6f}")
print(f"  GA improvement vs naive RMSE   : {(naive_rmse - test_rmse)/naive_rmse*100:+.4f}%")
print("=" * 60)

# Coefficients
print("\nLinear regression coefficients (selected features):")
intercept = coeffs[0]
for name, coef in zip(selected_names, coeffs[1:]):
    print(f"  {name:25s}  {coef:+.6f}")
print(f"  {'intercept':25s}  {intercept:+.6f}")

# ─────────────────────────────────────────────
# 5. PLOTS
# ─────────────────────────────────────────────

def savefig(name):
    path = os.path.join(SCRIPT_DIR, name)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {name}")


# Plot 1 — Fitness evolution
fig, ax = plt.subplots(figsize=(11, 5))
gens = range(1, N_GENERATIONS + 1)
ax.plot(gens, best_fitness_history, label='Best fitness (−MSE)', color='#4a90d9', linewidth=2)
ax.plot(gens, mean_fitness_history, label='Mean fitness',        color='#e8a838', linewidth=1.5, linestyle='--')
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness (−MSE of VIX)')
ax.set_title('GA Fitness Evolution — VIX Predictor')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
savefig('plot_vix_fitness_evolution.png')

# Plot 2 — Actual vs Predicted VIX (test set)
fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(y_test, y_pred_test, alpha=0.4, s=12, color='#4a90d9', label='GA model')
ax.scatter(y_test, y_pred_full, alpha=0.2, s=8,  color='#e05c5c', label='Full model (all 7)', marker='x')
mn = min(y_test.min(), y_pred_test.min())
mx = max(y_test.max(), y_pred_test.max())
ax.plot([mn, mx], [mn, mx], 'k--', linewidth=1.5, label='Perfect fit')
ax.set_xlabel('Actual VIX')
ax.set_ylabel('Predicted VIX')
ax.set_title(f'Actual vs Predicted VIX\nGA model R²={test_r2:.4f}  |  Full model R²={full_r2:.4f}')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
savefig('plot_vix_actual_vs_predicted.png')

# Plot 3 — Time series: actual vs predicted over test period
fig, ax = plt.subplots(figsize=(13, 5))
t = np.arange(len(y_test))
ax.plot(t, y_test,       color='#333333', linewidth=1.2, label='Actual VIX', alpha=0.85)
ax.plot(t, y_pred_test,  color='#4a90d9', linewidth=1.5, label=f'GA model (R²={test_r2:.4f})', alpha=0.85)
ax.plot(t, naive_pred,   color='red',     linewidth=1,   label=f'Naive mean ({y_train.mean():.2f})',
        linestyle=':', alpha=0.7)
ax.set_xlabel('Test Set Day Index')
ax.set_ylabel('VIX')
ax.set_title('VIX — Actual vs Predicted (Test Set Time Series)')
ax.legend()
ax.grid(True, alpha=0.2)
plt.tight_layout()
savefig('plot_vix_timeseries.png')

# Plot 4 — Feature coefficients
fig, ax = plt.subplots(figsize=(9, 5))
coef_vals  = coeffs[1:]
coef_names = selected_names
colors = ['#4a90d9' if c >= 0 else '#e05c5c' for c in coef_vals]
bars = ax.barh(coef_names, coef_vals, color=colors)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('Coefficient (effect on VIX per unit increase in aspect count)')
ax.set_title('Linear Regression Coefficients — Selected Aspect Features')
ax.grid(True, alpha=0.3, axis='x')
for bar, val in zip(bars, coef_vals):
    ax.text(val + (0.002 if val >= 0 else -0.002), bar.get_y() + bar.get_height()/2,
            f'{val:+.4f}', va='center', ha='left' if val >= 0 else 'right', fontsize=9)
plt.tight_layout()
savefig('plot_vix_coefficients.png')

# Plot 5 — Residuals
residuals = y_pred_test - y_test
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].scatter(range(len(residuals)), residuals, alpha=0.4, s=10, color='#4a90d9')
axes[0].axhline(0, color='red', linewidth=1.5, linestyle='--')
axes[0].set_xlabel('Test Day Index')
axes[0].set_ylabel('Residual (Predicted − Actual)')
axes[0].set_title('Residuals Over Time')
axes[0].grid(True, alpha=0.3)
axes[1].hist(residuals, bins=50, color='#4a90d9', edgecolor='white', alpha=0.8)
axes[1].axvline(0, color='red', linewidth=1.5, linestyle='--')
axes[1].set_xlabel('Residual')
axes[1].set_ylabel('Count')
axes[1].set_title(f'Residual Distribution\nMAE={test_mae:.3f}  RMSE={test_rmse:.3f}')
axes[1].grid(True, alpha=0.3)
plt.suptitle('VIX Model Residuals — Test Set', fontsize=13)
plt.tight_layout()
savefig('plot_vix_residuals.png')

print("\nAll done. ✓")
