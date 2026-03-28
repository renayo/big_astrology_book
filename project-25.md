# Project 25: Fixed Stars and Natal Interpretation

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Do major fixed stars — among the most ancient indicators in astrological tradition — show elevated "intensity" in the birth charts of individuals grouped by cause of fame, death, or biographical category? Do Regulus, Aldebaran, Algol, and the other Royal Stars carry the associations that tradition assigns to them?

---

## 💡 Why This Matters

Fixed stars are astrology's most neglected domain in statistical research. The four Royal Stars — Aldebaran, Regulus, Antares, Fomalhaut — have carried astrological weight since Babylonian times. The tradition assigns them specific character effects: Regulus brings leadership and warns against revenge; Algol brings intense, tumultuous energy; Spica brings unearned brilliance.

These associations have almost never been subjected to population-level quantitative analysis. With N=936 celebrity charts, this project applies a methodologically improved approach and asks whether the symbolic traditions attached to these stars have any empirical grounding.

---

## 📊 The Data

| Source | Description |
|---|---|
| Celebrity Dataset | ~936 public figures, biographical metadata (fate categories) |
| Fixed Star Catalog | 12 major fixed stars; positions from Yale Bright Star Catalog via Swiss Ephemeris |
| Swiss Ephemeris | Planetary positions for 12 bodies (Sun through Pluto + Nodes) |

**The 12 Fixed Stars Analyzed:**

| Star | Approx. Position | Traditional Association |
|---|---|---|
| Algol | 26° Taurus | Intense passion, dramatic fate |
| Aldebaran | 9° Gemini | Honor, courage, public success (Royal Star) |
| Rigel | 16° Gemini | Technical skill, education, wealth |
| Capella | 21° Gemini | Curiosity, speed, freedom |
| Sirius | 14° Cancer | Ambition, fame, creative power |
| Regulus | 29° Leo / 0° Virgo | Nobility, leadership — warns against revenge (Royal Star) |
| Spica | 23° Libra | Brilliance, artistic gifts, unearned success |
| Antares | 9° Sagittarius | Intensity, obsession, crises (Royal Star) |
| Vega | 15° Capricorn | Charismatic, magical influence |
| Altair | 1° Aquarius | Boldness, risk-taking, commercial success |
| Fomalhaut | 3° Pisces | Spirituality, ideals (Royal Star) |
| Deneb | 5° Pisces | Genius, intellectual leadership |

---

## 🔬 Method: Cosine Intensity

Traditional fixed star analysis uses binary orb cutoffs (a conjunction within X degrees counts; outside, it doesn't). This project replaces binary orbs with **cosine intensity**:

**Intensity = cos(δ)** where **δ = |θ_planet − θ_star|**

| Intensity | Angular Separation |
|---|---|
| 1.000 | 0° (exact conjunction) |
| ~0.999 | Within ~2.5° |
| ~0.966 | Within ~15° |

A high-pass filter removes very wide separations, and remaining intensities are **summed** across all 12 planetary bodies. This rewards tight conjunctions exponentially more than loose ones — reflecting how traditional astrologers actually think about exactitude.

Z-scores compare each category's mean intensity to the permuted null distribution (shuffled category labels, fixed birth charts).

---

## 📈 Key Findings

### Statistically Significant Results (|Z| > 2.0)

#### 1. Cancer Diagnosis & Altair: Z = −2.32 (p ≈ 0.024)

Individuals who died of cancer show a **significantly lower** mean Altair intensity than chance. Altair is traditionally associated with boldness, climbing ambition, and commercial success — its *absence* in cancer-death charts is an avoidance pattern. The direction is symbolically coherent: Altair's bold, expansive energy may map inversely to the circumstances of cancer.

#### 2. Overdose Deaths & Regulus: Z = +2.26 (p ≈ 0.030)

Individuals who died of drug overdose show a **significantly higher** Regulus intensity than chance. Regulus is the Royal Star most associated with both great heights and dramatic falls — "the lion's heart" that warns against revenge and excess. Its elevated presence in overdose charts is consistent with the traditional symbolism: the person who reaches the heights and then falls.

This is the study's most provocative finding. Regulus and overdose deaths — the conjunction of lions and destruction — is archetypally precise.

#### 3. Homicide Deaths & Altair: Z = +2.07 (p ≈ 0.042)

Individuals who died of homicide show a **higher** Altair connection than expected — the inverse of the cancer pattern for the same star. Altair's boldness and risk-taking may map differently onto violent death than onto chronic disease death.

### Heatmap Results

Category-level heatmaps were generated for all biographical categories across all 12 stars. Key visual patterns:

- **Politicians and Regulus:** Moderate elevated intensity (consistent with leadership symbolism)
- **Scientists and Rigel:** Slight above-average connection (consistent with technical skill)
- **Arts and Spica:** Mixed — no clear elevation (challenges "artistic gifts" association)
- **Sports and Antares:** No clear elevation (challenges "competitive intensity")

Most category-star combinations show **no systematic pattern** — the heatmaps are largely uniform, with the three significant results standing out against a background of null findings.

---

## ⚠️ Limitations & Caveats

**Multiple testing:** With 12 stars × 12 planets × 6+ categories × 2 zodiacs, hundreds of comparisons were implicitly made. A Bonferroni correction for 100 tests requires p < 0.0005 — the three results (p ≈ 0.02–0.04) do not survive this. Under FDR correction, they remain candidates for exploratory retention.

**Precession not fully corrected:** Fixed star positions shift ~1° every 72 years. For charts spanning the 19th and 20th centuries, this introduces ~1–2° systematic position offsets. The analysis uses epoch 2000.0 positions.

**Ecliptic latitude ignored:** Stars at high ecliptic latitude (Vega at ~+62°) are rarely conjunct any planet by true 3D alignment, yet the analysis uses only ecliptic longitude. This may inflate intensity scores for high-latitude stars.

**Category sample sizes:** Subcategories like "cancer" and "overdose" may contain 50–150 individuals. Power to detect category-level star effects is limited.

---

## 🌟 Conclusion

Analysis of 12 major fixed stars across ~936 public figures finds:

- **Two statistically significant patterns:** elevated Regulus intensity in overdose charts (Z = +2.26) and reduced Altair intensity in cancer charts (Z = −2.32)
- **One borderline pattern:** elevated Altair in homicide charts (Z = +2.07)
- **Broad null result:** The majority of star-category combinations show no systematic pattern

The significant findings are consistent with traditional astrological symbolism — Regulus's fall-from-greatness narrative mapping to overdose; Altair's bold/risky energy diverging between homicide and cancer — but require replication with corrected significance thresholds before drawing confident conclusions.

The cosine intensity methodology represents a genuine improvement over binary orb analysis. Future fixed star research should adopt this framework: the distribution of tight conjunctions tells a richer story than simple counts.
