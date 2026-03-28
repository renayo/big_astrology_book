#!/usr/bin/env python3
"""
Project 19: Mundane Astrology — Bootstrap Completion
=====================================================
Completes the previously incomplete analysis using:
- Chi-square tests for each traditional aspect-event claim
- Bootstrap permutation baseline: resample event dates by shuffling
  years, months, and days independently to destroy temporal structure
  while preserving the calendar distribution

Traditional claims tested:
  Saturn-Pluto  → Wars, destruction, collapse
  Uranus-Pluto  → Revolutions, mass upheaval
  Saturn-Neptune → Epidemics, collective delusion
  Jupiter-Uranus → Tech breakthroughs, sudden expansion
  Saturn-Uranus  → Structural crises, old vs new

Author: Renay Oshop / Edgar (completion)
"""

import csv, random, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE  = os.path.join(SCRIPT_DIR, 'event_data.csv')
N_BOOTSTRAP = 10000
RANDOM_SEED  = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────
rows = []
with open(DATA_FILE) as f:
    for r in csv.DictReader(f):
        rows.append(r)

print(f"Loaded {len(rows)} events spanning {rows[0]['date']} → {rows[-1]['date']}\n")

ASPECT_COLS = [
    'Saturn_Pluto', 'Uranus_Pluto', 'Saturn_Neptune',
    'Jupiter_Uranus', 'Saturn_Uranus', 'Jupiter_Saturn',
    'Jupiter_Pluto', 'Jupiter_Neptune'
]

# Traditional claims: which aspect → which event category is claimed
TRADITIONAL_CLAIMS = {
    'Saturn_Pluto':    ['war_start', 'war_end', 'military', 'revolution', 'massacre'],
    'Uranus_Pluto':    ['revolution', 'political'],
    'Saturn_Neptune':  ['epidemic', 'disaster'],
    'Jupiter_Uranus':  ['tech', 'economic'],
    'Saturn_Uranus':   ['political', 'revolution', 'economic_crisis'],
    'Jupiter_Saturn':  ['economic_crisis', 'economic', 'political'],
    'Jupiter_Pluto':   ['war_start', 'military', 'economic_crisis'],
    'Jupiter_Neptune': ['epidemic', 'disaster'],
}

# Hard aspects (conjunction, square, opposition) — the traditionally "difficult" ones
HARD = {'conjunction', 'square', 'opposition'}
SOFT = {'trine', 'sextile'}

def is_hard(val):
    return val in HARD

def is_any_aspect(val):
    return val != 'none'

# ─────────────────────────────────────────────
# 2. BOOTSTRAP BASELINE CONSTRUCTION
#
# Strategy: For each bootstrap iteration, independently shuffle
# the year, month, and day components of all event dates.
# This destroys the actual date structure (and thus the real
# planetary aspects) while preserving:
#   - The same number of events
#   - The same year distribution
#   - The same month distribution
#   - The same day-of-month distribution
# Then re-compute aspect activity from the shuffled dates
# using the pre-computed aspect angles in the dataset.
#
# Since we have aspect angles in the CSV, we can reconstruct
# aspect labels directly — but we need to reshuffle which
# aspect angle goes with which event.
# ─────────────────────────────────────────────

def get_aspect_label(angle_str):
    """Classify an angle into an aspect label."""
    try:
        angle = float(angle_str)
    except (ValueError, TypeError):
        return 'none'
    # Normalize to 0-180
    angle = abs(angle) % 360
    if angle > 180:
        angle = 360 - angle
    orbs = {
        'conjunction': (0, 8),
        'opposition':  (172, 180),
        'square':      (82, 98),
        'trine':       (112, 128),
        'sextile':     (52, 68),
    }
    for name, (lo, hi) in orbs.items():
        if lo <= angle <= hi:
            return name
    return 'none'

