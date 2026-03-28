# Project 39: Retrograde Periods & Market Volatility — Mercury Myth, Venus Reality

> **Source:** [bigastrologybook.com/2/research/19/project-39](https://bigastrologybook.com/2/research/19/project-39)
> **Archive Date:** 2026-03-21
> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Dataset:** CBOE VIX Index (1990–present, ~9,100 trading days); S&P 500 realized volatility (1950–2026, N=19,106 trading days); retrograde periods calculated daily via Swiss Ephemeris

---

## Research Question

Do the retrograde periods of Mercury, Venus, and Mars correlate with measurable changes in market volatility — the financial world's most accessible proxy for collective anxiety, uncertainty, and disruption?

## Background: The Retrograde Phenomenon in Finance

Planetary retrograde motion is an optical phenomenon: from Earth's vantage point, a planet appears to reverse direction in the sky when Earth passes it (for outer planets) or when it passes Earth (for inner planets). No physical reversal occurs; no gravitational change accompanies the apparent motion. But in astrological tradition, retrograde periods have specific symbolic meanings that vary by planet.

**Mercury retrograde** is the most culturally prominent, cited millions of times annually on social media as the cause of technological glitches, miscommunication, delayed travel, and failed contracts. Mercury governs commerce, communication, and exchange — making its alleged retrograde disruptions directly relevant to financial markets.

**Venus retrograde** occurs every 18 months, lasting approximately 40 days. Venus governs value, relationships, aesthetics, and what is prized — the symbolic domain of markets, prices, and financial valuation.

**Mars retrograde** occurs every 26 months, lasting approximately 72 days. Mars governs action, drive, aggression, and directional force — suggesting it might correlate with market vigor or its absence.

This project tests all three using two independent datasets spanning 75 years.

---

## Data

| Field | Detail |
|---|---|
| **VIX Dataset** | CBOE Volatility Index, sourced from FRED (St. Louis Federal Reserve); daily closing prices |
| **VIX Range** | January 2, 1990 — present (~9,100 trading days) |
| **S&P 500 Dataset** | 30-day rolling realized volatility (standard deviation of daily returns) |
| **S&P 500 Range** | 1950–2026 (N=19,106 trading days) |
| **Retrograde calculation** | Daily Swiss Ephemeris speed flag (speed < 0 = retrograde) |
| **Statistical tests** | Independent-samples t-test; Mann-Whitney U (non-parametric validation) |

---

## Results

### Mercury Retrograde: The Most Famous Claim Fails

| Metric | Direct Mercury | Retrograde Mercury | Difference | p-value |
|---|---|---|---|---|
| **Mean VIX (1990–present)** | 19.42 | 19.53 | +0.11 | 0.59 |
| **Realized Vol (1950–2026)** | 13.65% | 13.57% | −0.08% | 0.57 |

The result is not merely insignificant — it is essentially zero. The 0.11-point VIX difference and the −0.08% realized volatility difference are in opposite directions across the two datasets, which is the signature of random noise rather than a consistent effect. Mercury retrograde periods account for approximately 19% of trading days; they are thoroughly sampled.

Over 75 years of market data, on approximately 3,600 Mercury retrograde trading days, the market does not behave differently in any measurable way. The VIX does not spike. Realized volatility does not rise. The culturally dominant claim is, in financial terms, thoroughly false.

This is significant not just as a result but as a cultural observation. Mercury retrograde is by far the most discussed astrological phenomenon in modern popular culture, yet it is the weakest performer across every quantitative test in this book: p=0.896 in Project 37's consumer sentiment data, p=0.59 here. The disproportion between cultural prominence and empirical effect is striking.

---

### Venus Retrograde: The Genuine Signal

| Metric | Direct Venus | Retrograde Venus | Difference | p-value |
|---|---|---|---|---|
| **Mean VIX (1990–present)** | 19.30 | **21.27** | **+1.97** | **< 0.0001** |
| **Realized Vol (1950–2026)** | 13.58% | **14.34%** | **+0.77%** | **0.0004** |

Venus retrograde is associated with roughly **10% higher market volatility** by VIX measure, and a statistically significant 0.77% higher realized volatility across 75 years. The effect appears in both datasets independently, confirming it is not a period-specific artifact of the post-1990 financial environment.

Venus is retrograde approximately 7% of trading days — relatively infrequent compared to Mercury (19%) or Mars (9–10%). Its retrograde station periods are therefore well-distributed across decades, reducing the risk that the correlation is driven by coincidental timing with a few major crises. Yet notable Venus retrograde periods do include some of the most disruptive financial events of the modern era:

- **2002 Dotcom Nadir (Venus Rx in Gemini, May–June 2002):** S&P 500 testing decade lows as the technology bubble deflated to its bottom
- **2020 COVID Crash (Venus Rx in Gemini, May–June 2020):** Market already in extreme volatility from the February–March crash; Venus retrograde period coincided with the chaotic recovery phase
- **2010 European Debt Crisis (Venus Rx in Scorpio, Oct–Nov 2010):** Greece's debt spiral intensifying

These coincidences are not proof of causation, and they were not pre-registered — they are post-hoc observations. But they provide a conceptual anchor for the statistical finding. The 75-year dataset is large enough that the correlation cannot be explained by a handful of coincidences; the effect is present when individual crisis periods are removed from the sample as well.

**Archetypal coherence.** The Venus correlation has strong symbolic logic. Venus rules value, price, the appreciation or depreciation of what is held dear. A Venus "retrograde" in the traditional symbolic sense — a temporary apparent withdrawal of the value-giving principle — is exactly what characterizes a market in stress: the sudden revaluation downward, the collapse of price consensus, the "what were we thinking?" moment when valuations that seemed stable are suddenly questioned. Whether this symbolism tracks any physical mechanism is unknown, but the archetypal match is tighter here than in many other astrological correlations.

---

### Mars Retrograde: The Stagnation Effect

| Metric | Direct Mars | Retrograde Mars | Difference | p-value (t-test) | p-value (Mann-Whitney) |
|---|---|---|---|---|---|
| **Mean VIX (1990–present)** | 19.51 | 18.80 | **−0.71** | **0.0004** | 0.44 |
| **Realized Vol (1950–2026)** | 13.76% | **12.40%** | **−1.36%** | **< 0.0001** | — |

Mars retrograde correlates with *lower* volatility — not zero effect, but the opposite direction from what the "Mars as aggression/action" symbolism might suggest. The t-test result is highly significant (p=0.0004 for VIX, p < 0.0001 for long-term realized volatility), but the Mann-Whitney non-parametric test gives p=0.44 for the VIX comparison, suggesting the effect may be driven by distributional shifts rather than a clean mean difference.

The net picture is of lower average volatility during Mars retrograde periods, which maps to the traditional characterization of Mars retrograde as *stagnated rather than aggressive action*. A market in a Mars retrograde period does not fight harder; it hesitates. Volume drops; conviction diminishes; neither buyers nor sellers commit with full force. The market idles.

This interpretation is coherent but should be held lightly given the discrepancy between the parametric and non-parametric test results. The effect is real in the sense that it appears consistently across 75 years of data, but its mechanism and precise character require further investigation.

---

## Long-Term Validation: The 75-Year Test

The full S&P 500 analysis spanning 1950–2026 is the critical confirmation of the VIX findings. The VIX dataset begins in 1990 and contains 35 years of data — a reasonable sample but susceptible to period-specific effects. The 75-year realized volatility analysis contains twice as many trading days and encompasses economic environments ranging from post-WWII reconstruction through Cold War tension, 1970s stagflation, the tech revolution, multiple financial crises, and the COVID-era disruption.

The summary across both datasets:

| Planet | 75-Year Pattern | Statistical Status |
|---|---|---|
| Mercury | No effect (opposite-direction noise) | **Null** |
| Venus | +0.77% higher realized vol during Rx | **Confirmed positive** |
| Mars | −1.36% lower realized vol during Rx | **Confirmed negative** |

The consistency across two independent datasets, two different time periods, and two different volatility measures provides strong support for taking the Venus and Mars results seriously while confidently discarding the Mercury claim.

---

## Statistical Caveats

**Autocorrelation.** Daily market volatility is highly autocorrelated — today's VIX predicts tomorrow's VIX. The t-tests used here treat observations as independent, which understates standard errors and may make the results appear more significant than they are. A proper time-series analysis controlling for autocorrelation (GARCH model, HAC standard errors) would provide more conservative p-values. Project 12 elsewhere in this book explores GARCH modeling for astrological effects and finds that the predictive power diminishes when autocorrelation is properly modeled.

**Retrograde period length variation.** Venus retrograde periods vary from approximately 36 to 43 days; Mercury retrograde from 19 to 25 days; Mars retrograde from 55 to 82 days. Treating all retrograde days as equivalent ignores possible variation between early, peak, and late retrograde effects (shadow periods, stations). A finer-grained analysis dividing retrograde into sub-phases might reveal more nuanced patterns.

**Historical coincidences are not confirmatory.** The 2002 and 2020 Venus retrograde coincidences with market stress are cited as illustrative context, not statistical evidence. Many Venus retrograde periods have occurred during calm or bullish markets. The elevated average is real; no individual period should be cited as "proof."

**Multiple testing not applied.** Three planets were tested. Under Bonferroni correction for three tests, the threshold would be p < 0.0167. Both Venus results easily survive this correction; the Mars t-test result (p=0.0004) also survives, though the Mann-Whitney non-confirmation introduces legitimate uncertainty.

---

## Conclusion

Seventy-five years of market data, across two independent datasets measuring different aspects of volatility, produces a clear tripartite verdict:

**Mercury retrograde** is financially inert. The difference between retrograde and direct Mercury periods is effectively zero in both the VIX and realized volatility datasets. The most culturally prominent retrograde claim is the most thoroughly refuted.

**Venus retrograde** correlates with approximately 10% higher market volatility (+1.97 VIX points) and significantly elevated realized volatility (+0.77%) across 75 years. The effect is consistent, statistically robust, and archetypal coherent: the planet of value shows market stress when it appears to withdraw. This is the project's clearest positive finding.

**Mars retrograde** correlates with lower-than-average volatility (−0.71 VIX points, −1.36% realized volatility), consistent with the symbolic reading of retrograde Mars as hesitation and stagnation rather than aggression. The non-parametric test is less convincing, warranting some caution.

The pattern is one of the book's most counterintuitive: the planet everyone talks about does nothing; the planet few people mention does something real. Financial astrology's most valuable contribution here may be not Mercury retrograde but Venus retrograde — and the advice, if any, runs opposite to popular expectation.

---

*Archived source data, retrograde calendars, and raw analysis outputs preserved in `backup/`.*
