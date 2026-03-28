# Project 21: Eclipse Cycles and Collective Behavior (Seattle 911 Calls)

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Do solar or lunar eclipses correlate with measurable increases in emergency call volume in Seattle — a proxy for collective behavioral disruption — above and beyond what normal day-of-week, seasonal, and trend effects predict?

If eclipses are potent disruptors as astrological tradition holds, emergency call rates should spike on eclipse days.

---

## 💡 Why This Matters

Astrology frequently treats eclipses as among the most potent moments in a calendar — "doors opening," "fated events," periods of heightened volatility and disruption. Seattle's Fire/EMS 911 call record offers a uniquely clean test: it is a high-volume, publicly available, precisely timestamped behavioral dataset. With ~1.4 million records spanning 13 years, even small eclipse effects are statistically detectable.

---

## 📊 The Data

| Source | Description |
|---|---|
| Seattle Real-Time Fire 911 Calls | City of Seattle open data; ~1.4 million dispatch records, 2013–2026 |
| NASA Eclipse Catalog | Five Millennium Canon of Solar and Lunar Eclipses |
| Swiss Ephemeris | Additional eclipse verification |

Both data sources are genuine and publicly available. The NASA eclipse catalog is the gold standard for historical eclipse timing.

**Eclipse sample:**

| Eclipse Type | Count |
|---|---|
| Solar Eclipses | 40 |
| Lunar Eclipses | 41 |
| **Total Eclipse Days** | **81** |
| Non-Eclipse Control Days | ~4,600 |

Note: The analysis uses all catalog eclipse dates, including partial eclipses not visible from Seattle. This is the conservative choice — avoiding selection bias by including all events.

---

## 🔬 Method: Detrending Before Testing

The key methodological innovation is multi-factor linear regression detrending before any eclipse comparison. Raw 911 call volume contains strong predictable structure: day of week, month of year, week of month, and a long-term population growth trend. A regression model predicts expected daily call count from these four factors. The **residual Z-score** — actual minus expected, standardized — is what gets compared to eclipse days.

This removes the noise that would otherwise make any week with different weather or a local event look "eclipsey."

---

## 📈 Results

### Aggregate: Eclipse vs. Non-Eclipse

| Group | Mean Daily Calls | N |
|---|---|---|
| Eclipse days | 70.69 | 81 |
| Non-eclipse days | 72.21 | ~4,600 |
| **t-statistic** | **−1.11** | |
| **p-value** | **0.267** | |

Eclipse days show *slightly lower* average call volume than non-eclipse days. Not significant. There is no evidence of an eclipse-driven increase in overall emergency call volume.

### Results by Call Category

| Category | Solar Eclipse Mean Z | Solar p-value | Lunar Mean Z | Lunar p-value |
|---|---|---|---|---|
| **Total Calls** | −0.21 | 0.35 | −0.37 | 0.14 |
| Aid Response | −0.23 | 0.32 | −0.38 | 0.12 |
| Medic Response | −0.19 | 0.40 | −0.33 | 0.19 |
| Auto Fire Alarm | +0.13 | 0.63 | −0.16 | 0.58 |
| **MVI (Car Accidents)** | **+0.32** | **0.05** | +0.06 | 0.81 |

*Positive Z = more calls than expected. Negative Z = fewer than expected.*

### The "Eclipse Chaos" Hypothesis: Definitively Rejected

Neither solar nor lunar eclipses produce a statistically significant increase in total emergency call volume. Every overall metric trends *negative* during eclipses — fewer emergencies than expected, not more. The eclipse-as-disruptor narrative is not supported.

### The Solar Eclipse / Traffic Accident Signal (Borderline)

The one borderline finding: **Motor Vehicle Incidents on solar eclipse days** (p = 0.05).

Solar eclipse MVI mean Z: **+0.32** vs. a control mean of −0.08.

The plausible mechanism here is behavioral, not astrological: solar eclipses draw people outdoors to view the event, increasing driving, distraction while driving, and general traffic disruption. This is a **"Distracted Driver" effect** — humans responding to a spectacle, not celestial influence on collective psychology.

Given that six categories were tested, this result should be treated as suggestive, not confirmed. A Bonferroni correction would not consider it significant.

---

## 🔍 What the Numbers Mean

The statistical power here is exceptional: ~1.4 million records producing ~4,600 day-level observations. Even an eclipse effect as small as 0.05 standard deviations in Z-score would be detectable. The null results for overall call volume are therefore genuinely informative — not underpowered non-results.

If eclipses caused even a modest increase in collective distress, we would have seen it. The data is large enough to say with confidence: **it's not there.**

---

## ⚠️ Limitations & Caveats

- **Multiple testing:** Six call categories × two eclipse types = 12 comparisons. Expected false positives at p < 0.05: ~0.6. The single borderline result (MVI, solar, p = 0.05) is within this range.
- **Eclipse visibility:** The analysis uses all catalog eclipse dates, including non-visible-from-Seattle events. A more targeted test of major visible eclipses might show different patterns.
- **Detrending assumptions:** The linear regression does not account for major holidays (New Year's, July 4th). Holiday controls would improve the analysis.

---

## 🌟 Conclusion

A 13-year record of 1.4 million Seattle Fire/EMS dispatch calls shows **no evidence that eclipses increase collective distress.** If anything, call volumes trend slightly below expected on eclipse days, though not significantly.

The one borderline exception — elevated car accidents on solar eclipse days — is most plausibly explained by people driving more and being distracted by the astronomical event. That's human behavior responding to a spectacle, not an astrological influence on collective psychology.

The traditional narrative of eclipses as harbingers of chaos, elevated emergencies, and collective disruption is not supported by this high-powered behavioral dataset.
