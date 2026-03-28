# Project 27: Horary Astrology — The Moon as Oracle

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — What We Asked

Do traditional horary Moon conditions — Void of Course, Via Combusta, and Waxing/Waning phase — correlate with question outcomes across timestamped datasets? Does the ancient rule "Void of Course Moon = nothing will come of the matter" hold up when tested at scale?

---

## 💡 Why This Matters — Horary Is Uniquely Testable

Horary astrology is, in principle, the **most scientifically testable branch of the discipline.**

In natal astrology, the "outcome" — a person's character and life trajectory — is diffuse, subjective, and decades-long. In compatibility astrology, relationship success is multi-factorial. But in horary, the structure is elegantly simple:

- A specific question is asked at a specific time
- The answer is typically binary: Yes/No, Found/Not Found, Will happen/Won't happen
- The outcome is verifiable and often documented contemporaneously

This binary structure is ideal for the kind of frequency statistics that drive empirical astrological research. If the Moon truly encodes the outcome of questions in its position, that signal should appear in outcome rates across large samples of verified charts.

---

## 📊 The Three Moon Conditions

### 1. Void of Course Moon
The Moon makes no further Ptolemaic aspects before leaving its current sign.
**Traditional rule:** "Nothing will come of the matter." Questions asked under a Void Moon produce no result — stagnation, no decision, no change.
**Expected frequency:** ~20–30% of all moments.

### 2. Via Combusta
The Moon falls between 15° Libra and 15° Scorpio.
**Traditional rule:** Fear, instability, unfortunate outcomes. A "burnt path" traversing degrees associated with the fall of the Sun and the debility of the Moon.
**Expected frequency:** ~8% of all moments.

### 3. Moon Phase
**Waxing Moon** (New to Full): growth, increase, beginning.
**Waning Moon** (Full to New): completion, diminishment, endings.

---

## 📊 The Data

| Dataset | Type | N | Outcome Definition |
|---|---|---|---|
| Synthetic control | Random timestamps + random outcomes | 600 | 50/50 random True/False |
| Real IPO data (from Project 24) | Historical | 797 | 1-year return > 0% |
| William Lilly historical horary | Real — verified charts | 10 | Contemporaneously recorded Yes/No |

> *Important caveat: The synthetic control uses randomly assigned question times and outcomes — it verifies the pipeline produces expected baseline statistics, not that horary works. IPO data is a proxy; genuine horary requires a question with a specific binary outcome judged by an astrologer. The Lilly data (N=10) is too small for inference.*

---

## 📈 Results

### A. Synthetic Control: Baseline Verified

Success rates near 50% for most conditions with random outcomes, confirming the pipeline works correctly. The Via Combusta value (32.6%) in the synthetic data is within expected sampling variation for ~48 observations.

### B. Real IPO Data (N = 797): Against Genuine Outcomes

Base rate: **48.7%** of IPOs showed positive 1-year returns.

| Moon Condition | Success Rate | N | Delta vs. Base | Direction vs. Tradition |
|---|---|---|---|---|
| **Via Combusta** | **42.9%** | ~63 | **−5.8%** | ✓ Consistent with tradition |
| **Void of Course** | **53.9%** | ~102 | **+5.2%** | ✗ Contradicts tradition |
| **Waxing Moon** | **50.7%** | ~415 | +2.0% | ✓ Consistent with tradition |
| **Waning Moon** | **46.5%** | ~382 | −2.2% | ✓ Consistent with tradition |

### Via Combusta: The Intriguing Signal

Companies IPO'd when the Moon was in Via Combusta (15° Libra–15° Scorpio) showed a **42.9%** positive-return rate — **5.8 percentage points below** the 49.4% rate outside this zone.

This is the project's most provocative result. The direction exactly matches the traditional rule: outcomes are worse in the "burnt path." But with N=63, the confidence interval is enormous (~30%–55% at 95%), and no multiple testing correction has been applied.

### Void of Course: A Paradox

Void IPOs have a **53.9%** positive-return rate — 5.2 points *above* average, directly contradicting the traditional "nothing will come of the matter" rule.

One astrological interpretation: for free-market "questions" like IPOs, a Void Moon (no planetary interference, no competing agendas) may mean the market finds its level cleanly. The absence of interference could be beneficial. But more probably, this is sampling variation in ~102 observations.

### Waxing/Waning: Weak Directional Agreement

Waxing IPOs outperformed Waning IPOs by 4.2 percentage points (50.7% vs. 46.5%), in the direction tradition predicts. Not statistically significant (p ≈ 0.26), but directionally consistent.

---

## 🔬 The Right Study Design

The ideal horary study would:

1. **Use William Lilly's full archive as the primary dataset** — *Christian Astrology* (1647) contains hundreds of detailed horary judgments with question times and documented outcomes
2. **Digitize systematically** — the Lilly archive is the most verified horary dataset in existence
3. **Define outcomes precisely** — "the querent received the money: yes/no" is cleaner than "the stock went up"
4. **Pre-register the analysis** — specify which Moon conditions will be tested at what significance threshold, before looking at the data
5. **Have outcome recorded by someone other than the judging astrologer**

With 500 verified horary charts, the Void of Course test would have adequate power to detect a 10% success rate difference.

---

## ⚠️ Limitations & Caveats

- **IPO data is not real horary.** Genuine horary requires a specific question with a defined binary outcome judged by an astrologer. IPO "questions" are a proxy at best.
- **Small subgroup sizes:** N = 63 Via Combusta observations cannot support the effect size shown.
- **Multiple testing:** Three conditions × two datasets = six tests. None individually significant at corrected thresholds.
- **Market conditions:** A cluster of Via Combusta IPOs during a bear market would appear to confirm the rule for entirely non-astrological reasons.

---

## 🌟 Conclusion

This project is explicitly a **pilot and methodology chapter** rather than a completed empirical study.

1. **Horary is uniquely testable** — binary outcomes, specific timestamps, verifiable results
2. **The analysis pipeline works** — Moon conditions auto-calculated for any timestamp
3. **Via Combusta shows a possible signal** (−5.8% vs. base rate, N=63) — but preliminary only
4. **Void of Course contradicts tradition** (+5.2% above base) — requires replication before interpretation
5. **The Lilly archive is the right data source** — has not yet been systematically digitized for statistical analysis

Horary astrology presents the cleanest empirical test available in this field. That test has not yet been rigorously performed. This chapter outlines precisely how to do it.
