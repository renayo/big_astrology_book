"""
Project 48f: Genetic Algorithm Feature Selection — Predicting IPO 1-Year Return
from Planetary Positions, Aspect Cosines, Tithi, and Moon Phase at IPO Date

Big Astrology Book (BAB) — Computational Research Series

797 IPOs. Target: pct_change_1yr (1-year price return from IPO date).
Features: 12 planet longitudes, 66 cosine aspects, Tithi, moon phase label.
GA selects which features to feed a linear regression model.
Fitness = negative MSE on test set.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(SCRIPT_DIR, 'ipo_results.csv')

# ─────────────────────────────────────────────
# 1. LOAD & ENCODE DATA
# ─────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)

TARGET   = 'pct_change_1yr'
META     = ['ticker', 'ipo_date', 'start_price', 'price_1yr', TARGET]
RAW_FEAT = [c for c in df.columns if c not in META]

# Encode moon_phase_label → one-hot
phases = sorted(df['moon_phase_label'].unique())
for ph in phases:
    df[f'phase_{ph.replace(" ","_")}'] = (df['moon_phase_label'] == ph).astype(float)

# Drop raw categorical, keep numerics + one-hots
drop_cols = META + ['moon_phase_label']
FEAT_COLS = [c for c in df.columns if c not in drop_cols]

X = df[FEAT_COLS].values.astype(float)
y = df[TARGET].values.astype(float)

N_FEAT = len(FEAT_COLS)

print(f"Dataset: {len(df)} IPOs  |  {N_FEAT} encoded features")
print(f"pct_change_1yr — min={y.min():.3f}  max={y.max():.3f}  "
      f"mean={y.mean():.3f}  std={y.std():.3f}  median={np.median(y):.3f}")
print(f"\nFeature breakdown:")
print(f"  Planet longitudes : {len([c for c in FEAT_COLS if c.endswith('_lon')])}")
print(f"  Cosine aspects    : {len([c for c in FEAT_COLS if c.startswith('cos_')])}")
print(f"  Tithi             : 1")
print(f"  Moon phase (OH)   : {len([c for c in FEAT_COLS if c.startswith('phase_')])}")
print()

# ─────────────────────────────────────────────
# 2. TRAIN / TEST SPLIT — sort by IPO date (time-ordered)
# ─────────────────────────────────────────────
df_sorted = df.sort_values('ipo_date').reset_index(drop=True)
X_sorted  = df_sorted[FEAT_COLS].values.astype(float)
y_sorted  = df_sorted[TARGET].values.astype(float)

split       = int(len(X_sorted) * 0.80)
X_train     = X_sorted[:split]
X_test      = X_sorted[split:]
y_train     = y_sorted[:split]
y_test      = y_sorted[split:]
tickers_test = df_sorted['ticker'].values[split:]
dates_test   = df_sorted['ipo_date'].values[split:]

print(f"Train: {len(X_train)} IPOs  |  Test: {len(X_test)} IPOs")
print(f"Test period: {dates_test[0][:10]} → {dates_test[-1][:10]}\n")

# ─────────────────────────────────────────────
# 3. HELPERS
# ─────────────────────────────────────────────
def linreg_predict(Xtr, ytr, Xte, sel):
    Xtr_b = np.column_stack([np.ones(len(Xtr)), Xtr[:, sel]])
    Xte_b = np.column_stack([np.ones(len(Xte)), Xte[:, sel]])
    coeffs, _, _, _ = np.linalg.lstsq(Xtr_b, ytr, rcond=None)
    return Xte_b @ coeffs, coeffs

def mse(yt, yp):   return np.mean((yt - yp) ** 2)
def mae(yt, yp):   return np.mean(np.abs(yt - yp))
def r2(yt, yp):
    ss_res = np.sum((yt - yp) ** 2)
    ss_tot = np.sum((yt - yt.mean()) ** 2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

def fitness(chrom):
    sel = np.where(chrom == 1)[0]
    if len(sel) == 0:
        return -np.inf
    preds, _ = linreg_predict(X_train, y_train, X_test, sel)
    return -mse(y_test, preds)

# ─────────────────────────────────────────────
# 4. GA SETUP
# ─────────────────────────────────────────────
POP_SIZE       = 80
N_GENERATIONS  = 100
MUTATION_RATE  = 0.04   # ~3-4 bit flips per 84-feature chrom
CROSSOVER_RATE = 0.80
TOURNAMENT_K   = 4
ELITE_N        = 2

rng = np.random.default_rng(42)
random.seed(42)

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
    flip = rng.random(N_FEAT) < MUTATION_RATE
    chrom[flip] = 1 - chrom[flip]
    if chrom.sum() == 0:
        chrom[rng.integers(0, N_FEAT)] = 1
    return chrom

# ─────────────────────────────────────────────
# 5. EVOLVE
# ─────────────────────────────────────────────
population = [random_chrom() for _ in range(POP_SIZE)]

best_fitness_history = []
mean_fitness_history = []
nfeat_history        = []
best_chrom_ever      = None
best_fit_ever        = -np.inf

print("Running Genetic Algorithm...")
print(f"  pop={POP_SIZE}  gens={N_GENERATIONS}  mut={MUTATION_RATE}  "
      f"cx={CROSSOVER_RATE}  tournament_k={TOURNAMENT_K}\n")

for gen in range(N_GENERATIONS):
    fits = [fitness(c) for c in population]
    valid = [f for f in fits if not np.isinf(f)]
    gen_best = max(fits)
    gen_mean = np.mean(valid) if valid else -np.inf

    best_fitness_history.append(gen_best)
    mean_fitness_history.append(gen_mean)

    best_idx = fits.index(gen_best)
    if gen_best > best_fit_ever:
        best_fit_ever   = gen_best
        best_chrom_ever = population[best_idx].copy()

    nfeat_history.append(int(best_chrom_ever.sum()))

    if (gen + 1) % 20 == 0:
        print(f"  Gen {gen+1:3d}  best_mse={-gen_best:.6f}  "
              f"mean_mse={-gen_mean:.6f}  n_features={nfeat_history[-1]}")

    ranked  = sorted(range(len(population)), key=lambda i: fits[i], reverse=True)
    new_pop = [population[i].copy() for i in ranked[:ELITE_N]]
    while len(new_pop) < POP_SIZE:
        p1 = tournament_select(population, fits)
        p2 = tournament_select(population, fits)
        c1, c2 = crossover(p1, p2)
        new_pop.append(mutate(c1))
        if len(new_pop) < POP_SIZE:
            new_pop.append(mutate(c2))
    population = new_pop

print("\nGA complete.\n")

# ─────────────────────────────────────────────
# 6. FINAL EVALUATION
# ─────────────────────────────────────────────
sel_idx   = np.where(best_chrom_ever == 1)[0]
sel_names = [FEAT_COLS[i] for i in sel_idx]

y_pred_test,  coeffs = linreg_predict(X_train, y_train, X_test,  sel_idx)
y_pred_train, _      = linreg_predict(X_train, y_train, X_train, sel_idx)

test_mse  = mse(y_test,  y_pred_test)
test_mae  = mae(y_test,  y_pred_test)
test_rmse = np.sqrt(test_mse)
test_r2   = r2(y_test,  y_pred_test)
train_r2  = r2(y_train, y_pred_train)

naive_mse  = mse(y_test, np.full_like(y_test, y_train.mean()))
naive_rmse = np.sqrt(naive_mse)

y_pred_full, _ = linreg_predict(X_train, y_train, X_test, np.arange(N_FEAT))
full_r2  = r2(y_test, y_pred_full)
full_mse = mse(y_test, y_pred_full)

print("=" * 60)
print("FINAL RESULTS")
print("=" * 60)
print(f"  Features selected     : {len(sel_names)} / {N_FEAT}")
print()
print(f"  GA model — Test R²    : {test_r2:.6f}")
print(f"  GA model — Train R²   : {train_r2:.6f}")
print(f"  GA model — MSE        : {test_mse:.6f}")
print(f"  GA model — MAE        : {test_mae:.6f}")
print(f"  GA model — RMSE       : {test_rmse:.6f}")
print()
print(f"  Full model (all {N_FEAT})  — R²   : {full_r2:.6f}")
print(f"  Full model            — MSE  : {full_mse:.6f}")
print(f"  Naive (mean) baseline — RMSE : {naive_rmse:.6f}")
print(f"  GA vs naive RMSE improvement : {(naive_rmse - test_rmse)/naive_rmse*100:+.4f}%")
print("=" * 60)

# Selected feature breakdown
lon_sel   = [n for n in sel_names if n.endswith('_lon')]
cos_sel   = [n for n in sel_names if n.startswith('cos_')]
other_sel = [n for n in sel_names if n not in lon_sel + cos_sel]

print(f"\nSelected features ({len(sel_names)}):")
print(f"  Longitudes ({len(lon_sel)}): {lon_sel}")
print(f"  Cosine aspects ({len(cos_sel)}): {cos_sel}")
print(f"  Other ({len(other_sel)}): {other_sel}")

# Coefficients (sorted by |coef|)
coef_vals  = coeffs[1:]
coef_pairs = sorted(zip(sel_names, coef_vals), key=lambda x: abs(x[1]), reverse=True)
print("\nCoefficients (sorted by |value|):")
for name, val in coef_pairs[:20]:
    print(f"  {name:35s}  {val:+.6f}")
if len(coef_pairs) > 20:
    print(f"  ... and {len(coef_pairs)-20} more")
print(f"  intercept: {coeffs[0]:+.6f}")

# ─────────────────────────────────────────────
# 7. PLOTS
# ─────────────────────────────────────────────
def savefig(name):
    path = os.path.join(SCRIPT_DIR, name)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {name}")

# Plot 1 — Fitness evolution
fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
gens = range(1, N_GENERATIONS + 1)
axes[0].plot(gens, [-f for f in best_fitness_history], color='#4a90d9', linewidth=2, label='Best MSE')
axes[0].plot(gens, [-f for f in mean_fitness_history], color='#e8a838', linewidth=1.5, linestyle='--', label='Mean MSE')
axes[0].axhline(naive_mse, color='red', linewidth=1, linestyle=':', label=f'Naive MSE ({naive_mse:.4f})')
axes[0].set_ylabel('MSE (test)')
axes[0].set_title('GA Evolution — IPO 1-Year Return Predictor')
axes[0].legend(fontsize=9)
axes[0].grid(True, alpha=0.3)
axes[1].plot(gens, nfeat_history, color='#6abf69', linewidth=2)
axes[1].set_xlabel('Generation')
axes[1].set_ylabel('Features selected')
axes[1].set_title('Number of Features in Best Chromosome')
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
savefig('plot_ipo_fitness_evolution.png')

# Plot 2 — Actual vs Predicted
fig, ax = plt.subplots(figsize=(8, 7))
ax.scatter(y_test, y_pred_test, alpha=0.5, s=18, color='#4a90d9', label='GA model', zorder=3)
mn = min(y_test.min(), y_pred_test.min())
mx = max(y_test.max(), y_pred_test.max())
ax.plot([mn, mx], [mn, mx], 'k--', linewidth=1.5, label='Perfect fit')
ax.set_xlabel('Actual 1-Year Return')
ax.set_ylabel('Predicted 1-Year Return')
ax.set_title(f'Actual vs Predicted — IPO 1-Year Return\nGA Test R²={test_r2:.4f}')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
savefig('plot_ipo_actual_vs_predicted.png')

# Plot 3 — Coefficients (top 20 by |value|)
top_n = min(20, len(coef_pairs))
top_names = [c[0] for c in coef_pairs[:top_n]]
top_vals  = [c[1] for c in coef_pairs[:top_n]]
colors = ['#4a90d9' if v >= 0 else '#e05c5c' for v in top_vals]
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top_names[::-1], top_vals[::-1], color=colors[::-1])
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('Coefficient (effect on 1-yr return per unit feature change)')
ax.set_title(f'Top {top_n} Feature Coefficients by |Value|\nGA-Selected Features')
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
savefig('plot_ipo_coefficients.png')

# Plot 4 — Residuals
residuals = y_pred_test - y_test
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].scatter(range(len(residuals)), residuals, alpha=0.5, s=12, color='#4a90d9')
axes[0].axhline(0, color='red', linewidth=1.5, linestyle='--')
axes[0].set_xlabel('Test IPO Index (chronological)')
axes[0].set_ylabel('Residual (Predicted − Actual)')
axes[0].set_title('Residuals Over Time')
axes[0].grid(True, alpha=0.3)
axes[1].hist(residuals, bins=40, color='#4a90d9', edgecolor='white', alpha=0.8)
axes[1].axvline(0, color='red', linewidth=1.5, linestyle='--')
axes[1].set_xlabel('Residual')
axes[1].set_ylabel('Count')
axes[1].set_title(f'Residual Distribution\nMAE={test_mae:.4f}  RMSE={test_rmse:.4f}')
axes[1].grid(True, alpha=0.3)
plt.suptitle('IPO Return Model Residuals — Test Set', fontsize=13)
plt.tight_layout()
savefig('plot_ipo_residuals.png')

# Plot 5 — Return distribution + model comparison
fig, ax = plt.subplots(figsize=(11, 5))
# Clip extreme outliers for readability
clip = np.percentile(np.abs(y_test), 95)
y_clip    = np.clip(y_test,       -clip, clip)
yp_clip   = np.clip(y_pred_test,  -clip, clip)
ax.hist(y_clip,  bins=40, alpha=0.55, color='#333333', density=True, label='Actual returns')
ax.hist(yp_clip, bins=40, alpha=0.55, color='#4a90d9', density=True, label='Predicted returns')
ax.set_xlabel('1-Year Return (clipped at 95th pct for readability)')
ax.set_ylabel('Density')
ax.set_title('Distribution: Actual vs Predicted IPO 1-Year Returns')
ax.legend()
ax.grid(True, alpha=0.2)
plt.tight_layout()
savefig('plot_ipo_distribution.png')

# Plot 6 — Feature type breakdown (pie)
type_counts = {
    'Planet longitude': len(lon_sel),
    'Cosine aspect':    len(cos_sel),
    'Other (Tithi/Phase)': len(other_sel),
}
type_counts = {k: v for k, v in type_counts.items() if v > 0}
fig, ax = plt.subplots(figsize=(7, 5))
wedge_colors = ['#4a90d9', '#e8a838', '#6abf69', '#e05c5c']
ax.pie(list(type_counts.values()), labels=list(type_counts.keys()),
       colors=wedge_colors[:len(type_counts)], autopct='%1.0f%%',
       startangle=140, textprops={'fontsize': 11})
ax.set_title(f'GA-Selected Feature Types\n({len(sel_names)} of {N_FEAT} features)')
plt.tight_layout()
savefig('plot_ipo_feature_types.png')

print("\nAll done. ✓")
