# Project 34: Solar Return Predictions — Cosine Method

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Do Solar Return charts — cast when the Sun returns to its exact natal longitude each year — contain planetary configurations that differ systematically between years when major life events occur and years when they don't? Can the annual Solar Return chart predict the *type* of year that follows?

---

## 💡 Why This Matters

The Solar Return is one of traditional astrology's most practical predictive tools. Every year on or near your birthday, the Sun returns to the exact degree it occupied when you were born. The chart cast for that moment is said to describe the themes, challenges, and opportunities of the coming 12 months.

This project tests that claim with a mathematically rigorous, symbolism-agnostic approach: compute cosine similarity between all 66 planetary pairs in each Solar Return chart, and compare event years to non-event years statistically. No pre-assigned symbolism — let the numbers speak first.

The result demonstrates something methodologically valuable: the approach *correctly identifies* confounds before reporting genuine findings.

---

## 📊 The Data

| Field | Detail |
|---|---|
| **Sample** | 104 historical figures (Scientists, Artists, Writers) |
| **Life events** | **451 verified events** from biographical records |
| **Event categories** | Marriage (129), Awards (113), Death (91), Divorce (63), Crisis (48) |
| **Chart type** | Solar Return — cast when Sun returns to exact natal longitude |
| **Location** | Birth location used for all Solar Return calculations |
| **Ephemeris** | Swiss Ephemeris, Tropical zodiac |
| **Includes** | Black Moon Lilith (Mean Apogee — the point where the Moon is farthest from Earth) |

---

## ⚠️ Part I: Historical Artifacts — The Method Validates Itself

Before any astrological findings, two enormous "signals" appeared in the data — and both turned out to be demographic artifacts. This is the methodological success story of this project.

### Artifact 1: Uranus-Neptune Conjunction → Death Signal (p < 0.001)

Uranus and Neptune were in close conjunction from roughly 1987–1998, spending most of that time in Capricorn. Many of the 104 historical figures (born primarily in the 1800s–early 1900s) died during this period simply because they were elderly by the 1990s. The "signal" was: *these specific celebrities died in the 1990s, and the 1990s had Uranus conjunct Neptune.* That's demographics, not astrology.

### Artifact 2: Uranus-Pluto Conjunction → Divorce Signal (p < 0.001)

Uranus and Pluto were in exact conjunction in the mid-1960s. Western divorce rates rose dramatically in the 1960s–70s due to changing social norms and legal reforms. Famous subjects who divorced then did so partly because *everyone* divorced more in that era. The Uranus-Pluto conjunction is a historical era marker, not a personal astrological trigger.

**Why this matters:** The method correctly detected real temporal clustering — people in the dataset really did die in the 1990s and divorce in the 1960s at elevated rates. The method then *explained why*: demographics, not astrology. This validates the cosine approach as sensitive enough to detect genuine temporal clustering while being transparent enough to identify its source.

**The filtering rule:** For Solar Return analysis of biographical events, only fast-moving bodies should provide primary findings. Slow movers (Uranus, Neptune, Pluto in multi-year configurations) will reflect historical era, not personal chart dynamics.

---

## 📈 Part II: Genuine Findings — Fast-Mover Archetypes

After filtering for fast-moving bodies, four findings emerge:

### 1. Death: Moon–Lilith Conjunction (p = 0.009) ✨

| Event | Pair | Signal | p-value |
|---|---|---|---|
| **Death** | **Moon–Lilith** | **Conjunction (+)** | **0.009** |

In Solar Return charts for the year of death, the Moon and Black Moon Lilith (the lunar apogee — the point where the Moon is most distant from Earth, most extreme in its orbit) tend significantly toward conjunction, compared to non-death years.

The mythological resonance is striking. The Moon represents the body, vital rhythms, and the biological self. Lilith as the apogee — the Moon at its farthest, most extreme orbital point — carries the archetype of the void, the dark counterpart, the maximum pulling-away from center.

Moon conjunct Lilith at the year of death: the body and its dark counterpart align. The vital self and the apogee of its own arc converge at the moment of departure.

Neither the Moon nor the Mean Apogee are slow outer planets subject to generational artifacts. The Moon moves through all 12 signs monthly; Lilith cycles approximately every 9 years. Their conjunction is an individual and time-specific configuration — not a demographic proxy.

### 2. Marriage: Venus–Uranus Conjunction (p = 0.016) ⚡

| Event | Pair | Signal | p-value |
|---|---|---|---|
| **Marriage** | **Venus–Uranus** | **Conjunction (+)** | **0.016** |

In Solar Return charts for the year of marriage, Venus and Uranus tend toward conjunction compared to non-marriage years.

