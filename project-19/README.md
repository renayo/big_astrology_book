# Project 19: Mundane Astrology — Specific Aspect Claims

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com/2/research](https://bigastrologybook.com/2/research)

---

## 🌟 Overview — Status: Incomplete

This project collected data and established a methodology but did not complete the full statistical analysis before archiving. What follows presents the completed methodology, a crucial finding about base rates, and partial results — with full transparency about what was and wasn't finished.

---

## 💡 Why This Matters: The Traditional Claims

Mundane astrology assigns specific planetary pair aspects to specific types of worldly events. The most cited:

| Aspect | Traditional Claim |
|---|---|
| Saturn-Pluto conjunction/opposition | Wars, destruction, power struggles, collapse |
| Uranus-Pluto conjunction/square | Revolutions, mass social upheaval |
| Saturn-Neptune conjunction/opposition | Epidemics, collective delusion, spiritual crisis |
| Jupiter-Uranus conjunction | Scientific breakthroughs, sudden expansion |
| Saturn-Uranus opposition | Tension between old and new, structural crisis |

These claims are repeatedly "confirmed" by post-hoc pattern matching. The famous examples are compelling on the surface:

- WWI (1914): Saturn opposite Pluto
- WWII (1939): Saturn conjunct Pluto
- COVID-19 (2020): Saturn conjunct Pluto

But there is a critical problem lurking in those examples.

---

## 🔬 The Base Rate Problem — The Most Important Finding in This Chapter

*This is the most important analytical insight in this project, and it applies to all mundane astrology claims.*

The question that never gets asked: **how often does Saturn conjunct or oppose Pluto without a catastrophic war or pandemic?**

### Saturn-Pluto Aspects: ~48% Baseline Coverage

Outer planet aspects do not occur briefly. They are continuously active for *years* at a time. Using standard orbs (8° for conjunction/opposition):

- Saturn-Pluto conjunction recurs every ~33 years and stays in orb for 2–4 years
- Saturn-Pluto opposition similarly stays in orb for 2–4 years
- Together with squares, major Saturn-Pluto aspects cover a substantial fraction of any century

**Estimated coverage: Major outer planet hard aspects between any given pair are active roughly 48% of the time across a century.**

Under these conditions, it would be remarkable if major disasters did *not* cluster around Saturn-Pluto aspects. If you flip a coin that lands heads 48% of the time, and your coin happened to land heads during WWI, WWII, and COVID — that's not evidence the coin predicted the wars. That's a coin flip that you only notice when something bad happens.

**The null hypothesis for mundane astrology is not "no correlation." It is "correlation no better than the 48% base rate."** Any valid test must compare the aspect rate during events to the 48% background — not to zero.

### The Selection Bias Problem

The famous examples illustrate a second flaw: **selective reporting**.

Saturn conjunct Pluto occurred in 1914, 1947, 1982, and 2020:
- 1914: WWI begins ✓ (hit)
- 1947: Post-WWII settlement ✓ (hit, with flexibility)
- 1982: No world war ✗ (miss — Falklands War only)
- 2020: COVID-19 ✓ (hit)

Saturn opposed Pluto in 1901, 1931, 1965, and 2001:
- 1901: No obvious hit ✗
- 1931: Great Depression era ✓
- 1965: Vietnam escalating ✓ (stretch)
- 2001: 9/11 ✓ (hit)

We remember the hits. We forget the misses. A proper statistical test must count both.

---

## 📊 The Data and Methods

### Event Collection Target

500+ historical events, 1700–2025, across six categories:
- Wars and military conflicts
- Revolutions and regime changes
- Economic crises and crashes
- Natural disasters (major)
- Political changes (coups, elections, collapses)
- Technological milestones

Each event coded by: date, type, description, verified source.

### Aspect Calculation

For each event date, compute whether each of the 5 traditional aspect-event pairs is active (within standard orbs). Control group: 5,000+ random dates in the same period.

### Statistical Tests Planned (but not completed)

- **Chi-square test:** Does the proportion of events during active aspects exceed the 48% background rate?
- **Permutation test:** Shuffle event dates 5,000 times; compare actual aspect counts to shuffled distribution
- **Fisher's exact test:** For specific aspect-event category pairs (Saturn-Pluto during wars)

---

## 📈 Partial Results

The backup materials contain the research framework and base-rate analysis. Specific chi-square statistics for the major aspect-event pair comparisons were not completed.

**The one substantive finding:** Saturn-Pluto hard aspects are active approximately 48% of the time across 1700–2025. This substantially reduces the evidential weight of any single "hit."

### What Contrast with Project 17 Tells Us

Project 17 (aggregate planetary clustering, p < 0.0001) and Project 19 (specific named pairs, incomplete but weaker) together suggest:

- *Something planetary* correlates with historical disruption — but it may be diffuse
- Aggregate clustering captures a real signal that specific pair-wise analysis misses
- Traditional mundane astrology's specific claims (Saturn-Pluto = wars) may overfit the most memorable events while missing the underlying whole-system pattern

---

## ⚠️ What Remains Incomplete

The following analyses were planned but not completed:

- ☐ Chi-square test for each of the 5 traditional aspect-event claims
- ☐ Permutation test comparing actual to shuffled event dates
- ☐ Category breakdown: do wars specifically cluster at Saturn-Pluto above the 48% base rate?
- ☐ Full 500+ event CSV with sourcing documentation

---

## 🌟 Conclusion

The most important result of this project is not a chi-square statistic — it's the base rate calculation.

**Outer planet major aspects cover ~48% of any historical century.** Any mundane astrology study that does not correct for this background rate is measuring only that remarkable things happen during unremarkable astronomical conditions.

Once the base rate is properly accounted for, the question becomes: do wars, revolutions, and epidemics happen *more* during specific aspects than the already-elevated 48% background predicts? That test requires the complete event list, correct null hypothesis specification, and the statistical rigor that this project's partial results don't yet provide.

The tradition's famous hits — WWI, WWII, COVID — survive scrutiny as examples but not as statistical evidence. The misses must be counted equally. Until the complete analysis is performed, the specific claims of traditional mundane astrology remain unverified rather than confirmed or refuted.