# Extract all angle values per aspect pair (the raw planetary geometry)
# These are independent of which event falls on a given date.
angles_by_col = {}
for col in ASPECT_COLS:
    angle_col = col + '_angle'
    if angle_col in rows[0]:
        angles_by_col[col] = [r[angle_col] for r in rows]
    else:
        angles_by_col[col] = [r[col] for r in rows]  # already labeled

# Build actual aspect presence per event
actual_aspects = {}  # col → list of bool (hard aspect active for each event)
for col in ASPECT_COLS:
    labels = [get_aspect_label(a) for a in angles_by_col[col]]
    actual_aspects[col] = labels

# Event type per event
event_types = [r['event_type'] for r in rows]

# ─────────────────────────────────────────────
# 3. COMPUTE OBSERVED RATES
# ─────────────────────────────────────────────

def rate_for_category(aspect_labels, event_types, category_set, mode='hard'):
    """Fraction of category-matching events that have the aspect active."""
    cat_events = [i for i, t in enumerate(event_types) if t in category_set]
    if not cat_events:
        return 0.0, 0
    if mode == 'hard':
        hits = sum(1 for i in cat_events if aspect_labels[i] in HARD)
    else:
        hits = sum(1 for i in cat_events if aspect_labels[i] != 'none')
    return hits / len(cat_events), len(cat_events)

print("=" * 65)
print("OBSERVED RATES — Traditional Claims (Hard Aspects)")
print("=" * 65)

observed = {}
for asp, cats in TRADITIONAL_CLAIMS.items():
    labels = actual_aspects[asp]
    rate, n = rate_for_category(labels, event_types, set(cats), 'hard')
    # Also overall hard rate (base rate)
    overall_hard = sum(1 for l in labels if l in HARD) / len(labels)
    observed[asp] = {'rate': rate, 'n': n, 'base': overall_hard}
    print(f"\n  {asp}")
    print(f"    Claimed categories : {cats}")
    print(f"    N events in cats   : {n}")
    print(f"    Hard aspect rate   : {rate:.4f} ({rate*100:.1f}%)")
    print(f"    Overall base rate  : {overall_hard:.4f} ({overall_hard*100:.1f}%)")
    print(f"    Ratio (obs/base)   : {rate/overall_hard:.3f}x" if overall_hard > 0 else "")

# ─────────────────────────────────────────────
# 4. BOOTSTRAP PERMUTATION TEST
#
# For each iteration:
#   - Shuffle the aspect label arrays independently (per aspect column)
#   - This breaks the link between specific dates and specific events
#   - Compute the aspect rate for each claimed category
#   - Build a null distribution of rates
# ─────────────────────────────────────────────
print(f"\n\nRunning {N_BOOTSTRAP:,} bootstrap iterations...\n")

bootstrap_rates = defaultdict(list)

all_labels_by_col = {col: actual_aspects[col][:] for col in ASPECT_COLS}

for b in range(N_BOOTSTRAP):
    # Shuffle each aspect column independently (year/month/day destruction
    # equivalent — we're shuffling which planetary geometry goes with which event)
    shuffled = {}
    for col in ASPECT_COLS:
        perm = all_labels_by_col[col][:]
        random.shuffle(perm)
        shuffled[col] = perm

    for asp, cats in TRADITIONAL_CLAIMS.items():
        rate, _ = rate_for_category(shuffled[asp], event_types, set(cats), 'hard')
        bootstrap_rates[asp].append(rate)

    if (b + 1) % 2000 == 0:
        print(f"  {b+1:,} / {N_BOOTSTRAP:,} done...")

print("\nBootstrap complete.\n")

# ─────────────────────────────────────────────
# 5. STATISTICAL SUMMARY
# ─────────────────────────────────────────────
print("=" * 65)
print("BOOTSTRAP RESULTS")
print("=" * 65)

