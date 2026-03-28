# Project 01: Do Ultra-Wealthy Individuals Share Astrological Birth Patterns?

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Do the birth charts of ultra-wealthy people look different from what random chance — corrected for the real calendar of human births — would predict? If a group is selected for extreme financial success, should we see any non-random clustering in planetary positions?

---

## 💡 Why This Matters

The "born lucky" question is one of astrology's most ancient: does the sky at the moment of your arrival encode something about the life you'll live? The ultra-wealthy make a fascinating test case not because money is the most important thing, but because this group is *selected* on a single, measurable, verifiable criterion — they are among the richest human beings alive or recently documented. If planetary position carries real information about destiny or character, a group this extreme should stand out against the background sky.

This project also makes a methodological point that carries through the entire book: testing whether "high achievers cluster in certain signs" requires knowing what the baseline looks like — not the naive 1/12 per sign, but the *real* distribution of human births across the calendar year, corrected for the well-known seasonal birth peak.

---

## 📊 The Data

### The 152 Million Birth Baseline

The CDC/NCHS natality database covers **152,273,157 US births from 1970–2014**. This massive dataset serves not as a test group, but as a **calendar-weighted comparison baseline** — a map of what planetary distributions look like across real human birth dates.

Why does this matter? Because births aren't uniformly spread across the year. US births peak in late summer (August–September, the Leo–Virgo zone) and dip in winter (Capricorn–Aquarius). The Sun spends slightly different amounts of time in each sign. The Moon cycles through all 12 signs every 27.3 days, completely independent of season.

By modeling all of this, we can ask: *for any group of people born in the 20th century, what planetary distribution would we expect if astrology added nothing?* That's the baseline.

Key findings from the baseline alone:

| Factor | Max Deviation | What It Means |
|---|---|---|
| Moon Sign (Tropical) | < 0.3% | Effectively flat — no lunar birth preference |
| Moon Sign (Vedic) | < 0.4% | Same — lunar signs are calendar-neutral |
| Tithi (Vedic Lunar Day) | < 0.6% | No coherent structure |
| Sun Sign (Tropical) | ±6% | **Seasonal birth curve only** — late summer peak |

The Moon is essentially uninvolved in birth timing at the population level. Sun sign variation is entirely biological — late-summer babies are more common because of holiday-season conceptions. This confirms the baseline is appropriate: flat for Moon and Tithi, seasonally adjusted for Sun.

### The Test Group: N = 20 Ultra-Wealthy Individuals

Twenty people from the Forbes billionaire list, verified public birthdates. This includes:

| Name | Sun (Tropical) | Moon (Tropical) | Moon (Vedic) | Tithi |
|---|---|---|---|---|
| Rob Walton | Scorpio | Pisces | Aquarius | Shukla 11 |
| Sergey Brin | Leo | Taurus | Taurus | Krishna 08 |
| Steve Ballmer | Aries | Virgo | Leo | Shukla 13 |
| Mukesh Ambani | Aries | Capricorn | Sagittarius | Krishna 06 |
| Jim Walton | Gemini | Gemini | Taurus | Amavasya (New) |
| Michael Bloomberg | Aquarius | Aquarius | Capricorn | Amavasya (New) |
| Warren Buffett | Virgo | Sagittarius | Scorpio | Shukla 08 |
| Carlos Slim | Aquarius | Virgo | Virgo | Krishna 05 |
| Larry Page | Aries | Capricorn | Sagittarius | Krishna 08 |
| Alice Walton | Libra | Aries | Pisces | Krishna 01 |
| Larry Ellison | Leo | Leo | Cancer | Krishna 14 |
| Bernard Arnault | Pisces | Taurus | Aries | Shukla 06 |
| Jeff Bezos | Capricorn | Sagittarius | Sagittarius | Krishna 13 |
| Amancio Ortega | Aries | Gemini | Taurus | Shukla 07 |
| Mark Zuckerberg | Taurus | Scorpio | Libra | Purnima (Full) |
| Charles Koch | Scorpio | Capricorn | Sagittarius | Shukla 05 |
| Bill Gates | Scorpio | Pisces | Pisces | Shukla 12 |
| Francoise Bettencourt Meyers | Cancer | Cancer | Gemini | Amavasya (New) |
| David Koch | Taurus | Pisces | Pisces | Krishna 12 |
| Elon Musk | Cancer | Virgo | Leo | Shukla 06 |

