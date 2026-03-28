"""
Project 48: Genetic Algorithm Feature Selection for S&P 500 Price Prediction
Using Planetary / Financial Features

Big Astrology Book (BAB) — Computational Research Series
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────
df = pd.read_csv('financial_data.csv')

TARGET = 'sp500_close'
FEATURES = [c for c in df.columns if c != TARGET]

X = df[FEATURES].values
y = df[TARGET].values

print(f"Dataset shape: {df.shape}")
print(f"Target: {TARGET}  |  Features: {FEATURES}")
print(f"sp500_close  min={y.min():.2f}  max={y.max():.2f}  mean={y.mean():.2f}\n")

# ─────────────────────────────────────────────
# 2. TRAIN / TEST SPLIT (time-ordered, no shuffle)
# ─────────────────────────────────────────────
split = int(len(X) * 0.80)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

print(f"Train rows: {len(X_train)}  |  Test rows: {len(X_test)}\n")

# ─────────────────────────────────────────────
# 3. GENETIC ALGORITHM — from scratch
# ─────────────────────────────────────────────

# GA hyper-parameters
POP_SIZE       = 50
N_GENERATIONS  = 80
MUTATION_RATE  = 0.10
CROSSOVER_RATE = 0.80
TOURNAMENT_K   = 3
N_FEATURES     = len(FEATURES)

rng = np.random.default_rng(42)


def fitness(chromosome):
    """Fitness = negative MSE on test set (higher is better)."""
    selected = np.where(chromosome == 1)[0]
    if len(selected) == 0:
        return -np.inf
    model = LinearRegression()
    model.fit(X_train[:, selected], y_train)
    preds = model.predict(X_test[:, selected])
    mse = mean_squared_error(y_test, preds)
    return -mse


def tournament_select(population, fitnesses, k=TOURNAMENT_K):
    """Pick k individuals at random, return the best chromosome."""
    indices = rng.integers(0, len(population), size=k)
    best_idx = indices[np.argmax(fitnesses[indices])]
    return population[best_idx].copy()


def crossover(parent1, parent2):
    """Single-point crossover."""
    if rng.random() < CROSSOVER_RATE:
        point = rng.integers(1, N_FEATURES)
        child1 = np.concatenate([parent1[:point], parent2[point:]])
        child2 = np.concatenate([parent2[:point], parent1[point:]])
        return child1, child2
    return parent1.copy(), parent2.copy()


def mutate(chromosome):
    """Bit-flip mutation."""
    for i in range(N_FEATURES):
        if rng.random() < MUTATION_RATE:
            chromosome[i] = 1 - chromosome[i]
    # Ensure at least one feature is selected
    if chromosome.sum() == 0:
        chromosome[rng.integers(0, N_FEATURES)] = 1
    return chromosome


# Initialise population (random binary strings)
population = rng.integers(0, 2, size=(POP_SIZE, N_FEATURES)).astype(int)

# History for plotting
best_fitness_history = []
mean_fitness_history = []

best_chromosome = None
best_fit_ever   = -np.inf

print("Running Genetic Algorithm...")
print(f"  pop={POP_SIZE}  gens={N_GENERATIONS}  mut={MUTATION_RATE}  cx={CROSSOVER_RATE}  tournament_k={TOURNAMENT_K}\n")

for gen in range(N_GENERATIONS):
    # Evaluate fitness for every individual
    fitnesses = np.array([fitness(ind) for ind in population])

    gen_best = fitnesses.max()
    gen_mean = fitnesses[fitnesses > -np.inf].mean()

    best_fitness_history.append(gen_best)
    mean_fitness_history.append(gen_mean)

    if gen_best > best_fit_ever:
        best_fit_ever   = gen_best
        best_chromosome = population[np.argmax(fitnesses)].copy()

    if (gen + 1) % 10 == 0:
        print(f"  Gen {gen+1:3d}  best_fitness={gen_best:.4f}  mean_fitness={gen_mean:.4f}")

    # Build next generation
    new_population = []
    # Elitism: carry the best individual forward
    new_population.append(best_chromosome.copy())

    while len(new_population) < POP_SIZE:
        p1 = tournament_select(population, fitnesses)
        p2 = tournament_select(population, fitnesses)
        c1, c2 = crossover(p1, p2)
        c1 = mutate(c1)
        c2 = mutate(c2)
        new_population.append(c1)
        if len(new_population) < POP_SIZE:
            new_population.append(c2)

    population = np.array(new_population)

print("\nGA complete.\n")

# ─────────────────────────────────────────────
# 4. FINAL MODEL on best feature subset
# ─────────────────────────────────────────────
selected_indices = np.where(best_chromosome == 1)[0]
selected_features = [FEATURES[i] for i in selected_indices]

print(f"Best feature subset ({len(selected_features)} features):")
for f in selected_features:
    print(f"  • {f}")
print()

final_model = LinearRegression()
final_model.fit(X_train[:, selected_indices], y_train)

y_pred_test  = final_model.predict(X_test[:, selected_indices])
y_pred_train = final_model.predict(X_train[:, selected_indices])

train_r2 = r2_score(y_train, y_pred_train)
test_r2  = r2_score(y_test,  y_pred_test)
mse      = mean_squared_error(y_test, y_pred_test)
mae      = mean_absolute_error(y_test, y_pred_test)
rmse     = np.sqrt(mse)

print("=" * 50)
print("FINAL MODEL METRICS")
print("=" * 50)
print(f"  Train R²  : {train_r2:.6f}")
print(f"  Test  R²  : {test_r2:.6f}")
print(f"  MSE       : {mse:.4f}")
print(f"  MAE       : {mae:.4f}")
print(f"  RMSE      : {rmse:.4f}")
print("=" * 50)
print()

# Coefficients
coef_df = pd.DataFrame({
    'feature': selected_features,
    'coefficient': final_model.coef_
}).sort_values('coefficient', key=abs, ascending=False)

print("Feature coefficients (sorted by |coef|):")
print(coef_df.to_string(index=False))

# ─────────────────────────────────────────────
# 5. PLOTS
# ─────────────────────────────────────────────

# Plot 1 — Fitness evolution
fig, ax = plt.subplots(figsize=(10, 5))
gens = range(1, N_GENERATIONS + 1)
ax.plot(gens, best_fitness_history, label='Best fitness', color='steelblue', linewidth=2)
ax.plot(gens, mean_fitness_history, label='Mean fitness', color='orange', linewidth=1.5, linestyle='--')
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness (Negative MSE)')
ax.set_title('GA Fitness Evolution Over Generations')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('plot_fitness_evolution.png', dpi=150)
plt.close()
print("Saved: plot_fitness_evolution.png")

# Plot 2 — Actual vs Predicted
fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(y_test, y_pred_test, alpha=0.4, s=10, color='steelblue', label='Test predictions')
mn = min(y_test.min(), y_pred_test.min())
mx = max(y_test.max(), y_pred_test.max())
ax.plot([mn, mx], [mn, mx], 'r--', linewidth=1.5, label='Perfect fit')
ax.set_xlabel('Actual sp500_close')
ax.set_ylabel('Predicted sp500_close')
ax.set_title('Actual vs Predicted — S&P 500 Close')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('plot_actual_vs_predicted.png', dpi=150)
plt.close()
print("Saved: plot_actual_vs_predicted.png")

# Plot 3 — Feature importance (coefficients)
fig, ax = plt.subplots(figsize=(9, 5))
colors = ['steelblue' if c >= 0 else 'tomato' for c in coef_df['coefficient']]
bars = ax.barh(coef_df['feature'], coef_df['coefficient'], color=colors)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('Coefficient Value')
ax.set_title('Feature Importance — Linear Regression Coefficients\n(sorted by absolute value)')
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('plot_feature_importance.png', dpi=150)
plt.close()
print("Saved: plot_feature_importance.png")

# Plot 4 — Residuals
residuals = y_pred_test - y_test
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(range(len(residuals)), residuals, alpha=0.4, s=10, color='steelblue')
ax.axhline(0, color='red', linewidth=1.5, linestyle='--')
ax.set_xlabel('Test Set Index')
ax.set_ylabel('Residual (Predicted − Actual)')
ax.set_title('Residuals — Test Set')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('plot_residuals.png', dpi=150)
plt.close()
print("Saved: plot_residuals.png")

print("\nAll done. ✓")
