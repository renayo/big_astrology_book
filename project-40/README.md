# Project 40: Medical Astrology & Decumbiture — What 82 Million ED Visits Reveal

> **Source:** [bigastrologybook.com/project-40](https://bigastrologybook.com/project-40/)
> **Archive Date:** 2026-03-21
> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Dataset:** NYC Department of Health Syndromic Surveillance data, ~82 million Emergency Department visits aggregated into 1,008 unique days; 45 planetary pair cosine metrics per day; Pearson correlation with daily admission severity ratio

---

## Research Question

Among all planetary pair configurations observable on any given day, which correlate significantly with illness severity — specifically with the rate at which Emergency Department visits become hospital admissions? And do the traditional indicators of medical astrology — Moon-Mars and Moon-Saturn aspects, the Moon's passage through afflicted positions — show genuine signal in a dataset of this scale?

## Background: The Decumbiture Tradition

Medical astrology is among the most ancient and practically oriented branches of the discipline. The *decumbiture chart* — the astrological chart cast for the moment when a patient first falls ill and "takes to their bed" (from the Latin *decumbere*) — was a central tool of European medical practice from approximately the twelfth through the seventeenth century. Physicians trained in the Galenic tradition used the decumbiture to assess prognosis, identify the nature of the illness, and determine the best timing for treatment.

The key indicators in decumbiture theory are predictable given astrological symbolism: the Moon, as ruler of bodily fluids and the vital moist principle, is most important. Its aspects on the day of illness are critical. Moon conjunct or square Mars indicates inflammatory illness, fever, acute crisis. Moon conjunct or square Saturn indicates chronic debility, obstruction, cold conditions, poor vitality. The Moon's house placement, its reception by planets, and the Ascendant of the chart all contribute to the prognosis.

This project tests the decumbiture tradition directly — not against individual patient charts, but against aggregate emergency department data covering over 82 million visits across 1,008 days. If planetary configurations genuinely influence illness severity, the collective signal should be detectable at this scale.

---

## Methodology: Cosine Metrics Over Binary Aspects

Traditional aspect analysis uses binary categories: an aspect is either "applying" within orb or it is not. This introduces an arbitrary cutoff — is 9° conjunct with a 10° orb truly meaningfully different from 11° conjunct outside it? The cosine approach used throughout this book replaces the binary with a continuous measure:

$$\text{Cosine}_{AB} = \cos(\theta_A - \theta_B)$$

where θ_A and θ_B are the longitudes of any two planets. This maps the full 0–360° range to a continuous [−1, +1] scale:
- +1.0 = exact conjunction (0°)
- 0.0 = exact square (90°) or quincunx
- −1.0 = exact opposition (180°)

For 10 planetary bodies (Sun through Pluto), there are 45 unique planetary pairs. Each day in the dataset receives 45 cosine values, and each of these is correlated with that day's illness severity ratio.

| Field | Detail |
|---|---|
| **Dataset** | NYC Department of Health Syndromic Surveillance |
| **Volume** | ~82 million Emergency Department visits |
| **Days analyzed** | 1,008 days |
| **Severity metric** | Admissions / Total ED Visits (daily ratio) |
| **Feature** | 45 planetary pair cosines per day |
| **Statistical test** | Pearson correlation (r) with two-tailed p-values |

---

## Results: Part I — The Outer Planet Artifacts

The most striking correlations in the raw data come from outer planet pairs, and they require careful interpretation before any astrological claim can be made.

| Pair | Correlation (r) | p-value | True Interpretation |
|---|---|---|---|
| **Uranus-Pluto** | **+0.49** | < 10⁻⁶⁰ | Generational artifact |
| **Uranus-Ketu (South Node)** | **+0.46** | < 10⁻⁵⁰ | Generational artifact |
| **Uranus-Neptune** | **+0.46** | < 10⁻⁵⁰ | Generational artifact |
| **Neptune-Pluto** | **+0.43** | < 10⁻⁴⁰ | Generational artifact |

These r values of 0.43–0.49 are extremely large for epidemiological data. A correlation of r = 0.49 between any two variables in a dataset of this scale would typically be the finding of the decade. But these are not astrological findings. They are the signature of temporal clustering — the same lesson learned in Project 34 (Uranus-Neptune/death) and Project 36 (Uranus-Pluto/divorce), now manifesting in medical data.

Uranus and Pluto move so slowly that their angle to each other changes at a rate of only a fraction of a degree per day. Over the 1,008 days of the dataset (approximately 2.75 years), their angular relationship shifts by roughly 5–15 degrees total. The Uranus-Pluto cosine is essentially a trend variable — it increases smoothly across the dataset from beginning to end (or vice versa). Any other variable that also contains a secular trend across the same time window will correlate with it strongly.

The question is: what secular trend in NYC Emergency Department admission rates explains this? Medical presentation patterns shift seasonally, but more importantly, they shift across years. Changes in influenza strain virulence, COVID variant emergence, policy shifts in ED triage protocols, demographic changes in the population — all of these operate on timescales of months to years. Any of these long-period trends, coinciding with the long-period slow movement of Uranus and Pluto, will produce the correlation observed.

The r = 0.49 for Uranus-Pluto is not evidence of "generational crisis" in medical terms. It is evidence that whatever drove secular trends in NYC ED admission severity rates during the study period happened to co-vary with the slow angular drift of the outer planets. This is methodologically identical to the artifacts in Projects 34 and 36 and must be treated the same way: discard as confounded, examine what remains.

---

## Results: Part II — The Genuine Signals

After filtering for fast-to-medium speed planets that do not simply track time trends, two genuinely significant correlations emerge:

| Pair | Correlation (r) | p-value | Classification |
|---|---|---|---|
| **Sun-Saturn** | **+0.29** | < 10⁻²⁰ | **Genuine signal** |
| **Mars-Saturn** | **+0.27** | < 10⁻¹⁸ | **Genuine signal** |

The Sun completes a full cycle in one year; Saturn completes a cycle in 29 years. Their angular relationship cycles through all 360 degrees over a 12-month period (the synodic period of Sun-Saturn is approximately 12.4 months). This is not a trend variable — it oscillates at a rate that is genuinely independent of secular trends in the dataset. The correlation between Sun-Saturn alignment and daily illness severity is therefore a genuine signal.

**Sun-Saturn (r = +0.29):** Traditional medical astrology interprets Saturn as the planet of chronic weakness, debility, and resistance to vital force. The Sun represents vitality, health, and the animating life principle. Their conjunction (+1.0 cosine, meaning Saturn is "on top of" the Sun) is traditionally associated with periods of diminished vitality — the "vitality drain," as medieval astrologers called it. The data shows this: when the Sun and Saturn are in close conjunction (cosine approaching +1.0), the ratio of NYC emergency visits that require hospital admission is significantly higher. Days when the Sun-Saturn angle is at maximum separation (opposition) show lower severity ratios.

This is not a small effect for the dataset's parameters. A Pearson r of 0.29 with p < 10⁻²⁰ across 1,008 days — representing 82 million ED visits — suggests the Sun-Saturn conjunction is associated with a meaningfully elevated rate of illness severity at the population level.

**Mars-Saturn (r = +0.27):** The pairing of Mars and Saturn has been called the "Great Malefic Pair" in traditional astrology — the combination of acute force (Mars: inflammation, fever, sharp pain) with chronic hardship (Saturn: restriction, obstruction, cold). When these two planets conjoin, traditional astrology predicts heightened suffering. The data shows a statistically significant positive correlation consistent with this interpretation: when Mars and Saturn are conjunct or near-conjunct, admission severity ratios in NYC emergency departments are elevated.

Both of these findings survive the methodological scrutiny that correctly eliminated the outer-planet artifact results. The Sun and Mars both move fast enough that their annual cycles with Saturn create genuine temporal variation rather than secular trends.

---

## Results: Part III — Decumbiture Debunked

Traditional decumbiture theory emphasized the Moon above all other bodies. The Moon's aspects on the day of illness were considered the primary indicator of severity and prognosis. This project provides a direct test:

| Pair | Correlation (r) | p-value | Finding |
|---|---|---|---|
| **Moon-Saturn** | +0.01 | 0.74 | **Null** |
| **Moon-Mars** | −0.01 | 0.76 | **Null** |

These results are as close to zero as a real dataset ever produces. The Moon-Saturn correlation on illness severity is 0.01 — essentially unmeasurable. Moon-Mars is −0.01, in the opposite direction from prediction. Both p-values are far from significance.

This is a significant finding for the decumbiture tradition specifically. The Moon was considered the primary timer in medical astrology — the planet whose daily motion made decumbiture charts uniquely time-sensitive. The idea was that the Moon's passage through different degrees and aspects could be tracked through the illness, with critical days occurring when the Moon made specific aspects. The data says this doesn't work at the population level.

Why would the Moon fail while Sun-Saturn and Mars-Saturn succeed? Several considerations:

**Speed and signal averaging.** The Moon moves approximately 13° per day, completing its cycle in 27–28 days. This means its aspects to any given planet change multiple times daily and cycle through all configurations approximately 13 times per year. When 82 million ED visits are aggregated daily, the averaging effect may smooth out any Moon-driven variation that operates at finer timescales (hourly, for instance).

**Background climate versus daily weather.** The Sun-Saturn synodic cycle operates on a 12-month timescale — it represents the "climate" of the year. The Mars-Saturn cycle operates on a roughly 25-month timescale. These are slow-enough cycles that they create genuine monthly variation in the aggregate data. The Moon's 28-day cycle creates variation, but it may be variation that averages out when 80,000–100,000 daily ED visits are combined into a single severity ratio. Individual Moon-sensitive days exist; they are swamped by the aggregate.

**A structural limitation of aggregate data.** Decumbiture was always an individual-level technique — the Moon's aspects matter for *this patient* on *this day*, not for the average of 80,000 patients. The aggregate design may systematically miss exactly the Moon-driven variation that individual-level decumbiture was designed to detect.

---

## Summary Table

| Planet Pair | r | p-value | Status |
|---|---|---|---|
| Uranus-Pluto | +0.49 | < 10⁻⁶⁰ | Artifact — secular trend |
| Uranus-Neptune | +0.46 | < 10⁻⁵⁰ | Artifact — secular trend |
| Neptune-Pluto | +0.43 | < 10⁻⁴⁰ | Artifact — secular trend |
| Mercury-Neptune | +0.41 | < 10⁻⁴⁰ | Likely artifact — investigate |
| **Sun-Saturn** | **+0.29** | **< 10⁻²⁰** | **Genuine — fast/medium cycle** |
| **Mars-Saturn** | **+0.27** | **< 10⁻¹⁸** | **Genuine — medium cycle** |
| Moon-Saturn | +0.01 | 0.74 | Null — daily cycle averages out |
| Moon-Mars | −0.01 | 0.76 | Null — daily cycle averages out |

---

## Statistical Caveats

**Artifact identification relies on speed heuristics.** The classification of outer-planet correlations as "artifacts" and inner-planet correlations as "genuine" rests on the argument that fast-enough cycles cannot produce secular trend confounds. This argument is sound for Sun-Saturn (12-month synodic cycle) but less clear for Mars-Saturn (~25-month cycle). A rigorous detrending analysis (removing long-period components from both the planetary series and the severity ratio series before correlating) would provide stronger confirmation.

**Causation is undetermined.** Even the genuine Sun-Saturn and Mars-Saturn correlations cannot establish causation. They may reflect shared seasonal or annual patterns in both illness severity and planetary positions. The Sun-Saturn conjunction occurs once per year in a specific calendar period; if illness severity systematically varies by calendar period for non-astrological reasons (influenza season, respiratory virus peaks, etc.), this could create the observed correlation.

**NYC-specific sample.** The dataset reflects the epidemiological profile of New York City — a dense, highly mobile, specific climate, with specific socioeconomic patterns affecting ED utilization. Replication in other cities or countries would be needed before generalizing.

**Mercury-Neptune correlation.** The r = +0.41 Mercury-Neptune correlation is shown in the complete results table but was not classified above as either artifact or genuine. Mercury's cycle is fast enough (88-day orbit) that it may not be a pure trend variable, but Neptune's extreme slowness means any Mercury-Neptune aspect oscillates on a very long background arc. This result warrants investigation with detrending before acceptance.

---

## Conclusion

This project's central finding is a lesson in layers: beneath the spectacular-looking but artifactual outer-planet correlations lies genuine signal from the traditional astrological malefic pair.

**Outer planets (Uranus, Neptune, Pluto) produce large correlations that are secular trend artifacts**, not astrological effects. They track the same long-period demographic and policy changes that cause illness severity ratios to drift across multi-year periods. This is the third major study in this book (after Projects 34 and 36) to demonstrate this pattern explicitly.

**Sun-Saturn (r=+0.29) and Mars-Saturn (r=+0.27) show genuine population-level associations with illness severity**, surviving the methodological scrutiny that eliminates the artifactual results. The traditional "malefic" pairing — Saturn's restraining weight applied to the Sun's vitality and Mars's acute force — appears in the data in the direction traditional medical astrology predicts.

**Moon-based decumbiture indicators are null** at the aggregate level. Moon-Saturn and Moon-Mars show r values indistinguishable from zero. Whether this means the Moon has no role in illness dynamics or merely that its rapid daily cycle averages out in aggregate population data is a question that individual-level studies would need to address.

Medical astrology's "climate" indicators survive; its daily "weather" indicators do not. The broadest strokes of the tradition — the malefic planets, the configuration of chronic hardship — show population-level traces. The finer brushwork of decumbiture timing, measured through the Moon's daily passages, does not register in 82 million visits averaged by day.

---

*Archived source data, cosine correlation outputs, and visualization files preserved in `backup/`.*
