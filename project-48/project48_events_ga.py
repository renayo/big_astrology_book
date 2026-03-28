"""
Project 48c: Genetic Algorithm — Classify Event Category from cosine_metric

Big Astrology Book (BAB) — Computational Research Series

One feature (cosine_metric), four classes (political, military, disaster, economic).
The GA evolves three real-valued cut points that partition the number line into
four labelled bins. Fitness = classification accuracy on the test set.
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
DATA_PATH  = os.path.join(SCRIPT_DIR, 'events.csv')

# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────
categories = []
values     = []

with open(DATA_PATH) as f:
    reader = csv.reader(f)
    next(reader)                         # skip header
    for row in reader:
        cat = row[0].strip()
        try:
            val = float(row[1].strip())
        except ValueError:
            continue
        if cat:
            categories.append(cat)
            values.append(val)

X = np.array(values)
y = np.array(categories)

# Encode labels to integers
label_order = sorted(set(y))            # alphabetical: disaster, economic, military, political
label_to_int = {l: i for i, l in enumerate(label_order)}
int_to_label = {i: l for l, i in label_to_int.items()}
y_int = np.array([label_to_int[c] for c in y])

print(f"Dataset: {len(X)} rows")
print(f"Class distribution: {dict(Counter(y))}")
print(f"Label encoding: {label_to_int}")
print(f"cosine_metric  min={X.min():.4f}  max={X.max():.4f}  mean={X.mean():.4f}\n")

# ─────────────────────────────────────────────
# 2. TRAIN / TEST SPLIT (stratified, 80/20)
# ─────────────────────────────────────────────
rng = np.random.default_rng(42)
idx = rng.permutation(len(X))           # shuffle (categories not time-series)
split = int(len(X) * 0.80)
train_idx = idx[:split]
test_idx  = idx[split:]

X_train, y_train = X[train_idx], y_int[train_idx]
X_test,  y_test  = X[test_idx],  y_int[test_idx]

print(f"Train: {len(X_train)} rows  |  Test: {len(X_test)} rows\n")

# ─────────────────────────────────────────────
# 3. CHROMOSOME DESIGN
# ─────────────────────────────────────────────
# Each chromosome = [t1, t2, t3, label_a, label_b, label_c, label_d]
#   Thresholds split the number line: (-inf, t1], (t1, t2], (t2, t3], (t3, +inf)
#   label_a..d (int 0-3) assign a class to each bin
# Chromosome length = 7 genes (3 real thresholds + 4 integer labels)

N_CLASSES  = 4
LO, HI     = X.min() - 0.5, X.max() + 0.5  # threshold search range

POP_SIZE        = 100
N_GENERATIONS   = 120
MUTATION_RATE   = 0.12
CROSSOVER_RATE  = 0.80
TOURNAMENT_K    = 4
ELITE_N         = 2                       # elitism: carry top-N forward


def decode(chrom):
    """Return sorted thresholds and label assignments."""
    thresholds = sorted(chrom[:3])
    labels     = [int(round(g)) % N_CLASSES for g in chrom[3:]]
    return thresholds, labels


def predict(chrom, x_vals):
    thresholds, labels = decode(chrom)
    preds = []
    for v in x_vals:
        if v <= thresholds[0]:
            preds.append(labels[0])
        elif v <= thresholds[1]:
            preds.append(labels[1])
        elif v <= thresholds[2]:
            preds.append(labels[2])
        else:
            preds.append(labels[3])
    return np.array(preds)


def fitness(chrom):
    preds = predict(chrom, X_train)
    return np.mean(preds == y_train)      # accuracy on train set


def accuracy(chrom, x_vals, y_vals):
    preds = predict(chrom, x_vals)
    return np.mean(preds == y_vals)


# ─────────────────────────────────────────────
# 4. INITIALISE POPULATION
# ─────────────────────────────────────────────
def random_chrom():
    thresholds = sorted(rng.uniform(LO, HI, 3).tolist())
    labels     = rng.integers(0, N_CLASSES, 4).tolist()
    return thresholds + labels


population = [random_chrom() for _ in range(POP_SIZE)]

# ─────────────────────────────────────────────
# 5. GA OPERATORS
# ─────────────────────────────────────────────

def tournament_select(pop, fits, k=TOURNAMENT_K):
    idx = random.sample(range(len(pop)), k)
    best = max(idx, key=lambda i: fits[i])
    return pop[best][:]


def crossover(p1, p2):
    if random.random() < CROSSOVER_RATE:
        pt = random.randint(1, len(p1) - 1)
        return p1[:pt] + p2[pt:], p2[:pt] + p1[pt:]
    return p1[:], p2[:]


def mutate(chrom):
    chrom = chrom[:]
    for i in range(len(chrom)):
        if random.random() < MUTATION_RATE:
            if i < 3:   # threshold gene — nudge with Gaussian noise
                chrom[i] += random.gauss(0, (HI - LO) * 0.05)
                chrom[i]  = max(LO, min(HI, chrom[i]))
            else:       # label gene — random new class
                chrom[i] = random.randint(0, N_CLASSES - 1)
    return chrom

# ─────────────────────────────────────────────
# 6. EVOLVE
# ─────────────────────────────────────────────
best_fitness_history  = []
mean_fitness_history  = []
test_acc_history      = []

overall_best_chrom = None
overall_best_fit   = -1

random.seed(42)

print("Running Genetic Algorithm...")
print(f"  pop={POP_SIZE}  gens={N_GENERATIONS}  mut={MUTATION_RATE}  "
      f"cx={CROSSOVER_RATE}  tournament_k={TOURNAMENT_K}  elites={ELITE_N}\n")

for gen in range(N_GENERATIONS):
    fits = [fitness(c) for c in population]

    gen_best = max(fits)
    gen_mean = sum(fits) / len(fits)
    best_chrom = population[fits.index(gen_best)]
    test_acc   = accuracy(best_chrom, X_test, y_test)

    best_fitness_history.append(gen_best)
    mean_fitness_history.append(gen_mean)
    test_acc_history.append(test_acc)

    if gen_best > overall_best_fit:
        overall_best_fit   = gen_best
        overall_best_chrom = best_chrom[:]

    if (gen + 1) % 20 == 0:
        print(f"  Gen {gen+1:3d}  train_acc={gen_best:.4f}  "
              f"mean_acc={gen_mean:.4f}  test_acc={test_acc:.4f}")

    # Sort by fitness, keep elites
    ranked = sorted(range(len(population)), key=lambda i: fits[i], reverse=True)
    elites = [population[i][:] for i in ranked[:ELITE_N]]

    new_pop = elites[:]
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
# 7. FINAL EVALUATION
# ─────────────────────────────────────────────
thresholds, labels = decode(overall_best_chrom)
label_names = [int_to_label[l] for l in labels]

final_train_acc = accuracy(overall_best_chrom, X_train, y_train)
final_test_acc  = accuracy(overall_best_chrom, X_test,  y_test)

print("=" * 55)
print("FINAL RESULT")
print("=" * 55)
print(f"  Thresholds  : {[f'{t:.4f}' for t in thresholds]}")
print(f"  Bin labels  : "
      f"(-∞,{thresholds[0]:.2f}]→{label_names[0]}  "
      f"({thresholds[0]:.2f},{thresholds[1]:.2f}]→{label_names[1]}  "
      f"({thresholds[1]:.2f},{thresholds[2]:.2f}]→{label_names[2]}  "
      f"({thresholds[2]:.2f},+∞)→{label_names[3]}")
print(f"  Train accuracy : {final_train_acc:.4f} ({final_train_acc*100:.2f}%)")
print(f"  Test  accuracy : {final_test_acc:.4f} ({final_test_acc*100:.2f}%)")
print()

# Baseline: always predict most common class
baseline = max(Counter(y_train), key=lambda k: Counter(y_train)[k])
baseline_acc = np.mean(y_test == label_to_int[int_to_label[int(baseline)]])
# simpler: majority vote
majority_class_int = Counter(y_train).most_common(1)[0][0]
majority_class_name = int_to_label[majority_class_int]
baseline_test_acc = np.mean(y_test == majority_class_int)
print(f"  Majority-class baseline ('{majority_class_name}'): {baseline_test_acc:.4f} ({baseline_test_acc*100:.2f}%)")
print(f"  GA improvement over baseline: {(final_test_acc - baseline_test_acc)*100:+.2f} pp")
print("=" * 55)

# Per-class breakdown
y_pred_test = predict(overall_best_chrom, X_test)
print("\nPer-class accuracy on test set:")
for cls_name, cls_int in label_to_int.items():
    mask = y_test == cls_int
    if mask.sum() == 0:
        continue
    cls_acc = np.mean(y_pred_test[mask] == cls_int)
    print(f"  {cls_name:12s}: {int(mask.sum()):3d} samples  acc={cls_acc:.4f}")

# ─────────────────────────────────────────────
# 8. PLOTS
# ─────────────────────────────────────────────

def savefig(name):
    path = os.path.join(SCRIPT_DIR, name)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nSaved: {name}")


COLORS = {'disaster': '#e05c5c', 'economic': '#e8a838',
          'military': '#4a90d9', 'political': '#6abf69'}

# Plot 1 — Fitness / accuracy evolution
fig, ax = plt.subplots(figsize=(11, 5))
gens = range(1, N_GENERATIONS + 1)
ax.plot(gens, best_fitness_history, label='Best train acc', color='#4a90d9', linewidth=2)
ax.plot(gens, mean_fitness_history, label='Mean train acc', color='#e8a838', linewidth=1.5, linestyle='--')
ax.plot(gens, test_acc_history,     label='Best test acc',  color='#6abf69', linewidth=1.5, linestyle=':')
ax.set_xlabel('Generation')
ax.set_ylabel('Classification Accuracy')
ax.set_title('GA Accuracy Evolution — Event Category Classifier')
ax.legend()
ax.set_ylim(0, 1)
ax.grid(True, alpha=0.3)
plt.tight_layout()
savefig('plot_events_fitness_evolution.png')

# Plot 2 — cosine_metric distribution by category with threshold lines
fig, ax = plt.subplots(figsize=(12, 5))
for cls_name in label_order:
    mask = y == cls_name
    ax.hist(X[mask], bins=40, alpha=0.55, label=cls_name,
            color=COLORS.get(cls_name, 'grey'), density=True)
for t in thresholds:
    ax.axvline(t, color='black', linewidth=1.8, linestyle='--', alpha=0.85)
ax.set_xlabel('cosine_metric')
ax.set_ylabel('Density')
ax.set_title('cosine_metric Distribution by Category\n(dashed lines = GA-evolved thresholds)')
ax.legend()
ax.grid(True, alpha=0.2)
plt.tight_layout()
savefig('plot_events_distributions.png')

# Plot 3 — Confusion matrix (test set)
from collections import defaultdict
conf = defaultdict(lambda: defaultdict(int))
for true_int, pred_int in zip(y_test, y_pred_test):
    conf[int_to_label[true_int]][int_to_label[pred_int]] += 1

fig, ax = plt.subplots(figsize=(7, 6))
cm_data = np.zeros((N_CLASSES, N_CLASSES), dtype=int)
for i, true_cls in enumerate(label_order):
    for j, pred_cls in enumerate(label_order):
        cm_data[i, j] = conf[true_cls][pred_cls]

im = ax.imshow(cm_data, cmap='Blues')
ax.set_xticks(range(N_CLASSES))
ax.set_yticks(range(N_CLASSES))
ax.set_xticklabels(label_order, rotation=30, ha='right')
ax.set_yticklabels(label_order)
ax.set_xlabel('Predicted')
ax.set_ylabel('Actual')
ax.set_title('Confusion Matrix — Test Set')
for i in range(N_CLASSES):
    for j in range(N_CLASSES):
        ax.text(j, i, str(cm_data[i, j]), ha='center', va='center',
                color='white' if cm_data[i, j] > cm_data.max() * 0.5 else 'black',
                fontsize=13, fontweight='bold')
plt.colorbar(im, ax=ax)
plt.tight_layout()
savefig('plot_events_confusion_matrix.png')

# Plot 4 — Strip plot: cosine_metric by category, colour-coded by prediction correctness
fig, ax = plt.subplots(figsize=(12, 5))
jitter = rng.uniform(-0.15, 0.15, len(X_test))
y_labels_test = [int_to_label[i] for i in y_test]
for k, cls_name in enumerate(label_order):
    mask = np.array(y_labels_test) == cls_name
    correct = y_pred_test[mask] == y_test[mask]
    xvals   = X_test[mask]
    jit     = jitter[mask]
    ax.scatter(xvals[correct],  np.full(correct.sum(),  k) + jit[correct],
               color=COLORS.get(cls_name, 'grey'), s=18, alpha=0.7, label=f'{cls_name} ✓')
    ax.scatter(xvals[~correct], np.full((~correct).sum(), k) + jit[~correct],
               color='black', marker='x', s=25, alpha=0.5, label=f'{cls_name} ✗' if k == 0 else '')
for t in thresholds:
    ax.axvline(t, color='black', linewidth=1.5, linestyle='--', alpha=0.7)
ax.set_yticks(range(N_CLASSES))
ax.set_yticklabels(label_order)
ax.set_xlabel('cosine_metric')
ax.set_title('Test Set: Correct (●) vs Incorrect (✗) Predictions\n(dashed lines = GA thresholds)')
handles, lbls = ax.get_legend_handles_labels()
ax.legend(handles[:N_CLASSES+1], lbls[:N_CLASSES+1], loc='upper left', fontsize=8)
ax.grid(True, alpha=0.2, axis='x')
plt.tight_layout()
savefig('plot_events_strip.png')

print("\nAll done. ✓")
