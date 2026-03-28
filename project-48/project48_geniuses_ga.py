"""
Project 48d: Genetic Algorithm Feature Selection — Classifying Genius Field
Using Planetary Aspects, Creativity Scores, and Astrological Signals

Big Astrology Book (BAB) — Computational Research Series

758 historical geniuses, 7 fields (artist, actor, filmmaker, inventor,
musician, scientist, writer), 75 features (planetary aspect cosines,
boolean aspect flags, creativity scores, sun sign).

The GA evolves binary chromosomes (which features to include) and uses
a k-Nearest Neighbours classifier as the fitness function.
"""

import csv
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(SCRIPT_DIR, 'geniuses.csv')

# ─────────────────────────────────────────────────────
# 1. LOAD & ENCODE DATA
# ─────────────────────────────────────────────────────
rows = []
with open(DATA_PATH) as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

ALL_COLS   = list(rows[0].keys())
TARGET_COL = 'field'
FEATURE_COLS = [c for c in ALL_COLS if c != TARGET_COL]

# Separate feature types
BOOL_COLS     = ['sun_neptune_aspect','sun_uranus_aspect','venus_neptune_aspect',
                 'trop_sun_in_creative_sign','trop_venus_in_creative_sign',
                 'sid_sun_in_creative_sign','sid_venus_in_creative_sign']
SUN_SIGN_COL  = 'sun_sign'
NUMERIC_COLS  = [c for c in FEATURE_COLS
                 if c not in BOOL_COLS and c != SUN_SIGN_COL]

# Encode sun_sign as one-hot (12 signs)
signs = sorted(set(r[SUN_SIGN_COL] for r in rows))
sign_to_idx = {s: i for i, s in enumerate(signs)}

# Build feature matrix
def encode_row(r):
    # Numeric features
    nums  = [float(r[c]) for c in NUMERIC_COLS]
    # Boolean features (TRUE=1, FALSE=0)
    bools = [1.0 if r[c].upper() == 'TRUE' else 0.0 for c in BOOL_COLS]
    # Sun sign one-hot
    oh = [0.0] * len(signs)
    oh[sign_to_idx[r[SUN_SIGN_COL]]] = 1.0
    return nums + bools + oh

X_all = np.array([encode_row(r) for r in rows])
y_raw = [r[TARGET_COL] for r in rows]

# Feature names (for plotting)
sign_cols = [f'sign_{s}' for s in signs]
FEAT_NAMES = NUMERIC_COLS + BOOL_COLS + sign_cols
N_FEATURES = len(FEAT_NAMES)

# Encode labels
fields      = sorted(set(y_raw))
field_to_int = {f: i for i, f in enumerate(fields)}
int_to_field = {i: f for f, i in field_to_int.items()}
y_all = np.array([field_to_int[f] for f in y_raw])
N_CLASSES = len(fields)

print(f"Dataset: {len(rows)} geniuses  |  {N_FEATURES} encoded features  |  {N_CLASSES} classes")
print(f"Fields: {dict(Counter(y_raw))}")
print(f"Feature breakdown: {len(NUMERIC_COLS)} numeric, {len(BOOL_COLS)} boolean, {len(signs)} sign one-hot\n")

# ─────────────────────────────────────────────────────
# 2. TRAIN / TEST SPLIT (stratified 80/20)
# ─────────────────────────────────────────────────────
rng = np.random.default_rng(42)
random.seed(42)

train_idx, test_idx = [], []
for cls_int in range(N_CLASSES):
    idx = np.where(y_all == cls_int)[0]
    idx = rng.permutation(idx)
    split = max(1, int(len(idx) * 0.80))
    train_idx.extend(idx[:split].tolist())
    test_idx.extend(idx[split:].tolist())

train_idx = np.array(train_idx)
test_idx  = np.array(test_idx)

X_train, y_train = X_all[train_idx], y_all[train_idx]
X_test,  y_test  = X_all[test_idx],  y_all[test_idx]

print(f"Train: {len(X_train)}  |  Test: {len(X_test)}\n")

# ─────────────────────────────────────────────────────
# 3. CLASSIFIER — k-Nearest Neighbours (pure numpy)
# ─────────────────────────────────────────────────────
K_NEIGHBOURS = 7

