# Project 12: Market Volatility and GARCH-X Modeling

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Can planetary aspects, included as exogenous variables in GARCH models, improve volatility forecasting beyond what a standard GARCH model achieves on its own? This is the most rigorous financial astrology test in the book — and it uses the industry's own standard tools.

---

## 💡 Why This Matters

Project 02 found a statistically real but tiny correlation between planetary cycles and market volatility (r = 0.0226). But correlation is not prediction. The question that matters for anyone who might actually use this information is: **does knowing the planetary positions improve my next forecast?**

GARCH models are the financial industry standard for volatility prediction. They explicitly account for volatility clustering — the well-documented phenomenon where turbulent periods follow turbulent periods, and calm follows calm. GARCH-X extends this by adding external variables, directly testing whether planetary data improves predictions.

If planets contribute useful information, GARCH-X should outperform baseline GARCH on out-of-sample data. If not, we'll know precisely: adding planets makes forecasts *worse*.

---

## 📊 The Data

| Source | Description |
|---|---|
| Yahoo Finance (VIX) | CBOE Volatility Index, 1990–2024 |
| Yahoo Finance (S&P 500) | Daily returns |
| Swiss Ephemeris | Outer planet aspect angles — continuous cosine similarity values |
| **Sample** | **8,500+ trading days** |

Aspects analyzed: Jupiter-Saturn, Saturn-Uranus, Saturn-Neptune, Saturn-Pluto synodic cycles.

---

## 📈 Results

### Phase 1: GARCH-X — Does Adding Planets Help?

| Model | In-Sample AIC | Out-of-Sample MSE (2016–2024) |
|---|---|---|
| **Baseline GARCH(1,1)** | **−120,451.54** | **0.00013050** |
| **GARCH-X + Planetary Data** | **−120,449.56** | **0.00013054** |

Both metrics favor the baseline. AIC *increased* (worsened) by 2.0 when planetary data was added. Out-of-sample MSE also worsened slightly. By every measure, planetary variables add noise, not signal, to GARCH forecasting.

### Phase 2: VIX Correlations with Planetary Aspects

Despite failing the predictive test, correlations between aspects and elevated VIX do exist:

| Aspect Type | Correlation (r) | p-value |
|---|---|---|
| **Hard aspects overall** | **0.295** | < 0.0001 |
| Soft aspects overall | 0.089 | 0.042 |
| **Saturn-Pluto** | **0.312** | < 0.001 |

**Mean VIX by configuration:**

| Configuration | Mean VIX | N Days |
|---|---|---|
| **Grand Cross** | **24.8** | 145 |
| T-Square | 21.2 | 892 |
| Grand Trine | 17.8 | 234 |
| No major pattern | 19.4 | 7,229 |

Hard aspects correlate with elevated VIX; soft aspects with lower VIX. The Saturn-Pluto correlation (r = 0.312) is the strongest single-pair result.

**Notable historical coincidences:**

| Event | Date | VIX | Active Aspects |
|---|---|---|---|
| COVID Crash | Mar 2020 | 82.69 | Saturn-Pluto conjunction |
| 2008 Financial Crisis | Oct 2008 | 80.86 | Saturn-Uranus opposition |
| 2011 Debt Crisis | Aug 2011 | 48.0 | Uranus-Pluto square building |
| Brexit | Jun 2016 | 25.76 | Saturn square Neptune |

---

## 🔍 The Correlation-Prediction Paradox

How can planetary aspects correlate with VIX (r = 0.295, p < 0.0001) yet *worsen* GARCH predictions? This apparent contradiction has a clear resolution.

Hard Saturn aspects occur during roughly 20–30% of all trading days. During those same periods, economic cycles, political events, and other catalysts also increase. The planetary aspects do not *cause* the volatility — they are correlated with it because both respond to longer structural cycles (economic supercycles, geopolitical cycles) that coincidentally align with 15–30 year planetary periods.

**In-sample correlation exploits this historical coincidence.** Out-of-sample prediction fails because:
1. Planetary variables add parameters without proportional information gain
2. Future planetary cycles don't predict *which specific days* will be volatile
3. The economic cycles underlying the correlation are not locked to planetary periods

The regression analysis confirms the modest scale: planetary aspects alone explain only **8.7%** of VIX variance (R² = 0.087). Adding economic controls raises R² to 0.342 — showing that economic variables explain vastly more.

![VIX vs. planetary aspect type, 1990–2024](images/project-12-figure-1.png)

---

## ⚠️ Statistical Caveats

- **r = 0.295 is weak:** ~8.7% of VIX variance explained. Day-of-week explains more.
- **Multiple testing:** Dozens of aspect combinations tested. Bonferroni correction would substantially raise thresholds.
- **Temporal autocorrelation:** Both planetary aspects and VIX exhibit strong autocorrelation. Standard p-values likely overstate significance; Newey-West standard errors should be applied.
- **Look-ahead bias:** Identifying which configurations coincide with famous crises is data dredging. The test that matters is whether this information was usable *before* the crisis.

---

## 🌟 Conclusion

This project provides the book's most methodologically rigorous financial astrology test. Using GARCH models — the industry standard for volatility forecasting — planetary aspects **make predictions worse**, not better.

The statistical correlation between hard aspects and elevated VIX (r ≈ 0.295–0.312) is real but practically useless. It reflects a loose historical coincidence of economic and planetary cycles — not a mechanistic relationship. Adding planetary data increases noise and worsens out-of-sample performance.

The correlation findings, taken naively, might encourage a financial astrologer to conclude they've found something real. The GARCH out-of-sample test definitively shows they have not. This is what proper financial modeling looks like: not "does this correlate historically?" but "does knowing this improve my next prediction?"

**For planetary aspects and market volatility, the answer is no.**

> *This project does not constitute financial advice.*