results = {}
for asp, cats in TRADITIONAL_CLAIMS.items():
    obs_rate = observed[asp]['rate']
    boot = np.array(bootstrap_rates[asp])
    boot_mean = boot.mean()
    boot_std  = boot.std()
    # One-tailed p-value: fraction of bootstrap samples >= observed
    p_value = np.mean(boot >= obs_rate)
    # Effect size: (obs - boot_mean) / boot_std
    z = (obs_rate - boot_mean) / boot_std if boot_std > 0 else 0.0
    # 95% CI of bootstrap null
    ci_lo, ci_hi = np.percentile(boot, [2.5, 97.5])

    results[asp] = {
        'obs': obs_rate, 'boot_mean': boot_mean, 'boot_std': boot_std,
        'p': p_value, 'z': z, 'ci_lo': ci_lo, 'ci_hi': ci_hi,
        'n': observed[asp]['n'], 'base': observed[asp]['base'],
        'cats': cats
    }

    sig = "✅ p < 0.05" if p_value < 0.05 else ("⚠️  p < 0.10" if p_value < 0.10 else "❌ n.s.")
    print(f"\n  {asp}")
    print(f"    Observed rate      : {obs_rate:.4f} ({obs_rate*100:.1f}%)")
    print(f"    Bootstrap mean     : {boot_mean:.4f} ({boot_mean*100:.1f}%)")
    print(f"    Bootstrap 95% CI   : [{ci_lo:.4f}, {ci_hi:.4f}]")
    print(f"    Z-score            : {z:+.3f}")
    print(f"    P-value (1-tail)   : {p_value:.4f}  {sig}")
    print(f"    Base rate          : {observed[asp]['base']:.4f}")

# ─────────────────────────────────────────────
# 6. CATEGORY BREAKDOWN — Saturn-Pluto per event type
# ─────────────────────────────────────────────
print("\n\n" + "=" * 65)
print("SATURN-PLUTO HARD ASPECT RATE BY EVENT CATEGORY")
print("=" * 65)
sp_labels = actual_aspects['Saturn_Pluto']
sp_base = sum(1 for l in sp_labels if l in HARD) / len(sp_labels)
print(f"  Overall base rate: {sp_base:.4f} ({sp_base*100:.1f}%)\n")

cat_results = {}
for cat in sorted(set(event_types)):
    idxs = [i for i, t in enumerate(event_types) if t == cat]
    if len(idxs) < 5:
        continue
    hits = sum(1 for i in idxs if sp_labels[i] in HARD)
    rate = hits / len(idxs)
    # bootstrap p for this category
    boot_cat = []
    for b in range(2000):
        perm = sp_labels[:]
        random.shuffle(perm)
        h = sum(1 for i in idxs if perm[i] in HARD)
        boot_cat.append(h / len(idxs))
    p = np.mean(np.array(boot_cat) >= rate)
    cat_results[cat] = {'rate': rate, 'n': len(idxs), 'p': p}
    sig = "✅" if p < 0.05 else ("⚠️ " if p < 0.10 else "  ")
    print(f"  {sig} {cat:20s}: {rate:.4f} ({rate*100:.1f}%)  n={len(idxs):3d}  p={p:.4f}")

# ─────────────────────────────────────────────
# 7. PLOTS
# ─────────────────────────────────────────────
def savefig(name):
    path = os.path.join(SCRIPT_DIR, name)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nSaved: {name}")

COLORS = {'war': '#c0392b', 'battle': '#e74c3c', 'revolution': '#e67e22',
          'political': '#2980b9', 'economic': '#27ae60', 'tech': '#8e44ad',
          'disaster': '#7f8c8d', 'epidemic': '#16a085', 'other': '#95a5a6'}

# Plot 1 — Bootstrap null distributions with observed values
fig, axes = plt.subplots(4, 2, figsize=(14, 16))
axes = axes.flatten()
asp_list = list(TRADITIONAL_CLAIMS.keys())

