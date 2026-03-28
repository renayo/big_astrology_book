# Project 14: Essential Dignities — Tropical vs. Sidereal

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Does the ancient system of Essential Dignities — scoring planetary "strength" based on sign placement — predict professional excellence? And does the choice of zodiac (Tropical vs. Sidereal) dramatically change who has a "strong" or "weak" chart?

---

## 💡 Why This Matters

Essential Dignities are the original astrological scoring system. They descend from Ptolemy and Hellenistic tradition: each planet is "strong" in certain signs (its Domicile and Exaltation) and "weak" in others (its Detriment and Fall). A chart full of dignified planets should, by traditional theory, describe a capable, fortunate person.

This project tests that claim directly on performers and scientists. The result is one of the book's most counterintuitive: not only do the scores fail to predict success in the expected direction, but the Tropical and Sidereal systems produce wildly different assessments of the same chart — sometimes inverting from deeply debilitated to strongly dignified.

The practical question the divergence raises: if two zodiac systems produce opposed assessments of the same person, can either be measuring something real?

---

## 📊 The Data

- **Celebrity cohort:** 52 individuals — 31 performers, 21 scientists
- **Subset of:** Project 13's celebrity dataset; verified birth dates
- **Dignity tables:** Ptolemaic tradition (domicile, exaltation, detriment, fall)
- **Scoring:** +5 (Domicile), +4 (Exaltation), 0 (Peregrine), −4 (Fall), −5 (Detriment)
- **Calculation:** Swiss Ephemeris, Lahiri ayanamsha for Sidereal

---

## 📈 Results

### 1. Overall Dignity Scores

Both systems produce slightly negative averages across all 52 celebrities:

| Cohort | Tropical Mean | Sidereal Mean |
|---|---|---|
| All Celebrities (N=52) | −1.08 | −0.54 |

Famous people are not astrologically "strong" by traditional standards. This is already striking — if dignified charts predicted celebrity achievement, the average should be positive.

### 2. The Scientist Shift (p = 0.042)

| Profession | N | Tropical Mean | Sidereal Mean | p-value |
|---|---|---|---|---|
| Performers | 31 | +0.22 | −1.38 | 0.455 |
| **Scientists** | **21** | **−3.15** | **+0.80** | **0.042** |

Scientists have strongly *debilitated* charts in the Tropical system (mean −3.15) but shift to *positive* territory in the Sidereal system (mean +0.80). The difference is statistically significant.

**What this means:** The same group of scientists looks like a collection of astrologically "weak" charts in Western astrology, but looks like a collection of "strong" charts in Vedic astrology. The 24° zodiac shift completely reverses the apparent astrological assessment.

Performers show no significant difference between systems (p = 0.455) — the zodiac choice matters more for scientists than performers in this sample.

> *Statistical caveat: N=21 scientists provides low power. This test was not pre-registered, and represents 1 of 28 possible profession × zodiac combinations. One result at p=0.042 across 28 tests is approximately what chance predicts.*

### 3. Individual Chart Reversals

The 24° shift is large enough to completely invert some charts:

| Name | Tropical Score | Sidereal Score | Δ Change |
|---|---|---|---|
| **George Carlin** | −13 | **+13** | +26 |
| Prince | +15 | −10 | −25 |
| Taylor Swift | +19 | −5 | −24 |
| Paul McCartney | +14 | −9 | −23 |
| **Richard Feynman** | −15 | **+7** | +22 |
| Nikola Tesla | −5 | +10 | +15 |
| Michael Jackson | −5 | +10 | +15 |

**Richard Feynman** — a Nobel laureate and one of the most celebrated physicists of the 20th century — has the *most debilitated* Tropical chart in the dataset (−15). In Sidereal, he shifts to positive territory (+7). **George Carlin** swings from −13 to +13 — a 26-point reversal.

**Taylor Swift** has the most dignified Tropical chart (+19) but drops to mildly debilitated in Sidereal (−5).

These reversals are not edge cases. They affect some of the most recognizable names in each group. They demonstrate concretely what the Tropical/Sidereal schism means in practice: astrological "strength" is not a property of a person's birth — it is a function of which coordinate system you use.

---

## 🔍 What the Numbers Mean

The scientist-specific finding creates a genuine puzzle. If Essential Dignities measure something real about capacity or destiny, then:

1. **If Tropical is correct** — Taylor Swift's +19 predicts her success, but Richard Feynman's −15 is an unexplained failure to predict a Nobel laureate's genius
2. **If Sidereal is correct** — Feynman's +7 makes more sense, but Taylor Swift's −5 becomes harder to explain
3. **If neither system captures what it claims** — dignity scores don't predict success in either zodiac

The scientist-specific finding aligns with the **Hardship Hypothesis** running through Projects 06, 20, and 33: scientists' charts being most debilitated in Tropical astrology flatly contradicts the "strong planets = capable person" narrative. The most intellectually accomplished group in the sample has the *lowest* mean dignity score in the zodiac system most commonly used in Western practice.

---

## ⚠️ Limitations & Caveats

- N=21 scientists is small. The p=0.042 result represents 1 of ~28 implicit tests — approximately what chance predicts at α=0.05.
- This was not pre-registered. All interpretations are post-hoc.
- The 52-celebrity sample is not representative of any population; selection bias from fame is present.

---

## 🌟 Conclusion

This project doesn't establish that Essential Dignities predict success. What it establishes:

1. **The zodiac choice radically changes individual chart assessments** — by as much as 26 dignity points for the same person
2. **Scientists have strongly debilitated Tropical charts** (mean −3.15), which directly contradicts the dignity-equals-success narrative
3. **In Sidereal, scientists' charts shift to positive territory** (mean +0.80) — a borderline result (p=0.042) requiring replication with N≥100 scientists
4. **Performers show no significant difference between systems**

Whether the Sidereal shift "works better" for scientists, or whether this is a small-sample artifact, remains open. A replication with 100+ scientists would settle it.