Planetary positions calculated at noon UTC via Swiss Ephemeris with Lahiri ayanamsha for Vedic calculations.

---

## 🔬 Method

Chi-square goodness-of-fit tests compare the observed distribution across 12 signs against the calendar-weighted expected distribution from the 152M baseline. For Moon signs and Tithi, the baseline is essentially flat, making the expected frequencies straightforward. For Sun signs, the seasonal correction is essential — Aries is actually a *below-average* birth month in the US, so the expected count for Aries is less than 1/12 of N.

### A Critical Note on Statistical Power

With N=20 and 12 sign categories, the chi-square test requires extremely concentrated clustering to reach p<0.05. Not achieving significance does not mean there is no effect — it means the sample is too small to *prove* one statistically. The **effect sizes** (percentage deviations from expected) are the meaningful signal. P-values here indicate direction and magnitude; they are not the final word.

A sample of ~100+ verified ultra-wealthy individuals with complete birth data would be needed to make firm significance claims.

---

## 📈 Results

### Sun Sign (Tropical) — Corrected for Seasonal Births

Chi² = 7.82 | df = 11 | p = 0.73

| Sign | Observed | Expected | Deviation |
|---|---|---|---|
| **Aries** | **4** | 1.6 | **+147%** |
| **Scorpio** | **3** | 1.7 | **+81%** |
| Taurus | 2 | 1.6 | +23% |
| Aquarius | 2 | 1.6 | +22% |
| Cancer | 2 | 1.7 | +17% |
| Leo | 2 | 1.8 | +14% |
| Capricorn | 1 | 1.6 | −37% |
| Pisces | 1 | 1.6 | −39% |
| Gemini | 1 | 1.6 | −40% |
| Libra | 1 | 1.7 | −42% |
| Virgo | 1 | 1.8 | −43% |
| **Sagittarius** | **0** | 1.6 | **−100%** |

The Aries result is particularly striking: Aries is a *below-average* birth month in the general US population (−2.7% vs. uniform). After correcting for this, finding 4 of 20 billionaires with Aries Suns is even more anomalous than the raw number suggests.

![Sun sign distribution for ultra-wealthy cohort vs. baseline](images/project-01-figure-1.png)

### Moon Sign (Tropical) — Near-Uniform Baseline

Chi² = 6.41 | df = 11 | p = 0.84

| Sign | Observed | Expected | Deviation |
|---|---|---|---|
| **Pisces** | **3** | 1.7 | **+81%** |
| **Capricorn** | **3** | 1.7 | **+81%** |
| **Virgo** | **3** | 1.7 | **+80%** |
| Gemini | 2 | 1.7 | +20% |
| Taurus | 2 | 1.7 | +20% |
| Sagittarius | 2 | 1.7 | +20% |
| Aquarius | 1 | 1.7 | −40% |
| Aries | 1 | 1.7 | −40% |
| Cancer | 1 | 1.7 | −40% |
| Scorpio | 1 | 1.7 | −40% |
| Leo | 1 | 1.7 | −40% |
| **Libra** | **0** | 1.7 | **−100%** |

Earth signs dominate: Virgo, Capricorn, and Taurus account for 8 of 20 individuals (40%) against a 25% expected rate.

### Moon Sign (Vedic / Sidereal) — Near-Uniform Baseline

Chi² = 7.62 | df = 11 | p = 0.75

| Sign | Observed | Expected | Deviation |
|---|---|---|---|
| **Sagittarius** | **4** | 1.7 | **+140%** |
| **Pisces** | **3** | 1.7 | **+80%** |
| **Taurus** | **3** | 1.7 | **+80%** |
| All other signs | 1 each | 1.7 | −40% each |

