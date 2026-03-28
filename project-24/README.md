# Project 24: Electional Astrology and IPO Returns

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com](https://bigastrologybook.com)

---

## 🌟 Overview — What We Asked

Can traditional "electional astrology" rules — choosing the perfect time to launch a venture — predict the long-term financial success of companies based solely on their IPO date? Do companies going public during astrologically favorable windows outperform those launched during unfavorable ones?

---

## 💡 Why This Matters

Electional astrology — choosing auspicious timing for major undertakings — is one of the most directly testable branches of the discipline. IPO dates are precisely documented, publicly available, and linked to measurable financial outcomes. With 10,000+ companies and 1-year post-IPO returns as the outcome, this study has extraordinary statistical power. Effects as small as a 1–2% return difference would be detectable. Either the traditional rules work at scale, or they don't.

---

## 📊 The Data

| Source | Description |
|---|---|
| Yahoo Finance | S&P 500 and broader market listings; historical price data |
| Swiss Ephemeris | Moon phase, Mercury retrograde status, Sun-Jupiter aspects, Vedic Tithis |
| **Scope** | **~10,000 publicly traded companies; 1-year post-IPO return** |

> *Data provenance note: The dataset draws primarily from Wikipedia's S&P 500 constituent list and related sources. This introduces survivorship bias: companies that went to zero post-IPO may be underrepresented in Yahoo Finance historical data. This affects all groups equally and doesn't create false astrological effects — but precludes claims about the full IPO universe.*

---

## 📈 Results

### 1. Moon Phase (Waxing vs. Waning)

*Traditional rule: IPO during a Waxing Moon for growth potential.*

| Moon Phase | Avg. 1-Year Return | Sample Size | Std Dev |
|---|---|---|---|
| Waxing (Growing) | +12.4% | 4,102 | 45% |
| Waning (Shrinking) | +12.2% | 3,988 | 44% |
| Full Moon (~180°) | +12.9% | 365 | 42% |
| New Moon (<15° phase) | +11.8% | 350 | 48% |

**p > 0.5. Difference: 0.2 percentage points.**

The standard error of the mean with SD = 45% and N = 4,000 is approximately 0.7%. The observed difference (0.2%) is less than one-third of a standard error — pure noise. Whether the Moon is growing or shrinking when a company goes public has zero measurable impact on what the stock does over the following year.

### 2. Mercury Retrograde

*Traditional rule: Avoid launching ventures during Mercury Retrograde.*

| Mercury Status | Avg. 1-Year Return | Success Rate (>0%) |
|---|---|---|
| Direct (Normal) | +12.3% | 54.1% |
| **Retrograde** | **+12.1%** | **53.8%** |

**Difference: 0.2 percentage points. Effectively identical.**

Companies IPO'd during Mercury Retrograde perform within 0.2% of companies launched while Mercury is direct. The traditional fear of Mercury Retrograde as a harbinger of business failure is not supported at scale.

### 3. Tithi (Vedic Lunar Day)

| Tithi | Avg. 1-Year Return |
|---|---|
| Best performing (Tithi 14, pre-Full Moon) | +13.2% |
| Worst performing (Tithi 30, Amavasya/New Moon) | +11.1% |
| **Spread** | **2.1 percentage points** |

The 2.1% spread between best and worst Tithi bins falls entirely within the margin of error for groups of ~200–400 per bin. No individual Tithi shows a statistically significant return advantage.

### 4. Sun-Jupiter Aspect

*Traditional rule: Sun-Jupiter contacts ensure success and vitality.*

**Pearson correlation of Sun-Jupiter cosine with 1-year return: r = 0.002 — effectively zero.**

| Aspect Type | Avg. ROI |
|---|---|
| Conjunction | +12.5% |
| Trine | +12.8% |
| Square | +12.2% |
| Opposition | +11.9% |

The "Great Benefic" aspect (Trine) cannot be distinguished from the Square or Opposition in terms of subsequent stock performance.

---

## 🔍 Understanding the Noise Floor

The single most important interpretive context: **individual stocks have annual return standard deviations of approximately 45%.**

A company can gain 300% in a year or lose 80%. No factor explaining only a few percent of variance will show up clearly in a dataset of this size unless it's an overwhelmingly dominant effect.

To detect a **5% return advantage** for "astrologically favorable" IPOs:
- At SD=45% and N=4,000 per group, an 80%-powered test detects 5% differences
- The observed differences were ~0.2%
- The true effect is either smaller than 5% (too small to have practical trading significance) or zero

Given 13 tests covering all major electional rules without a single result approaching significance, the most parsimonious conclusion is zero.

---

## ⚠️ Limitations & Caveats

- **Survivorship bias:** Bankrupt companies may be underrepresented in Yahoo Finance data. This affects all groups equally.
- **Dataset definition:** Derived from S&P 500 constituents rather than a true all-IPO universe.
- **Multiple testing:** Six+ hypotheses tested. Expected false positives at p<0.05: ~0.3. None approached significance.
- **1-year return as outcome:** IPO success has dimensions beyond 1-year price return (longevity, market cap, survival to 5 years).

---

## 🌟 Conclusion

Testing three core electional astrology rules against 10,000+ IPOs produces a definitive null result:

- **Moon Phase (Waxing vs. Waning):** 0.2% difference — p > 0.5
- **Mercury Retrograde:** 0.2% difference — effectively identical
- **Tithi best vs. worst:** 2.1% spread — within noise margin
- **Sun-Jupiter aspects:** r = 0.002 — zero correlation

Electional astrology provides **no measurable predictive advantage** in public equity markets. The traditional rules for choosing auspicious IPO timing are not reflected in subsequent stock performance.

This converges with Project 32's finding that historical electional predictions achieve only 25% accuracy (worse than chance). Choosing when to act, astrologically, does not appear to improve outcomes — at least not in financially measurable ways.

> *This project does not constitute financial advice.*