for i, asp in enumerate(asp_list):
    ax = axes[i]
    r = results[asp]
    boot = np.array(bootstrap_rates[asp])
    ax.hist(boot, bins=50, color='#4a90d9', alpha=0.7, edgecolor='white', density=True)
    ax.axvline(r['obs'], color='#c0392b', linewidth=2.5, label=f"Observed: {r['obs']:.3f}")
    ax.axvline(r['boot_mean'], color='#2c3e50', linewidth=1.5, linestyle='--', alpha=0.7,
               label=f"Bootstrap mean: {r['boot_mean']:.3f}")
    ax.axvspan(r['ci_lo'], r['ci_hi'], alpha=0.15, color='steelblue', label='95% CI')
    sig_str = f"p={r['p']:.3f}" + (" ✅" if r['p'] < 0.05 else "")
    ax.set_title(f"{asp.replace('_','-')}  ({sig_str})", fontsize=10, fontweight='bold')
    ax.set_xlabel('Hard aspect rate in claimed categories')
    ax.set_ylabel('Density')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.2)

plt.suptitle('Project 19: Bootstrap Null Distributions vs Observed Rates\n'
             f'(N={N_BOOTSTRAP:,} permutations — hard aspects in claimed event categories)',
             fontsize=12, y=1.01)
plt.tight_layout()
savefig('plot_p19_bootstrap_distributions.png')

# Plot 2 — Z-scores summary bar chart
fig, ax = plt.subplots(figsize=(12, 5))
asp_labels_short = [a.replace('_', '-') for a in asp_list]
z_scores = [results[a]['z'] for a in asp_list]
colors = ['#27ae60' if z > 1.65 else ('#e67e22' if z > 1.0 else '#bdc3c7') for z in z_scores]
bars = ax.bar(asp_labels_short, z_scores, color=colors, edgecolor='white')
ax.axhline(1.645, color='#27ae60', linewidth=1.5, linestyle='--', label='p=0.05 (one-tail)')
ax.axhline(1.282, color='#e67e22', linewidth=1.2, linestyle=':', label='p=0.10')
ax.axhline(0, color='black', linewidth=0.8)
ax.set_ylabel('Z-score (observed vs bootstrap null)')
ax.set_title('Traditional Mundane Claims: Z-scores Against Bootstrap Baseline')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.2, axis='y')
for bar, z in zip(bars, z_scores):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            f'{z:+.2f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
savefig('plot_p19_z_scores.png')

# Plot 3 — Saturn-Pluto rate by event category
fig, ax = plt.subplots(figsize=(13, 5))
cats_sorted = sorted(cat_results.keys(), key=lambda c: -cat_results[c]['rate'])
rates_plot  = [cat_results[c]['rate'] for c in cats_sorted]
ns_plot     = [cat_results[c]['n'] for c in cats_sorted]
ps_plot     = [cat_results[c]['p'] for c in cats_sorted]
bar_colors  = ['#c0392b' if p < 0.05 else ('#e67e22' if p < 0.10 else '#bdc3c7')
               for p in ps_plot]
bars = ax.bar(cats_sorted, rates_plot, color=bar_colors, edgecolor='white')
ax.axhline(sp_base, color='#2c3e50', linewidth=2, linestyle='--',
           label=f'Overall base rate: {sp_base:.2f}')
ax.set_ylabel('Saturn-Pluto hard aspect rate')
ax.set_title('Saturn-Pluto Hard Aspect Rate by Event Category\n(red = p<0.05, orange = p<0.10 vs bootstrap)')
ax.set_xticklabels(cats_sorted, rotation=30, ha='right')
ax.legend()
ax.grid(True, alpha=0.2, axis='y')
for bar, n, r in zip(bars, ns_plot, rates_plot):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
            f'n={n}\n{r:.2f}', ha='center', va='bottom', fontsize=8)
plt.tight_layout()
savefig('plot_p19_saturn_pluto_by_category.png')

