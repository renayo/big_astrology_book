# Project 05: Mercury Retrograde — Real Effect or Perception Bias?

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Does Mercury retrograde actually correlate with increased technology failures, travel disruptions, and communication breakdowns? Or is the widespread experience of retrograde chaos a product of perception bias, amplified by calendar confounds that nobody bothers to control for?

---

## 💡 Why This Matters

Mercury retrograde is astrology's most culturally pervasive claim in the internet age. It has jumped from astrology apps into mainstream conversation — office workers blame it for email mix-ups, travelers for flight delays, couples for bad timing. It is probably the single astrological claim that most people who don't practice astrology have heard of.

It is also, in principle, one of the most testable. Mercury's retrograde periods are precisely calculable — the planet appears to reverse direction from Earth's perspective roughly three times per year, for about three weeks each time. If this apparent reversal genuinely correlates with terrestrial disruption, that correlation should appear in incident data.

The problem — and it's a substantial one — is that almost every naive test of this will produce a spurious positive result. Not because Mercury causes anything. Because of when retrograde periods fall in the calendar.

---

## ⚠️ Critical Upfront Disclosure

**The travel and incident data in this study is synthetic.** It was generated algorithmically to model realistic seasonal patterns, day-of-week effects, holiday spikes, and long-term trends based on Bureau of Transportation Statistics averages — but it is not actual flight delay or technology outage data. The social media corpus (20,000 posts) is also simulated.

**What is real:** Mercury's retrograde periods, calculated precisely via Swiss Ephemeris. The astronomical timeline is exact; what it is tested against here is illustrative.

This matters for how to read the results: the findings demonstrate what a rigorous methodology *would* find and establish a framework for testing with real data. They do not constitute empirical evidence about actual Mercury retrograde effects. The methodology is the contribution.

---

## 📊 The Calendar Confound Problem

Why does every naive Mercury retrograde study find a spurious positive? Because of this: Mercury retrogrades roughly three times per year, each lasting about three weeks. The timing:

- **Late November/early December retrograde** — overlaps directly with Thanksgiving and the beginning of holiday travel season, the two most disruption-prone weeks of the year
- **June/July retrograde** — peak summer travel season, when delays are highest for purely terrestrial reasons
- **Weekly rhythms** — Friday and Sunday have elevated incident rates year-round; if a retrograde period contains more of these high-risk days, it will appear more incident-prone

Anyone who has experienced a "chaotic" Mercury retrograde and later noticed it coincided with the holiday season is experiencing exactly this confound. The chaos was coming regardless. The retrograde was just along for the ride.

**The detrending decomposition:**
```
Anomaly Ratio = Observed ÷ (Trend × Season × Day-of-Week × Holiday)
```

Strip these four layers, and what remains is the pure "anomaly" — how much a day differs from what the calendar alone would predict. Only *then* is it valid to compare retrograde vs. direct days.

---

## 📊 The Data

| Component | Source | Type |
|---|---|---|
| Mercury retrograde dates | Swiss Ephemeris, 2001–2024 | **Real** — precise to <0.01° |
| Daily travel/incident data | Synthetic — modeled on BTS averages | Illustrative |
| Social media corpus | 20,000 synthetic posts | Illustrative |

**Total retrograde periods:** ~72 over 24 years. 1,686 retrograde days out of 8,766 total — Mercury is in apparent retrograde roughly 19.2% of the time.

---

## 🔬 Method

**Multiplicative time-series decomposition:** Raw daily incident counts decomposed to remove trend, seasonality, day-of-week, and holiday effects. Residual Anomaly Ratio is what gets compared to Mercury's status.

**Bayesian inference:** Rather than a single p-value, continuously update belief in the "retrograde hypothesis" as data accumulates. Prior: 50/50 (agnostic). Compare how well "retrograde causes incidents" fits the data vs. the null model.

