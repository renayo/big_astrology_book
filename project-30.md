# Project 30: Cross-Cultural Zodiac and Personality (Chinese Zodiac)

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Do birth year animal signs in the Chinese Zodiac predict meaningful differences in Big Five personality traits? Are Dogs more extroverted? Are Roosters more conscientious? Does the 12-year cycle of animals encode real personality information?

---

## ⚠️ The Critical Problem — Up Front

**The Chinese Zodiac is a 12-year cycle. Twelve animal groups in a dataset covering people born across 60–70 years means each group contains people from multiple overlapping generations. Testing "Dog vs. Dragon personality" is functionally testing people born in 1982 vs. 1988.**

Personality traits are systematically shaped by generation. People who grew up during the Great Depression have different Conscientiousness baselines than people who grew up during the 1990s economic boom. People who came of age during social upheaval score differently on Agreeableness and Openness than those who didn't.

**The design conflates zodiac archetype with generational cohort.** Any significant ANOVA result is therefore ambiguous: we cannot know whether we're measuring the animal year or the historical era.

The correct test would compare people born in *the same decade* across different animal years — removing generational confounds while testing zodiac effects. That test was not possible with the available data.

This project is valuable precisely because it **demonstrates the problem clearly** while documenting statistically significant results. The self-awareness about the confound is what makes it honest.

---

## 📊 The Data

| Field | Detail |
|---|---|
| **Dataset** | Open-Source Psychometrics Project (OSPP) Big Five questionnaire |
| **Sample size** | **N = 19,632** (filtered for ages 13–90) |
| **Collection period** | Circa 2018 |
| **Personality measures** | E, N, A, C, O scores |
| **Zodiac calculation** | Birth Year = 2018 − Age; Sign = (Birth Year − 1900) mod 12 |

> *Boundary misclassification: The Chinese New Year falls in January–February, not January 1. People born in January–February may be assigned the wrong animal sign at ~100% for that window — affecting roughly 1/12 of the sample (~1,636 participants).*

---

## 📈 Results

### ANOVA: All Five Traits Statistically Significant

| Trait | F-statistic | p-value | η² (Effect Size) |
|---|---|---|---|
| Extraversion | 3.98 | **8.1 × 10⁻⁶** | ~0.002 |
| Neuroticism | significant | **< 0.001** | ~0.002 |
| Agreeableness | significant | **< 0.001** | ~0.002 |
| Conscientiousness | significant | **< 0.001** | ~0.002 |
| Openness | significant | **< 0.001** | ~0.002 |

Every trait is highly statistically significant. But effect size η² ≈ 0.002 means Chinese Zodiac sign explains approximately **0.2% of Big Five trait variance**.

**Statistical significance ≠ meaningful effect size.** N = 19,632 with 12 groups of ~1,636 each has enormous power to detect vanishingly small effects.

### Personality Profiles by Sign — Peak Values

The Z-score heatmap shows each animal's deviation from the population mean:

| Trait | Highest Sign | Lowest Sign |
|---|---|---|
| Extraversion | **Dog** (Z ≈ +0.12) | Dragon (Z ≈ −0.12) |
| Conscientiousness | **Rooster** (Z ≈ +0.10) | Monkey (Z ≈ −0.10) |
| Neuroticism | Goat (peaks notably) | varies |

The patterns are small but internally consistent: Dogs score highest on Extraversion; Roosters on Conscientiousness. These archetypally match traditional Chinese Zodiac descriptions — the loyal, social Dog; the punctual, disciplined Rooster. But whether these fits reflect zodiac effects or generational coincidence is exactly what the available data cannot determine.

---

## 🔍 The Confound — A Concrete Example

Consider the Extraversion finding: **Dog years are most extroverted, Dragon years least**.

Dog years in the 2018 dataset include: 1934, 1946, 1958, 1970, 1982, 1994, 2006.
Dragon years include: 1940, 1952, 1964, 1976, 1988, 2000, 2012.

The 1994 Dogs (Millennials, age 24 in 2018) are systematically compared to the 1988 Dragons (Millennials, age 30 in 2018). But the cohort also spans 1946 (postwar baby boom) vs. 1952 (Korean War era). **These populations differ for historical reasons that have nothing to do with animal signs.**

The 6-year age offset between Dog and Dragon groups in 2018 means at the younger end (ages 12–25), Dog people are 6 years younger than Dragon people. Age alone produces personality differences in this developmental range.

---

## 🔬 What a Valid Test Would Look Like

1. **Control for age as a continuous covariate** (ANCOVA). If zodiac effects survive after removing age, that's genuine evidence.

2. **Compare same-cohort, different-sign participants.** People born within the same 5-year window contain multiple animal signs — comparing them tests zodiac without generational noise.

3. **Longitudinal design.** The same people retested across multiple 12-year cycles would show whether scores track their generation or their animal sign.

None of these were possible with birth-year-only data.

---

## ⚠️ Limitations & Caveats

- With N=19,632, even η² = 0.001 would achieve significance. P-values tell us effects are non-zero; η² tells us whether they matter.
- Chinese New Year misclassification affects ~1/12 of participants.
- OpenPsychometrics participants are self-selected — younger, more educated, more digitally engaged than the general population.
- Ages 13–90 span 5–6 complete 12-year zodiac cycles, maximizing the generational confound.

---

## 🌟 Conclusion

Big Five personality scores differ significantly across Chinese Zodiac animal signs (every trait p < 0.001), with profiles matching certain traditional archetypes (Dog = Extroverted, Rooster = Conscientious).

**However, these results cannot be interpreted as evidence for Chinese Zodiac effects on personality.** The 12-year cycle creates systematic generational confounds in any cross-sectional dataset. The "zodiac differences" almost certainly reflect birth cohort differences — generational, historical, developmental — rather than the animal year archetype.

**Statistically significant. Likely confounded by generation.** The project is valuable as a demonstration of why cross-sectional zodiac research requires age controls — not as confirmation of Chinese Zodiac personality effects. Future work using birth-month data and age-matched designs would be needed to separate the signals.
