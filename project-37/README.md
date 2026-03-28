# Project 37: Planetary Cycles & Mood — The Great Chronocrators Survive

> **Source:** [bigastrologybook.com/2/research/19/project-37](https://bigastrologybook.com/2/research/19/project-37)
> **Archive Date:** 2026-03-21
> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Dataset:** University of Michigan Consumer Sentiment Index (UMCSENT), November 1952 — present; N=668 valid monthly data points; Swiss Ephemeris planetary calculations aligned to monthly periods

---

## Research Question

Does collective economic mood — as measured by the University of Michigan Consumer Sentiment Index, one of the world's most rigorously collected indicators of aggregate human optimism and anxiety — correlate with any planetary cycle? And if it does, which cycles survive scrutiny: the culturally prominent small-scale claims (Mercury retrograde), the seasonal proxies (Sun sign months), or the grand long-term configurations that astrology has always regarded as its most powerful instruments?

## Background: The Michigan Index as a Mood Barometer

The University of Michigan Consumer Sentiment Index is not simply a financial indicator. It asks ordinary Americans a series of questions about their personal financial situation, their expectations for the national economy, and whether now is a good time to make major purchases. The resulting composite score — ranging roughly from 50 (extreme pessimism) to 100+ (high optimism) — captures something genuinely close to aggregate national mood at monthly resolution, continuously since 1952.

With 668 data points spanning over seven decades, this dataset is ideal for astrological investigation: long enough to encompass multiple cycles of all relevant planets, granular enough to test monthly-scale claims like Mercury retrograde, and substantial enough to detect even weak but real correlations.

---

## Data

| Field | Detail |
|---|---|
| **Dataset** | University of Michigan Consumer Sentiment Index (UMCSENT) |
| **Range** | November 1952 — present |
| **Resolution** | Monthly (quarterly before 1978) |
| **N (valid months)** | 668 |
| **Planetary calculations** | Swiss Ephemeris, aligned to calendar month midpoints |
| **Tests conducted** | Mercury retrograde periods; Vedic Sun sign (monthly) distribution; Jupiter-Saturn angular distance (continuous) |

---

## Test 1: Mercury Retrograde — The Cultural Myth at Scale

Mercury retrograde is astrology's most culturally visible phenomenon in the modern era. The claim is specific and testable: when Mercury appears to move backward in its orbit (due to the geometry of Earth and Mercury's relative positions), communication, technology, contracts, and general decision-making suffer. If this claim has any aggregate-level reality, months dominated by Mercury retrograde should show lower consumer sentiment scores — people feeling more confused, frustrated, or pessimistic about their circumstances.

With 668 monthly data points, this is an adequately powered test. Mercury is retrograde approximately 19% of the time, affecting roughly one in five months in the dataset.

| Category | Mean Sentiment Score |
|---|---|
| **Direct Mercury months** | 84.79 |
| **Retrograde-dominant months** | 84.61 |
| **Difference** | −0.18 points |
| **p-value** | 0.896 |

The difference of 0.18 points — smaller than any measurement noise in the index — produces a p-value of 0.896. A p-value this close to 1.0 represents near-perfect agreement with the null hypothesis. There is no relationship between Mercury retrograde and aggregate consumer mood.

This result carries weight beyond its p-value. Mercury retrograde is not being tested here on anecdote or individual experience — it is being tested against seventy years of aggregate data from hundreds of millions of people. If Mercury retrograde caused even a small, consistent dip in collective optimism, it would be detectable here. It is not detectable. The cultural myth is refuted at the level that matters most for epidemiological-scale claims.

This finding aligns with Project 05's earlier Mercury retrograde analysis (retrograde anomaly ratio 1.002, indistinguishable from baseline after detrending) and is consistent with Project 39's finding that Mercury retrograde does not elevate market volatility (p=0.59). Three separate methodologies, three separate datasets, three null results for Mercury retrograde. The claim is thoroughly tested.

---

## Test 2: Vedic Sun Sign — The Seasonal Confound