def knn_predict(X_tr, y_tr, X_te, k=K_NEIGHBOURS):
    """Vectorised kNN with Euclidean distance."""
    # Shapes: X_tr (n_tr, d), X_te (n_te, d)
    # Distance matrix: (n_te, n_tr)
    diff = X_te[:, np.newaxis, :] - X_tr[np.newaxis, :, :]  # (n_te, n_tr, d)
    dists = np.sqrt((diff ** 2).sum(axis=2))                 # (n_te, n_tr)
    nn_idx = np.argpartition(dists, k, axis=1)[:, :k]        # (n_te, k)
    nn_labels = y_tr[nn_idx]                                  # (n_te, k)
    # Majority vote
    preds = np.array([Counter(row).most_common(1)[0][0] for row in nn_labels])
    return preds


def fitness(chromosome, subsample=200):
    """Accuracy of kNN on training subsample using selected features.
    Subsampling speeds up the GA inner loop significantly."""
    selected = np.where(chromosome == 1)[0]
    if len(selected) == 0:
        return 0.0
    # Subsample training set for speed
    idx = rng.choice(len(X_train), size=min(subsample, len(X_train)), replace=False)
    Xsub, ysub = X_train[idx][:, selected], y_train[idx]
    preds = knn_predict(Xsub, ysub, Xsub, k=min(K_NEIGHBOURS, len(idx)-1))
    return np.mean(preds == ysub)


def full_accuracy(chromosome, X, y):
    selected = np.where(chromosome == 1)[0]
    if len(selected) == 0:
        return 0.0
    preds = knn_predict(X_train[:, selected], y_train, X[:, selected])
    return np.mean(preds == y)

# ─────────────────────────────────────────────────────
# 4. GA SETUP
# ─────────────────────────────────────────────────────
POP_SIZE       = 60
N_GENERATIONS  = 60
MUTATION_RATE  = 0.05   # per bit (75 bits → ~3-4 flips/individual)
CROSSOVER_RATE = 0.80
TOURNAMENT_K   = 4
ELITE_N        = 2

def random_chrom():
    # Start with roughly half features active
    return rng.integers(0, 2, size=N_FEATURES).astype(int)

def tournament_select(pop, fits):
    idx = random.sample(range(len(pop)), TOURNAMENT_K)
    return pop[max(idx, key=lambda i: fits[i])].copy()

def crossover(p1, p2):
    if random.random() < CROSSOVER_RATE:
        pt = random.randint(1, N_FEATURES - 1)
        return np.concatenate([p1[:pt], p2[pt:]]), np.concatenate([p2[:pt], p1[pt:]])
    return p1.copy(), p2.copy()

def mutate(chrom):
    flip = rng.random(N_FEATURES) < MUTATION_RATE
    chrom = chrom.copy()
    chrom[flip] = 1 - chrom[flip]
    if chrom.sum() == 0:
        chrom[rng.integers(0, N_FEATURES)] = 1
    return chrom

# ─────────────────────────────────────────────────────
# 5. EVOLVE
# ─────────────────────────────────────────────────────
population = [random_chrom() for _ in range(POP_SIZE)]

best_train_history = []
mean_train_history = []
best_chrom_ever    = None
best_fit_ever      = -1.0

print("Running Genetic Algorithm...")
print(f"  pop={POP_SIZE}  gens={N_GENERATIONS}  mut={MUTATION_RATE}  "
      f"cx={CROSSOVER_RATE}  k={K_NEIGHBOURS}-NN  elites={ELITE_N}\n")

for gen in range(N_GENERATIONS):
    fits = [fitness(c) for c in population]
    gen_best = max(fits)
    gen_mean = sum(fits) / len(fits)
    best_idx = fits.index(gen_best)

    best_train_history.append(gen_best)
    mean_train_history.append(gen_mean)

    if gen_best > best_fit_ever:
        best_fit_ever   = gen_best
        best_chrom_ever = population[best_idx].copy()

    if (gen + 1) % 10 == 0:
        n_sel = int(best_chrom_ever.sum())
        print(f"  Gen {gen+1:3d}  best_train={gen_best:.4f}  "
              f"mean={gen_mean:.4f}  features_selected={n_sel}")

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

print("\nGA complete. Evaluating best chromosome on full train/test sets...\n")

# ─────────────────────────────────────────────────────
# 6. FINAL EVALUATION
# ─────────────────────────────────────────────────────
selected_idx   = np.where(best_chrom_ever == 1)[0]
selected_names = [FEAT_NAMES[i] for i in selected_idx]

final_train_acc = full_accuracy(best_chrom_ever, X_train, y_train)
final_test_acc  = full_accuracy(best_chrom_ever, X_test,  y_test)

