# Project 04: Who Believes in Astrology, and Where?

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

What geographic, demographic, and cultural factors predict interest in and belief in astrology across the United States? Can we explain why some states are more astrologically engaged than others?

---

## 💡 Why This Matters

Before we can evaluate whether astrology *works*, it helps to understand who actually engages with it — and why. The cultural distribution of astrological belief is not random, and the patterns reveal something important: astrology in 21st-century America is not what the "folk superstition" stereotype would lead you to expect.

This project doesn't test whether the zodiac predicts character. It tests whether *demographic variables* predict *astrological engagement*. The answer is a remarkably clean yes — and the direction of the relationships upends the usual assumptions about astrology's audience.

---

## 📊 The Data

Two data sources, measuring two different things:

**Google Trends "horoscope" search interest** — measures *engagement and curiosity.* Searching for one's horoscope is a behavioral measure; it doesn't necessarily indicate deep belief. This is state-level data from 2023.

**Pew Research Center survey (2017–2018)** — measures *stated belief in astrology*, from a nationally representative survey of 4,729 respondents. This is a conviction measure.

Both tell the same demographic story, but they're distinct — a curious non-believer contributes to Google Trends but not to Pew's "belief" category. The findings below draw on both and are labeled accordingly.

> *Data transparency note: The Google Trends state-level figures used cached 2023 data. The Pew survey figures are fully published and verified.*

| Source | Description | N |
|---|---|---|
| Pew Research Center (2017–2018) | National survey, belief in astrology by age/gender/region | 4,729 |
| Google Trends (2023) | State-level relative search interest for "horoscope" | 50 states |
| US Census Bureau | Urbanization %, college graduation %, median income, median age | All states |

---

## 🔬 Method

**For the Pew analysis:** Standard frequency and cross-tabulation analysis to characterize belief rates by age group, gender, and census region.

**For the state-level analysis:** Pearson correlation between Google Trends search interest and Census demographic variables, followed by multiple linear regression to identify the best predictor combination.

---

## 📈 Results

### Who Believes: The National Picture

The national baseline from Pew: **29% of Americans believe in astrology.** But that aggregate conceals dramatic variation.

**By age — the steepest gradient:**

| Age Group | % Who Believe in Astrology |
|---|---|
| 18–29 | **44%** |
| 30–49 | 32% |
| 50–64 | 22% |
| 65+ | 17% |

Young adults are more than twice as likely to believe in astrology as seniors. Whether this reflects a cohort effect (younger generations are genuinely more drawn to astrology) or a life-stage effect (people grow out of it as they age) can't be determined from a single survey. But the gap is enormous — larger than most cultural belief differences measured by Pew.

**By gender:**

| Gender | % Who Believe |
|---|---|
| Women | **37%** |
| Men | 20% |

A 17-point gap. This is consistent with decades of research on gender and metaphysical belief systems.

**By region:**

| Region | % Who Believe |
|---|---|
| West | **33%** |
| Northeast | 31% |
| South | 28% |
| Midwest | 25% |

The regional spread is modest — only 8 points between the most and least astrologically engaged regions. But the direction is clear: coastal and urban-heavy regions lead.

### Where the Interest Is: State-Level Correlations

| Demographic Variable | Correlation (r) | p-value | Significant? |
|---|---|---|---|
| **Urban population %** | **0.719** | <0.0001 | ✓ Yes |
| **Median income** | **0.621** | <0.0001 | ✓ Yes |
| **College graduation %** | **0.620** | <0.0001 | ✓ Yes |
| **Total population** | 0.518 | 0.0001 | ✓ Yes |
| Median age | 0.214 | 0.135 | No |

**Urbanization is the strongest single predictor** — r = 0.719, which is a remarkably clean relationship for social science data. A state's urban population share accounts for a substantial fraction of its astrological search activity.

A multiple regression model combining urbanization, college graduation rate, and median income explains **74.3% of state-level variation in astrological interest** (R² = 0.743).

> *Methodological note: Urbanization, education, and income are themselves correlated with each other. The model tells us these variables together predict astrological interest well, but cannot cleanly partition the effect across them.*

![State-level astrological search interest vs. urbanization rate](images/project-04-figure-1.png)

---

## 🔍 What the Numbers Mean

### The Counterintuitive Finding

The most important result here is directional. Astrology interest is **higher** in more urban, more educated, higher-income states. This is the opposite of what a "folk superstition" framing would predict.

If astrology were primarily a belief system of rural or less educated communities — as it is sometimes stereotyped — we would expect negative correlations with education and income, and weak correlations with urbanization. We find exactly the reverse: all three variables correlate positively with astrological engagement, and urbanization does so most strongly.

**What this means:** In 21st-century America, astrology is an urban cultural practice, embedded in wellness culture, identity-based spirituality, and the social milieus of educated young adults. It travels through the same networks that spread yoga, therapy culture, and progressive lifestyle branding. It is not primarily the belief of people "left behind by modernity" — it is, to a significant degree, *carried by* modernity's most mobile and culturally connected populations.

### Education and Belief

The correlation between education and astrological interest might seem puzzling. Educated people are more likely to understand that astrology lacks a proven physical mechanism. But education also produces:
- More exposure to wellness and New Age frameworks through urban social networks
- Greater comfort with psychological frameworks (astrology as personality language)
- More disposable income and time for spiritual exploration

The Pew data clarifies this: overall *belief* rates are lower than Google Trends *engagement* rates would suggest. Many urban, educated astrology consumers are curious participants rather than literal believers — using the framework for self-reflection and social connection rather than as a predictive oracle.

### The Age Axis

The Pew data's age gradient (44% at 18–29 vs. 17% at 65+) compounds the geographic pattern. Young people are disproportionately urban, and they're also the most likely to believe. Whether the current 18–29 cohort will maintain their astrological engagement as they age is the most consequential unanswered question for astrology's cultural future — and cannot be answered from a cross-sectional survey.

---

## ⚠️ Limitations & Caveats

- Google Trends measures search interest, not practice or belief. Curiosity, skepticism, and genuine belief all show up in search data.
- The Google Trends data is approximate — cached state-level figures rather than live API output.
- Multicollinearity between urbanization, education, and income means we can't cleanly attribute the effect to any single factor.
- The survey data is US-only. Astrological belief patterns differ substantially in India, Western Europe, and other markets where astrology has different cultural positioning.

---

## 🌟 Conclusion

Astrological interest in the United States is not randomly distributed. It concentrates in urban, younger, educated, higher-income populations, with women significantly overrepresented. Three demographic variables together explain 74.3% of the state-level variation in search interest.

The sociological conclusion: astrology in 21st-century America is not a rural folk belief persisting at the margins of modernity. It is an urban cultural practice, most prevalent in the same populations that lead trends in wellness, identity-based consumer behavior, and digital culture. Understanding astrology's contemporary role requires understanding that social context, not just the content of astrological tradition itself.

Whether the practice is worth evaluating empirically — whether its technical claims have substance — is what the other 33 projects in this book address. What *this* project establishes is: the people doing the evaluating and the believing are not who you might have assumed.
