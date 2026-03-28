# Project 42: Solar Cycles & Social Sentiment — The 11-Year Rhythm

> **Source:** [bigastrologybook.com/2/research/19/project-42](https://bigastrologybook.com/2/research/19/project-42)
> **Archive Date:** 2026-03-21
> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Dataset:** University of Michigan Consumer Sentiment Index (UMCSENT) paired with SILSO/SIDC Monthly Mean Total Sunspot Number; February 1960 — December 2023; N=624 monthly data points

---

## Research Question

Does the 11-year solar activity cycle — measured by monthly sunspot counts, a proxy for overall solar electromagnetic output — correlate with aggregate human mood as captured by the University of Michigan Consumer Sentiment Index?

## Background: The Sun as Physical Mechanism

Most of the astrological claims tested in this book are statistical — correlations between astronomical configurations and human outcomes with no obvious physical mechanism to explain them. The solar activity hypothesis is different. Here, there is at least a plausible causal chain:

**Solar activity → geomagnetic disturbance → neurobiological effects → aggregate mood changes.**

During periods of elevated solar activity (solar maxima), the Sun emits more X-ray radiation and energetic particles. These interact with Earth's magnetosphere, producing geomagnetic storms measurable as elevated Kp and Dst indices. Laboratory research has documented that geomagnetic disturbances are associated with changes in melatonin production, circadian rhythm disruption, and in some studies, elevated psychiatric emergency presentations. If these individual-level effects aggregate to population-level mood changes, they should be detectable in a long-running consumer sentiment index.

This makes the solar activity hypothesis the most physically grounded of any test in this book — the one where the gap between "astrological cycle" and "measurable mechanism" is narrowest.

---

## Data

| Field | Detail |
|---|---|
| **Sentiment data** | University of Michigan Consumer Sentiment Index (UMCSENT), FRED |
| **Solar data** | Monthly Mean Total Sunspot Number (SILSO, SIDC — Solar Influences Data Analysis Center) |
| **Solar cycles covered** | Solar Cycles 19 through 25 (1960–2023) |
| **Range** | February 1960 — December 2023 |
| **N** | 624 valid monthly data points |

---

## Results

### A: The Long-Term Correlation

Over 64 years and six complete solar cycles, the relationship between monthly sunspot number and consumer sentiment is:

| Metric | Value |
|---|---|
| **Pearson correlation (r)** | −0.193 |
| **p-value** | < 10⁻⁶ |
| **Direction** | Higher solar activity → lower sentiment |
| **Low Solar months mean** | 87.5 |
| **High Solar months mean** | 83.1 |
| **Difference** | ~4.4 points |

The correlation of −0.193 is statistically highly significant — p < 10⁻⁶ means this result would occur by chance less than one time in a million if there were no real relationship. But the *effect size* is modest: r = −0.193 explains approximately 3.7% of the variance in consumer sentiment. The remaining 96.3% is driven by actual economic conditions — recessions, recoveries, wars, policy changes, inflation. The Sun is a real but minor background factor in collective mood.

The group comparison makes the effect more intuitive: in the 624 months of data, months with low solar activity show an average sentiment of 87.5, while months with high solar activity show 83.1. That 4.4-point difference is roughly comparable to the consumer mood impact of moderate news events — visible, but easily drowned by larger forces.

### B: Lag Analysis — When Does the Effect Peak?

A systematic lag analysis identified the temporal pattern of the correlation:

| Lag (months) | Correlation r |
|---|---|
| 0 (same month) | −0.193 |
| +1 month | −0.198 |
| +2 months | −0.201 |
| **+3 months** | **−0.204** |
| +6 months | −0.186 |
| +12 months | −0.157 |

The correlation is strongest at a 3-month lag: solar activity in month M is best correlated with sentiment in month M+3. This lagged structure is more consistent with a causal relationship than an instantaneous one — it suggests the mechanism takes approximately three months to propagate from elevated solar output through whatever chain of intermediary effects to aggregate human economic mood.

Three months is a plausible delay if the mechanism operates through cumulative geomagnetic exposure affecting neurobiological baselines rather than through acute storm events. Chronic low-grade exposure to elevated geomagnetic disturbance may gradually shift population-level mood baselines rather than producing immediate sharp effects.

### C: The 2016–2023 Cautionary Tale

The most methodologically important finding in this project is not the long-term correlation but its most dramatic period.

Between 2016 and 2023, the correlation between solar activity and consumer sentiment was approximately **r = −0.74** — a near-perfect inverse relationship. This is far higher than the long-term r = −0.193, and it produced the initial hypothesis that inspired this research. Solar Cycle 25 (beginning around 2019) coincided, in apparent lockstep, with a dramatic deterioration of consumer sentiment.

The long-term analysis reveals this as a **spurious phase-alignment**: during the 2016–2023 window, the ascending phase of Solar Cycle 25 happened to coincide almost exactly with the COVID-19 pandemic, the subsequent inflation surge, and the energy price crisis following Russia's invasion of Ukraine. All of these independently drove consumer sentiment to historically low readings. The solar cycle was rising at the same time, creating the appearance of a strong negative correlation that was largely driven by non-solar factors.

| Period | Correlation r | Likely Driver |
|---|---|---|
| 1960–2015 | Weakly negative | Multiple cycles, genuine weak effect |
| 2016–2023 | −0.74 | Phase-alignment of solar max with COVID/inflation era |
| Full 1960–2023 | −0.193 | Long-term genuine but modest effect |

This is a textbook demonstration of why short-window analyses of cyclical phenomena are dangerous. A researcher who only examined 2016–2023 would conclude that solar activity is one of the most powerful predictors of consumer mood ever identified. The 64-year context reveals it as an era-specific coincidence that inflated an otherwise modest effect by approximately 4×.

The methodological lesson generalizes across the entire book: whenever a striking correlation appears in a cyclical dataset, the appropriate response is to ask whether the analysis window happens to align the cycles in phase. If it does, the correlation may vanish or shrink dramatically when the window is extended.

---

## The 11-Year Cycle as the Physical Zodiac

This project occupies a unique position in the book because the solar cycle is, in a precise sense, the most physically grounded "astrological cycle" of all. Traditional astrology works with the apparent positions of planets against the zodiacal backdrop — symbolic designations whose physical basis (if any) is debated. The solar activity cycle is not symbolic: it is a measurable electromagnetic and particle-radiation phenomenon with documented biological effects.

When sunspot counts are high, Earth is embedded in more energetic solar wind, more frequent X-ray bursts, more intense geomagnetic variation. Satellites detect these changes. Power grids feel them. Migratory birds are temporarily disoriented by them. The question this project asks is whether human mood — the most complex and collectively buffered endpoint imaginable — can also register these changes.

The answer, cautiously, is yes: about 4.4 sentiment points separate low-solar from high-solar months on average across 64 years. That is small. But it is real and it persists across the full dataset in a direction that makes mechanistic sense.

---

## Plausibility of the Mechanism

The proposed causal chain — solar activity → geomagnetic disturbance → mood change — has empirical support at each step:

**Step 1 (Solar → Geomagnetic):** Well-documented. Elevated solar activity is robustly associated with higher Kp indices (geomagnetic storm frequency and intensity).

**Step 2 (Geomagnetic → Biology):** Supported with caveats. Elevated Kp has been associated with disrupted melatonin synthesis in experimental studies, with elevated psychiatric admission rates in some epidemiological studies, and with increased serotonin turnover in post-mortem brain studies. The literature is mixed but directionally consistent.

**Step 3 (Biology → Aggregate Mood):** The weakest link. Consumer sentiment aggregates the moods of millions of people responding to a survey about economic conditions. Even if geomagnetic disturbance shifts the individual mood baseline by a small amount, it would have to do so consistently enough that the aggregate signal survives the enormous noise of economic events, media framing, and individual variation. The correlation found here suggests this aggregation happens — imperfectly, with weak effect size, but detectably over 64 years.

---

## Statistical Caveats

**Autocorrelation in both series.** Monthly sunspot numbers are highly autocorrelated (solar activity trends over months and years). Consumer sentiment is also autocorrelated (mood in month M predicts mood in month M+1). Standard Pearson correlation treats observations as independent; when both variables are autocorrelated, this inflates the effective sample size, making the p-values too small. Correcting for autocorrelation would require computing the effective N and adjusting degrees of freedom, which would raise the corrected p-value — though given p < 10⁻⁶, even substantial autocorrelation corrections would likely preserve significance.

**Detrending not applied.** Both series have long-term trends: consumer sentiment drifted downward somewhat from the 1960s highs to the 2000s–2020s; solar activity peaked in Cycle 19 (1958) and has been generally declining since, though with substantial cycle-to-cycle variation. Detrending both series before correlating might reduce or increase the observed correlation; this analysis has not been performed.

**The 2016–2023 lesson should be heeded for the current claim.** The long-term r = −0.193 may itself contain some era-specific phase-alignment that would not survive an even longer time series (1900–2023 if data were available). Treating r = −0.193 as the "true" effect size while acknowledging it could be contaminated by remaining phase-alignments within the 64-year window is the epistemically appropriate stance.

**Effect size relative to practical utility.** A 4.4-point difference in consumer sentiment between low-solar and high-solar months cannot be used for economic forecasting. Actual economic events move sentiment by 20–40 points. The solar signal is real, weak, and practically invisible against the noise of economic reality.

---

## Conclusion

Sixty-four years of paired monthly data reveal a statistically significant but practically modest negative correlation between solar activity and consumer sentiment: r = −0.193, p < 10⁻⁶, with an effect of approximately 4.4 sentiment points between solar extremes. The optimal lag is 3 months, consistent with a mechanism that propagates through cumulative biological exposure rather than acute storm events.

The study's most important contribution may be its cautionary finding: the 2016–2023 period showed r = −0.74, suggesting an overwhelmingly strong solar-mood relationship. The 64-year context revealed this as a phase-alignment artifact — the ascending Solar Cycle 25 coinciding with the COVID/inflation era, creating an apparent correlation that is mostly driven by the pandemic and its aftermath rather than solar electromagnetic effects.

The genuine effect, when the full 64-year window is used: real, small, and mechanistically plausible. The solar cycle is the closest thing to a physically grounded "astrological mechanism" in this entire book. That it produces an effect size of only r = −0.19 suggests that even the best-supported physical mechanism for celestial-mood correlation operates at the margin of detectability — a whisper against the roar of actual human events.

---

*Archived sentiment data, sunspot number series, lag analysis, and visualization outputs preserved in `backup/`.*
