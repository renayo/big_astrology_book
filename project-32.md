# Project 32: Historical Astrological Predictions — Accuracy Analysis

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

When astrologers have made specific, documented predictions about future events, how accurate have those predictions been? Is their success rate statistically distinguishable from a coin flip?

---

## 💡 Why This Matters

All the statistical analysis in the world means less if practitioners can't actually make correct predictions. This project takes the most direct possible approach: collect documented historical predictions, evaluate their outcomes, and count.

The dataset spans 1555 to 2022 — four and a half centuries of recorded astrological prediction. If any astrologer, in any era, with any technique, has demonstrated above-chance predictive accuracy at a documented scale, it should show up here.

---

## 📊 The Dataset: 39 Famous Predictions

39 predictions drawn from the historical record — mundane, personal, financial, and electional predictions from 1555 to 2022. Each rated as **Success** or **Failure** against available historical records.

Sample entries:

| Predictor | Made | Target | Event | Result |
|---|---|---|---|---|
| William Lilly | 1651 | 1666 | Great Fire of London | ✓ Success |
| William Lilly | 1651 | 1665 | Great Plague of London | ✓ Success |
| Nostradamus | 1555 | 1789 | French Revolution (vague) | ✓ Success |
| Nostradamus | 1555 | 1999 | "King of Terror from Sky" | ✗ Failure |
| Jeane Dixon | 1956 | 1960 | Democrats win election | ✗ Failure |
| Jeane Dixon | 1956 | 1963 | President dies in office | ✓ Success |
| Jeane Dixon | 1958 | 1958 | World War III | ✗ Failure |
| Evangeline Adams | 1914 | 1917 | US enters the War | ✓ Success |
| André Barbault | 1974 | 1989 | Collapse of Soviet Union | ✓ Success |
| André Barbault | 2011 | 2020 | Great Pandemic | ✓ Success |
| Joan Quigley | 1985 | 1986 | Challenger Disaster (warned Reagan) | ✓ Success |
| Susan Miller | 2016 | 2016 | Hillary Clinton wins election | ✗ Failure |
| Various | 2012 | 2012 | Mayan Apocalypse | ✗ Failure |
| Cheiro (Count Hamon) | 1926 | 1929 | Market Crash | ✓ Success |
| John Gribbin | 1974 | 1982 | Jupiter Effect Earthquakes | ✗ Failure |
| Elizabeth Teissier | 1999 | 1999 | Solar Eclipse Disaster | ✗ Failure |
| Indian Astrologers | 1962 | 1962 | World Doom (8-planet cluster) | ✗ Failure |

---

## 📈 Results

### Overall Accuracy

| Metric | Value |
|---|---|
| **Total predictions** | 39 |
| **Successes** | 22 |
| **Failures** | 17 |
| **Overall accuracy** | **56.4%** |
| **Binomial test p-value** | **0.2612** |

With 22 successes out of 39, overall accuracy is 56.4%. The binomial test (testing whether 22/39 could arise by chance if the true success rate were 50%) yields p = 0.2612 — far from significance.

**Historical astrological predictions, in aggregate, are not statistically distinguishable from a coin flip.**

### Accuracy by Category

| Category | N | Successes | Accuracy |
|---|---|---|---|
| Personal | 1 | 1 | 100% |
| Financial | 5 | 4 | **80%** |
| Mundane | 25 | 15 | 60% |
| **Electional** | **8** | **2** | **25%** |

**Electional astrology (25%, N=8): Worse than chance.** The practical application of astrology to choose auspicious times for actions performs at 25% — half of what random guessing would produce. This directly convergences with Project 24's null result on IPO timing: choosing *when* to act, astrologically, does not improve outcomes.

Financial predictions (80%, N=5) look impressive but N=5 is meaningless — one different outcome drops this to 60%.

### Accuracy by Time Horizon

| Horizon | N | Successes | Accuracy |
|---|---|---|---|
| Short term (< 2 years) | 20 | 9 | **45%** |
| Medium (2–10 years) | 12 | 7 | 58.3% |
| Long term (> 10 years) | 7 | 6 | **85.7%** |

The reversal — short-term predictions *below* chance, long-term predictions appearing excellent — is the most intellectually interesting finding in the dataset.

**The likely explanation:** Very long-range predictions are necessarily vague. Nostradamus writing in 1555 about "upheaval in Europe leading to a new order" in 1789 has enormous latitude for retrospective fitting to almost any major historical event. Vague statements that can match many outcomes appear prophetic when any matching event occurs.

Short-term predictions may underperform chance because evaluation is stricter for near-term forecasts (a specific election outcome is either right or wrong), while long-term evaluations can be generous ("close enough" becomes success).

---

## 🔍 The Nostradamus Problem

Nostradamus presents a methodological challenge that cannot be fully resolved. His quatrains are written in deliberately ambiguous Old French filled with metaphor and incomplete syntax. The "success" count for Nostradamus depends entirely on the interpreter's willingness to match vague imagery to specific events.

Including Nostradamus in a success/failure framework introduces subjective judgment at the foundation of the analysis. This is an inherent limitation of historical prediction research when Nostradamus is included — not a criticism of this project specifically.

---

## ⚠️ Why This Study Is Underpowered

N=39 cannot detect a genuine moderate effect. To detect 65% accuracy at 80% statistical power requires **N ≈ 46 predictions**. N=39 can only reliably detect accuracy above approximately **67%** — a high bar.

This means the study genuinely cannot distinguish between "astrologers predict at random" and "astrologers predict at 55–65% accuracy." The null result (p=0.26) is consistent with modest genuine predictive skill that sample size cannot resolve.

Selection bias further complicates: the 39 predictions were selected from the historical record because they are *famous* — either spectacular successes (Lilly's Great Fire) or spectacular failures (Mayan Apocalypse). This does not represent average practice.

---

## 🌟 Conclusion

39 famous astrological predictions from 1555 to 2022 achieve 56.4% overall accuracy — not statistically distinguishable from a coin flip (p=0.26).

The most interesting sub-findings:
1. **Electional astrology: 25%** — worse than random, convergent with Project 24
2. **Long-term predictions appear excellent (85.7%)** — most likely reflecting vagueness that allows retrospective fitting
3. **Short-term predictions underperform chance (45%)** — stricter near-term evaluation criteria

The null result should be interpreted carefully: this study is underpowered (N=39), biased toward memorable predictions, and relies on retrospective subjective evaluation. It neither confirms nor convincingly refutes astrological predictive ability.

**The appropriate conclusion:** A large-scale, pre-registered prediction study — where astrologers submit specific, falsifiable forecasts before events occur, with outcomes coded by independent evaluators — is needed to settle this question scientifically. No such study currently exists in the published literature.
