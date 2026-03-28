# Project 03: Lunar Effects on Biological Events

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Does the Moon's phase — or its position in the zodiac — measurably influence the timing of human births? Does the Full Moon actually trigger more babies to arrive?

This is one of astrology's most culturally embedded claims, tested here against 156 million births over 45 years.

---

## 💡 Why This Matters

The Full Moon Effect is medicine's most durable myth. ER nurses swear the department gets chaotic on full moons. Obstetricians sometimes schedule C-section avoidance around the lunar calendar. Police stations have lore about full-moon crime spikes. This belief predates astrology as a formal system — it is baked into languages, idioms, and folklore worldwide.

It is also, in principle, one of astrology's most testable claims. Birth data is public, massive, and precisely dated. If the Moon exerts any measurable influence on the timing of biological events, 156 million births across 45 years should reveal it.

The methodological challenge is that birth data isn't clean. It has its own powerful rhythms — completely unrelated to the Moon — that will create false "lunar effects" if you don't strip them out first.

---

## 📊 The Data

| Field | Detail |
|---|---|
| **Dataset** | US daily birth counts, CDC (1969–1988, 1994–2003) + SSA (2004–2014) |
| **Total births** | 156,198,246 |
| **Duration** | 45 years — 14,975 daily records |
| **Astronomical data** | Swiss Ephemeris (`pyswisseph`) — lunar positions precise to <0.01° |

This is real federal public health data. The astronomical calculations are precise to within a hundredth of a degree — more than sufficient for identifying lunar phase effects, if they existed.

Why use births? Hospital admission data is often aggregated monthly or restricted. Births provide a massive, high-resolution daily proxy for spontaneous biological activity with verified public data spanning nearly half a century.

---

## 🔬 Method: Stripping the Calendar Before Testing the Moon

The central methodological insight of this project is something that invalidates most prior lunar research: **you cannot compare raw birth counts to lunar phase.** Birth data has powerful non-lunar rhythms that will masquerade as a Moon effect if they aren't removed.

The three layers that must be stripped:

**1. The Weekly Cycle**
Weekends consistently show 12–15% fewer births than weekdays. Why? Scheduled inductions and C-sections cluster on weekdays. This is the single strongest signal in the raw data — and it has nothing to do with the Moon. If a retrograde period or a full moon happens to contain more weekdays than average, the raw count will look elevated.

**2. Annual Seasonality**
US births peak in late summer. August and September have systematically more births than January or February. The holiday effect is dramatic: Christmas Day shows ~30% below-average births; Thanksgiving is ~35% below. These are cultural calendars, not astronomical ones.

**3. Long-Term Generational Trend**
The overall US birth rate changed substantially across the 45 years of this dataset. The Baby Boom echo, the baby bust, and demographic shifts all create a long-term trend that must be removed before daily comparisons.

After stripping all three layers, what remains is the **Anomaly Ratio**: the actual birth count divided by what the model predicts from week, season, and trend alone. An Anomaly Ratio of 1.00 means exactly as expected. Values above 1.00 mean more births than the calendar alone predicts; below 1.00 means fewer. This residual — and only this residual — is what we compare to the Moon.

**Lunar variables tested:**
- **Phase Angle** (0–360°): Sun-Moon elongation. 0° = New Moon, 180° = Full Moon.
- **Sidereal Longitude** (0–360°): Moon's Vedic zodiac position
- **Tropical Longitude** (0–360°): Moon's Western zodiac position

---

## 📈 Results

### Lunar Phase: Flat

| Metric | Result |
|---|---|
| Full Moon (180°) ratio | **1.001** — +0.1% above average |
| New Moon (0°) ratio | **1.000** — exactly average |
| Maximum deviation observed | **+1.2%** — at a random phase angle, not at a named phase |
| Overall pattern | **Flat** |

The detrended anomaly line across the full 0–360° phase wheel is flat. There is no hump at 180°, no trough at 0°, no consistent elevation anywhere. The Full Moon ratio is 1.001 — one tenth of one percent above average. That is noise.

![Detrended birth anomaly ratio across lunar phase angle 0°–360°](images/project-03-figure-1.png)

### Sidereal Zodiac: Flat

| Sign Position | Ratio | Interpretation |
|---|---|---|
| Aries (0°) | 1.014 | +1.4% — highest observed, but isolated |
| Libra (180°) | 1.002 | +0.2% — negligible |
| General trend | Flat | No sine wave, no zodiacal signature |

The Aries blip (1.014) is exactly the kind of local fluctuation that appears somewhere in any 360° scan of noisy data. It shows no coherent pattern and does not reproduce consistently.

### Tropical Zodiac: Also Flat

Statistically indistinguishable from the Sidereal results. Both zodiacal frameworks trace random noise around 1.0 with no coherent structure.

### Signal-to-Noise Quantification

| Measure | Value | What It Means |
|---|---|---|
| Modulation Index | **0.000001** | Effectively zero coupling |
| Rayleigh Test | Technically significant | Artifact of N=156M — see below |
| Practical effect size | **Negligible** | <0.1% of birth variance explained |

The Rayleigh test provides a lesson in what statistics can do to your intuitions at large scale: with 156 million events, even a directional tendency too small to measure in the real world will produce a statistically significant p-value. The Modulation Index of 0.000001 is the honest number — it tells you that lunar coupling, if it exists at all, is essentially zero.

---

## 🔍 What the Numbers Mean

This null result is not a weak negative — it is strong positive evidence of absence.

Consider the standard: if the Moon had even a 0.1% influence on birth timing, this dataset would detect it. One tenth of one percent. The Modulation Index of 0.000001 means the actual coupling is roughly 100 times smaller than the already-tiny hypothetical threshold.

Why do so many smaller studies find lunar effects? Because they fail to remove one or more of the confounds above. If you don't strip the weekly cycle, you might find a "lunar effect" that's actually a Monday effect. If you don't account for holidays, Christmas and Thanksgiving look astrologically strange. Every previous study that reported significant lunar effects on hospital admissions or birth rates was almost certainly measuring calendar artifacts, not the Moon.

This study uses:
- 156 million events (power to detect even microscopic effects)
- A three-layer detrending procedure before any lunar comparison
- Three separate lunar frameworks tested simultaneously
- Astronomical calculations accurate to <0.01°

After all of that, the line is flat.

---

## ⚠️ Limitations & Caveats

- The dataset covers US births only. Cultural birth patterns differ internationally (especially where scheduled births are less common), and lunar effects might theoretically differ by geography or biological context.
- This analysis tests whether the Moon affects *when* babies are born. It does not test whether the Moon affects individual characteristics of people born near a Full Moon — a separate and much harder question.
- Spontaneous vs. induced labor is not distinguished in the CDC dataset. If anything, the prevalence of scheduled births would *dilute* any true lunar signal in spontaneous labor timing — making the null result even more conservative.

---

## 🌟 Conclusion

After removing the weekly rhythms, seasonal patterns, and generational trends from 45 years and 156 million US births, the Moon's phase and zodiacal position show no measurable influence on birth timing.

The Full Moon ratio: **1.001.** The Modulation Index: **0.000001.** The pattern across all 360° of the lunar cycle: **flat.**

The Full Moon Effect — a belief embedded in medicine, policing, and popular culture — is not present in the most powerful dataset ever applied to the question. This is not absence of evidence. It is evidence of absence, at the scale that matters for any meaningful claim about lunar influence on biological timing.

The fault is not in the Moon. It is in calendars — and in the human mind's powerful tendency to notice and remember the dramatic events that happen to fall near a bright and beautiful full moon.