majority_class_int  = Counter(y_train.tolist()).most_common(1)[0][0]
majority_class_name = int_to_field[majority_class_int]
baseline_acc = np.mean(y_test == majority_class_int)

print("=" * 58)
print("FINAL RESULTS")
print("=" * 58)
print(f"  Features selected  : {len(selected_names)} / {N_FEATURES}")
print(f"  Train accuracy     : {final_train_acc:.4f}  ({final_train_acc*100:.2f}%)")
print(f"  Test  accuracy     : {final_test_acc:.4f}  ({final_test_acc*100:.2f}%)")
print(f"  Majority-class baseline ('{majority_class_name}'): {baseline_acc:.4f}  ({baseline_acc*100:.2f}%)")
print(f"  Improvement over baseline: {(final_test_acc - baseline_acc)*100:+.2f} pp")
print("=" * 58)

print(f"\nSelected features ({len(selected_names)}):")
for fn in selected_names:
    print(f"  • {fn}")

# Per-class breakdown
y_pred_test = knn_predict(X_train[:, selected_idx], y_train, X_test[:, selected_idx])
print("\nPer-class accuracy on test set:")
for cls_int, cls_name in int_to_field.items():
    mask = y_test == cls_int
    if mask.sum() == 0:
        continue
    acc = np.mean(y_pred_test[mask] == cls_int)
    print(f"  {cls_name:12s}: {int(mask.sum()):3d} samples  acc={acc:.4f}")

# ─────────────────────────────────────────────────────
# 7. PLOTS
# ─────────────────────────────────────────────────────

def savefig(name):
    path = os.path.join(SCRIPT_DIR, name)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {name}")

FIELD_COLORS = {
    'artist':    '#e05c5c',
    'actor':     '#e8a838',
    'filmmaker': '#9b59b6',
    'inventor':  '#4a90d9',
    'musician':  '#6abf69',
    'scientist': '#3daac2',
    'writer':    '#c27b3d',
}

# Plot 1 — Fitness evolution
fig, ax = plt.subplots(figsize=(11, 5))
gens = range(1, N_GENERATIONS + 1)
ax.plot(gens, best_train_history, label='Best train acc', color='#4a90d9', linewidth=2)
ax.plot(gens, mean_train_history, label='Mean train acc', color='#e8a838', linewidth=1.5, linestyle='--')
ax.axhline(baseline_acc, color='red', linewidth=1, linestyle=':', label=f'Baseline ({baseline_acc:.3f})')
ax.set_xlabel('Generation')
ax.set_ylabel('Classification Accuracy (subsample)')
ax.set_title('GA Accuracy Evolution — Genius Field Classifier')
ax.legend()
ax.set_ylim(0, 1)
ax.grid(True, alpha=0.3)
plt.tight_layout()
savefig('plot_geniuses_fitness_evolution.png')

# Plot 2 — Confusion matrix
N_CLS = len(fields)
conf_mat = np.zeros((N_CLS, N_CLS), dtype=int)
for t, p in zip(y_test, y_pred_test):
    conf_mat[t, p] += 1

fig, ax = plt.subplots(figsize=(9, 7))
im = ax.imshow(conf_mat, cmap='Blues')
ax.set_xticks(range(N_CLS))
ax.set_yticks(range(N_CLS))
ax.set_xticklabels(fields, rotation=35, ha='right')
ax.set_yticklabels(fields)
ax.set_xlabel('Predicted Field')
ax.set_ylabel('Actual Field')
ax.set_title(f'Confusion Matrix — Genius Field (Test Set)\n'
             f'Test accuracy: {final_test_acc*100:.1f}%')
for i in range(N_CLS):
    for j in range(N_CLS):
        ax.text(j, i, str(conf_mat[i, j]), ha='center', va='center',
                color='white' if conf_mat[i, j] > conf_mat.max() * 0.55 else 'black',
                fontsize=11, fontweight='bold')
plt.colorbar(im, ax=ax, label='Count')
plt.tight_layout()
savefig('plot_geniuses_confusion_matrix.png')

