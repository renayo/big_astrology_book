# Project 17: Planetary Alignment and Historical Events

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com](https://bigastrologybook.com)

---

## 🌟 Overview — What We Asked

Do major historical events — wars, revolutions, economic crashes, natural disasters — cluster on dates when the planets are unusually bunched together in the sky? Does *aggregate planetary alignment* predict historically significant days?

This is the book's most statistically striking study. The finding surprised even the researcher.

---

## 💡 Why This Matters

Traditional mundane astrology asks specific questions: "Is Saturn squaring Pluto during this war?" "Is Jupiter conjunct Uranus during this revolution?" These questions produce mixed results because they test particular symbolic claims.

This project asks something more fundamental: *when the planets happen to be clustered together in the sky — when many of them are in the same part of the zodiac simultaneously — does that clustering correlate with the timing of major historical events?*

This isn't asking about the symbolic meaning of individual planets. It's asking whether the coherence of the whole planetary system — how "bunched" or "spread" it is — tracks with collective human disruption.

The answer is a striking yes.

---

## 📊 The Data

| Component | Description |
|---|---|
| Historical events | **498 events, 1666–2023** |
| Event categories | Political (coups/revolutions), Military (wars), Disasters, Economic (crashes) |
| Random baseline | **100,000 dates** drawn randomly within the same 1666–2023 window |
| Planetary positions | Swiss Ephemeris — all 8 planets: Sun, Moon, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto |

**Event selection:** Filtered to geopolitical disruptions and physical disasters — wars, revolutions, coups, crashes, catastrophes. Excluded cultural, artistic, and scientific milestones.

---

## 🔬 Method: The Sum of Cosines

Prior mundane astrology research counted discrete "hard aspects" (90°, 180° with defined orbs). This project uses a different metric:

$$\text{Cosine Sum} = \sum_{i < j} \cos(\theta_i - \theta_j)$$

for all pairs (i, j) among 8 planets, producing **28 unique pair contributions** per day.

**Interpreting this metric:**
- **High positive value** → planets are clustered (many near-conjunctions, low angular spread)
- **High negative value** → planets spread in opposing directions (many near-oppositions)
- **Near zero** → planets distributed evenly around the zodiac

This continuous metric captures *overall coherence* of the whole planetary system — something discrete aspect counting misses entirely. A day with 6 planets in Scorpio produces an enormous cosine sum even if no traditional "hard aspect" is registered.

---

## 📈 Results

### The Core Finding: +148% Elevation

| Metric | Historical Events (N=498) | Random Baseline (N=100,000) | Difference |
|---|---|---|---|
| **Mean Cosine Sum** | **2.41** | **0.97** | **+148%** |
| Standard Deviation (random) | — | 4.44 | — |
| T-Test p-value | **< 0.0001** | — | — |
| Bootstrap p-value | **< 0.0001** | — | — |

The mean cosine sum on historical event dates is **148% higher** than on 100,000 random dates in the same period. Both parametric and bootstrap tests confirm significance at effectively p=0.

Effect size: Cohen's d ≈ 0.32 — a moderate effect. Not enormous, but consistent and robustly detected.

### Results by Event Category

All four categories show elevated cosine sums:

| Category | N | Mean Cosine Sum | Elevation vs. Random |
|---|---|---|---|
| **Political** | ~125 | **2.93** | **+202%** |
| **Military** | ~125 | **2.88** | **+197%** |
| Economic | ~125 | 2.12 | +118% |
| Disaster | ~125 | 1.94 | +100% |

Political and Military events show the strongest signals. Natural disasters and economic crises show moderate elevations.

![Distribution of cosine sum values: historical events vs. random baseline](images/project-17-figure-1.png)

### The Methodology Comparison

| Approach | Result | p-value |
|---|---|---|
| Traditional hard aspects (0°, 90°, 180°) | No signal | p ≈ 0.30 |
| **Sum of Cosines (all 28 pairs)** | **Strong signal** | **p < 0.0001** |

The same 498 events. The same historical period. Different metric — dramatically different result. The measurement choice is everything.

---

## 🔍 What the Numbers Mean

### Why Clustering, Not Hard Aspects?

The cosine sum is maximized by conjunctions and clustering, not by squares and oppositions. Historical events appear to cluster on dates of planetary *bunching* — many planets gathered in one sector of the sky — rather than the "tense" configurations (squares, oppositions) that traditional astrology emphasizes.

This is conceptually unexpected. Traditional mundane astrology associates *hard aspects* with tension and conflict. The data says the signal is in *conjunctions* — the "new cycle" archetype, when multiple planetary cycles are simultaneously beginning or renewing.

The Military Reversal is particularly striking: a traditional hard-aspect approach finds *no signal* for Military events (p ≈ 0.30). The cosine sum approach finds Military events nearly as elevated as Political ones (2.88 vs. 2.93). Wars apparently don't begin at squares and oppositions — they begin when planets are clustering together.

### What This Study Doesn't Explain

The correlation is documented. The mechanism is entirely unknown. Possible frameworks include:
- Tidal and gravitational effects during planetary clustering
- Solar magnetic field changes during clustered configurations
- Psychological or cultural priming by visible astronomical patterns
- Selection/recording bias: dramatic events near visually striking configurations get more detailed historical documentation
- Coincidence in a finite sample

The data cannot discriminate among these. The correlation is real; its cause is genuinely open.

---

## ⚠️ Limitations & Caveats

**Event selection bias:** The 498 events were curated and filtered. Historians document dramatic events more thoroughly, and unusual astronomical configurations are visually striking — if "unusual sky → more careful historical recording," the correlation could partly reflect archival patterns rather than real causal relationships.

**Exclusion of positive events:** Only disruptive, negative events were included. Whether planetary clustering also predicts positive historical events (scientific breakthroughs, social movements) is untested. If clustering predicts all dramatic events regardless of valence, the effect is about *intensity* rather than disruption specifically.

**The Moon:** Included among the 8 planets, the Moon moves ~13°/day, dramatically shifting the cosine sum within hours. Moon contributions should average out across 498 events with varied times, but Moon-day timing is an additional noise source.

---

## 🌟 Conclusion

498 historical events spanning 357 years show mean planetary clustering 148% higher than 100,000 random dates in the same period. Both parametric and bootstrap tests confirm significance at p < 0.0001. This is the most statistically robust positive finding in the book.

**What the data supports:** Historical disruption clusters on dates of unusual planetary bunching.

**What the data does not support:** A specific causal mechanism, a predictive model, or the traditional mundane astrology framework of named aspect pairs.

**The appropriate next step:** A prospective test. Compile a pre-specified list of the 20 highest-cosine-sum dates in the next decade and evaluate — without post-hoc selection — whether they correspond to major events. This would move the finding from historically observed correlation to prospectively tested prediction.

> *The contrast with Project 19 (Specific Aspects) is instructive: aggregate clustering strongly predicts event timing (p<0.0001), while traditional named pairs show weaker, mixed results. The signal is in the whole-system behavior, not individual planetary relationships.*
