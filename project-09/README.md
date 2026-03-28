# Project 09: Solar Activity and Quality of Time

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com](https://bigastrologybook.com)

---

## 🌟 Overview — What This Chapter Is

This chapter documents a research design that was fully specified but not executed. The methodology is complete. The solar data is freely available. But the critical missing piece — a suitable crowd-sourced mood dataset at scale — was never obtained. Rather than fabricate results, this chapter stands as a **methodology paper**: what would an honest scientific test of the solar activity ↔ human experience hypothesis look like?

The question is worth preserving, because it is genuinely distinct from the rest of the book and more physically plausible than most astrological claims.

---

## 💡 Why This Matters

Most of this book tests whether *planetary positions* (where Jupiter is in the zodiac, whether Moon is in Pisces) correlate with outcomes. This project asks something different: whether the *intensity* of the Sun's output affects human behavior.

These are mechanistically distinct in an important way:

**Planetary position hypotheses** require some unknown mechanism by which geometric angles between distant bodies influence people. No physically plausible mechanism has been identified — electromagnetic effects are far too weak at the distances involved; gravitational effects are dwarfed by ordinary terrestrial forces.

**Solar activity hypotheses** have a *candidate physical mechanism*: geomagnetic storms alter Earth's magnetic field, which influences melatonin secretion, disrupts sleep architecture, and has documented associations with cardiovascular events and mood disorders in epidemiological literature. People living near the poles, where geomagnetic effects are strongest, show stronger correlations.

This distinction matters: the solar activity question sits closer to legitimate biophysics than most of the book's content. It deserves a rigorous test.

---

## 📊 What We Know From Existing Literature

| Finding | Quality |
|---|---|
| Geomagnetic activity correlates with hospital admissions for psychiatric disorders | Moderate — replication needed |
| Kp index correlates with suicide attempt rates in some studies | Inconsistent across studies |
| Geomagnetic storms disrupt sleep architecture | Good — confirmed in sleep lab settings |
| Solar cycle (11-year) correlates weakly with economic activity | Methodologically contested |
| No robust link found between sunspot number and mood in diary studies | Good — Kelly & Saklofske, 1994 |

The literature is inconclusive — not because the question is unanswerable, but because most studies have small N, short time windows, or poor mood measurement. A well-powered modern study using daily data over 10+ years would provide a more definitive answer.

---

## 🔬 The Solar Data (Available and Ready)

NOAA's Space Weather Prediction Center publishes complete, free daily archives:

| Measure | What It Captures | Available Since |
|---|---|---|
| **Sunspot Number** | Count of sunspots; proxy for solar magnetic activity | 1600s (observational) |
| **F10.7 Solar Flux** | Radio emissions at 10.7 cm — best continuous proxy for solar UV | 1947 |
| **Kp Index** | Geomagnetic disturbance (0 = quiet, 9 = extreme storm) | 1932 |
| **Dst Index** | Ring current disturbance; measures magnetic storm strength | 1957 |
| **Ap Index** | Linear version of Kp; easier for regression | 1932 |

These are all freely downloadable, spanning 60–80 years of daily records. The solar side of this study is essentially pre-completed.

---

## 🔬 The Mood Data Problem (What's Missing)

The hard part is mood measurement. Several approaches exist, each with real limitations:

| Approach | Pros | Cons |
|---|---|---|
| Crowd-sourced mood apps (Daylio, Moodflow) | Direct subjective mood; daily resolution | No public aggregate export; proprietary |
| Social media sentiment indices | Large scale; publicly analyzable | Changed API access post-2023; NLP noise |
| Google Trends (searches for "depression," "anxiety") | Free; daily; population-level proxy | Search ≠ mood; confounded by news events |
| WHO/CDC emergency department data | Objective outcomes | Monthly resolution; 1–2 year reporting lag |
| Academic diary studies | Gold standard | Small N; expensive; rare multi-year datasets |

The project stalled here. The solar data collection was written and tested. The analysis pipeline (time-lagged regression, Granger causality, PCA) was fully designed. But no suitable mood proxy was identified and acquired.

---

## 🔬 The Full Proposed Analysis Pipeline

Had mood data been obtained, the analysis would have proceeded in five steps:

**Step 1 — Stationarity Tests**
Both solar activity series and mood series have known periodicities (the 11-year solar cycle; weekly mood patterns). These must be removed via seasonal decomposition before correlation analysis to avoid spurious periodicity matches.

**Step 2 — Cross-Correlation at Multiple Lags**
Pearson and Spearman correlations between each solar measure and mood at lags from −7 to +14 days. The expected biological mechanism (melatonin disruption, sleep disturbance) predicts a 1–3 day lag. Testing multiple lags without pre-specification requires correction for multiple testing.

**Step 3 — Granger Causality**
Tests whether past solar values improve prediction of future mood *beyond* what past mood alone predicts. This is a directional test: does solar activity *precede* mood changes, or are they merely co-occurring?

**Step 4 — PCA on Mood Variables**
If multiple mood dimensions are available (e.g., positive affect, negative affect, arousal), PCA reduces them to composite components before modeling — preventing overfitting.

**Step 5 — Control for Season**
The key confound: solar flux and human mood both have annual cycles, and both correlate with day length and temperature. Partial correlation controlling for day-of-year is essential before any solar-mood connection is claimed.

---

## 💡 What a Positive Result Would and Would Not Mean

A positive correlation between geomagnetic activity and aggregate mood would be:

- ✓ Evidence for a measurable physical influence of solar environment on human affect
- ✓ Consistent with existing epidemiological literature
- ✗ Not evidence for traditional astrological claims about planetary *positions*
- ✗ Not sufficient to establish causation (both could respond to a third variable)

A negative result would not be surprising — the literature is inconsistent — but a well-powered null at N=3,650 daily observations (10 years) would itself be a useful contribution.

---

## 🌟 Conclusion

This chapter presents a research design, not results. The question — whether solar electromagnetic activity correlates with human mood — is scientifically legitimate, physically plausible, and underexplored compared to the rest of astrology research.

The methodology is ready. The solar data is free and available. What's missing is approximately 10–20 GB of mood proxy data and the time to process it.

**Viable next steps for a researcher wanting to complete this:**
1. Download F10.7 and daily Kp data from NOAA
2. Use Reddit Pushshift or Google Trends as mood proxies (acknowledging limitations)
3. Align to daily time series, control for weekday effects and seasonality
4. Run cross-correlation and Granger causality with 0–7 day lags
5. Report confidence intervals, not just p-values

The contrast with the rest of this book is instructive: while projects testing zodiac signs and planetary positions consistently return null results, the solar activity question provides a physical mechanism to test. Whether that mechanism produces detectable effects on human mood is genuinely open — and worth finding out.