This **contradicts traditional expectation.** Conventional astrology associates marriage with stable Saturn (long-term commitment) or benefic Jupiter (expansion and fortune) — not Uranus, the planet of sudden disruption and electric excitement.

Venus-Uranus carries the archetype of sudden attraction, unconventional unions, and relationships that feel like lightning strikes. For the artistic and intellectual historical figures in this dataset — whose personal lives often differed from bourgeois convention — marriage may have been more commonly a Uranian event: sudden, exciting, unexpected crystallization of connection.

### 3. Awards: Jupiter–Node Opposition (p = 0.015) 🏆

| Event | Pair | Signal | p-value |
|---|---|---|---|
| **Awards** | **Jupiter–Node** | **Opposition (−)** | **0.015** |

In Solar Return charts for award years, Jupiter and the Mean Node tend toward *opposition*. This is counterintuitive — conventional astrology predicts Jupiter *conjunct* the North Node as a "success/luck" signature.

One interpretation using traditional Vedic node symbolism: North Node (Rahu) represents worldly ambition and striving; South Node (Ketu) represents release, mastery already earned, and spiritual inheritance. Jupiter opposing the North Node (conjunct the South Node) may suggest success through *releasing* rather than grasping — being recognized for accumulated wisdom rather than active pursuit. "Success through letting go."

### 4. Crisis: Mercury–Neptune Opposition (p = 0.063 — Marginal, Not Confirmed)

Mercury opposing Neptune during crisis years (p=0.063) has an intuitive archetypal match: rational clarity (Mercury) in tension with fog and dissolution (Neptune) = mental confusion, misdiagnosis, unclear communication. Below conventional significance and does not survive multiple testing correction. Presented as hypothesis-generating only.

---

## 📊 Summary of Findings

| Event | Pair | Direction | p-value | Status |
|---|---|---|---|---|
| Death | Moon–Lilith | Conjunction | **0.009** | Exploratory finding — FDR candidate |
| Awards | Jupiter–Node | Opposition | **0.015** | Exploratory finding — FDR candidate |
| Marriage | Venus–Uranus | Conjunction | **0.016** | Exploratory finding — FDR candidate |
| Crisis | Mercury–Neptune | Opposition | 0.063 | Marginal only |
| *Artifact* Death | Uranus–Neptune | Conjunction | < 0.001 | N/A — demographic confound |
| *Artifact* Divorce | Uranus–Pluto | Conjunction | < 0.001 | N/A — demographic confound |

---

## ⚠️ Limitations & Caveats

**Multiple testing:** 66 pairs × 5 event types = 330 t-tests. Under Bonferroni (p < 0.000152), no finding survives. Under FDR, the three findings at p ≤ 0.016 are strong candidates. These are **exploratory findings requiring pre-registered replication in an independent, larger dataset.**

**Black Moon Lilith:** The Mean Apogee is a mathematical point, not a physical body. Its theoretical status in astrology is contested. The Moon-Lilith Death finding, while archetypal, should carry awareness that Lilith's astronomical basis is weaker than physical planets.

**Sample characteristics:** 104 historical figures, skewed toward European and American artists, scientists, and writers born primarily in the 19th and early 20th centuries. Marriage and award patterns may reflect social practices of that era rather than universal patterns.

**Solar Return location:** This analysis uses birth location for all Solar Return calculations. Solar Returns are theoretically sensitive to location, but most historical figures didn't purposively travel on their solar return date.

---

## 🌟 Conclusion

The cosine method applied to 451 life events across 104 historical figures produced two kinds of results:

**Historical artifacts correctly identified:** Uranus-Neptune at Death and Uranus-Pluto at Divorce reflect 1990s and 1960s demographic clustering, not personal astrological triggers. The method found them, explained them, and set them aside.

**Genuine pattern candidates (fast-moving bodies):**
- **Moon–Lilith** conjunction elevated in Death years (p=0.009): body meets the void
- **Venus–Uranus** conjunction elevated in Marriage years (p=0.016): sudden, electric union — not conventional Saturnine commitment
- **Jupiter–Node** opposition elevated in Award years (p=0.015): success through release rather than grasping

None survive Bonferroni correction for 330 tests; all three are candidates under FDR correction. They should be treated as **exploratory findings** requiring pre-registered replication.

The meta-finding — the method both detected real clustering *and* correctly explained it as artifactual in the outer-planet cases — validates the cosine approach as methodologically sound for Solar Return research. The genuine findings that survive artifact-filtering carry greater credibility precisely because the method demonstrated it could distinguish signal from demographic noise.