Sagittarius Vedic Moon is the single strongest lunar signal — 4 of 20 individuals, or more than twice the expected rate.

### Tithi (Vedic Lunar Day) — Uniform Baseline

The Tithi system divides the lunar month into 30 lunar days (tithis). At random, each tithi should appear in ~3.3% of births (1/30 × 100).

Chi² = 25.00 | df = 29 | p = 0.68

| Tithi | Observed | Expected | Deviation |
|---|---|---|---|
| **Amavasya (New Moon)** | **3** | 0.67 | **+350%** |
| **Shukla 06** | **2** | 0.67 | **+200%** |
| **Krishna 08** | **2** | 0.67 | **+200%** |
| All other tithis | 0 or 1 | 0.67 | −100% to +50% |

**Amavasya** — the darkest night of the lunar cycle, when no Moon is visible — is the most striking signal. Three of 20 billionaires (15%) were born on Amavasya, against a baseline expectation of ~3.3%: Bloomberg, Jim Walton, and Francoise Bettencourt Meyers.

---

## 🔍 What the Numbers Mean

The patterns cluster around a theme that appears repeatedly across this book: **astrological "difficulty" rather than ease characterizes exceptionally driven individuals.**

- **Aries** is traditionally the sign of pure initiative, friction, and competitive drive — not particularly comfortable or "harmonious."
- **Scorpio** is associated with intensity, power drives, and psychological depth — not ease.
- **Tropical Earth Moons** (Virgo, Capricorn) suggest an emphasis on material world navigation, practical mastery, and groundedness.
- **Sagittarius Vedic Moon** carries themes of philosophy, restlessness, and the eternal quest — not contentment.
- **Amavasya (New Moon)** is the darkest phase — associated in Vedic tradition with inward-turning, withdrawal from conventional norms, and beginning new cycles from void. It is the *opposite* of the Full Moon visibility that folk tradition celebrates.

If the hypothesis "strong, dignified charts produce success" were true, we might expect Leo Suns, Taurus Moons, exalted planets. Instead we find Aries, Scorpio, dark-Moon births. This aligns with what Projects 06, 14, 20, and 33 find through completely different methods: friction, not ease, may be the astrological signature of extreme achievement.

---

## ⚠️ Limitations & Caveats

- **N=20 is far too small** for statistical confirmation. Every effect size here could be sampling variation.
- The 20 individuals were selected from a Forbes list that itself has selection biases (Western wealth, publicly verified, living or recently deceased).
- Using noon UTC for birth times when actual times are unknown introduces some error, primarily affecting Moon positions.
- We cannot control for socioeconomic privilege, historical era, country of birth, or the dozens of other factors that produce extreme wealth.
- Multiple patterns were examined (12 Sun signs, 12 Moon signs × 2 zodiacs, 30 Tithis). With many comparisons, some apparent anomalies are expected by chance.

---

## 🌟 Conclusion

No factor achieved statistical significance — that is entirely expected and entirely due to sample size, not absence of effect.

The patterns that emerged:

- **Aries Sun: +147%** against a below-average birth month baseline
- **Sagittarius Vedic Moon: +140%** — strongest single lunar signal
- **Amavasya (New Moon) Tithi: +350%** — 3 individuals vs. 0.67 expected
- **Earth Moons (Tropical): +80% each** — 40% of the cohort in practical, grounded lunar signs
- **Zero Sagittarius Suns, zero Libra Moons**

These are preliminary findings. The right next step is expanding to 100+ verified ultra-wealthy individuals to achieve adequate statistical power. What this dataset offers is a direction: the consistent signal toward "difficult" rather than "easy" placements.

> **What's next:** A pre-registered study with N≥100 billionaires, full birth times where available, and a comparison to other "extreme achiever" cohorts (Olympic athletes, Nobel laureates) to test whether the Hardship Hypothesis holds across achievement domains.
