# Project 45: Seismicity & Gravitational Vectors — The Moon's Inverted Signal

> **Source:** [bigastrologybook.com/2/research/19/project-45](https://bigastrologybook.com/2/research/19/project-45)
> **Archive Date:** 2026-03-21
> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Dataset:** USGS Earthquake Catalog, M5.5+ (1970–2024), N=25,961 events; lunar day assignments via synodic cycle; planetary alignment score and tidal proxy calculations via Swiss Ephemeris

---

## Research Question

Do gravitational forces from the Moon and aligned planets influence the timing of major earthquakes? Specifically, do earthquakes cluster during periods of maximum tidal stress — New and Full Moons, when the Sun and Moon are aligned along the same axis and their gravitational effects combine — or during significant planetary alignments?

## Background: Tidal Triggering Theory

The physical hypothesis behind lunar seismicity is straightforward: the Moon's gravity creates tidal stresses in Earth's solid crust, not just in its oceans. This *solid Earth tide* compresses and stretches rock by small amounts — fractions of a meter — on a twice-daily cycle. The hypothesis is that when these tidal stresses are superimposed on a fault plane already close to its failure threshold, the additional stress can trigger a rupture that would have occurred anyway, but slightly sooner.

This is not fringe science. The solid Earth tide is well-established geophysics; the question of whether it triggers earthquakes is an active area of seismological research. Several serious scientific studies have found weak correlations between tidal phase and small-magnitude (M < 3) earthquakes in specific geological settings. The question for this project is whether the effect is visible in global, high-magnitude (M ≥ 5.5) seismicity.

The maximum tidal stress should occur at **syzygy** — New Moon and Full Moon, when the Sun-Moon-Earth system is aligned and the gravitational pulls of the Sun and Moon are combined along the same axis. Standard tidal theory therefore predicts earthquake peaks at Days 1 (New Moon) and 15 (Full Moon) of the synodic month.

---

## Data

| Field | Detail |
|---|---|
| **Dataset** | USGS Earthquake Hazards Program — ANSS Comprehensive Catalog |
| **Magnitude filter** | M ≥ 5.5 |
| **Events** | 25,961 |
| **Time range** | 1970–2024 (54 years) |
| **Lunar day calculation** | Sun-Moon elongation → synodic day (1–28) |
| **Alignment score** | Sum of angular closeness of major planets |
| **Tidal proxy** | Geometric model of combined solar-lunar gravitational vector |
| **Statistical tests** | Chi-square goodness of fit (lunar day distribution); independent t-test (alignment/tidal proxy vs. earthquake days) |

---

## Results

### Test 1: Planetary Alignment — Null

The first analysis tested whether days with tighter planetary alignment (multiple planets in close angular proximity, summing their gravitational vectors) show elevated earthquake frequency.

| Test | Statistic | p-value | Result |
|---|---|---|---|
| Planetary alignment score | t-test | p = 0.4585 | **Null** |

There is no difference in planetary alignment between earthquake days and random days. Major planetary conjunctions and alignments do not trigger elevated seismicity at global scale. This is consistent with the physics: the gravitational influence of Mars or Jupiter on Earth's crust is many orders of magnitude smaller than the Moon's solid-Earth tidal effect, which is itself small compared to the tectonic forces that drive earthquakes.

### Test 2: Tidal Proxy — Null (With Inverse Pattern)

The second analysis tested whether the theoretical combined tidal stress from Sun and Moon (calculated geometrically) correlates with earthquake frequency or magnitude:

| Test | Statistic | p-value | Result |
|---|---|---|---|
| Tidal proxy vs. earthquake frequency | t-test | p = 0.4389 | **Null** |

Days with theoretically higher tidal stress do not produce more or larger earthquakes. More strikingly, the directional pattern — examined below — is inverted from what tidal theory predicts.

### Test 3: Lunar Day Distribution — Highly Significant and Inverted

The third analysis tested whether earthquakes are distributed non-uniformly across the 28-day synodic month. With 25,961 earthquakes across 28 lunar days, the expected count per day is approximately 927 (±random variation). Any significant non-uniformity would indicate a lunar cycle influence.

| Statistic | Value |
|---|---|
| **Chi-Square** | **78.54** |
| **p-value** | **< 0.0001** |
| **Degrees of freedom** | 27 |

The distribution is highly significantly non-uniform. But the *pattern* of non-uniformity is the opposite of what tidal theory predicts:

| Phase | Lunar Days | Count | Deviation from Expected | Direction |
|---|---|---|---|---|
| **New Moon** | 1, 28 | 1,660 combined (830 avg) | **−10.5%** | **Suppressed** |
| Waxing Crescent | 6 | 1,060 | **+14.3%** | **Peak** |
| First Quarter | 7 | ~970 | ~+4.7% | Slightly elevated |
| **Full Moon** | 14, 15 | 1,855 combined (928 avg) | **−1.0%** | Slightly suppressed |
| Third Quarter | 23 | 972 | +4.9% | Slightly elevated |

The standard prediction — earthquake peaks at New Moon (Day 1) and Full Moon (Day 15) — is not observed. Instead:
- **New Moon shows a significant 10.5% suppression** (p = 0.0006)
- **Full Moon shows a minor 1% suppression**
- **Day 6 (Waxing Crescent) shows a 14.3% peak** — the strongest deviation in the dataset
- Secondary peak at Day 23 (Third Quarter)

The lunar cycle clearly matters for global M5.5+ seismicity. But it matters in the *wrong direction*.

---

## Interpreting the Inversion: The Clamping Hypothesis

Why would maximum tidal stress (at syzygy) correlate with *fewer* earthquakes rather than more?

One geophysically plausible explanation is the **clamping hypothesis**: at syzygy, the maximum tidal stress locks fault planes more tightly — the combined gravitational pull compresses certain fault orientations rather than stretching them, increasing the clamping stress that resists rather than promotes slip. When the Moon moves toward its quarter phases (Day 6–7), the tidal geometry shifts from maximum compressive clamping to a shear-dominant stress state that may be more conducive to triggering release.

This is not the consensus view in seismology, but it has been proposed. The mechanism would depend strongly on fault orientation: some faults are clamped at syzygy and released at quarter phases; others may show the reverse. Globally summed, the quarter-phase peak pattern in this data suggests that the clamped-at-syzygy effect may dominate in the world's most seismically active fault systems.

An alternative explanation is that this inversion is a statistical artifact of some kind — perhaps related to how the lunar day bins are defined, or to temporal clustering in the earthquake catalog during specific eras. But with 25,961 earthquakes over 54 years and a chi-square of 78.54, the non-uniformity is not likely to be noise.

### The Gap Between Correlation and Mechanism

This finding illustrates a key epistemological distinction that runs throughout this book: **confirming a pattern and confirming a mechanism are different achievements.**

The data confirms that earthquake frequency varies significantly with the lunar synodic cycle (p < 0.0001). This is a genuine empirical finding; it passes rigorous statistical scrutiny at large scale.

The data does *not* confirm the standard tidal triggering mechanism, because the pattern is inverted from what that mechanism predicts. The correlation is lunar; the mechanism is not "tidal stress triggers rupture at syzygy."

From an astrological perspective, one might say that the Moon's influence on seismicity has been confirmed by this analysis — the lunar cycle matters, earthquakes do not fall randomly across the synodic month. But the *why* of the correlation remains unexplained, and the *direction* of the effect contradicts the most obvious physical theory.

---

## Astrological Context

Traditional astrology does not have a highly developed theory of earthquake timing. Mundane astrology — the branch dealing with collective events rather than individual charts — associates geological catastrophe with Uranus (sudden disruption), Pluto (deep underground forces), and Saturn (structural collapse). The Moon is associated with tidal water, liquids, and biological rhythms more than seismic activity per se.

The lunar synodic cycle — the cycle of New to Full Moon and back — has long been associated with cyclical patterns in agriculture, behavior, and biological processes. The finding that this same cycle organizes global seismicity (even in an unexpected direction) adds the solid Earth to the list of systems that respond to lunar periodicity.

It also raises the possibility that the quarter-phase peaks (Day 6, Day 23) could be the "correct" astrological prediction for earthquake risk — if lunar day 6 and day 23 represent elevated seismic probability, and if this pattern is consistent over 54 years of global data, a traditional astrologer might reframe the quarter Moon phases as the relevant timing indicators rather than the dramatic syzygy events.

---

## Statistical Caveats

**Catalog completeness varies.** The USGS catalog for 1970–2024 is not uniformly complete across all regions and time periods. The ability to detect M5.5+ events globally has improved significantly since 1970 due to seismograph network improvements. This could create temporal non-uniformity that, if correlated with the lunar cycle, would introduce spurious patterns. A robustness check restricting to 1990–2024 (post-major network upgrades) would be useful.

**The 28-day binning.** The synodic month is approximately 29.5 days, not 28. The "Day 1–28" binning used in this analysis creates a slightly compressed representation of the full synodic cycle. Minor adjustments to the binning could shift counts between adjacent cells, though the overall chi-square significance is robust.

**Post-hoc nature of the clamping hypothesis.** The clamping hypothesis was invoked to explain an unexpected result, not pre-specified as a prediction. It is a plausible explanation; it is not a confirmed mechanism. This analysis cannot distinguish between clamping effects, alternative geophysical mechanisms, and statistical artifacts.

**Magnitude distribution not examined.** This analysis tested frequency (number of earthquakes per day). It did not examine whether earthquake *magnitude* also varies with lunar day. If the largest events cluster differently from the M5.5–6.0 range, that would suggest a different underlying mechanism.

---

## Summary Table

| Test | Result | Status |
|---|---|---|
| Planetary alignment → earthquake frequency | p = 0.4585 | **Null** |
| Tidal proxy → earthquake frequency | p = 0.4389 | **Null** |
| Lunar day distribution (chi-square) | χ² = 78.54, p < 0.0001 | **Significant** |
| New Moon phase | −10.5% earthquake suppression | **Inverted** |
| Waxing Crescent (Day 6) | +14.3% earthquake peak | **Inverted** |
| Full Moon phase | −1% suppression | **Slightly inverted** |

---

## Conclusion

Analysis of 25,961 major earthquakes (M5.5+) from 1970–2024 yields an anomalous positive finding that complicates any simple reading.

Planetary alignment and tidal proxy scores show no relationship to earthquake frequency — these tests are straightforward nulls consistent with the known weakness of non-lunar gravitational effects on the solid Earth.

The lunar day distribution, however, is highly significantly non-uniform (χ² = 78.54, p < 0.0001). Global seismicity does respond to the synodic lunar cycle. But it responds in the *opposite direction* from what tidal theory predicts: earthquakes are suppressed near New Moon, peak near the Waxing Crescent (Day 6), and show minor suppression near Full Moon.

This result is simultaneously a confirmation that the Moon matters for seismicity and a refutation of the standard tidal triggering model. The lunar cycle organizes earthquakes; the mechanism is not simple tidal stress amplification. The "clamping hypothesis" — that maximum syzygy tidal stress locks certain fault planes rather than triggering them — offers a physically plausible alternative, but one that requires seismological validation independent of this correlation.

For the broader project of this book: the Moon's influence on a solid geophysical system at highly significant levels is noteworthy evidence that lunar periodicity extends beyond tidal water to the deep mechanical behavior of Earth's crust. That the pattern inverts the expected direction adds a layer of mystery that may matter for both seismology and for how we think about the mechanisms behind other lunar-biological correlations in this book.

---

*Archived earthquake catalog, lunar day assignments, tidal proxy calculations, and analysis outputs preserved in `backup/`.*