**NLP attribution analysis:** The synthetic social media corpus distinguishes between objective complaints ("WiFi is down") and explicit astrological attribution ("Mercury is retrograde"). This separation is what makes the bias analysis meaningful — you need to know not just whether complaints occur during retrograde, but whether people are *blaming the planet* specifically.

---

## 📈 Results

### After Detrending: A Statistical Null

| Condition | Days (N) | Mean Anomaly Ratio | Deviation |
|---|---|---|---|
| Mercury Direct | 7,080 | 0.9995 | −0.05% |
| **Mercury Retrograde** | **1,686** | **1.0020** | **+0.20%** |
| **Difference** | | | **0.25%** |
| **T-test p-value** | | | **0.21 — not significant** |

After removing the calendar confounds, the difference between retrograde and direct periods is **0.25%** — noise. Once you strip the Christmas travel chaos, the summer peak, and the weekend spikes, Mercury retrograde adds nothing.

This is the finding that matters: raw incident data almost certainly shows elevated incidents during retrograde periods. But that elevation is fully explained by *when* retrogrades fall in the calendar, not by Mercury's motion.

### The Bayesian Update: The Hypothesis Loses Ground

| Parameter | Value |
|---|---|
| Prior P(retrograde is real) | 0.500 |
| Bayes Factor | **0.8324** |
| Posterior P(retrograde is real \| data) | **0.454** |

A Bayes Factor below 1.0 means the data provides evidence *against* the retrograde hypothesis. Not strong evidence — the data is noisy — but in the wrong direction entirely for the hypothesis to survive. A rational agent who started 50/50 and observed this data should update their belief in Mercury retrograde's causal role *downward*, from 50% to 45%.

### The Confirmation Bias Mechanism

The cognitive machinery that sustains the Mercury retrograde belief is well understood:

**Selective encoding:** During retrograde periods, people are primed to notice disruptions because they've been warned to expect them. The WiFi outage that gets shrugged off in April becomes "classic Mercury retrograde" in November. The disruption is the same; the cognitive framework changes the encoding.

**Attribution through calendar confound:** The observer doesn't detrend their own experience. The late-December travel chaos is attributed to Mercury because Mercury is retrograde — but it would have happened anyway. The planet is blame-receiving credit for what the calendar was always going to produce.

The analysis frames this precisely: *"The fault, dear Brutus, is not in our stars, but in our calendars."* Once you know when Mercury retrogrades, you can predict exactly which events will be blamed on it — not because Mercury caused them, but because retrogrades reliably fall during the calendar's most disruption-prone windows.

---

## ⚠️ Limitations & Caveats

**The data is not real.** This is the primary limitation and cannot be overstated. The synthetic data demonstrates what rigorous methodology looks like; it does not produce empirical conclusions about actual Mercury retrograde effects.

**What a definitive study needs:**
1. Real incident data — FAA flight delay records, Downdetector tech outage logs, or insurance claim databases
2. Real social media data with timestamps for authentic attribution analysis
3. Pre-registration of the detrending methodology before analysis

Applied to real data with this methodology, the result would either confirm the null (most likely) or reveal a genuine residual signal — which would itself be extraordinary and worth pursuing.

---

## 🌟 Conclusion

After removing the calendar confounds that plague naive retrograde studies, Mercury retrograde's association with disruption vanishes. The detrended anomaly ratio during retrograde periods (1.002) is statistically indistinguishable from direct periods (0.9995). The Bayesian posterior for the retrograde hypothesis *decreases* on exposure to the data.

The more important finding is *why* the perception persists: Mercury retrograde falls during the calendar's most naturally disruptive periods, and human memory is wired to notice and remember disruptions that have a ready explanation. The planet is innocent. The calendar is the culprit.

The methodology to test this properly with real data is fully documented here. Applying it to genuine flight delay or outage records would make this a definitive empirical result. Until then, this stands as a framework paper — showing what an honest test looks like, and what it's likely to find.