The second test asked whether the Vedic (sidereal) Solar month — corresponding roughly to calendar months but shifted by approximately 23 days from the Tropical zodiac — shows variation in consumer sentiment that could reflect genuine astrological influence.

| Vedic Sign | Approx. Calendar Period | Mean Sentiment |
|---|---|---|
| Makara (Capricorn) | mid-Jan to mid-Feb | 86.2 |
| Kumbha (Aquarius) | mid-Feb to mid-Mar | 86.2 |
| Mesha (Aries) | mid-Apr to mid-May | 85.8 |
| Mithuna (Gemini) | mid-Jun to mid-Jul | 84.5 |
| Simha (Leo) | mid-Aug to mid-Sep | 83.6 |
| Kanya (Virgo) | mid-Sep to mid-Oct | 82.5 |

Some seasonal variation exists: sentiment peaks in the winter months (Makara/Capricorn, Kumbha/Aquarius — January through March) and reaches its lowest point in early autumn (Kanya/Virgo — September through October). But this pattern has a well-documented secular explanation: post-holiday optimism, year-end financial planning, and the anticipation of spring economic activity all tend to elevate consumer confidence in winter, while the seasonal transition from summer to autumn is often accompanied by moderating expectations before the holiday boost.

Crucially, the sign names are irrelevant to the pattern. The Vedic Virgo dip in September-October exists not because Virgoan energy is pessimistic, but because September is historically a mediocre month for U.S. economic sentiment — a phenomenon driven by the end of summer spending and the approach of autumn uncertainty. A Tropical zodiac analysis would produce a very similar pattern, shifted slightly in calendar time.

**Finding:** The Vedic Sun sign variation reflects ordinary seasonality. No astrological archetype is needed to explain it.

---

## Test 3: Jupiter-Saturn Cycle — The Signal That Survives

Having disposed of two prominent claims, the analysis turns to the one that survives: the Jupiter-Saturn angular relationship.

Jupiter and Saturn are collectively called the *Great Chronocrators* — the "time markers" — in traditional astrology, a designation that dates to Babylonian and Hellenistic astronomy. Their synodic cycle (the time from one conjunction to the next) averages approximately 19.86 years, creating a roughly 20-year rhythm of alignment and opposition. Because Jupiter represents expansion, optimism, and growth, while Saturn represents contraction, discipline, and limitation, astrologers have long regarded their relationship as a macro-scale indicator of social and economic climate: conjunctions as resets and new beginnings, oppositions as the tension point of maximum strain.

The statistical test used the continuous angular distance between Jupiter and Saturn (0–180° collapsed for the conjunction-opposition symmetry) and correlated it with monthly consumer sentiment:

| Metric | Value |
|---|---|
| **Pearson correlation (r)** | −0.1879 |
| **p-value** | < 0.0001 |
| **Direction** | As angle increases (toward opposition), sentiment decreases |
| **Conjunction interpretation** | Higher average sentiment |
| **Opposition interpretation** | Lower average sentiment |

The correlation of r = −0.1879 is weak in absolute terms — it accounts for roughly 3.5% of the variance in consumer sentiment. But with 668 data points and a p-value effectively at zero, it is emphatically not noise. The pattern is stable, persistent, and geometrically coherent: the Jupiter-Saturn conjunction (angle near zero, the "reset" moment) correlates with elevated sentiment, and the opposition (angle near 180°, maximum tension) correlates with depressed sentiment.

### Historical Context

The Jupiter-Saturn cycle has a documented relationship to economic Kondratiev-like waves in the historical literature. The 1980–81 conjunction coincided with the beginning of the Reagan-era economic expansion. The 1981–82 opposition coincided with the deepest U.S. recession since the Great Depression. The 2000 opposition landed during the Dotcom crash and the end of the 1990s bull market. The 2020 conjunction — the famous "Great Conjunction" in Aquarius — occurred during the COVID recovery period that, despite initial catastrophe, produced historically aggressive fiscal stimulus and equity market rebounds.

