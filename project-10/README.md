# Project 10: Synastry and Relationship Longevity

> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Source:** [bigastrologybook.com](https://bigastrologybook.com)

---

## 🌟 Overview — What We Asked

Does astrological synastry — comparing two birth charts to assess compatibility — predict whether a romantic relationship will endure? Do specific inter-chart planetary alignments distinguish long-lasting marriages from short ones?

---

## 💡 Why This Matters

Compatibility is arguably astrology's most commercially significant claim. Millions of people consult astrologers before major relationships, use apps that calculate compatibility percentages, and organize their romantic lives around synastry charts. If any astrological analysis has practical stakes, it's this one.

This project tests the claim at scale: 2,722 couples from Wikidata, with verified birth dates and relationship timelines, analyzed with cosine-similarity metrics across 100+ inter-chart planetary combinations. The answer reveals something important about which aspects of compatibility astrology might be measuring — and which parts are measuring something else entirely.

---

## 📊 The Data

| Parameter | Value |
|---|---|
| Source | Wikidata (SPARQL query for spouse pairs with verified birth dates) |
| Valid couples analyzed | **2,722** |
| Duration metric | Relationship duration (marriage date to divorce or death) |
| Long-term group | Top 25%: > **54.4 years** |
| Short-term group | Bottom 25%: < **8.1 years** |

> *Data quality note: Wikidata relationship data has known issues. Date precision varies (some entries list year only), and "relationship end" conflates divorce with death of partner — two demographically distinct events. Survival-censored analysis would be more rigorous.*

Rather than traditional binary aspect orbs, the analysis used **cosine similarity** of inter-chart planetary angles — a continuous measure:

| Cosine Value | Aspect |
|---|---|
| **+1.0** | Conjunction (0°) |
| **0.0** | Square (90°) |
| **−1.0** | Opposition (180°) |

No prior assumptions were made about which aspects are "favorable" — the analysis was fully agnostic.

---

## 📈 Results

### ⚠️ Critical First: The Demographic Artifacts

The strongest signals in this dataset are **not astrological**. They are mathematical consequences of human mortality combined with planetary orbital periods.

To be married for 60 years, both partners must survive 60 years from the wedding date. Couples with similar outer planet positions (the same generational positions) are close in age. Close-in-age couples are more likely to both survive to a golden anniversary. This creates a **survival bias** that inflates the apparent predictive power of outer planet conjunctions.

| Synastry Pair | Correlation (r) | Status |
|---|---|---|
| **Pluto-Pluto** | **+0.15** | **Demographic artifact — discard** |
| **Uranus-Uranus** | **+0.14** | **Demographic artifact — discard** |
| Uranus-Pluto | −0.14 | Artifact (generational contrast) |
| Neptune-Pluto | +0.139 | Artifact (age matching) |

A researcher who claimed "Pluto-Pluto conjunction predicts lasting marriages" would be publishing a demographic finding about age-similar couples, not an astrological one. These results must be set aside before any astrological interpretation.

### The Mars-Mars Signal (After Removing Artifacts)

After discarding all outer-planet signals:

| Synastry Pair | Mean Cosine Diff (Long − Short) | p-value | Interpretation |
|---|---|---|---|
| **Mars-Mars** | **+0.133** | **0.0006** | Long-term couples share Mars sign more often |

The Mars-Mars result: couples in the long-duration group showed average cosine similarity 0.133 higher than short-duration couples. Long-term couples are more likely to share a Mars sign (conjunction tendency) than short-term couples.

**Why Mars?** Mars governs action style, libido, conflict rhythm, and how anger is expressed and resolved. When one partner escalates (Mars in Aries) while the other withdraws (Mars in Pisces), the *asymmetry* in conflict rhythm accumulates friction. When both partners share the same Mars pattern — even if individually intense — the *synchronicity* allows repair after conflict. "Eros fades, but friction kills" as a relationship dynamic.

> *Statistical caveat: The Bonferroni-corrected threshold for 100 planetary pairs × multiple aspects is approximately p < 0.0005. Mars-Mars at p=0.0006 barely misses this threshold. It is highly suggestive — not yet confirmed by strict multiple-testing standards.*

### The Love Planets: Null Results

| Synastry Pair | Correlation | p-value |
|---|---|---|
| Venus-Mars | ~0 | > 0.05 |
| Sun-Moon | ~0 | > 0.05 |
| Venus-Venus | ~0 | > 0.05 |
| Moon-Moon | ~0 | > 0.05 |

These null results may be the most practically interesting finding. Romantic chemistry — commonly attributed to Venus-Mars and Sun-Moon — does not predict whether a relationship lasts 50 years. Venus may govern who *attracts* us; Mars may govern whether we can *tolerate each other* decade after decade.

---

## 🔍 What the Numbers Mean

The data reveals a two-tier structure in synastry analysis:

**Tier 1 — Demographics dominate:** Outer planet conjunctions appear to predict marriage duration, but this is entirely explained by age similarity and survival statistics. Recognizing this artifact is the single most important methodological contribution of this project.

**Tier 2 — Mars emerges:** The one personal-planet signal, Mars-Mars conjunction, points toward *conflict-style compatibility* as the driver of long-term relationship success — not romantic chemistry (Venus-Mars, Sun-Moon, Moon-Moon), but the mundane day-to-day friction management between two people.

This is a hypothesis worth taking seriously. Relationships end not when the romantic spark fades (that's expected), but when conflict becomes irresolvable. Two people who fight in the same rhythm can make up in the same rhythm. Two people whose Mars energies are fundamentally out of sync may accumulate damage that doesn't repair.

---

## ⚠️ Limitations & Caveats

- **Survival analysis not implemented:** Partner deaths should be treated as censored events (Cox proportional hazards), not counted as "relationship failures." This inflates duration for couples where one partner died young.
- **Wikidata quality:** Relationship dates for historical figures are often approximate or conflated.
- **Selection bias:** Couples notable enough for Wikidata may overrepresent long marriages (marital stability as reputation).
- **Quartile split:** Comparing only top and bottom 25% inflates effect sizes vs. continuous regression.

---

## 🌟 Conclusion

Testing 2,722 couples' synastry against relationship duration reveals a clear hierarchy:

1. **Outer planet conjunctions predict duration** — but as a demographic artifact of age-similarity and mortality, not astrology
2. **Mars-Mars Conjunction** (p=0.0006, diff +0.133) is the strongest personal-planet signal — shared action/conflict style may support long-term relationship survival
3. **Venus, Moon, Sun connections** — astrology's traditional compatibility pillars — show no statistical association with how long relationships last

Venus may capture who we fall for. Mars may capture who we can build a life with. The data, at least tentatively, supports that distinction.
