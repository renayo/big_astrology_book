# Project 11: Longitudinal Health and Longevity

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Do natal astrological factors — Sun sign, elemental emphasis, Saturn aspects — predict longevity or death timing in a large dataset of celebrity deaths? Does the birthday effect (dying near one's solar return) hold up? And do planets in traditional "malefic" positions shorten lives?

---

## 💡 Why This Matters

Medical astrology is one of the oldest branches of the tradition. Ptolemy wrote extensively about astrological indicators of health and lifespan. The modern claim — that certain planetary configurations "afflict" health while others protect it — has never been rigorously tested on a large, verified dataset.

This project uses 936 celebrity deaths with verified birth and death dates to test whether any astrological factor predicts lifespan, death timing, or age at death.

---

## 📊 The Data

| Parameter | Value |
|---|---|
| N | **936 verified celebrity deaths** |
| Date range | Deaths 1929–2024 |
| Birth data quality | AstroDatabank / Wikipedia, verified birth dates |
| Method | Cosine similarity of planet position at death vs. natal position |

**Cosine interpretation for planetary timing:**
- **+1.0** = Planetary Return (planet at same zodiacal position as at birth)
- **−1.0** = Opposition (planet at opposite natal position)
- **0.0** = Random (planet at 90° from natal position)

---

## 📈 Results

### 1. Planetary Timing of Death

| Planet | Mean Cosine | p-value | Interpretation |
|---|---|---|---|
| **Sun** | +0.011 | 0.628 | **No birthday effect** |
| Moon | −0.049 | 0.038* | Slight tendency to die at Moon Opposition |
| Mercury | +0.046 | 0.042* | Slight tendency near Mercury Return |
| Saturn | +0.136 | <0.001* | **Age artifact — see below** |
| Uranus | +0.226 | <0.001* | **Age artifact — see below** |
| Neptune | −0.590 | <0.001* | **Age artifact — see below** |
| Pluto | −0.420 | <0.001* | **Age artifact — see below** |

### 2. ⚠️ The Critical Artifact: Age and Planetary Cycles

The most dramatic results — Saturn, Uranus, Neptune, Pluto — are **not astrological findings**. They are mathematical consequences of human lifespan combined with planetary periods.

**Saturn Return at ages ~29, ~58, ~88:** Most people die between ages 60–90. This overlaps heavily with the second and third Saturn returns. The "Saturn Conjunction" effect at death simply means most people die at ages when Saturn happens to be near its natal position.

**Uranus Return at age ~84:** Uranus completes one orbit in ~84 years. Its return therefore occurs at approximately the median death age in a celebrity dataset. The high positive cosine for Uranus is a tautology: people die at ~84, and at ~84, Uranus is completing its return.

**Neptune Opposition at age ~82:** Neptune takes ~165 years; its Opposition falls around age 82–83 — near the mode of celebrity deaths.

**None of these outer-planet signals should be interpreted astrologically.** They are precise artifacts of the demographic distribution of death ages combined with known planetary periods.

### 3. The Birthday Effect: Definitively Absent

| Metric | Observed | Expected (random) |
|---|---|---|
| Mean days from birthday at death | 90.4 days | 91.2 days |
| Deaths within 7 days of birthday | 4.0% | 3.8% |
| Correlation of death DOY with birth DOY | r = −0.006 | — |
| p-value | **0.865** | — |

**Deaths are uniformly distributed throughout the year relative to birthdays.** The folk belief that people die near their birthdays is not supported in this dataset.

### 4. Sun Sign and Longevity

| Sign | Mean Age at Death | Deviation from Average (66 yrs) |
|---|---|---|
| Cancer | 70.9 | +4.9 yrs |
| Taurus | 68.6 | +2.6 yrs |
| … | … | … |
| Aquarius | 62.9 | −3.1 yrs |
| Scorpio | 61.9 | −4.1 yrs |

**Chi-square: p = 0.964.** The variation between signs is entirely consistent with random sampling from the same underlying distribution.

### 5. Elemental Longevity

| Element | Mean Age at Death |
|---|---|
| Earth | 66.5 |
| Fire | 66.0 |
| Water | 66.1 |
| Air | 65.4 |

**ANOVA p = 0.957.** No significant difference.

### 6. Saturn Aspects and Longevity

Traditional medical astrology holds that Saturn "afflictions" (hard aspects to Sun or Moon) shorten life. The data:

| Group | Mean Age at Death | p-value |
|---|---|---|
| Hard Saturn-Sun or Moon aspect | 66.3 yrs | 0.71 |
| No hard Saturn aspect | 65.8 yrs | — |

Not significant. The 0.5-year difference is within noise.

### 7. The Fast-Planet Signals

After discarding all outer-planet results as age artifacts, two fast-planet findings at p < 0.05:

- **Moon Opposition at death** (mean cosine −0.049, p = 0.038)
- **Mercury Return at death** (mean cosine +0.046, p = 0.042)

These planets move quickly enough to avoid the age confound (Moon: 27 days per cycle; Mercury: 88 days). If real, they represent genuine timing signals — small ones.

However: two significant results from 11 planetary tests is exactly what would be expected by chance at α = 0.05. These findings are not Bonferroni-corrected and should be treated as hypothesis-generating only.

---

## 🔍 What the Numbers Mean

The clean takeaway: **no natal astrological factor predicts lifespan or death timing in this dataset.**

- Sun sign has no effect on lifespan (p = 0.964)
- Elements have no effect (p = 0.957)
- Saturn "afflictions" don't shorten life (p = 0.71)
- The birthday effect doesn't exist (p = 0.865)
- Outer planet timing at death reflects mortality demographics, not astrology

The two marginal fast-planet findings (Moon, Mercury at p ≈ 0.04) are interesting but unconfirmed at corrected thresholds. They need pre-registered replication on an independent death dataset.

---

## ⚠️ Limitations & Caveats

- **Original design (UK Biobank)** was not achievable — formal data access was required and not obtained. The celebrity death analysis is a valid alternative but not the gold-standard design.
- **Celebrity selection bias:** Famous people are not representative mortality samples. They may have better healthcare access, more public scrutiny of risk behaviors, and different SES characteristics.
- **Survival analysis not implemented:** People still alive at data collection should be censored, not excluded.
- UK Biobank-style analysis (500K people, disease onset, SES controls) remains the ideal dataset for medical astrology claims.

---

## 🌟 Conclusion

Across 936 celebrity deaths, no evidence was found that natal astrological factors predict longevity or death timing:

- **Birthday effect:** Absent
- **Sun signs:** No effect (p = 0.964)
- **Elements:** No effect (p = 0.957)
- **Saturn afflictions:** No effect (p = 0.71)
- **Outer planet timing:** Strong signals that are entirely explained by age demographics

The most honest summary: this dataset finds no evidence for astrological effects on lifespan. The apparent signals in outer-planet timing are precisely what you'd predict from mortality demographics alone, with no astrology involved.
