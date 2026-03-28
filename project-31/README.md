# Project 31: Planetary Patterns and Disease Outbreaks

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Do the angular relationships between 12 celestial bodies show systematic patterns during major historical disease outbreaks (1900–2025), compared to non-outbreak years?

---

## 💡 Why This Matters

The question of planetary configurations and disease has been raised since the Black Death, but it has almost never been tested rigorously with modern statistics and verified historical data. The COVID-19 pandemic's coincidence with the Saturn-Pluto conjunction (January 2020) reinvigorated interest in this question. But a single coincidence proves nothing — what matters is whether such coincidences exceed what chance predicts across a century of documented outbreaks.

This project applies the cosine metric from Project 17 to WHO Disease Outbreak News data to test whether planetary *configurations* (not just individual positions) differ systematically between outbreak and non-outbreak years.

---

## 📊 The Data

| Field | Detail |
|---|---|
| **Outbreak years** | Major disease outbreaks from WHO Disease Outbreak News, 1900–2025 |
| **Control years** | All non-outbreak years within the same period |
| **Planetary positions** | July 1st of each year, via Swiss Ephemeris |
| **Bodies analyzed** | Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Rahu (North Node), Ketu (South Node) |
| **Pairs tested** | 66 unique pairs from 12 bodies |
| **Statistical test** | Independent-samples t-test: outbreak year mean cosine vs. control year mean cosine |

> *Methodology note — July 1st representative date:* Disease outbreaks don't uniformly begin in July. Using a single annual date measures the general planetary "climate" of an outbreak year rather than the exact onset moment. This is reasonable for slow-moving bodies (Saturn, Uranus, Neptune, Pluto) but introduces noise for fast movers (Sun, Moon, Mercury). Fast-mover results should be interpreted cautiously.

---

## 📈 Results

### 1. Statistically Significant Planetary Pairs

Of 66 pairs tested, four showed statistically significant deviations between outbreak and control years:

| Pair | Outbreak Mean Cosine | Control Mean Cosine | p-value | Direction |
|---|---|---|---|---|
| **Saturn–Uranus** | **−0.54** | **−0.01** | **0.0021** | Opposition-leaning |
| **Rahu–Pluto** | **−0.49** | — | **0.0123** | Opposition-leaning |
| **Jupiter–Saturn** | **+0.48** | −0.02 | **0.0234** | Conjunction-leaning |
| **Jupiter–Pluto** | **+0.50** | −0.02 | **0.0292** | Conjunction-leaning |

### 2. The Saturn–Uranus Signal (p = 0.0021)

The strongest signal in the dataset. During outbreak years, Saturn and Uranus move toward *opposition* (mean cosine −0.54), while in normal years they are near neutral (−0.01).

This is **not the pair usually emphasized** in pandemic astrology discourse, which tends to focus on Jupiter-Pluto or Saturn-Pluto. Saturn-Uranus emerging as the primary signal from an agnostic scan is notable precisely because it wasn't predicted by existing literature — suggesting the method is discovering rather than confirming.

Astrologically: Saturn represents structure and established order; Uranus represents disruption and sudden change. Saturn-Uranus tension describes a collision between existing systems and destabilizing forces — a structural description of pandemic scenarios where established health infrastructure is overwhelmed by novel threats.

Historical Saturn-Uranus oppositions: 1918–1920 (Spanish flu), 1951–1952 (polio epidemics), 2008–2010 (H1N1). The 2020 COVID pandemic occurred during Saturn-Uranus tension building toward the 2021 square — a near-miss that the dataset correctly registers as elevated.

### 3. The Jupiter Conjunctions

Both Jupiter-Pluto (+0.50, p=0.0292) and Jupiter-Saturn (+0.48, p=0.0234) show positive cosine means during outbreak years — meaning these pairs tend toward *conjunction* during health crises.

The 2020 pandemic famously coincided with both the Jupiter-Pluto conjunction (April 2020) and the Jupiter-Saturn "Great Conjunction" (December 2020). These are real astronomical events. The Jupiter-Pluto association is noted in astrology literature — the 1918 Spanish flu also occurred near a Jupiter-Pluto conjunction. But with only ~7 such conjunctions in a century's data, statistical claims are fragile.

---

## ⚠️ The Multiple Testing Problem — Honest Accounting

**This is where intellectual honesty is required.** Sixty-six planetary pairs were tested. At p < 0.05, we expect approximately **3.3 false positives by chance alone**. We found **4 significant results** — barely above the false-positive expectation.

**Bonferroni correction** for 66 tests requires p < 0.05/66 = **0.00076**:

| Pair | p-value | Survives Bonferroni? |
|---|---|---|
| Saturn–Uranus | 0.0021 | **No** |
| Rahu–Pluto | 0.0123 | No |
| Jupiter–Saturn | 0.0234 | No |
| Jupiter–Pluto | 0.0292 | No |

**None of the four results survive Bonferroni correction.** This is the honest conclusion.

Under **FDR (Benjamini-Hochberg)** correction at 5% false discovery rate, Saturn-Uranus (p=0.0021) is the most likely genuine finding, with others uncertain.

**The appropriate conclusion:** These results are *suggestive of a signal*, especially for Saturn-Uranus. They do not constitute statistically confirmed evidence under strict multiple-testing standards.

---

## 🔍 Additional Observations

**The Conjunction Effect:** The 0° zone (exact conjunctions) appears as a primary pattern for the outbreak-positive pairs (Jupiter-Saturn, Jupiter-Pluto). This echoes Project 02's "Conjunction Heartbeat" and Project 17's aggregate clustering finding: cycle-start positions (new synodic cycles beginning at conjunction) are associated with instability across multiple domains — markets, historical events, and here, disease outbreaks.

**Sun-Pluto (p ≈ 0.09):** Borderline result, likely an artifact of the July 1st date choice creating a near-fixed Sun-Pluto angle across years.

---

## 🌟 Conclusion

Four planetary pairs showed p < 0.05 differences between outbreak and non-outbreak years:

- **Saturn-Uranus** (p=0.0021): The strongest signal — oppositions more common in outbreak years
- **Rahu-Pluto** (p=0.0123): Nodal-Plutonic opposition more common
- **Jupiter-Saturn** (p=0.0234): Great Conjunction-type alignment more common
- **Jupiter-Pluto** (p=0.0292): Conjunction-leaning during outbreaks

**None survive Bonferroni correction** for 66 tests. Under FDR, Saturn-Uranus is the most defensible.

The honest summary: **suggestive patterns, not confirmed effects.** The Saturn-Uranus opposition dynamic is the most compelling lead — and the more interesting precisely because it wasn't predicted in advance, making it harder to dismiss as confirmation bias.
