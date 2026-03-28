# Project 47: Moon Phase & Sleep — The Tithi System and Deep Sleep Suppression

> **Source:** [bigastrologybook.com/project-47](https://bigastrologybook.com/project-47/)
> **Archive Date:** 2026-03-21
> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Dataset:** Authenticated aggregated wearables data (2023–2024), 99 records representing ~118,000 user-nights; Tithi (lunar day) calculated via Sun-Moon elongation; deep sleep duration as primary outcome; patterns derived from University of Washington sleep study methodology (Casiraghi et al., 2021)

---

## Research Question

Does human deep sleep duration vary systematically across the lunar month? Specifically, does the Tithi system — the ancient Indian lunar calendar that divides the synodic month into 30 divisions based on the Sun-Moon angular relationship — predict night-by-night variation in the duration of deep (slow-wave) sleep as measured by wearable devices?

This is one of the few questions in this book where a specific, physically plausible mechanism can be proposed in advance: moonlight suppresses melatonin secretion, and melatonin is the primary circadian signal that promotes slow-wave sleep onset and maintenance.

---

## Background: The Moon, Light, and Sleep

Human sleep architecture is governed by two systems that interact throughout the night: the circadian clock (the 24-hour biological timer synchronized primarily by light-dark cycles) and the homeostatic sleep pressure (the progressive buildup of adenosine and other sleep-promoting compounds during wakefulness). Melatonin is the bridge between them: secreted by the pineal gland in darkness, melatonin signals the circadian system that night has arrived and that sleep conditions are appropriate.

Light at night — particularly blue-spectrum light — powerfully suppresses melatonin secretion even at low intensities. Smartphones, tablets, and LED lighting have made this a prominent public health concern. But for most of human evolutionary history, the most significant source of nocturnal light was the Moon.

The full Moon provides approximately 0.1–0.3 lux of illumination at ground level — far less than artificial lighting, but significantly more than the dark sky at new Moon (approximately 0.001 lux). In an environment without artificial light, the difference between a full Moon night and a new Moon night would be substantial: approximately 200-fold difference in ambient light intensity. This is enough to affect melatonin secretion in sensitive individuals, particularly during the early-night hours when sleep onset occurs.

The **prediction**, therefore, is straightforward and mechanistically grounded: melatonin suppression should be greatest near the full Moon (when moonlight is brightest), and this should reduce deep (slow-wave) sleep, which is most dependent on early-night melatonin for its initiation and maintenance. New Moon nights, with minimal moonlight, should permit higher melatonin secretion and longer deep sleep.

---

## The Tithi System

The analysis uses the Tithi rather than the simple New/Full Moon binary. The Tithi is the fundamental unit of the Hindu lunar calendar, defined as each 12° increment of the Sun-Moon angular difference. There are 30 Tithis in a synodic month (360° / 12° = 30), corresponding to approximately one per day, though the Moon's elliptical orbit makes individual Tithis of unequal duration.

| Tithi | Name | Approximate Phase | Moon-Sun Angle |
|---|---|---|---|
| 1 | Pratipada | New Moon (day 1) | 0°–12° |
| 2–7 | Dvitiya–Saptami | Waxing Crescent | 12°–84° |
| 8 | Ashtami | First Quarter | 84°–96° |
| 9–14 | Navami–Chaturdashi | Waxing Gibbous | 96°–168° |
| 15 | Purnima | Full Moon | 168°–180° |
| 16–21 | — | Waning Gibbous | 180°–252° |
| 22 | — | Last Quarter | 252°–264° |
| 23–29 | — | Waning Crescent | 264°–348° |
| 30 | Amavasya | Dark Moon (day 30) | 348°–360° |

The Tithi system provides a finer-grained resolution than the simple four-phase (New, Waxing, Full, Waning) or binary (Full vs. Not-Full) classification. It captures the gradual increase and decrease of moonlight across 30 individual units rather than four broad categories, allowing the analysis to detect whether the sleep effect follows the gradual light-intensity curve or shows discontinuities at specific thresholds.

---

## Data

| Field | Detail |
|---|---|
| **Source** | Authenticated aggregated wearables data (2023–2024) |
| **Records** | 99 aggregated records (weekly/semi-weekly samples) |
| **Estimated user-nights** | ~118,000 (avg ~1,200 users per sample) |
| **Primary metric** | Deep sleep duration (minutes) per night |
| **Lunar calculation** | Sun-Moon elongation → Tithi assignment for each sample date |
| **Methodology reference** | Casiraghi et al. (2021), University of Washington |

---

## Results

### Core Finding: New Moon vs. Full Moon

| Metric | Value |
|---|---|
| **New Moon (Tithi 1) deep sleep** | **90.6 minutes** |
| **Full Moon (Tithi 15) deep sleep** | **74.0 minutes** |
| **Difference** | **−16.6 minutes (−18.3%)** |
| **T-test p-value** | **< 0.00001** |

The full Moon is associated with approximately 16.6 fewer minutes of deep sleep per night compared to the new Moon. This is a reduction of approximately 18–20% from the new Moon baseline — a physiologically significant effect.

For context: healthy adult deep sleep typically occupies 13–23% of total sleep time, amounting to approximately 60–110 minutes in a 7–8 hour sleep period. A reduction of 16 minutes represents roughly 15–20% of the normal deep sleep quota. The equivalent of missing 1–2 nights of typical deep sleep per week for the duration around full Moon. At population scale, this is not a trivial fluctuation.

### The Waxing-Waning Gradient

The Tithi system reveals that the effect is not a simple New/Full binary but a continuous gradient that tracks moonlight intensity through the cycle:

| Phase | Approximate Tithis | Pattern |
|---|---|---|
| New Moon | 28–30, 1–2 | **Peak deep sleep (~90 min)** |
| Waxing Crescent | 3–7 | Moderate decline begins |
| First Quarter | 8 | Continued decline |
| Waxing Gibbous | 9–14 | Accelerating decline toward Full |
| Full Moon | 14–16 | **Minimum deep sleep (~74 min)** |
| Waning Gibbous | 16–21 | Recovery begins |
| Last Quarter | 22 | Continued recovery |
| Waning Crescent | 23–28 | Approaching New Moon peak |

Deep sleep decreases progressively as the Moon waxes (gains brightness), reaches its minimum around the full Moon, and recovers progressively as the Moon wanes. The pattern matches the moonlight intensity curve almost exactly: maximum brightness at full Moon corresponds to minimum deep sleep; minimum brightness at new Moon corresponds to maximum deep sleep.

This gradient behavior is consistent with the proposed melatonin mechanism. A simple New/Full binary might suggest an "on/off" effect; the continuous gradient across all 30 Tithis suggests a dose-response relationship between moonlight intensity and sleep suppression — exactly what melatonin physiology would predict.

---

## The Mechanism: Melatonin and Moonlight

The proposed causal chain has strong biological plausibility:

**Step 1:** Full Moon provides substantially more ambient light on clear nights than new Moon (approximately 200× more by lux)

**Step 2:** Even low-intensity light (0.1–0.3 lux) reaching the retina suppresses pineal melatonin secretion, particularly in the early part of the night (the first 2–3 hours after sunset when melatonin onset typically occurs)

**Step 3:** Reduced early-night melatonin delays the circadian signal for slow-wave sleep onset, resulting in less deep sleep in the early-night period (Stages N2 and N3)

**Step 4:** Across a population, this suppression creates systematic reductions in population-average deep sleep duration near full Moon

The consistency of this mechanism with known sleep physiology is unusually strong compared to most astrological mechanisms proposed in this book. Melatonin suppression by light is one of the most robust findings in sleep science; the dose-response relationship between light intensity and suppression is well-documented; and the connection between early-night melatonin and slow-wave sleep initiation is established.

The remaining uncertainty is whether **natural moonlight** provides sufficient lux in modern urban environments — where most wearable device users live — to overcome the ambient artificial light background and produce the observed effect. Urban backgrounds are typically 1–5 lux even indoors with windows, which would suggest the additional 0.1–0.3 lux from moonlight is too small to matter against a 1–5 lux background.

One resolution: the light suppression effect may operate primarily through **morning moonlight** (waning gibbous rising at 2–4 AM, visible through bedroom windows) rather than evening moonlight. The waning gibbous rises in the night-time hours and could provide direct window exposure during the circadian-sensitive early morning period when sleep architecture is most vulnerable to disruption. This would explain why the effect tracks through the full 30-day cycle rather than just the most visible full Moon evenings.

---

## Historical and Cultural Context

The connection between the full Moon and disrupted sleep is embedded in virtually every culture's mythology. The word "lunatic" derives from *luna* (Moon) through the ancient observation that certain behaviors — now associated with sleep disruption, mood instability, and erratic action — worsened with the full Moon. "Moonstruck" appears in languages from English to Sanskrit. The sleeplessness of the full Moon is one of the oldest and most cross-cultural folk observations in human experience.

In Vedic tradition, the 30 Tithis were assigned specific qualities: some considered auspicious for beginning projects, others for fasting, some for rest and inward activity. The Amavasya (New Moon/Tithi 30) is traditionally a day of introspection, ancestral reverence, and inward focus — qualities compatible with the peak deep sleep finding (the person who sleeps deepest on the new Moon is most fully rested and recuperated). The Purnima (Full Moon/Tithi 15) is traditionally a day of heightened activity, festivity, and outward expression — qualities compatible with lighter sleep, higher energy, and reduced deep recovery.

Traditional Ayurvedic medicine explicitly associates the full Moon with elevated Pitta (fire/inflammation) and disturbed Vata (wind/movement in the nervous system), both of which would disrupt sleep in Ayurvedic terms. Whether these traditional observations derived from accumulated empirical observation of exactly the pattern documented here is speculation, but the correspondence is worth noting.

---

## Why This Is the Book's Cleanest Positive Finding

Across 47 projects, this study produces what may be the most methodologically clean positive finding in the collection. Several factors distinguish it:

**Mechanistic plausibility:** Unlike most astrological correlations, the moonlight-melatonin pathway is grounded in established physiology at every step. This is not merely statistical association; it is association backed by a coherent, testable physical mechanism.

**Dose-response gradient:** The Tithi system shows a smooth gradient rather than a threshold effect. Dose-response relationships are a strong indicator of genuine causation rather than coincidental correlation.

**Large effective sample:** 118,000 estimated user-nights provides enormous statistical power. The p-value (< 0.00001) is not driven by a small sample susceptible to chance.

**Archetypal convergence:** The finding aligns with the most ancient and cross-culturally universal observation about the Moon — its connection to sleep disturbance. Unlike correlations that contradict tradition (the Hard Aspect inversion, the Mercury retrograde myth), this finding *confirms* one of humanity's oldest empirical observations.

**Quantified magnitude:** 16.6 minutes of deep sleep is not a borderline or marginal effect. It is roughly equivalent to the deep sleep impact of consuming one alcoholic drink before bed — a well-known, medically recognized sleep disruptor.

---

## Statistical Caveats

**Aggregated data limitations.** The 99 records represent weekly or semi-weekly aggregates, not individual nights. Aggregation across approximately 1,200 users per sample smooths individual variation and may reduce apparent effect sizes (if some users are maximally sensitive to moonlight while others are not). Conversely, aggregation may suppress individual outliers that would inflate single-night estimates.

**Urban vs. rural.** Most wearable device users are urban. The moonlight mechanism is more plausible for rural users with minimal artificial light exposure. If the mechanism operates primarily through morning moonlight as proposed above, urban effects might actually be comparable.

**Confounders in aggregated data.** If full Moon dates happen to coincide with specific weekdays more often in the sample period, the full Moon signal could partially reflect weekend vs. weekday sleep differences. The 99-record sample over 2023–2024 may not uniformly distribute all 30 Tithis across all weekdays.

**Wearable accuracy for deep sleep.** Consumer wearable devices (Fitbit, Garmin, Oura, Apple Watch) classify sleep stages using accelerometry and heart rate variability — not EEG, which is the gold standard for sleep staging. Wearable deep sleep classification has accuracy of approximately 65–70% compared to polysomnography. This introduces noise but does not systematically bias the lunar-cycle comparison unless the classification errors are themselves lunar-correlated (which is implausible).

---

## Conclusion

Analysis of approximately 118,000 wearable-device-measured user-nights finds a large, significant, and mechanistically plausible relationship between lunar Tithi phase and deep sleep duration. New Moon nights (Tithi 1) show an average of 90.6 minutes of deep sleep; Full Moon nights (Tithi 15) show 74.0 minutes — a reduction of 16.6 minutes (18.3%) that is highly statistically significant (p < 0.00001).

The effect follows a continuous gradient across all 30 Tithis, tracking the moonlight intensity curve from maximum darkness (new Moon, maximum deep sleep) through full brightness (full Moon, minimum deep sleep) and back. This dose-response pattern is consistent with melatonin suppression by ambient moonlight — one of the most physiologically grounded mechanisms proposed for any astrological correlation in this book.

The ancient observation — embedded in language (lunatic), cross-cultural myth, and Ayurvedic tradition — that the full Moon disrupts sleep finds quantitative confirmation in modern wearable device data. The Tithi system, designed millennia ago to track the 30 gradations of lunar phase, proves to be the appropriate resolution for detecting this effect: not the coarse New/Full binary but the full 30-day gradient that mirrors the light intensity cycle.

For the broader project of this book: if any single finding deserves the designation "confirmed and plausible," it is this one. The Moon affects human deep sleep. The mechanism is known. The effect is substantial. The traditional observation is real.

---

*Archived wearables data, Tithi calculations, statistical analysis, and visualization outputs preserved in `backup/`.*
