# Project 43: Progressions & Psychological Development — What Changes, and What Doesn't

> **Source:** [bigastrologybook.com/project-43](https://bigastrologybook.com/project-43/)
> **Archive Date:** 2026-03-21
> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Dataset:** 171 verified celebrities with AA-rated birth times (AstroDatabank); 925 documented life events from biographical sources; secondary progressions calculated via Swiss Ephemeris (day-for-year method)

---

## Research Question

Secondary progressions — the symbolic timing technique in which each day after birth corresponds to one year of life — are among the most widely used predictive tools in astrological practice. The core claim is that progressed aspects to natal planets correlate with the *nature* of life events: hard aspects (conjunctions, squares, oppositions) bring challenge, crisis, and difficulty; soft aspects (trines, sextiles) bring ease, success, and favorable development. A second claim is that planetary ingresses — when a progressed planet changes zodiacal sign — mark meaningful shifts in life orientation.

This project tests both claims against 925 documented life events from 171 verified celebrity charts.

---

## Background: Secondary Progressions

The day-for-year system (also called secondary progressions) is based on a remarkable symbolic equivalence: each day after birth corresponds to one year of life. To find a person's progressed chart for age 35, you locate the planetary positions 35 days after their birth. The progressed Sun moves approximately 1° per year; the progressed Moon travels 13° per year (changing sign every 2.5 years); Mars advances approximately 0.5° per year; Venus and Mercury move at variable speeds and can be retrograde.

Traditional teaching attributes specific event signatures to specific progressions:
- **Progressed Sun conjunct natal Venus** → marriage, creative peak, harmony
- **Progressed Mars square natal Saturn** → crisis, conflict, physical challenge
- **Progressed Moon into a new sign** → a 2.5-year shift in emotional focus and priorities
- **Progressed Venus conjunct natal Moon** → relationship development, emotional pleasure

The theory predicts that negative life events (crises, divorces, health emergencies, death) should occur under hard progressed aspects (square, opposition, conjunction with malefics), while positive events (career breakthroughs, marriages, awards) should occur under soft aspects or benefic conjunctions.

---

## Data

| Field | Detail |
|---|---|
| **Sample** | 171 verified celebrities with documented birth times |
| **Birth time quality** | AA-rated (Rodden Rating) from AstroDatabank |
| **Events analyzed** | 925 life events from Wikipedia and biographical sources |
| **Event types** | Career (372), Marriage (224), Divorce (115), Crisis (91), Death (78), Child (45) |
| **Progression method** | Secondary progressions (day-for-year), Swiss Ephemeris |
| **Aspects counted** | Hard (conjunction 0°, square 90°, opposition 180°) and soft (trine 120°, sextile 60°) within 2° orb |

### Sample Composition

| Category | Count |
|---|---|
| Musicians | 42 |
| Actors/Directors | 46 |
| Politicians/Leaders | 29 |
| Scientists/Intellectuals | 19 |
| Athletes | 21 |
| Writers/Artists | 15 |
| **Total Individuals** | **171** |
| **Total Life Events** | **925** |

---

## Finding 1: The Sun Progression — Pure Age Mathematics

The most dramatically significant ANOVA result in the entire analysis (p < 0.0001) is immediately revealed as a methodological artifact.

| Event Type | Mean Progressed Sun Movement | Mean Age at Event |
|---|---|---|
| Career | 30.4° | 30.8 years |
| Child | 32.7° | 33.3 years |
| Marriage | 33.4° | 34.0 years |
| Crisis | 36.5° | 37.2 years |
| Divorce | 40.0° | 40.8 years |
| Death | 60.4° | 61.2 years |

The progressed Sun moves almost exactly 1 degree per year. Therefore, the number of degrees the progressed Sun has traveled from its natal position is, with negligible error, equal to the subject's age in years. The ANOVA "detecting" a significant difference in Sun movement across event types is simply detecting that people die older than they divorce, and divorce older than they marry. This is trivially true and has no astrological content whatsoever.

This is a methodologically important cautionary demonstration: a statistical test can return extreme significance (p < 0.0001) for a finding that is pure mathematical tautology. The Sun progression cannot carry any information about the *nature* of events beyond "events at this age" because the progressed Sun position *is* age. Astrological claims involving the progressed Sun's *aspects* to natal planets are a different matter (tested below); but the Sun's raw progressed longitude is worthless as an event predictor.

---

## Finding 2: Hard Aspects — The Wrong Direction

The central test of progressed aspect theory asks whether negative events (crises, divorces, deaths) occur under more hard aspects than positive events. This is the foundational claim of the hard aspect/difficult event model.

| Event Category | Mean Hard Aspects |
|---|---|
| **Positive events** (Career, Marriage, Child) | **6.03** |
| **Negative events** (Crisis, Divorce, Death) | **5.72** |
| **Difference** | **+0.31 more hard aspects at POSITIVE events** |
| **p-value** | **0.048** |

The result is statistically significant — p = 0.048 — but in the *wrong direction*. Positive life events occur under slightly *more* hard progressed aspects on average than negative events. The model predicts crises correlate with more hard aspects; the data shows the opposite.

This is one of the book's clearest confirmations of the **Hardship Hypothesis** — the running theme in which data consistently suggests that astrological difficulty markers are associated with achievement and positive outcomes rather than negative ones. Here the pattern is explicit: the events that represent career success, marriage, and the birth of children happen under *more squares and oppositions* than the events representing crisis, divorce, and death.

This does not necessarily mean hard aspects *cause* positive outcomes. It may mean that high-achieving people — the kind of historically notable individuals who populate AstroDatabank — are chronically active in all planetary directions, including hard ones, precisely because they are chronically engaged with the world. A person who marries four times, has a productive career spanning decades, writes 30 books, and navigates three health crises simply accumulates more total aspects of all types. But the finding that hard aspects are *relatively elevated* in positive events compared to negative ones is directionally damning for the traditional claim.

---

## Finding 3: Mars and Venus Ingresses — The Real Signal

The most compelling genuine findings in this project are not about aspect type but about planetary sign changes.

| Planet | Sign Change p-value (Chi-Square) | Interpretation |
|---|---|---|
| **Mars** | **< 0.0001** | Mars ingresses correlate highly with specific event types |
| **Venus** | **0.0077** | Venus ingresses correlate with specific event types |
| Mercury | 0.0497 | Marginally significant |
| Moon | 0.1714 | Not significant |

When a progressed planet changes sign — Mars moving from Virgo into Libra, for instance, or Venus crossing from Scorpio into Sagittarius — something about the distribution of life event types changes in a statistically significant way. The effect is strongest for Mars (p < 0.0001) and genuine for Venus (p = 0.0077).

What does this mean? The simplest interpretation is that a progressed Mars sign change marks a meaningful reorientation of drive, action, and forward momentum — the flavor of "doing" in the person's life shifts, and this shift correlates with external life category shifts. Career events may cluster differently around Mars ingresses than personal relationship events. Venus ingresses, similarly, may shift the landscape of the person's relational and aesthetic life in ways that make certain event types more probable.

This is subtler and richer than the simple hard/soft aspect model. It is not saying "Mars square something bad"; it is saying "when Mars changes sign, the texture of events changes." The specific direction of the effect — which event types cluster before and after which ingresses — would require more detailed analysis than this study provides.

---

## Finding 4: Progressed Moon — The Personal Timer

| Metric | Value |
|---|---|
| **ANOVA p-value (Moon movement vs. event type)** | **0.0028** |
| **Moon movement at Career events** | 205.0° |
| **Moon movement at Death events** | 169.9° |
| **Moon movement at Divorce events** | 162.4° |
| **Moon movement at Marriage events** | 182.0° |

The progressed Moon shows significant variation by event type (p = 0.0028) that is not purely explained by age. Because the Moon advances approximately 13° per year, completing a full 360° cycle every 27 years, its position is genuinely age-independent in the way that the Sun's position (1° per year, = age) is not. The Moon cycles through all degrees multiple times in a lifetime; finding that its degree position varies by event type is therefore a genuine astrological signal.

Career events cluster when the progressed Moon has traveled farther from its natal position (205°), while divorce and death events cluster at shorter distances (162–170°). This pattern suggests that the phase of the progressed Moon cycle — where in its 27-year journey the Moon is at the time of each event — has some relationship to the nature of what unfolds.

The traditional astrological use of the progressed Moon involves its conjunctions with and aspects to natal planets, its house transits, and its sign changes (a new sign every 2.5 years). These are more granular than the simple "total degrees traveled" metric used here. A more detailed progressed Moon analysis — tracking sign ingresses and conjunctions with natal outer planets — might reveal even stronger patterns.

---

## Summary of Findings

| Test | Result | Verdict |
|---|---|---|
| Sun progression vs. event type | p < 0.0001 | Age confound — not astrological |
| Hard aspects vs. event positivity | p = 0.048 (wrong direction) | Hard aspects NOT negative event markers; opposite trend |
| Mars ingresses | p < 0.0001 | Genuine — event distribution changes at Mars sign changes |
| Venus ingresses | p = 0.0077 | Genuine — event distribution changes at Venus sign changes |
| Moon movement vs. event type | p = 0.0028 | Genuine — progressed Moon phase correlates with event category |
| Mercury ingresses | p = 0.0497 | Marginal — investigate with larger sample |

---

## What Secondary Progressions Are Telling Us

The picture that emerges from this analysis is different from both the traditional astrological view and a simple null result. It is neither "progressions work as advertised" nor "progressions have no validity."

What the data suggests instead is:

1. **The hard/soft aspect frame is wrong.** The binary model in which squares and oppositions bring trouble while trines bring ease is not supported. If anything, the data slightly inverts it.

2. **Sign changes matter more than aspect types.** When Mars or Venus change sign — when the principle they represent shifts its qualitative mode — this correlates with meaningful changes in the type of events the person encounters. The *ingress* may be the primary timing marker, not the aspects along the way.

3. **The progressed Moon is a genuine personal timer.** Its 27-year cycle creates real variation in life event patterns that is not reducible to age. This is consistent with the traditional practice of tracking the progressed Moon's house and sign transits as indicators of where a person's attention and emotional life is focused in any given 2.5-year period.

4. **The progressed Sun is mathematically identical to age.** Any analysis using progressed Sun position as a predictor is using age as a predictor. This needs to be accounted for in all progression research.

---

## Statistical Caveats

**Sample characteristics.** AstroDatabank celebrities are not a random sample of the population. They are historical notables whose event-dense lives produce 925 events in 171 people — an average of 5.4 events per person. This selection toward prolific, multi-domain lives may amplify any effect involving cumulative aspect counts.

**Orb definition.** Hard aspects were counted within a 2° orb. This is tighter than many traditional practitioners use (5–8°). A wider orb would increase the total aspect count and might shift the balance between hard and soft aspects differently.

**Event classification.** "Positive" (Career, Marriage, Child) and "Negative" (Crisis, Divorce, Death) are crude categorizations. Some career events represent devastating failures; some divorces represent liberation. The blunt valence assignment may suppress real patterns within event types.

**Multiple ingresses not tracked.** The Mars ingress analysis identifies *whether* a sign change occurred near each event, not *which* sign-to-sign transition it was. Mars entering Libra (the sign of partnerships) near marriage events, if that effect existed, would be washed out in an analysis that treats all Mars ingresses equivalently.

---

## Conclusion

Secondary progression analysis of 171 celebrity charts and 925 life events produces a mixed verdict that is more interesting than a simple null or confirmation.

The Sun progression result (p < 0.0001) is a methodological trap, not a finding — it detects age, not astrology, because progressed Sun position is mathematically identical to age.

The hard aspect test (p = 0.048) is a genuine finding — but it inverts the traditional model. Positive events show slightly more hard aspects than negative events, adding another data point to the Hardship Hypothesis running through this book.

The genuine positive findings are the Mars ingress (p < 0.0001), Venus ingress (p = 0.0077), and progressed Moon variation (p = 0.0028). These suggest that the symbolic language of progressions may carry real information — not through the crude valence of "hard = bad, soft = good," but through the more nuanced signal of *sign change as qualitative threshold* and *Moon phase as personal temporal marker*.

Secondary progressions are not confirmed as working in their traditional form. But neither are they null. What appears to work is a subset of the system — the ingress mechanics and the Moon cycle — while the aspect-valence model fails its most direct empirical test.

---

*Archived celebrity charts, event data, progression calculations, and visualization files preserved in `backup/`.*
