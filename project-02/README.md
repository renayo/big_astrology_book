# Project 02: Planetary Cycles and Market Volatility

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com](https://bigastrologybook.com)

---

## 🌟 Overview — What We Asked

Is there a measurable, statistically robust correlation between major planetary cycles — particularly the ~20-year Jupiter-Saturn synodic cycle — and changes in stock market volatility or returns across 74 years of daily trading data?

---

## 💡 Why This Matters

Financial astrology is one of the oldest practical applications of astrological thinking. And of all the domains where you might look for astrological effects, markets are one of the most compelling candidates: they are driven *entirely* by human psychology, and they produce precise daily numbers stretching back decades. If planetary cycles encode any real structural information about collective human behavior, the cumulative buying and selling decisions of millions of people should be where a signal shows up.

This project doesn't rely on anecdote or cherry-picked historical "hits." It applies the full toolkit of modern time-series econometrics to 74 years of daily data and asks: *is there anything here, and if so, is it big enough to matter?*

The answer is illuminating precisely because it's split. There is a statistically real signal. And it is essentially useless for prediction.

---

## 📊 The Data

| Source | Description |
|---|---|
| Yahoo Finance | S&P 500, VIX, Gold, Crude Oil — daily close prices, 1950–2024 |
| Swiss Ephemeris | Jupiter-Saturn angular separation (degrees of orb from exact aspect) — same period |
| **Scope** | **18,869 trading days across 74 years** |

All data is real. No synthetic datasets, no generated numbers. This is the most extensive time-series analysis in the book.

---

## 🔬 Method

The analysis used four complementary approaches:

**ARIMA modeling** fitted time-series models to daily returns and tested whether adding planetary variables improved in-sample fit (AIC criterion) and out-of-sample prediction error (MSE).

**GARCH(1,1)** modeled volatility clustering — the well-established pattern where calm periods cluster together and turbulent periods cluster together. GARCH-X extended this by including planetary variables as exogenous regressors in the variance equation.

**Granger Causality Tests** asked a directional question: does knowing yesterday's planetary position help you predict tomorrow's market price, above and beyond knowing yesterday's price? This is the operational definition of predictive information.

**Polar Cycle Analysis** mapped 74 years of daily returns and volatility onto the 360° wheel of the Jupiter-Saturn synodic cycle — essentially a full picture of which parts of that cycle are historically associated with what market behavior.

**15-Pair Expanded Analysis** extended the single Jupiter-Saturn pair to all combinations of Mars, Jupiter, Saturn, Uranus, Neptune, and Pluto — 15 pairwise cycles in total.

---

## 📈 Results

### The Core Finding: Real But Tiny

The headline number: **Pearson r = 0.0226 (p = 0.0019)** between Jupiter-Saturn angular separation and GARCH-derived market volatility.

That p-value is genuine. Bootstrap resampling (1,000 iterations) produced a 95% confidence interval of **[0.0050, 0.0354]** — the interval does not contain zero, meaning the correlation is unlikely to be pure noise.

But "statistically significant" and "practically meaningful" are two very different things. This correlation explains **less than 0.1% of market variance**. For comparison, the day of the week explains more about returns than planetary positions do.

The direction is also counterintuitive: the correlation is *positive* with orb degrees, meaning as Jupiter and Saturn move *farther apart*, volatility *increases*. Exact aspects (conjunction, opposition, trine — 0° orb) are associated with *calmer* markets. Most financial astrology would predict the opposite.

### Predictive Power: Worse Than Nothing

| Test | Baseline Model | With Planetary Data | Verdict |
|---|---|---|---|
| ARIMA AIC | −120,451.54 | −120,449.56 | **Worse** (higher AIC is worse) |
| Out-of-sample MSE (2016–2024) | 0.00013050 | 0.00013054 | **Worse** |
| Granger causality, lag 5 | — | p = 0.84 | **Fail** |
| Granger causality, lag 20 | — | p = 0.78 | **Fail** |

Adding planetary data to a predictive model makes it *slightly worse*, not better. Past planetary positions add noise. The correlation, while statistically detectable, contains no actionable predictive information.

Think of it this way: imagine you had a friend who could tell you, with perfect accuracy, where Jupiter and Saturn are in the sky on any given trading day. Would that help you beat the market? According to 74 years of daily data: no. Not even a little.

![Polar cycle map: Jupiter-Saturn orb degrees vs. market volatility](images/project-02-figure-1.png)

### The Trine Instability Paradox

The polar cycle analysis produced the project's most intellectually interesting surprise.

**The Trine (120°) is the most unstable zone in the data:**

| Aspect Zone | Avg. Daily Volatility | Avg. Daily Return |
|---|---|---|
| **Trine (115°–125°)** | **0.011 (highest)** | **−0.12% (negative)** |
| Conjunction (355°–5°) | 0.0108 (high) | +0.05% (positive) |
| Quincunx (155°) | — | **+0.13% (highest returns)** |
| Semi-Square (315°) | — | +0.10% |

In traditional astrology, the Trine is the most "harmonious" aspect — associated with ease, luck, and natural flow. In 74 years of market data, it correlates with the highest volatility and negative average returns. The Conjunction generates similar turbulence but with positive average returns — a "market reset" rather than a correction.

The highest actual returns appear at the *minor* Quincunx and Semi-Square aspects — the ones most traditional systems consider insignificant or ignore entirely.

One possible interpretation: the "ease of flow" that a Trine represents might manifest in markets as ease of *selling* — capitulation happening without friction. This is speculative and interesting. It suggests that if any planetary influence operates on markets, it follows its own logic rather than mapping neatly onto traditional astrological symbolism.

### The 15-Pair Expanded Analysis

| Pair | Correlation | Character |
|---|---|---|
| **Saturn-Uranus** | **−0.18 (strongest)** | Volatility at hard aspects *and* the Trine |
| Saturn-Neptune | +0.14 | Separating aspects correlate with volatility |
| Jupiter-Saturn | +0.08 | "Trine Instability" + "Cycle Reset" |
| Mars-Jupiter | +0.05 | Volatility concentrated at Conjunction |
| Neptune-Pluto | +0.05 | The Long Sextile — correlates with its persistent aspect |

**Saturn-Uranus** is the standout: nearly 8× stronger than Jupiter-Saturn (r = −0.18). Volatility spikes at hard aspects *and* at the Trine, suggesting this pair's influence is unusually pervasive.

**The Conjunction Effect:** The 0° zone appears as a primary volatility peak in roughly 7 of 15 tested pairs. The start of a planetary cycle — the "New Moon" of synodic astrology — consistently coincides with elevated market instability.

> **Multiple testing caveat:** With 15 pairs × multiple aspect zones × multiple metrics, many hypothesis tests were implicitly run. The Saturn-Uranus result (r = −0.18) is robust enough to likely survive correction; weaker traces (r = 0.03–0.05) should be treated as suggestive only.

---

## 🔍 What the Numbers Mean

The data supports a specific, modest claim: **planetary cycles may function as background "seasons" of volatility** — describing the risk climate in very general terms, not forecasting daily prices.

The Conjunction Effect (volatility at cycle starts) is the most replicable structural finding. The Trine Anomaly (sharp drops at astrology's "lucky" aspect) is the most intellectually interesting. Neither provides actionable trading information.

The project's real contribution is methodological: showing what "planetary-market correlation" actually looks like when tested rigorously. It looks like a signal-to-noise ratio of roughly 1:1000, and a model that gets slightly *worse* when you add planetary data. That's the honest picture.

---

## ⚠️ Limitations & Caveats

- **r = 0.0226 explains <0.1% of variance.** The day of the week explains more about market behavior.
- ARIMA and Granger tests confirm no predictive value, regardless of the correlation.
- The Trine Instability finding, while reproducible, is a historical observation — not a trading rule.
- With 15 pairs and multiple metrics, some patterns are expected from multiple comparisons. Bonferroni correction would tighten all significance thresholds.
- Market correlations in historical data do not guarantee future performance.

---

## 🌟 Conclusion

Seventy-four years of daily market data and rigorous econometric testing yield an honest split verdict:

**Yes, a correlation exists.** Jupiter-Saturn orbital distance correlates with GARCH volatility at r=0.0226, p=0.0019. Saturn-Uranus shows r=−0.18 — the strongest single-pair signal. The correlation is not imaginary.

**No, it cannot predict markets.** ARIMA and Granger tests show planetary data adds noise to prediction models. Out-of-sample error worsens when planets are included. The statistical signal, while real, carries no information that improves forecasts.

The genuinely surprising result — that the Trine correlates with market drops, not rises — is the most interesting finding. It suggests that if planetary influence on markets operates at all, it follows its own logic rather than the traditional astrological symbolism. That's worth knowing, even if the practical implications are nil.

> **This project does not constitute financial advice.** Correlations in historical data do not guarantee future performance.
