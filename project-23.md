# Project 23: Birth Chart Similarity and Career Outcomes

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Do individuals in the same professional field have more similar planetary sign placements than individuals from different fields? Can chart similarity predict career category better than chance?

---

## 💡 Why This Matters

Most astrological career research asks: "Does sign X predict trait Y?" This project takes a different approach: rather than testing specific astrological rules, it asks whether people in the same profession tend to *share chart features* — an agnostic, data-driven question that bypasses prescriptive zodiac symbolism entirely.

The methodology — cosine similarity between full one-hot-encoded planetary vectors — preserves more information than traditional sun-sign analysis. Pairwise within-group vs. between-group comparison is the correct statistical framework for clustering questions.

---

## 📊 The Data

| Field | Detail |
|---|---|
| **Sample** | **95 unique individuals** across 8 career categories |
| **Categories** | Tech, Music, Science, Arts, Politics, Sports, Literature, Philosophy |
| **Source** | Merged dataset: 24 manually selected celebrities + extended celebrity database |
| **Planets** | 11 bodies: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, North Node |
| **Zodiacs** | Both Tropical and Vedic (Lahiri ayanamsha) analyzed separately |

Each person's astrological fingerprint: 11 planets × 12 one-hot-encoded sign positions = **132-element binary vector**.

**Similarity Metric:** Cosine similarity between all pairs of vectors. Higher values = more similar planetary sign distributions.

---

## 📈 Results

| Zodiac System | Within-Group Mean | Between-Group Mean | p-value | Conclusion |
|---|---|---|---|---|
| **Tropical** | 0.1015 | 0.0920 | 0.061 | Not significant (near-miss) |
| **Vedic (Lahiri)** | **0.1123** | **0.0920** | **0.000086** | **SIGNIFICANT** |

### Tropical: Near-Miss

Same-career individuals show slightly higher Tropical chart similarity (0.1015) than cross-career pairs (0.0920), but the difference doesn't reach p < 0.05 (p = 0.061). This is a near-miss that could reflect genuine weak clustering or statistical noise.

### Vedic: Statistically Significant Signal

The Vedic (Sidereal) analysis shows a **statistically significant difference** (p < 0.0001): people in the same career field have more similar planetary sign distributions than people in different fields.

The effect is modest but real:
- Within-group mean cosine: **0.112**
- Between-group mean cosine: **0.092**
- Difference: +0.020 (approximately **22% higher within-group similarity**)

With N=95 and thousands of pairwise comparisons, the signal is robust to sampling variation.

![Cosine similarity heatmap: within-career vs. cross-career pairs, Vedic zodiac](images/project-23-figure-1.png)

---

## 🔍 Interpreting the Vedic Signal — With Caveats

Several important caveats must be addressed before treating this as evidence for astrological career influence:

**1. Generational clustering:** Some career categories naturally concentrate births in certain decades (Tech pioneers in 1940–1960; modern musicians more recently). Slow-moving outer planets (Jupiter through Pluto) occupy the same signs for years. If Tech founders and Scientists cluster in similar birth decades, their outer planet signs will be similar — not because of career influence, but because of shared birth era. This is the same confound identified in Projects 10 and 26.

**2. Selection bias:** The celebrity dataset is dominated by historically prominent individuals — not a random sample of professionals. Chart features that cluster among highly successful musicians may differ from those among average musicians.

**3. Multiple testing:** Two zodiac systems × multiple career-category comparisons = several tests. The Vedic result (p < 0.001) survives a Bonferroni correction for two systems, but not if subcategory analyses are included.

**4. What "similarity" measures:** Cosine similarity of one-hot-encoded signs is agnostic but imprecise. It doesn't distinguish tight conjunctions from coincidentally shared signs due to generational position.

---

## 🔬 What a Better Study Would Do

1. **Use AstroDatabank** — thousands of profession-tagged charts with verified birth data
2. **Control for birth decade** — focus on fast-moving personal planets (Sun, Moon, Mercury, Venus, Mars) that can't be explained by generational cohort effects
3. **Run permutation tests** — shuffle profession labels 10,000 times to build a null distribution that respects the astronomical structure of the data
4. **Replicate across zodiac systems** — confirm whether the Vedic advantage persists with a larger sample

---

## 🌟 Conclusion

Pairwise cosine similarity analysis of 95 celebrity charts finds a **statistically significant clustering of planetary sign patterns within career categories in the Vedic zodiac** (p < 0.0001), with a modest effect (~22% higher within-group similarity than between-group). The Tropical zodiac shows a near-significant trend (p = 0.061).

These findings do not establish astrological causation. The most likely explanation is (a) generational birth-date clustering producing shared outer-planet positions, and/or (b) a genuine but small astrological signal requiring larger, better-controlled replication to characterize.

What is established: the similarity-based methodology is sound, detects structure in the data, and points toward the generational confound as the critical variable to control in future work.