# Plot 3 — Selected feature categories (bar chart of feature type counts)
type_counts = {'Planetary aspect': 0, 'Boolean aspect': 0, 'Sun sign': 0, 'Creativity score': 0}
for fn in selected_names:
    if fn.startswith('sign_'):
        type_counts['Sun sign'] += 1
    elif fn in BOOL_COLS:
        type_counts['Boolean aspect'] += 1
    elif 'score' in fn:
        type_counts['Creativity score'] += 1
    else:
        type_counts['Planetary aspect'] += 1

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: type breakdown
ax = axes[0]
cat_labels = list(type_counts.keys())
cat_vals   = [type_counts[k] for k in cat_labels]
cat_colors = ['#4a90d9', '#e8a838', '#6abf69', '#e05c5c']
bars = ax.bar(cat_labels, cat_vals, color=cat_colors, edgecolor='white', linewidth=0.5)
ax.set_ylabel('Count selected')
ax.set_title(f'Selected Feature Types\n({len(selected_names)} of {N_FEATURES} total)')
ax.bar_label(bars, padding=3)
ax.grid(True, alpha=0.2, axis='y')

# Right: top 20 individual planetary aspect features selected
aspect_feats = [(fn, i) for i, fn in enumerate(FEAT_NAMES)
                if best_chrom_ever[i] == 1 and fn in NUMERIC_COLS
                and fn not in ['trop_creativity_score', 'sid_creativity_score']][:20]
ax2 = axes[1]
if aspect_feats:
    names_plot = [f[0] for f in aspect_feats]
    # Use mean absolute value across classes as a proxy for "informativeness"
    vals_plot = []
    for fn, fi in aspect_feats:
        class_means = [X_train[y_train == ci, fi].mean() for ci in range(N_CLASSES)]
        vals_plot.append(np.std(class_means))   # std of class means = between-class spread
    order = np.argsort(vals_plot)[::-1]
    ax2.barh([names_plot[i] for i in order], [vals_plot[i] for i in order],
             color='#4a90d9', edgecolor='white')
    ax2.set_xlabel('Std of class means (between-class spread)')
    ax2.set_title('Top Selected Planetary Aspects\n(by between-class variance)')
    ax2.grid(True, alpha=0.2, axis='x')
else:
    ax2.text(0.5, 0.5, 'No planetary aspects selected', ha='center', va='center')

plt.tight_layout()
savefig('plot_geniuses_selected_features.png')

# Plot 4 — Per-class accuracy bar
fig, ax = plt.subplots(figsize=(10, 5))
cls_accs, cls_names_plot, cls_ns = [], [], []
for cls_int, cls_name in int_to_field.items():
    mask = y_test == cls_int
    if mask.sum() == 0:
        continue
    acc = np.mean(y_pred_test[mask] == cls_int)
    cls_accs.append(acc)
    cls_names_plot.append(cls_name)
    cls_ns.append(int(mask.sum()))

colors_plot = [FIELD_COLORS.get(n, 'steelblue') for n in cls_names_plot]
bars = ax.bar(cls_names_plot, cls_accs, color=colors_plot, edgecolor='white')
ax.axhline(baseline_acc, color='red', linewidth=1.5, linestyle='--', label=f'Baseline ({baseline_acc:.3f})')
ax.axhline(final_test_acc, color='black', linewidth=1.5, linestyle=':', label=f'Overall ({final_test_acc:.3f})')
for bar, n, acc in zip(bars, cls_ns, cls_accs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f'{acc:.2f}\n(n={n})', ha='center', va='bottom', fontsize=9)
ax.set_ylabel('Accuracy')
ax.set_ylim(0, 1.15)
ax.set_title('Per-Class Test Accuracy — Genius Field Classifier')
ax.legend()
ax.grid(True, alpha=0.2, axis='y')
plt.tight_layout()
savefig('plot_geniuses_per_class_accuracy.png')

# Plot 5 — Class distribution in dataset
fig, ax = plt.subplots(figsize=(9, 4))
field_counts = Counter(y_raw)
sorted_fields = sorted(field_counts, key=lambda x: -field_counts[x])
ax.bar(sorted_fields, [field_counts[f] for f in sorted_fields],
       color=[FIELD_COLORS.get(f, 'grey') for f in sorted_fields], edgecolor='white')
ax.set_ylabel('Number of geniuses')
ax.set_title('Dataset Class Distribution — 758 Geniuses by Field')
for i, f in enumerate(sorted_fields):
    ax.text(i, field_counts[f] + 2, str(field_counts[f]), ha='center', fontsize=10)
ax.grid(True, alpha=0.2, axis='y')
plt.tight_layout()
savefig('plot_geniuses_class_distribution.png')

print("\nAll done. ✓")
