# Project 44: Machine Learning Chart Rectification — Teaching an Algorithm to See Aspects

> **Source:** [bigastrologybook.com/project-44](https://bigastrologybook.com/project-44/)
> **Archive Date:** 2026-03-21
> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Dataset:** 5,000 synthetic individuals with 83,203+ generated life events; Random Forest regressor trained to predict birth hour from event geometry; two-phase experiment (raw coordinates vs. cosine features)

---

## Research Question

If the timing of life events is systematically linked to the geometry of planetary transits to natal chart angles, a machine learning algorithm given the event timing should be able to work backward — to deduce, from a list of *when* major events occurred, *what time of day* the person was born. This is the problem of *chart rectification*: recovering an unknown birth time from biographical information.

Can a Random Forest regressor, trained on the astrological geometry of life events, reduce the birth time uncertainty from ±6 hours to something meaningfully smaller?

---

## Background: The Rectification Problem

Birth time is the most consequential data point in natal astrology. A difference of two hours shifts the Ascendant (Rising Sign) by approximately 30°, potentially changing it entirely. The house positions of all planets shift; the Midheaven changes; the house cusps rotate. For many people — particularly those born before the systematic registration of birth times, in countries with poor record-keeping, or whose birth certificates were lost — the birth time is unknown or uncertain to within several hours.

Traditional astrological rectification involves a skilled practitioner examining the subject's biographical events (marriages, career changes, bereavements, physical accidents), hypothesizing what transits or progressions should have coincided with each event, and working backward to find the birth time that would make those coincidences most consistent. This is a laborious and highly subjective process, and its reliability has never been rigorously tested.

Machine learning offers the possibility of automating and systematizing this process — finding patterns in thousands of charts with known birth times that allow the algorithm to infer birth time geometry from event timing, without requiring a human practitioner to apply subjective astrological rules.

The project faces an immediate data problem: verified birth times with complete biographical event records are rare. The solution adopted here is to test the *principle* using synthetic data — generating birth times and events according to astrological rules, then asking whether the algorithm can recover what was put in. This is a proof-of-concept, not a real-world validation.

---

## Data Generation

| Field | Detail |
|---|---|
| **Population** | 5,000 synthetic individuals |
| **Events generated** | 83,203+ life events |
| **Event types** | Marriage, Career, Crisis, Death, Child |
| **Birth hours** | Randomly assigned, uniform 0–24 |
| **Generation rule** | Events were created to coincide with specific transit geometry (conjunctions, oppositions, squares from transiting planets to natal Ascendant, Midheaven, Sun) |
| **Noise** | Random events added to simulate biographical incompleteness |

The synthetic data is explicitly built so that a signal *does exist* — life events are generated to coincide with astrological transits to chart angles. If the algorithm cannot find this built-in signal, it cannot work on real data either. The synthetic test is therefore a lower bound: it tests whether the method is capable in principle, under conditions more favorable than real data.

---

## Phase 1: Raw Coordinate Approach — Failure

The first attempt fed the model raw planetary longitudes: "Jupiter is at 125.4°," "Saturn is at 287.2°," "natal Sun is at 42.6°." The algorithm saw these as continuous numbers on a 0–360° scale.

| Metric | Phase 1 Result |
|---|---|
| **Baseline MAE** (random guessing) | 6.10 hours |
| **Model MAE** | **6.40 hours** |
| **Improvement** | **−4.9% (worse than random)** |

The model performed *worse than guessing*. This is not surprising in retrospect but deserves explanation.

A Random Forest — or any standard regression algorithm — operates in linear feature space. It can learn "when feature X is large, Y increases" and "when feature X is between 125 and 130, Y decreases." But astrological aspects are defined by *circular geometry*: a conjunction occurs when two planets are close on a circle, and 359° is close to 0°. The numbers 1° and 359° are numerically far apart (358 units) but geometrically adjacent (2° separation). A standard regressor has no way to understand that these values are "close" without being explicitly told so.

More fundamentally, the relationship between a transit's effectiveness and its angle to a natal planet is not a linear function of the raw longitude difference. Jupiter at 180° from the natal Ascendant is an "opposition" — a significant transit. Jupiter at 181° is almost identical. Jupiter at 90° is a "square" — also significant. Jupiter at 45° is a "semisquare" — less significant but present. Jupiter at 30° is a "semisextile" — minor. This is a highly non-linear, multi-peaked function that a standard regressor cannot infer from raw coordinates.

The model learned nothing because the features did not encode the information in a form the algorithm could use.

---

## Phase 2: Geometric Cosine Approach — The Breakthrough

The insight of Phase 2 is that domain knowledge can be baked into the feature engineering rather than left for the algorithm to discover. Instead of providing raw coordinates, the analysis pre-computed the cosine of the angular difference between each transiting planet and each natal reference point:

$$\text{Feature} = \cos(\theta_{\text{Transit}} - \theta_{\text{Natal}})$$

This encoding has precisely the properties the algorithm needs:
- **Conjunction (0°)** maps to cos(0°) = **+1.0**
- **Opposition (180°)** maps to cos(180°) = **−1.0**
- **Square (90°)** maps to cos(90°) = **0.0**
- **Sextile (60°)** maps to cos(60°) = **+0.5**
- **Trine (120°)** maps to cos(120°) = **−0.5**

This is not an approximation — it is an exact encoding of all harmonic relationships simultaneously. The cosine is high near conjunctions, negative near oppositions, zero near squares. Every aspect has a unique signature. Crucially, it is *continuous*: an applying conjunction at 5° (cos = 0.996) is recognized as very similar to an applying conjunction at 3° (cos = 0.999), while a separating conjunction at 20° (cos = 0.940) is recognized as progressively weaker. The algorithm can now "see" aspects.

| Metric | Phase 2 Result |
|---|---|
| **Baseline MAE** (random guessing) | 5.95 hours |
| **Model MAE** | **2.71 hours** |
| **Improvement** | **+54.4%** |

A mean absolute error of 2.71 hours means the model's birth time estimate is, on average, within 2 hours and 43 minutes of the true birth time. Starting from a ±6-hour uncertainty window (uniform distribution over 24 hours with MAE ≈ 6), the model narrows this to roughly ±2.7 hours — a reduction of more than half the uncertainty.

---

## Feature Importance

The Random Forest provides feature importance scores — a measure of which features contributed most to the accuracy improvement. The top predictors:

| Rank | Feature | Interpretation |
|---|---|---|
| 1 | **Jupiter-Sun geometry** (`cos_Jup_nSun`) | Jupiter transit to natal Sun — the most informative signal |
| 2 | **Event Type** | Knowing *whether* it was a marriage, career event, or crisis helps locate the chart geometry |
| 3 | **Saturn-Sun geometry** (`cos_Sat_nSun`) | Saturn transit to natal Sun — classic timing mechanism |
| 4 | **Node-Chiron geometry** | A surprising finding — generational/karmic timing structures |

Jupiter-Sun geometry as the top predictor is consistent with traditional astrological practice: Jupiter transits to the natal Sun are among the most commonly cited timing markers for significant positive life events (career breakthroughs, marriage, public recognition). The model "learned" that when Jupiter was at a specific angle to the natal Sun at the time of a major event, the natal Sun was probably at a specific longitude — which helps constrain the Ascendant position and thus the birth time.

Saturn-Sun geometry as the third-ranked predictor aligns with the Jupiter-Saturn dynamic. Saturn's approximately 29-year cycle creates distinctive transit signatures to the natal Sun (Saturn square Sun at approximately age 7; Saturn opposite Sun at approximately age 14–15; Saturn return at approximately age 29) that are strong temporal markers.

Event Type matters because different event categories are associated with different transit signatures. A marriage is more likely to occur under certain planetary configurations than a career event; knowing the event type helps the model narrow which geometric features are most relevant.

---

## What This Means for Practical Rectification

The practical implication of the Phase 2 success is specific and limited:

- **Birth time uncertainty before:** ±6 hours (uniform distribution, no information)
- **Birth time uncertainty after (synthetic):** ±2.7 hours
- **Remaining uncertainty:** Still approximately a ±2.7-hour window, which may span 1–2 Ascendant degrees

For astrological practice, a 2.7-hour uncertainty still means the Ascendant could be in any of up to 3–4 different degrees, and the house positions of faster planets could shift by up to one house. The method significantly reduces uncertainty but does not eliminate it.

For real-world application, the limitation is that the model was trained on *synthetic* data where the signal was artificially implanted. Real biographical data contains:
- Imprecise or poorly documented event dates
- Events that occurred for non-astrological reasons
- Significant missing events (the researcher does not have the full biography)
- Ambiguity about what constitutes a "major event"

These real-world complications would reduce the accuracy below the synthetic benchmark. Nevertheless, the proof of concept is valuable: if a consistent astrological signal exists in life event timing, a correctly feature-engineered algorithm can detect and use it. The question for real-world application is whether the signal-to-noise ratio in actual biographical data is high enough to produce meaningful accuracy.

---

## The Feature Engineering Principle

The broader lesson of this project extends beyond rectification. It is a demonstration of a general principle for astrological machine learning: **domain knowledge must be encoded in features before the algorithm is trained, not after.**

Raw astronomical coordinates are not a natural language for machine learning. The cyclical, modular nature of aspects — the fact that 0° and 360° are the same point, that 90° and 270° are both "square," that closeness is measured on a circle not a number line — cannot be inferred from raw numbers without explicit encoding. Projects that feed raw planetary longitudes into neural networks or random forests and then claim to test "whether astrology works" are testing whether the algorithm can invent trigonometry on its own. It generally cannot.

Cosine encoding of angular differences is not a trick or an imposition of astrological theory onto the data. It is simply the correct representation of circular geometry in a form that linear algebraic algorithms can process. It is as natural as normalizing input data or encoding categorical variables — standard data preprocessing applied to an astronomical domain with circular structure.

The 54.4% improvement in prediction accuracy from Phase 1 (raw coordinates) to Phase 2 (cosine encoding) is essentially the value of knowing basic trigonometry.

---

## Statistical Caveats

**Synthetic data is optimistic.** The 54.4% improvement is achieved on data that was generated *with* an astrological signal. Real biographical data has substantially lower signal-to-noise ratio. The synthetic result is a theoretical ceiling, not a practical estimate.

**100 tree Random Forest, not optimized.** The model architecture is a standard out-of-the-box Random Forest. Systematic hyperparameter optimization (tree depth, feature sampling, number of trees) might improve performance modestly.

**The baseline calculation.** The baseline MAE of 5.95 hours (Phase 2) represents a uniform random guess of birth hour in [0, 24] — which has an expected absolute deviation of approximately 6 hours. The model's 2.71-hour MAE is measured against this random baseline. If the test individuals' true birth hours were not uniformly distributed, the baseline would shift accordingly.

**Event generation rules may favor certain transit types.** If the synthetic event generation was biased toward, say, Sun-Jupiter conjunctions and Sun-Saturn squares over Moon conjunctions and Mars oppositions, the model will over-represent the feature importance of those transit types and may not generalize even to other synthetic datasets using different generation rules.

---

## Conclusion

Phase 1 demonstrated that raw coordinate features are useless for machine learning rectification — the algorithm performs worse than chance because it cannot infer circular geometry from linear numbers. Phase 2 demonstrated that cosine-encoded features reduce birth time uncertainty by 54.4% on synthetic data, from ±6 hours to ±2.7 hours.

The top predictors — Jupiter-Sun geometry, Event Type, and Saturn-Sun geometry — are exactly the planetary relationships traditional astrologers most commonly invoke for timing major life events. The algorithm, trained on thousands of synthetic charts with built-in astrological signals, "discovered" the same principles that centuries of astrological practice had encoded in tradition.

This proof-of-concept establishes that the goal of algorithmic chart rectification is achievable in principle. The gap between this synthetic demonstration and practical real-world application is substantial — real data is noisier, more ambiguous, and less complete than the idealized synthetic training set. But the direction is clear: with proper feature engineering and a sufficiently large dataset of verified birth times with documented event histories, machine learning rectification could provide a systematic, reproducible alternative to the subjective practitioner-based method currently used.

---

*Archived synthetic data, feature matrices, model weights, and performance visualization preserved in `backup/`.*