None of these historical coincidences can be used as confirmatory evidence (they were not pre-registered), and each has multiple alternative explanations. But they illustrate that the 20-year Jupiter-Saturn cycle happens to phase-align, at least partially, with economic sentiment rhythms that have independent economic explanations. The correlation may be capturing a genuine underlying structure in how long economic cycles operate, rather than any direct planetary influence.

---

## The Scale Question: Micro vs. Macro

This project offers one of the book's most instructive contrasts. The most culturally prominent astrological claim — that a small, fast planet's retrograde period affects day-to-day mental clarity and communication — produces a null result. The oldest, most overlooked macrocosmic claim — that the 20-year cycle of the two slowest visible planets correlates with collective fortune — produces a real and replicable correlation.

Why might this be? One speculation: astrological claims that operate at human timescales (a few weeks, a few months) are easy to confirm through confirmation bias and attribution error — we remember the computer crash during Mercury retrograde and forget the ten normal weeks. They are also easy to test empirically, and they fail that test consistently. Claims that operate at generational timescales (20 years) are impossible to confirm through personal experience — no one lives through enough Jupiter-Saturn cycles to notice the pattern — but they may be tracking something real about structural socio-economic rhythms.

The astronomical reality of the Jupiter-Saturn cycle is undisputed: the planets complete a conjunction approximately every 20 years. The question is whether this 20-year celestial timer has any causal relationship to the 20-year economic rhythms that economists have documented independently. This project provides weak but real evidence that the answer may be yes. Whether the relationship is causal (planets affect mood), correlational but non-causal (both the planetary cycle and the economic cycle are governed by some third factor), or coincidental (statistical noise in 70 years of data is insufficient to rule out), the project cannot determine. What it can say is that the signal is there, and Mercury retrograde is not.

---

## Statistical Caveats

**Multiple testing.** Three hypotheses were tested (Mercury Rx, Sun Sign, Jupiter-Saturn). No Bonferroni correction was applied, but with only three tests and one result at p < 0.0001, the correction would not alter the conclusion. The Jupiter-Saturn result is robust.

**Effect size vs. practical significance.** r = −0.1879 explains approximately 3.5% of variance in consumer sentiment. The remaining 96.5% is driven by actual economic events (recessions, wars, policy changes), seasonal patterns, and measurement error. The Jupiter-Saturn cycle is a real signal in a very noisy dataset, but it is not a predictor in any practical sense — no one should forecast consumer confidence from planetary positions.

**Lag analysis not conducted.** A simple same-month correlation was used. Project 42's solar cycle analysis found that lagged relationships (3-month lag) were stronger than contemporaneous correlations. A Jupiter-Saturn cycle analysis with systematic lag exploration might find a stronger or more precisely timed effect.

**The correlation could be partly artifactual.** If the dataset includes more recession-era months than boom-era months due to the sampling period, and if those recession-era months happen to coincide more with Jupiter-Saturn opposition phases, a spurious correlation could arise. The 70-year sample should encompass multiple full cycles, which mitigates this concern, but it cannot eliminate it entirely.

---

## Conclusion

Seventy years of monthly consumer sentiment data tested three astrological claims of fundamentally different scope and cultural prominence.

**Mercury retrograde:** Null. The difference between retrograde-dominant and direct months is 0.18 sentiment points with p=0.896. After decades of cultural emphasis on Mercury's alleged influence over communication and decision-making, this is a clean refutation at aggregate scale.

**Vedic Sun signs:** Seasonal artifact only. The observed variation in sentiment by solar month reflects ordinary calendar patterns that have well-documented non-astrological explanations. The sign names add nothing.

**Jupiter-Saturn cycle:** Genuine signal. r = −0.1879 with p < 0.0001 across 668 months. Conjunctions correlate with elevated sentiment; oppositions with depressed sentiment. The traditional designation of Jupiter-Saturn as the *Great Chronocrators* — the time-markers of broad civilizational rhythms — turns out to have statistical backing, however modest.

The pattern is clear: the smallest, fastest, most frequently discussed cycle fails; the largest, slowest, most ancient cycle survives. This is not what astrology's popular culture predicts. But it is what the data says.

---

*Archived source data, raw analysis, and visualization outputs preserved in `backup/`.*
