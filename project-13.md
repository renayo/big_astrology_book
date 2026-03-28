# Project 13: Circular Statistics and Personality by Birth Angle

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Using proper circular statistics — which treat the zodiac as a 360° circle rather than 12 unordered categories — do performers, scientists, and writers cluster at different zodiacal positions? Does the fire-sign extraversion hypothesis hold up?

---

## 💡 Why This Matters

The claim that fire signs (Aries, Leo, Sagittarius) produce extraverted, performative people while earth signs produce introverts is one of astrology's most direct and testable personality predictions. Performers are a reasonable extraversion proxy; scientists are a reasonable introversion proxy.

The methodological contribution here: zodiac data is *circular*, and most zodiac research ignores this. Standard chi-square tests treat the 12 signs as unordered categories, missing patterns that straddle sign boundaries (a clustering centered on 28° Pisces / 2° Aries would look like two separate weak signals rather than one strong one). Circular statistics handle this correctly.

There's also a critical baseline issue that prior studies frequently miss.

---

## 📊 The Seasonal Confound: A Tutorial

Births are not uniformly distributed across the zodiac in the real world. CDC birth data (2010–2020) shows:

- **Late summer peak:** More births in August–September (Leo/Virgo zone)
- **Winter trough:** Fewer births in January–February (Capricorn/Aquarius)
- **Rayleigh test on CDC data: p < 0.0001** — birth timing is emphatically non-uniform

In practice: if you sampled 100 random Americans, you'd find more Virgos than Capricorns simply because more babies are born in September than January — with no astrological effect involved. **Any claimed zodiac effect must exceed this non-uniform background.**

Seasonal birth variation is biologically driven (holiday conceptions leading to September births, etc.) and creates approximately 20% variation across the year. Correcting for this baseline is not optional — it's the core methodological requirement.

---

## 📊 The Data

| Group | N | Professional category |
|---|---|---|
| Performers | 100 | Actors, musicians, comedians |
| Scientists | 50 | Physicists, mathematicians, inventors |
| Writers | 61 | Novelists, poets, playwrights |
| **Total** | **211** | — |

Baseline: CDC monthly birth distribution, 2010–2020, used to construct expected frequencies corrected for seasonal non-uniformity.

---

## 📈 Results

### Primary Hypothesis Tests

| Test | Result | p-value |
|---|---|---|
| Performers vs. Scientists by sign | No difference | 0.562 |
| Element distribution by profession | No difference | 0.711 |
| **Fire signs = extraversion hypothesis** | **Not supported** | **0.683** |
| Performers circular clustering (Rayleigh) | Uniformly distributed | 0.710 |
| Scientists circular clustering (Rayleigh) | Marginal — not significant | 0.094 |

**All primary tests returned null results.** No zodiac sign or element shows a statistically significant association with professional category. The fire-sign extraversion hypothesis — one of astrology's most direct and testable claims — is not supported.

### The Marginal Scientists Result

The only near-significant finding: scientists may show slight non-uniform zodiacal distribution (p = 0.094). This does not survive α = 0.05 and would not survive Bonferroni correction for the 7+ tests performed (corrected threshold ≈ p < 0.007).

Additional concerns:
- Effect size (R) for circular clustering not reported — direction and magnitude unknown
- The specific signs driving the marginal result were not identified
- N=50 scientists is adequate for medium effects but not small ones

This is a marginal result in the wrong direction for confirmatory analysis. It would need pre-specification, replication, and confidence intervals before any weight can be placed on it.

### Statistical Power Context

| Group | N | Detectable effect size (80% power) |
|---|---|---|
| Performers | 100 | Cohen's w ≥ 0.28 |
| Scientists | 50 | Cohen's w ≥ 0.40 |
| Writers | 61 | Cohen's w ≥ 0.36 |

The Gauquelin "Mars effect" — the most famous claimed positive finding in astrological research — reported an effect size of approximately w ≈ 0.05–0.10. **This study would not have the power to detect an effect that small.** Detecting zodiac effects at realistically small magnitudes requires N ≥ 500 per group.

---

## ⚠️ Limitations & Caveats

- **Celebrity selection bias:** Fame requires unusual achievement, and different eras, countries, and socioeconomic contexts produce fame differently. The CDC 2010–2020 baseline may not accurately represent historical celebrities' expected birth distributions.
- **Profession as personality proxy:** Not all performers are highly extraverted; not all scientists are introverted. Direct Big Five measurement is more appropriate.
- **Tropical zodiac only:** Sidereal assignments would shift all signs by ~24°. Different clustering patterns might emerge — see Project 08 for that comparison.
- **No birth times:** Without birth times, no ascendant, house, or exact Moon position analysis is possible. Traditional astrology places substantial emphasis on the ascendant for personality.

### Published Literature Context

The null result here is consistent with the broader scientific literature:
- Kelly (1979): Reviewed 23 studies testing astrological predictions — no consistent evidence
- Eysenck & Nias (1982): No sun-sign extraversion correlation in large samples
- Comprehensive meta-analyses (Pieron & Monzie, 1989): No zodiac-personality relationship after multiple-comparison correction

---

## 🌟 Conclusion

Circular statistics applied to 211 verified celebrity births yield clean null results:

- **Fire signs and extraversion:** No association (p = 0.683)
- **Zodiac sign and profession:** No difference (p = 0.562)
- **Elemental distribution:** No difference (p = 0.711)
- **Performer clustering:** Uniformly distributed
- **Scientist clustering:** Marginal (p = 0.094) — does not survive correction

The methodological contribution: explicitly demonstrating the **seasonal birth confound** with CDC data, showing that zodiac frequencies are inherently non-uniform in any population sample due to biological seasonal variation. All future zodiac-personality research must correct for this baseline.

To detect realistic small effect sizes in this domain requires N ≥ 500 per group with pre-registered hypotheses and corrected significance thresholds.
