# Project 36: Synastry Harmonics & Logistic Regression — The Generational Confound

> **Source:** [bigastrologybook.com/project-36](https://bigastrologybook.com/project-36/)
> **Archive Date:** 2026-03-21
> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Dataset:** ~4,000 couples from Wikidata; 700+ astrological features (Tropical signs, Vedic signs, inter-chart cosine interactions); logistic regression and Random Forest models

---

## Research Question

Can a machine learning model distinguish divorced couples from still-married couples using astrological synastry features? Specifically, do the harmonic relationships between partners' planets — encoded as the cosine of inter-chart angular distances — contain predictive information about relationship outcomes?

## Hypothesis

Synastry astrology has elaborate rules for assessing compatibility: Venus trine Venus promises ease, Saturn opposite Venus warns of restriction, Mars square Mars suggests conflict. If these rules carry real predictive power, a sufficiently rich feature set capturing the full range of inter-chart planetary geometry should allow a well-trained model to classify relationship outcomes better than chance. The null hypothesis is that it cannot — that the 700+ features add no meaningful predictive lift above the class imbalance baseline.

---

## Why Synastry Deserves Machine Learning

The traditional approach to synastry compatibility research checks whether specific aspect configurations (Venus conjunct partner's Mars; Moon trine partner's Sun) occur more frequently in lasting relationships than in failed ones. This is valid but inherently cherry-picks which aspects to examine. Hundreds of inter-chart configurations exist; testing them individually invites multiple-comparison inflation.

Machine learning sidesteps this problem by considering all features simultaneously. A logistic regression or Random Forest does not need a priori hypotheses about which aspects matter; it discovers what matters from the pattern of the data. If Venus trine Venus really predicts longevity, the model will learn that coefficient. If Saturn square Ascendant predicts divorce, the model will learn that too. The approach is, in principle, more generous to astrology than traditional hypothesis-specific testing — it allows any of 700 features to contribute, and it considers interactions between features.

The caveat is that this generosity cuts both ways: a model trained on noisy data will find patterns that aren't there. Which is precisely what happened — and the story of exactly what spurious pattern it found is the most instructive part of this project.

---

## Data

| Field | Detail |
|---|---|
| **Sample** | ~4,000 couples from Wikidata (filtered from Project 26 dataset) |
| **Target variable** | Divorced (1) vs. Not divorced (0) |
| **Class balance** | ~20% divorced, ~80% not divorced → baseline accuracy = 79.1% |
| **Feature count** | 700+ features |
| **Feature types** | Tropical sun/moon/etc. signs (one-hot); Vedic/Sidereal signs (one-hot); 12×12 inter-chart cosine interactions (pairwise angles between all partner planets) |
| **Models tested** | Logistic Regression (L1/Lasso), Random Forest, SVM, MLP |

---

## Experiment 1: Logistic Regression (L1 Regularization)

The first model was logistic regression with L1 (Lasso) regularization — a technique that forces the model to eliminate useless features by shrinking their coefficients to zero, retaining only genuinely informative predictors. L1 is well-suited to high-dimensional, potentially noisy feature spaces because it effectively performs automatic variable selection: if a feature has no real relationship with the outcome, its coefficient goes to zero.

This experiment was restricted to the 144 geometric cosine features only (no categorical sign encodings), testing whether pure angular geometry between charts contains signal.

| Metric | Value |
|---|---|
| **Coefficients set to zero** | ~100% (essentially all) |
| **Accuracy** | 80.50% |
| **Baseline Accuracy** | 80.55% |
| **ROC-AUC** | 0.5000 |

The L1 regularization eliminated virtually every coefficient. The model that "learns nothing" — defaulting to the majority class — achieves essentially the same accuracy (80.55%) as the trained model (80.50%). An ROC-AUC of 0.500 means the model has precisely zero discriminative ability: it is predicting at the level of a coin flip after accounting for class imbalance.

This is a particularly clean null result because the model architecture itself acts as a filter. L1 is not aggressive pruning applied externally — it is the mathematical expression of the data saying "none of these 144 features deserve any weight." The geometry of inter-chart planetary angles contains no detectable linear signal about divorce probability.

---

## Experiment 2: Random Forest — The Discovery and the Trap

The Random Forest model achieved 80.88% accuracy — a lift of approximately 1.7% above the baseline. More impressively, it identified a small "High Risk" subset of couples with 94% precision for predicting divorce. These numbers sound promising: a machine learning model that can flag nearly-certain divorces with 94% confidence would be a remarkable finding.

It is not a remarkable finding. It is a textbook demonstration of a generational artifact.

### The Top Features and Their Problem

Investigating which features the Random Forest found most informative reveals the source of its apparent success:

| Rank | Feature | What It Actually Encodes |
|---|---|---|
| 1 | `Angle_Cos_Pluto_Neptune` (inter-chart) | How close Pluto-Neptune are across both charts = *which era they were born in* |
| 2 | `Trop_P2_Pluto_Sign` | Partner 2's Pluto sign = *decade of birth* |
| 3 | `Angle_Cos_Saturn_Lilith` (inter-chart) | Saturn-Lilith angular proximity = *birth year proximity* |

Pluto transits a single sign for approximately 12–30 years. Neptune for approximately 14–21 years. A person's Pluto sign is not a personal attribute — it is a generational label. "Person born with Pluto in Cancer" means "person born between approximately 1914 and 1939." The inter-chart Pluto-Neptune angle is a measure of how close the two birth years are in terms of the slow outer planet cycle.

The model's 94%-precision "High Risk" group was not detecting astrologically incompatible couples. It was detecting couples where one or both partners were born in a specific historical cohort — specifically, the "successfully predicted divorced" couples had an average birth year of approximately **1905** with a small standard deviation. The model had learned to identify a generation.

### Why That Cohort Had Higher Divorce Rates

This is not mysterious: couples born around 1905, marrying primarily in the 1920s–1940s, and appearing in a dataset like Wikidata (which over-represents historically prominent individuals) include many figures from the Hollywood golden age, early 20th century aristocracy, and political circles — social contexts where divorce rates were genuinely higher than in the general population of the era, and where such divorces were historically documented. The model correctly identified this demographic cluster. It then dressed that identification in astrological language.

### Testing Without Outer Planets

When Uranus, Neptune, and Pluto features were removed from the model to eliminate birth-year proxies, accuracy remained at 80.88%. But the model simply switched to Jupiter, Saturn, and the Node — slightly faster-moving bodies that still encode multi-year cohort information. The predictive lift was entirely robust to this substitution, because the substitute features were doing the same proxy job.

| Configuration | Accuracy |
|---|---|
| All 700+ features | 80.88% |
| Outer planets removed | 80.88% (unchanged) |
| All slow-cycle features removed | ~79.1% (baseline) |

The implication is precise: 100% of the predictive lift came from birth cohort encoding. Zero percent came from synastry astrology.

---

## The Generational Confound: A Deeper Analysis

This project provides one of the book's clearest articulations of a problem that recurs throughout astrological research: slow outer planets are not personal astrological indicators — they are time stamps.

Uranus takes 84 years to complete one orbit. Neptune takes 165 years. Pluto takes 248 years. At any given moment, everyone on Earth who is within roughly 12–30 years of your age shares essentially the same Pluto sign, the same Neptune sign, and nearly the same Uranus sign. These are generational markers, not individual fingerprints.

When these bodies appear in research data, correlations involving them have a prior alternative explanation that must be ruled out before any astrological interpretation is warranted: they may simply be proxies for birth year. Any outcome that varies by historical era — divorce rates, career patterns, mortality statistics, economic behavior — will automatically correlate with outer planet positions. Not because the planets caused the outcome, but because both the planets and the outcome are time-indexed.

The 94%-precision divorce detection in this project is a vivid illustration. The model did not learn about Venus and Mars and the complex geometry of attraction. It learned that "these two people were born around 1905, and therefore belong to a cohort with elevated Wikidata-recorded divorce rates." It then described that knowledge in terms of Pluto angles and Neptune signs. The language was astrological; the knowledge was demographic.

### Jupiter and Saturn as Partial Proxies

Even Jupiter (12-year cycle) and Saturn (29-year cycle) can become partial cohort proxies in analyses that span decades. Saturn's position at birth cycles through all 12 signs in 29 years — meaning that any study sampling people born across multiple decades will find Saturn sign correlating with birth decade, and birth decade correlating with essentially everything: marriage patterns, educational attainment, economic outcomes, health. Saturn is not quite as contaminated a proxy as Pluto, but it is not a clean individual indicator either.

---

## What a Genuine Synastry Effect Would Look Like

For this experiment to have produced evidence of real synastry effects, it would need to show predictive lift in a model that had been scrubbed of all birth-year information. This means:

1. All outer planet features (Uranus, Neptune, Pluto) removed
2. All features that encode absolute zodiacal position (sign placements, house positions) removed, or controlled for
3. Only features that are genuinely person-specific remaining: fast-moving inner planet aspects, inter-chart angles between fast movers

When the analysis is restricted to this residual feature set, accuracy returns to baseline. The fast-mover geometry carries no detectable predictive signal about divorce probability in this dataset.

---

## Statistical Caveats

**The baseline is high.** With 80% of couples classified as "not divorced," even a model that predicts nothing achieves 80% accuracy. This limits the apparent headroom for improvement and can make small lifts seem meaningful when they are not. The ROC-AUC (0.5000 in the logistic regression) is the correct metric for this problem — it is immune to class imbalance — and it is unambiguous.

**Dataset definition matters.** The Wikidata couples dataset used here includes historical public figures across a wide range of eras. Divorce rates varied enormously across eras (very low in 1900, rising through the century, high in 1970–1990). Any model trained on this data will find era-related signals. A study restricted to couples married within a single decade would eliminate much of this confound.

**Feature engineering is theory.** The 700+ features include one-hot encodings of sign placements — a feature engineering choice that encodes the traditional astrological assumption that sign membership is the relevant unit. If astrological influence operates at finer resolution (specific degrees) or coarser resolution (element/modality) or through a completely different axis (harmonic waveforms, midpoints), this feature set might miss it while still looking comprehensive.

---

## Conclusion

A logistic regression model applied to 700+ synastry features found that L1 regularization set virtually all coefficients to zero, producing an ROC-AUC of 0.500 — random chance. A Random Forest model achieved a modest 1.7% accuracy improvement and a 94%-precision "High Risk" cluster, but follow-up analysis confirmed this was a generational artifact: the model had learned to identify couples born in a specific historical cohort rather than couples with astrologically "incompatible" charts.

The conclusion is not merely that machine learning failed to find synastry effects. The conclusion is that when machine learning *appeared* to find something, the explanation was demographic rather than astrological — and this explanation was discovered through transparent feature-importance analysis and cohort investigation. The null hypothesis stands: in this dataset, astrological synastry features do not predict divorce beyond what birth cohort alone would predict.

This joins Project 26 (r=0.009 for compatibility scoring against relationship duration) and Project 10 (outer planet mortality artifacts in synastry) as a third independent analysis reaching the same conclusion: when properly controlled for generational confounds, synastry data does not predict relationship outcomes.

---

*Archived source data and raw outputs preserved in `backup/`.*
