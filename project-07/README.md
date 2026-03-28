# Project 07: Machine Learning and Planetary Cycles

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com](https://bigastrologybook.com)

---

## 🌟 Overview — What We Asked

Two distinct questions tested under one umbrella:

1. **Cyclic Age Hypothesis:** Do planetary return cycles (Saturn at 29.5 years, Jupiter at 11.9 years, Lunar Nodes at 18.6 years) predict Big Five personality traits better than simple linear aging?
2. **Profession Classification:** Can a birth chart predict what professional field someone belongs to, better than chance?

---

## 💡 Why This Matters

The Saturn Return — the moment around ages 29 and 58 when Saturn completes a full orbit and returns to its birth position — is one of astrology's most famous concepts. It's supposed to mark a developmental threshold, a moment of reckoning and maturity. If Saturn Returns genuinely shape personality, that pattern should be visible in a large personality dataset.

For the second question: if planetary patterns carry real career information, a machine learning classifier trained on birth charts should outperform random guessing at profession prediction. The result turns out to be nuanced — and raises an important question about what "prediction" actually means when outer planets are involved.

---

## 📊 The Data

| Dataset | Source | N | What It Provides |
|---|---|---|---|
| Big Five Personality | OpenPsychometrics (IPIP-NEO-300) | 19,632 | E/N/A/C/O scores + birth year |
| Verified Celebrity Charts | Project 06 dataset | 82 | Full natal charts + professional category |

The Big Five dataset provides personality scores with only birth *year*, not full birth date. This is a critical constraint: without month and day, only slow outer planets (Jupiter through Pluto) can be meaningfully analyzed. Inner planets cycle faster than a year and can't be pinned down from annual data.

The celebrity dataset provides full birth dates and times with known professional categories — appropriate for the classification experiment.

---

## 🔬 Method

**Experiment 1 — Cyclic Age:** From each person's birth year, compute Saturn cycle phase (0–1 over 29.5 years), Jupiter cycle phase, and Nodal cycle phase. Test whether these cyclic variables predict Big Five traits better than simple linear age.

**Experiment 2 — Profession Classification:** Train a Random Forest classifier on full birth chart features (planetary signs encoded as sin/cos components, element counts, mode counts). Validate using Leave-One-Out Cross Validation (LOO-CV) — each chart is tested against a model trained on all the others.

---

## 📈 Results

### Experiment 1: Cyclic Age — Null

| Trait | Linear Age R² | Cyclic Age R² | Delta |
|---|---|---|---|
| Conscientiousness | 0.0514 | 0.0507 | −0.0007 |
| Neuroticism | 0.0234 | 0.0235 | +0.0001 |
| Extraversion | ~0.02 | ~0.02 | ≈ 0 |
| Agreeableness | ~0.02 | ~0.02 | ≈ 0 |
| Openness | ~0.02 | ~0.02 | ≈ 0 |

Adding cyclic planetary phases over linear age provides effectively zero additional predictive power for any Big Five trait. The Saturn Return (ages 29 and 58) shows no statistical spike in Neuroticism or Conscientiousness compared to adjacent ages.

The personality R² values themselves (0.02–0.05) are small but typical for age-personality research — age predicts some variance in maturity-related traits like Conscientiousness, but most personality variance is explained by other factors.

### The Saturn Opposition Dip

While the global model comparison showed no improvement, closer inspection of Conscientiousness residuals revealed a localized pattern at the **Saturn Opposition** (~ages 14, 44, and 73 — the *midpoint* of the cycle, not the Return):

| Saturn Cycle Phase | Conscientiousness Deviation |
|---|---|
| 0.40–0.45 (pre-Opposition) | Above expected |
| **0.50–0.55 (Opposition)** | **−0.59 points below expected** |
| 0.60–0.65 (post-Opposition) | Above expected |

This "Mid-Cycle Crisis" is unconventional — traditional astrology emphasizes the Saturn *Return*, not the Opposition. Yet the data hints that the midpoint may correspond to the adolescent and midlife periods when discipline is most under stress. The effect is small (~0.59 points on a 10–50 scale) and requires formal p-value calculation before it's treated as more than exploratory.

### Experiment 2: Profession Classification — Modest Above Chance

| Metric | Score |
|---|---|
| **LOO-CV Accuracy** | **29.3%** |
| **Baseline (random guessing, 6 classes)** | **15.8%–16.7%** |
| **Lift** | **1.85× better than chance** |

The classifier correctly identifies profession at 29.3% — about 75% better than guessing. Wrong 70.7% of the time, but statistically above chance.

**Top predictive features:**

| Rank | Feature | Interpretation |
|---|---|---|
| 1 | Pluto position | **Generational proxy** — tags the historical era |
| 2 | Neptune position | Same generational confound |
| 3 | Mars position | Drive and energy — separates Athletes from Artists |
| 4 | Jupiter position | Expansion |
| 5 | Uranus position | Innovation |

The top two features (Pluto and Neptune signs) are essentially age proxies. Pluto stays in one sign 12–20 years; Neptune stays 14 years. Scientists born in 1940 share the same Pluto sign but also share the same cultural and institutional context. The classifier may be detecting historical patterns in *who became famous in which category* — not anything intrinsic to the chart.

Mars placement (rank 3) is not confounded by generation in the same way (Mars changes sign every ~45 days) and aligns with Project 06's finding that Mars carries real signal in astrological data.

![Feature importance plot for Random Forest profession classifier](images/project-07-figure-1.png)

---

## 🔍 What the Numbers Mean

**Experiment 1 (null):** Cyclic planetary phases add nothing to personality prediction beyond simple linear age. The Saturn Return has no detectable personality signature in 19,632 people.

**Experiment 2 (modest above-chance):** A 29.3% accuracy on 6-class profession prediction is real but heavily confounded by generational outer planet patterns. Strip the confound and the result likely shrinks substantially. The Mars signal is the most interesting lead — not confounded by generation, consistent with Project 06.

---

## ⚠️ Limitations & Caveats

- **Annual resolution (Experiment 1):** Inner planet cycles can't be tested on birth-year-only data. The null result for cyclic age applies only to outer planets.
- **Generational confound (Experiment 2):** The classifier's top features are essentially birth-year proxies. A true test would need to partial out this confound by testing within narrow birth-year cohorts.
- **Small N for classification (N=82):** LOO-CV on 82 observations produces wide confidence intervals (~±10 percentage points at 95%).
- **Multiple testing (Experiment 1):** Five Big Five traits tested; no corrections needed since nothing approached significance.

---

## 🌟 Conclusion

**Cyclic age is null:** Saturn return cycles add nothing to Big Five personality prediction over simple linear aging. The legendary Saturn Return has no detectable personality signature at N=19,632.

**Profession classification is above chance, but confounded:** 29.3% vs. 16.7% random is real — but likely reflects historical era patterns in outer planet positions, not genuine astrological career signal. The Mars feature is the most interesting: not confounded by generation, and consistent with harmonic analysis in Project 06.

The methodological lesson: annual-resolution data is insufficient for inner-planet research. Future work needs full birth dates, birth times, and should partial out the generational confound by testing within narrow birth-year cohorts.
