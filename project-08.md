# Project 08: Tropical vs. Sidereal Zodiac — An Empirical Comparison

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Which zodiac system is empirically better for profession prediction: the **Tropical** zodiac (seasonal, tied to the Spring Equinox) or the **Sidereal** zodiac (constellation-based, tied to the fixed stars)? And is the Sun Sign — astrology's most iconic feature — actually doing any useful predictive work?

---

## 💡 Why This Matters

Astrology has an internal fault line that most public discussions ignore. Western astrology uses the Tropical zodiac, where 0° Aries is defined as the Spring Equinox — it's a seasonal calendar. Vedic/Jyotish astrology uses the Sidereal zodiac, where 0° Aries is defined by the position of the first stars in the Aries constellation.

Due to Earth's axial precession — the 26,000-year wobble that slowly shifts the equinoxes through the constellations — these two systems have diverged by approximately **24 degrees**. That means roughly 80% of people born today have a different Sun sign in the Sidereal system than in the Tropical. When a Western astrologer says "you're a Scorpio," a Vedic astrologer looking at the same chart says "you're a Libra." Both can't be right.

This project tests them directly against observable outcomes. One clear test: which zodiac's Sun Sign placement better predicts professional category?

---

## 📊 The Data

86 verified celebrities from Project 06, across 6 professional categories. Leave-One-Out Cross Validation throughout.

**Baseline:** The largest category ("Arts") accounts for 24.4% of observations. A classifier that always guesses "Arts" achieves 24.4% — the floor below which a model is less useful than no model at all.

The Lahiri ayanamsa (2025 value: 24.21°) is used for Sidereal calculations, consistent with the Government of India standard.

---

## 🔬 Method

Three progressive experiments:

1. **Sun Sign alone** — can knowing only which of 12 signs the Sun occupies predict profession?
2. **Harmonics + Sun Sign** — does adding Sun Sign improve models that already include Project 06's harmonic features?
3. **Full chart** — all nine traditional planets (Sun through Pluto + Nodes) as sign placements

All models validated with Leave-One-Out Cross Validation.

---

## 📈 Results

### Experiment 1: Sun Sign Alone as Profession Predictor

| Zodiac System | LOO-CV Accuracy | vs. 24.4% Baseline |
|---|---|---|
| **Tropical** | **17.1%** | **−7.3% (worse than guessing)** |
| **Sidereal Lahiri** | **17.1%** | **−7.3% (worse than guessing)** |
| **Sidereal Fagan-Bradley** | **15.9%** | **−8.5% (worse than guessing)** |

**All three systems performed worse than simply guessing the most common category.** Knowing someone's Sun sign — in any zodiac — makes you *less* likely to correctly guess their profession than ignoring it entirely.

The exact tie between Tropical and Sidereal Lahiri at 17.1% is not a coincidence — it reflects symmetric error exchange. When the sidereal shift reassigns a celebrity from one sign to another, it may correctly reclassify one person while misclassifying another. The errors trade symmetrically, leaving overall accuracy unchanged.

### Experiment 2: Harmonics + Sun Sign

| Model | Features | Accuracy | Beat Baseline (24.4%)? |
|---|---|---|---|
| Baseline | H4, H5, H7 only | 15.1% | No |
| Tropical | Harmonics + Tropical Sun Sign | 15.1% | No |
| Sidereal Lahiri | Harmonics + Sidereal Sun Sign | 17.4% | No |

Adding Tropical Sun Sign to harmonics: zero lift. Adding Sidereal Sun Sign: +2.3% lift, still well below the naive baseline.

### Experiment 3: Full Chart — The "Graha Shootout"

| System | Features | Accuracy | Beat Baseline (24.4%)? |
|---|---|---|---|
| Tropical Full | 9 signs + Harmonics | 20.9% | **No** (−3.5%) |
| **Sidereal Full** | **9 signs + Harmonics** | **26.7%** | **Yes (+2.3%)** |

For the first time, a zodiac-based model beats random guessing: Sidereal Full Chart achieves 26.7%, narrowly above the 24.4% baseline. Tropical Full Chart remains below it.

**Feature Importance — Which Planet Drives the Sidereal Edge?**

| Rank | Planet | Importance | Note |
|---|---|---|---|
| 1 | **Mercury** | 0.1048 | Communication, skill, intellect |
| 2 | **Mars** | 0.1042 | Drive, energy — separates Athletes |
| 3 | Jupiter | 0.0941 | Expansion |
| 4 | Saturn | 0.0897 | Structure |
| 5 | Moon | 0.0879 | Emotional orientation |
| 6 | Venus | 0.0831 | Aesthetics |
| 7 | Rahu (N. Node) | 0.0803 | — |
| **8** | **Sun** | **0.0797** | **Last among major bodies** |

**The Sun — astrology's most famous feature, the basis of all sun-sign horoscopes — ranks last among the nine traditional bodies in prediction importance.** Mercury and Mars do the most work.

---

## 🔍 What the Numbers Mean

The Tropical vs. Sidereal debate resolves into a nuanced answer: neither system's Sun Sign contains useful profession information. Both perform worse than guessing. But when the full chart is used, the Sidereal system shows a marginal advantage (26.7% vs. 20.9%).

More importantly: the Sun Sign being worst, and Mercury/Mars being best, suggests that the information content in astrological charts — if any exists — lies in the faster-moving personal planets, not in the annual solar cycle that drives popular astrology.

The Sun sign is what everyone knows. It is what horoscope columns are built on. It is astrology's public face. And in this dataset, it is the least predictive feature in the entire chart.

---

## ⚠️ Limitations & Caveats

- N=86 produces wide confidence intervals on LOO-CV accuracy (~±10 pp at 95%). The Sidereal 2.3% advantage over the naive baseline is not independently significant.
- Multiple comparisons: three zodiac systems × three experiments = nine hypothesis tests. No Bonferroni correction would elevate the marginal Sidereal result to significance.
- Generational confound: outer planet sign placements are correlated with birth era. Mercury and Mars results are less contaminated by this.
- The 86 celebrities are not representative of any general population. Fame is a filter.

---

## 🌟 Conclusion

The Tropical vs. Sidereal debate — a centuries-old schism in astrology — yields a clear empirical answer for profession prediction by Sun Sign alone: **neither system contains meaningful information**. Both perform worse than random guessing.

When extended to full-chart analysis, the Sidereal system shows a marginal advantage (26.7% vs. 20.9%). The finding is small and statistically fragile — but consistent.

The deeper insight: **the Sun, astrology's most public symbol, is the least predictive planet in the chart.** The signal, if it exists anywhere, lives in Mercury (how someone thinks) and Mars (how someone acts). Not in the annual cycle that tells you you're a Sagittarius.

> **What's next:** Testing Sidereal full-chart predictions on a larger, pre-registered dataset with birth-year-controlled samples to eliminate the generational confound from outer planet signs.
