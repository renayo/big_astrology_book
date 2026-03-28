# Project 26: Compatibility and Relationship Survival

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Does an aggregate "astrological compatibility score" — the sum of cosine similarities across all pairwise planetary interactions between two birth charts — predict relationship survival? Do couples with higher scores divorce less and stay together longer?

This is the definitive test of the compatibility scoring concept at the heart of most astrology apps and services.

---

## 💡 Why This Matters

Pop astrology apps output a single compatibility percentage. Match.com-style astrological filters operate on similar logic. Millions of people use these scores to evaluate potential partners, feel reassured or concerned about existing relationships, and make real decisions.

The aggregate compatibility score concept deserves a rigorous test. This project builds the most defensible version of such a score — a mathematically rigorous, agnostic sum of cosine similarities across 100 planetary pair combinations — and tests it against 2,722 couples' relationship timelines.

The result is one of the book's most decisive findings.

---

## 📊 The Data

| Source | Description |
|---|---|
| Wikidata | Spouse pairs with verified birth dates; relationship start/end dates; N = 2,722 couples |
| Swiss Ephemeris | Full planetary positions for all birth dates |
| `lifelines` (Python) | Kaplan-Meier survival estimation |
| scikit-learn ElasticNet | Regularized regression to identify best-fit predictors |

**The Compatibility Score:**
Interaction(P1, P2) = cos(θ_{P1,person1} − θ_{P2,person2})

- **+1.0** = Conjunction (maximum "harmony")
- **−1.0** = Opposition (maximum "tension")

The **Total Harmonic Score** sums this across all 100 planetary pair combinations, producing a single aggregate compatibility number. This is the rigorous mathematical equivalent of what astrology apps produce.

---

## 📈 Results

### The Core Finding: r = 0.009

**Aggregate compatibility score correlation with relationship duration:**

> **r ≈ 0.009** (N = 2,722)

A Pearson correlation of 0.009 is, for practical purposes, zero. The aggregate compatibility score explains less than **0.01% of variance** in relationship duration. This is one of the book's most decisive null results.

### Kaplan-Meier Survival Analysis

Couples were split at the median Total Harmonic Score (top 50% = "High Compatibility"; bottom 50% = "Low Compatibility"):

| Group | 5-Year Survival Rate |
|---|---|
| High Compatibility (Top 50%) | **88.1%** |
| Low Compatibility (Bottom 50%) | **87.9%** |

The two survival curves overlap **perfectly across all 50+ years** of relationship duration. A log-rank test finds no significant difference. High-compatibility couples and low-compatibility couples divorce at exactly the same rate.

### The "Pluto Artifact" (Experiment V4)

When outer planets were included as features, the model appeared to achieve R² = 0.08 (8% explanatory power). But this was entirely a **demographic artifact**:

- **Pluto in Libra (negative predictor)** → associated with shorter marriages
- **Pluto in Aries (positive predictor)** → associated with longer marriages

Pluto in Aries describes people born in the early 19th century; Pluto in Libra describes people born roughly 1971–1984. Historical couples (early 1800s) had longer marriages on average simply because **divorce was less common, legally more difficult, and socially stigmatized in earlier centuries**. The model learned that generation predicts marriage duration — not because of Pluto, but because of history.

### Traditional Planets Only: Near-Zero (V5)

After removing all outer planets (Uranus, Neptune, Pluto) to eliminate the demographic confound:

| Metric | Result |
|---|---|
| R² | **0.01** |
| Signal remaining | Nearly zero |

All personal planet coefficients (Venus-Mars, Sun-Moon, Mars-Mars pairs) are shrunk to near zero by ElasticNet regularization. No specific aspect type predicts relationship longevity.

### A Genuine Nuance: Specific Pair Analysis

Though the aggregate score fails entirely, a Kolmogorov-Smirnov analysis comparing long-term (>35 years) vs. short-term (<7 years) marriages found borderline-significant differences in two aspect distributions:

| Aspect | Short-Term Mean Cosine | Long-Term Mean Cosine | p-value |
|---|---|---|---|
| **Sun-Moon** | −0.06 | +0.02 | **0.027** |
| **Mars-Mars** | −0.05 | +0.05 | **0.027** |
| Venus-Mars | −0.05 | −0.00 | 0.33 (n.s.) |

Long-lasting couples show slightly more aligned Sun-Moon and Mars-Mars aspects. The effect is small but not zero — and it points to *specific pairs* carrying information that *aggregate scoring* destroys.

---

## 🔍 The Soup Metaphor: Why Aggregation Fails

This project's conceptual contribution is the **Soup Metaphor** of astrological compatibility scoring.

When you blend a cup of coffee and a glass of orange juice and a spoonful of salt into a single liquid and taste the result, you get undifferentiated mush. The coffee flavor, the citrus acidity, the salt are all present — but the blending has destroyed the differential information.

Similarly: averaging 100 planetary interactions into a single number destroys the differential information. A +1.0 Venus-Venus (deep value alignment) and a −1.0 Mars-Mars (constant friction in action and desire) *cancel out* in an aggregate score — yet both may be profoundly meaningful. The aggregate score is mathematically lossy: information that might have predictive value gets homogenized away before statistics even begin.

The Sun-Moon and Mars-Mars results above suggest that differential analysis of specific pairs preserves signal that aggregation destroys. Don't make soup. Test individual ingredients.

---

## ⚠️ Limitations & Caveats

- r = 0.009 with N = 2,722: 95% CI ≈ [−0.028, +0.046] — entirely consistent with zero
- ElasticNet R² = 0.01 with ~100 predictors: regularization correctly prevents overfitting while confirming near-zero signal
- Survival analysis did not implement censoring for partner death (Cox model needed)
- Wikidata relationship data includes entry errors and ambiguous end-dates

---

## 🌟 Conclusion

After testing aggregate compatibility scoring against N = 2,722 couples with Kaplan-Meier survival analysis, ElasticNet regression, and five experimental variants, the verdict is unambiguous:

**Aggregate astrological compatibility scoring does not predict relationship survival.** r = 0.009. High- and low-compatibility couples divorce at identical rates. Survival curves overlap perfectly.

The only apparent "signal" was a demographic artifact (Pluto generation marker). When removed, explanatory power collapses from 8% to 1%.

**The aggregate score is not just wrong — it is methodologically broken.** By summing all planetary interactions into one number, it destroys the differential information that might contain genuine signal.

The Sun-Moon and Mars-Mars borderline results suggest that specific pair analysis — not aggregate scoring — is where any true compatibility signal might live. The take-away for anyone building astrological compatibility tools: don't make soup. Test the ingredients individually.
