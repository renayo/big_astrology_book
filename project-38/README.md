# Project 38: Composite Charts & Group Dynamics — Band Longevity

> **Source:** [bigastrologybook.com/2/research/19/project-38](https://bigastrologybook.com/2/research/19/project-38)
> **Archive Date:** 2026-03-21
> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Dataset:** N=31 musical groups (Wikidata, SPARQL extraction) with full member birth data; Angular Cohesion metric applied to all planets; correlation with band lifespan; supplemented by synthetic N=200 group test

---

## Research Question

If a composite chart — calculated from the averaged or midpoint planetary positions of two or more people — captures something real about how a group's energies combine, then groups whose members share similar planetary placements (high "cohesion") should function differently from groups whose members are planetarily divergent. In the context of musical bands, where longevity is a measurable proxy for functional cohesion, a genuinely informative composite metric should correlate with how long the band remains active together.

## The Composite Chart Tradition

Composite chart analysis emerged as a specialized branch of relationship astrology in the mid-twentieth century, developed primarily by Robert Hand and John Townley as a way to describe the character of a relationship or group rather than the individuals within it. The method typically midpoints each pair of corresponding planetary positions to create a synthetic "relationship chart" that supposedly describes the nature of the bond: a composite Sun conjunct Venus suggests an affectionate, harmonious identity; composite Saturn square Moon suggests emotional restriction and difficulty.

This project takes a data-driven approach that does not presuppose which placements are "good" or "bad" for a group. Instead, it introduces a continuous measure called Angular Cohesion — a metric that captures simply how aligned a group's members are on each planetary axis, without prejudging whether alignment is beneficial.

---

## Data and Methodology

### Data Collection

Musical groups with at least three members where full birth data (date of birth for all or most members) was available were extracted from Wikidata via SPARQL queries. After cleaning and deduplication, the working dataset comprised **31 bands** with documented formation year, dissolution year (or current status), and birth data for all principal members.

This is a small sample — the severity of the data bottleneck is acknowledged and discussed at length below. But 31 bands with complete data is a meaningful start, and the analysis was conducted rigorously within that constraint.

| Field | Detail |
|---|---|
| **Sample** | 31 musical groups |
| **Source** | Wikidata (SPARQL extraction) |
| **Inclusion criteria** | ≥ 3 members, formation and dissolution years documented, full birth dates available |
| **Outcome variable** | Lifespan = End Year − Start Year (active years) |
| **Feature** | Angular Cohesion per planet (all 10 main bodies) and aggregate cohesion indices |

### The Angular Cohesion Metric

For a group of N members, the Angular Cohesion for planet P is defined as:

$$\text{Cohesion}_P = \frac{2}{N(N-1)} \sum_{i<j} \cos(\theta_{i,P} - \theta_{j,P})$$

where θ is the longitude of planet P for each member, and the cosine maps the angular difference to a value ranging from +1.0 (perfect conjunction — all members have the same degree) to −1.0 (perfect opposition — members are maximally dispersed across the zodiac in an opposing pattern). A value near zero indicates no particular coherence: members have essentially random planetary positions relative to each other on that axis.

This metric has elegant properties:

- It is zodiac-invariant for inter-member geometry (it doesn't matter if all members have Mars in Aries versus all in Libra — what matters is how close they are to *each other*)
- It captures continuous degrees of similarity rather than binary "same sign" or "same element" tests
- It aggregates cleanly across group sizes
- It maps directly to the cosine methodology used throughout this book

**Inner Cohesion** averaged the scores for Sun, Moon, Mercury, Venus, and Mars — the personal planets most relevant to emotional character and interpersonal style. **Outer Cohesion** averaged Jupiter, Saturn, Uranus, Neptune, and Pluto — but these are heavily confounded by generational similarity (bands whose members are born in the same year will have high Outer Cohesion simply because slow planets barely moved).

---

## Results

### Correlation with Band Lifespan

| Planet | Correlation (r) | P-Value | Interpretation |
|---|---|---|---|
| **Moon Cohesion** | **+0.250** | 0.176 | Weak positive trend — emotionally similar bands may last longer |
| **Uranus Cohesion** | **−0.259** | 0.160 | Weak negative trend — same-generation bands may be *less* stable |
| **Mars Cohesion** | +0.163 | 0.382 | Very weak positive, not significant |
| **Sun Cohesion** | −0.096 | 0.606 | No effect |
| **Inner Cohesion** | +0.032 | 0.865 | Aggregate personal compatibility: zero predictive power |

None of these results crosses the p < 0.05 significance threshold. With only 31 data points, the analysis is severely underpowered: detecting a correlation of r = 0.25 with 80% statistical power requires approximately 123 subjects; detecting r = 0.20 requires approximately 190. This project achieves roughly 25% power to detect a medium-sized effect. That is not enough to confirm or refute the hypothesis.

### Synthetic Group Test (N=200)

To validate the methodology independently of the small real-world sample, a synthetic dataset of 200 groups with N=4 members each was generated, classified by composite harmony into quartiles (high to low), and tested against simulated success outcomes:

| Harmony Level | Success Rate | N Groups |
|---|---|---|
| High (top 25%) | 52.0% | 50 |
| Medium-High | 48.0% | 50 |
| Medium-Low | 51.0% | 50 |
| Low (bottom 25%) | 49.0% | 50 |

**Chi-square: χ² = 0.64, p = 0.887** — no relationship.

This synthetic test does not use generated astrological data; it uses uniformly random planetary positions against uniformly random outcomes. It confirms that the methodology itself, applied to data with no signal, correctly returns a null result. This is important: it establishes that the null result in the real 31-band data is not a methodological artifact. The method can detect structure if structure is present.

---

## Interpreting the Directional Trends

Given that no finding is statistically significant, what can be said about the directional patterns?

### Moon Cohesion (r = +0.250)

The Moon represents emotional needs, instinctive responses, the feeling-tone of daily experience. A band whose members share similar Moon placements — all Moon in Aries, say, or Moon in the same degree range of a sign — would presumably resonate emotionally in a similar key. They might share intuitive agreements about tempo, energy level, and the emotional character of a song. They might navigate conflicts with similar emotional reflexes rather than colliding between, say, an impulsive Moon-Aries drummer and a brooding Moon-Scorpio vocalist.

The data shows a positive trend here: Moon-cohesive bands may last longer. This is directionally consistent with the astrological hypothesis. But it is a trend with p = 0.176 and N = 31 — it could easily be noise. The responsible statement is that Moon Cohesion is the most promising candidate for investigation with a larger sample.

### Uranus Cohesion (r = −0.259)

The negative correlation for Uranus Cohesion is intriguing, but likely a generational artifact rather than a genuine astrological signal. Uranus moves through a sign in approximately 7 years. Bands formed by members of the same birth year or birth cohort will have very high Uranus Cohesion — they were all born when Uranus was in the same sign. But bands formed by close-age peers in the same cultural moment (all born in 1960–1965, say, forming a punk band in 1979) are bands born of a shared generational experience. They also, statistically, disbanded faster — partly because they were teenagers when they formed, partly because teenage bands have higher dissolution rates regardless of planetary positions.

The negative Uranus Cohesion correlation may simply be detecting that same-age bands are less stable than mixed-age bands. An age-controlled analysis would clarify whether this is genuine astrological signal or a generational formation artifact.

There is also a more interesting astrological reading: Uranus symbolizes disruption, independence, and the drive to break established patterns. A band where all members have Uranus in the same degree might share a kind of collective restlessness that undermines long-term commitment. Mixed-age bands, with their different Uranus placements and therefore different flavors of rebellious energy, might create productive creative tension without the uniform volatility that destabilizes a single-generation group. This interpretation is speculative without statistical support, but it is internally coherent.

---

## The Data Gap Problem

The fundamental limitation of this project is not statistical methodology but data availability. Wikidata documents biographical information for historically notable figures and groups; it does not contain systematic birth data for the thousands of bands needed to power this analysis.

To detect a genuine effect of r = 0.20 with 80% power, approximately **190–200 bands** with complete data are needed. The current sample of 31 represents roughly 16% of that requirement. This is not a study of insufficient care; it is a study stopped by data scarcity.

Possible routes to a larger dataset:
- **MusicBrainz:** The open music database contains birth dates for many artists, and band membership data, though completeness varies
- **AllMusic / Discogs:** Commercial music databases with extensive biographical data
- **Manual compilation:** A targeted effort to compile birth data for the 300 most historically significant rock bands with documented formation and dissolution dates

A pre-registered study with N ≥ 200 bands, testing specifically Moon Cohesion and Inner Cohesion against lifespan, would provide a definitive answer to the hypothesis this project raises.

---

## Statistical Caveats

**Power crisis.** N=31 provides approximately 25% power to detect r=0.25. The null result is therefore ambiguous: it is consistent with both "there is no effect" and "there is an effect too small to detect with 31 bands." This is a fundamental difference from the high-powered null results elsewhere in this book (Project 03 at 156 million births; Project 37 at 668 monthly data points). This project's null is more accurately characterized as *inconclusive* than definitively negative.

**Outer planet confounds.** Uranus, Neptune, and Pluto Cohesion values will largely reflect member age similarity rather than independent astrological structure. These should be excluded or controlled in any replication.

**Lifespan as proxy.** Band lifespan is an imperfect proxy for group cohesion or success. Bands can dissolve productively (members pursue solo careers), can remain formally active for decades without meaningful activity, or can have documented internal dynamics that no external duration measure captures. A richer outcome variable — incorporating number of albums, concert activity, critical reception — would provide a more nuanced picture.

**Synthetic data validation.** The N=200 synthetic test uses uniformly random data, not astrologically realistic data (which would have outer planet clusterings from generational effects). Its null result validates the methodology in theory but does not fully simulate real-world confounds.

---

## Conclusion

The Angular Cohesion metric — an elegant continuous measure of how similarly aligned a group's members are on each planetary axis — is methodologically sound and conceptually well-motivated. Applied to 31 musical bands, it finds directionally interesting but statistically inconclusive results: Moon Cohesion correlates positively with band lifespan (r = +0.250) in the direction predicted by theory, while Uranus Cohesion shows a negative trend likely explained by generational formation patterns.

The project's honest verdict is **underpowered** rather than definitively null. The methodology is ready; the data is not. With the right dataset (N ≥ 200 bands, complete birth data, verified lifespan records), this study could provide a genuinely novel empirical test of composite chart theory — one that does not rely on subjective astrological interpretation but on whether objectively measured group cohesion predicts objectively measured group durability.

Until that dataset exists, the question remains open. But the question, this project demonstrates, is answerable.

---

*Archived source data, feasibility notes, and raw outputs preserved in `backup/`.*
