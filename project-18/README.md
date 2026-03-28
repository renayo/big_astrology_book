# Project 18: Solar House System Analysis (Surya Lagna)

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com](https://bigastrologybook.com)

---

## 🌟 Overview — What We Asked

Can Solar House systems — where the Sun substitutes for the Ascendant, eliminating the need for birth time — produce above-chance predictions about career archetypes? Do planets falling in specific houses relative to the Sun predict what kind of work someone does?

---

## 💡 Why This Matters

The single biggest obstacle to large-scale astrological research isn't motivation — it's birth time. Traditional house systems require birth time accurate to within 4–15 minutes. Most historical figures lack this. Most large public databases (Wikidata, census records, genealogy archives) contain birth *date* but not birth *time*.

Solar Houses bypass this constraint entirely by anchoring the chart to the Sun's position, which is known from date alone:

- **Solar Whole Sign:** The Sun's sign becomes the entire 1st House; each subsequent sign maps to subsequent houses.
- **Solar Equal House:** The Sun's exact degree becomes the 1st House cusp; houses are 30° arcs from that point.

These are real astrological techniques — used in Western astrology as "Solar Charts" and in Vedic astrology as *Surya Lagna* ("Sun Ascendant"). If they work at above-chance rates, they open millions of historical figures to astrological study.

---

## 📊 The Data

86 celebrities from Project 06, verified birth dates, across 6 professional categories. The **random expected hit rate is 25%** (3 target houses out of 12 = 25% chance of a random "hit").

### Archetype-to-House Mapping

For each profession, "target" planet-house combinations were defined from traditional astrological symbolism:

| Category | Target Planets | Target Houses |
|---|---|---|
| Scientists | Uranus, Mercury | 9th, 11th |
| Artists | Venus, Neptune | 5th, 12th, 2nd |
| Politicians | Sun, Jupiter | 10th, 11th |
| Athletes | Mars, Sun | 1st, 10th |
| Writers | Mercury, Jupiter | 3rd, 9th |
| Philosophy | Saturn, Jupiter | 9th, 11th |

Total checks: 274 (86 celebrities × ~3.2 checks per person, reflecting multiple planet-house combinations per archetype).

> *Critical methodological note: The results stand or fall on whether these archetype-to-house mappings were specified before analysis. The mappings align with established traditional astrological symbolism, suggesting they were not data-driven — but the study should have explicitly confirmed pre-specification in documentation.*

---

## 📈 Results

### Hit Rates vs. Random Baseline

| System | Hits | Total Checks | Hit Rate | vs. 25% Baseline |
|---|---|---|---|---|
| **Solar Equal House** | **87** | **274** | **31.8%** | **+6.8%** |
| **Solar Whole Sign** | **86** | **274** | **31.4%** | **+6.4%** |
| Random Baseline | — | — | 25.0% | — |

Both systems produce hit rates approximately 6–7 percentage points above the 25% random baseline. The effect is modest but consistent across both variants.

### Bayesian Evidence

| System | Bayes Factor | Interpretation |
|---|---|---|
| Solar Equal House | **BF = 23.53** | **Strong Evidence** |
| Solar Whole Sign | **BF = 17.00** | **Strong Evidence** |

By conventional Bayesian benchmarks (BF > 10 = strong evidence; BF > 100 = decisive), both systems provide strong evidence that hit rates exceed 25%. The data is approximately 24× more likely if Solar Equal House predicts careers than if it doesn't.

Solar Equal House marginally outperforms Whole Sign (BF 23.53 vs. 17.00), suggesting the Sun's exact degree carries more information than its sign membership alone.

---

## 🔍 What the Numbers Mean

A 31–32% hit rate against a 25% baseline is modest in absolute terms. Six or seven extra correct classifications per hundred. But for a technique that requires no birth time — unlocking potentially millions of historical records — even modest hit rates carry practical significance.

The Bayes Factor result is noteworthy: BF = 23.53 means the data strongly favors the hypothesis that Solar Equal House works over the null. This is not a marginal finding; it's a substantial Bayesian update.

**Solar Equal House vs. Whole Sign:** The difference (23.53 vs. 17.00) suggests the Sun's exact degree matters — not just which sign contains the Sun, but where in that sign it sits. This is consistent with treating the Sun as a precise "sensitive point" rather than a categorical label.

---

## ⚠️ Limitations & Caveats

**Dependence among observations:** 274 checks across 86 people means an average of ~3.2 checks per person. These are not independent — multiple checks for the same person share the same Sun position. The effective sample size is closer to 86 than 274. With N=86, the BF values would be lower, though the directional result (above 25%) would remain.

**The pre-specification problem:** The hit rate depends entirely on which planet-house combinations are defined as "hits" for each profession. If mappings were chosen after observing data, the results are inflated. Using traditional astrological symbolism as the source of mappings is the strongest argument for validity here.

**Replication needed:** The strongest version would train archetype mappings on half the data and test on the other half. The current study reports in-sample performance only.

---

## 🌟 Conclusion

Both Solar House variants produce hit rates of ~31–32% against a 25% random baseline, with Bayes Factors of 17–24 providing strong evidence against the null.

**The practical implication:** Solar Houses may be a viable research tool for populations without reliable birth times — opening large historical databases to astrological study. Project 15's WLS analysis and Project 13's celebrity datasets both suffered from the birth-time limitation. Solar Houses offer a path around it.

The critical outstanding question is pre-specification. If the archetype-to-house mappings were locked in before analysis (as the use of traditional symbolism implies), this is a meaningful positive finding. If not, replication on an independent dataset is required.

> **What's next:** A pre-registered study applying Solar Equal House archetype mappings to a held-out dataset of 200+ professionals with verified birth dates, specifying all mappings before analysis begins.