# Plot 4 — All aspect hard rates heatmap by event category
asp_plot_list = ['Saturn_Pluto', 'Uranus_Pluto', 'Saturn_Neptune',
                 'Jupiter_Uranus', 'Saturn_Uranus', 'Jupiter_Saturn']
cat_list = [c for c in sorted(set(event_types))
            if sum(1 for t in event_types if t == c) >= 5]

matrix = np.zeros((len(asp_plot_list), len(cat_list)))
for i, asp in enumerate(asp_plot_list):
    labels = actual_aspects[asp]
    for j, cat in enumerate(cat_list):
        idxs = [k for k, t in enumerate(event_types) if t == cat]
        hits = sum(1 for k in idxs if labels[k] in HARD)
        matrix[i, j] = hits / len(idxs) if idxs else 0.0

fig, ax = plt.subplots(figsize=(15, 6))
im = ax.imshow(matrix, cmap='RdYlGn', vmin=0, vmax=0.6, aspect='auto')
ax.set_xticks(range(len(cat_list)))
ax.set_xticklabels(cat_list, rotation=35, ha='right', fontsize=9)
ax.set_yticks(range(len(asp_plot_list)))
ax.set_yticklabels([a.replace('_', '-') for a in asp_plot_list], fontsize=10)
ax.set_title('Hard Aspect Rate by Aspect Pair × Event Category\n(green = high rate, red = low rate; white dashes = base rate zones)')
for i in range(len(asp_plot_list)):
    for j in range(len(cat_list)):
        ax.text(j, i, f'{matrix[i,j]:.2f}', ha='center', va='center', fontsize=8)
plt.colorbar(im, ax=ax, label='Hard aspect rate')
plt.tight_layout()
savefig('plot_p19_aspect_category_heatmap.png')

# ─────────────────────────────────────────────
# 8. SAVE RESULTS CSV
# ─────────────────────────────────────────────
with open(os.path.join(SCRIPT_DIR, 'bootstrap_results.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['aspect', 'claimed_categories', 'n_events', 'observed_rate',
                     'bootstrap_mean', 'bootstrap_std', 'ci_lo_95', 'ci_hi_95',
                     'z_score', 'p_value_1tail', 'significant_p05',
                     'overall_base_rate', 'ratio_obs_to_base'])
    for asp in asp_list:
        r = results[asp]
        writer.writerow([
            asp, ';'.join(r['cats']), r['n'],
            f"{r['obs']:.6f}", f"{r['boot_mean']:.6f}", f"{r['boot_std']:.6f}",
            f"{r['ci_lo']:.6f}", f"{r['ci_hi']:.6f}",
            f"{r['z']:.4f}", f"{r['p']:.4f}",
            'YES' if r['p'] < 0.05 else 'NO',
            f"{r['base']:.6f}",
            f"{r['obs']/r['boot_mean']:.4f}" if r['boot_mean'] > 0 else 'N/A'
        ])

print("\nSaved: bootstrap_results.csv")

# ─────────────────────────────────────────────
# 9. FINAL SUMMARY
# ─────────────────────────────────────────────
print("\n\n" + "=" * 65)
print("FINAL SUMMARY")
print("=" * 65)
sig_count = sum(1 for r in results.values() if r['p'] < 0.05)
trend_count = sum(1 for r in results.values() if 0.05 <= r['p'] < 0.10)
print(f"\nOf {len(results)} traditional claims tested:")
print(f"  Significant (p < 0.05) : {sig_count}")
print(f"  Trend (p < 0.10)       : {trend_count}")
print(f"  Null (p >= 0.10)       : {len(results) - sig_count - trend_count}")
print()
for asp in sorted(results.keys(), key=lambda a: results[a]['p']):
    r = results[asp]
    mark = "✅" if r['p'] < 0.05 else ("⚠️ " if r['p'] < 0.10 else "❌")
    print(f"  {mark} {asp:25s}  z={r['z']:+.3f}  p={r['p']:.4f}")
print()
print("All done. ✓")
