# The Big Astrology Book of Research

**By Renay Oshop**
**Published at:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 What This Book Is

*The Big Astrology Book of Research* is an honest attempt to find out whether astrology works — not the astrology of vague sun-sign horoscopes in the back of magazines, but the full, rigorous, technically demanding practice of natal chart analysis, mundane prediction, compatibility scoring, and traditional technique.

The author is a computational biologist who became a practicing Vedic astrologer. This combination — scientific training alongside genuine engagement with astrological tradition — means the book asks hard questions and accepts uncomfortable answers. When the data says null, it says null. When the data says something surprising, it doesn't hide behind caveats.

Thirty-four original research projects are collected here, spanning:
- Personality and birth charts
- Financial markets and planetary cycles
- Relationship compatibility and longevity
- Historical predictions and their accuracy
- Traditional techniques (dignities, solar houses, fixed stars, horary)
- Weather, eclipses, and collective human behavior
- Evolutionary computation and machine learning on astrological data

This is not a book where everything "works." Roughly a third of the projects return clean null results. The full moon does not cause more babies to be born. Mercury retrograde is a calendar artifact. Aggregate compatibility scores predict nothing about which couples stay together. Historical astrologers' documented predictions are statistically indistinguishable from coin flips.

But some things do show up in the data — sometimes in unexpected ways. Planetary clustering correlates with historical disruption at a striking level (p<0.0001). Traditional dignities distinguish writers from filmmakers in an archetypally coherent direction. Mars placement outperforms Sun Sign for career prediction. Solar houses produce above-chance results without needing birth times at all.

The pattern of what works and what doesn't is itself the finding. This is a book about the shape of the evidence.

---

## 📁 Project Structure

Each project file in this directory (`project-01.md` through `project-34.md`) is a complete research report with:

- Overview of what was asked
- Data sources and sample sizes
- Methodology explained for non-statisticians
- Full results with tables and effect sizes
- Honest limitations and caveats
- Conclusions and directions for future work

**Project 48** (`project-48/`) contains the genetic algorithm series — an advanced multi-dataset application of evolutionary computation to astrological feature selection, with full Python source code and visualization plots.

---

## 🔬 A Note on Methods

Throughout the book, two methodological choices recur and are worth explaining upfront:

**The Cosine Metric:** Rather than the traditional binary "aspect within orb" approach (is Mars within 8° of a trine to Venus?), many projects use the cosine of the angular difference between planetary pairs. This produces a continuous value from +1 (exact conjunction) to -1 (exact opposition) that preserves more information than a yes/no threshold. It has become the preferred tool across projects testing compatibility, historical events, Solar Returns, and fixed stars.

**The Generational Confound:** Several projects involving slow-moving outer planets (Uranus, Neptune, Pluto) initially appear to show strong astrological signals, which upon examination turn out to reflect birth-year clustering among the samples. People born in the same era share outer planet positions by definition. This is flagged every time it occurs and results interpreted accordingly.

---

## 📊 Quick Verdict Summary

| # | Project | Verdict |
|---|---|---|
| 01 | Ultra-Wealthy Birth Patterns | Mixed — compelling signals, underpowered |
| 02 | Planetary Cycles & Market Volatility | Weak positive — real but not predictive |
| 03 | Lunar Effects on Biological Events | **Null** — definitively |
| 04 | Who Believes in Astrology, and Where? | **Positive** — urbanization R²=0.74 |
| 05 | Mercury Retrograde — Real or Bias? | **Null** — calendar artifact |
| 06 | Harmonic Analysis of Planetary Aspects | **Positive (selective)** — tension > ease |
| 07 | Machine Learning & Planetary Cycles | Mixed — 29.3% vs 16.7% baseline |
| 08 | Tropical vs. Sidereal Zodiac | **Null** — Sun Sign worse than random |
| 09 | Solar Activity & Quality of Time | **Incomplete** — methodology paper |
| 10 | Synastry & Relationship Longevity | Mixed — Mars-Mars genuine; outer planets artifact |
| 11 | Longitudinal Health & Longevity | **Null** — sun sign p=0.964 |
| 12 | Market Volatility & GARCH-X | **Null** — planets worsen forecasts |
| 13 | Circular Statistics & Personality | **Null** — fire signs ≠ extraversion |
| 14 | Essential Dignities: Tropical vs. Sidereal | Mixed — scientists debilitated Tropical |
| 15 | Birth Order & Astrological Factors | Mixed — Saturn shift real; Fire firstborns |
| 16 | Creativity, Genius & Astrology | **Null** — Neptune lower in geniuses |
| 17 | Planetary Alignment & Historical Events | **Strong positive** — +148%, p<0.0001 |
| 18 | Solar House System (Surya Lagna) | **Positive** — 31.8% vs 25%, BF=23.5 |
| 19 | Mundane Astrology — Specific Aspects | **Incomplete** — base rate problem |
| 20 | Astrological Rule Discovery | **Positive (selective)** — Hardship Hypothesis |
| 21 | Eclipse Cycles & Seattle 911 Calls | **Null** — no chaos signal |
| 22 | Astro-Weather Forecasting | Mixed — seasonal artifact; syzygy dip marginal |
| 23 | Chart Similarity & Career Outcomes | **Partial positive** — Vedic p<0.001 |
| 24 | Electional Astrology & IPO Returns | **Null** — all rules: <0.2% difference |
| 25 | Fixed Stars & Natal Interpretation | Descriptive — Regulus/overdose suggestive |
| 26 | Synastry and Relationship Survival | **Null** — r=0.009, aggregate fails |
| 27 | Horary Astrology — Moon as Oracle | **Incomplete** — framework ready, data needed |
| 28 | Solar Houses & Life Domains | **Positive (descriptive)** — politicians +166% |
| 29 | Asteroid Analysis in Celebrity Charts | Mixed — Pallas/Vesta solar conjunctions elevated |
| 30 | Chinese Zodiac & Big Five Personality | **Confounded** — generational artifact |
| 31 | Pandemic Outbreaks & Planetary Configurations | Suggestive — Saturn-Uranus p=0.0021 |
| 32 | Historical Prediction Accuracy | **Null** — 56.4%, p=0.26 |
| 33 | Planetary Dignities — Extended | **Positive (selective)** — Writers/Mars; Filmmakers/Sun |
| 34 | Solar Return Predictions — Cosine Method | Mixed — Moon-Lilith/Death (p=0.009) |
| 35 | Project in progress | — |
| 36 | Project in progress | — |
| 37 | Project in progress | — |
| 38 | Project in progress | — |
| 39 | Project in progress | — |
| 40 | Project in progress | — |
| 41 | Project in progress | — |
| 42 | Project in progress | — |
| 43 | Project in progress | — |
| 44 | Project in progress | — |
| 45 | Project in progress | — |
| 46 | Project in progress | — |
| 47 | Project in progress | — |
| 48 | Genetic Algorithm Feature Selection for S&P 500 Prediction Using Planetary Data | Mixed — linear null; GA infrastructure validated |

---

*© Renay Oshop | bigastrologybook.com*
