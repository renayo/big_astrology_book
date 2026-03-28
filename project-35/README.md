# Project 35: Professional Clustering — Unsupervised Learning

> **Source:** [bigastrologybook.com/project-35](https://bigastrologybook.com/project-35/)
> **Archive Date:** 2026-03-21
> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Dataset:** 766 verified professionals from Astro-Databank across 8 career categories; K-means, HDBSCAN, GMM, Spectral Clustering on planetary longitudes and cosine interaction features

---

## Research Question

If astrology contains genuine information about professional vocation — if the planetary configurations at birth shape what a person becomes — then professionals in the same field should resemble each other astrologically more than they resemble professionals in other fields. An unsupervised algorithm given only birth chart data should, in theory, be able to discover these groupings without being told which charts belong to which professions.

This project tests that premise directly: do birth charts cluster by profession in high-dimensional planetary space?

## Hypothesis

The null hypothesis is that they do not — that professionals in any given field do not form a detectable cluster in chart space, and that the clustering algorithms will produce groupings that bear no relationship to actual professional categories. This is the honest starting assumption for rigorous inquiry.

---

## Why Unsupervised Learning Is the "Fair" Test

Before examining the results, it is worth dwelling on why this particular methodology deserves special attention among the book's many approaches to the profession question.

Most of the analyses in this book are *supervised* — they start with labeled data (this person is a scientist, that person is an artist), and ask whether a model can learn to predict the label from the chart features. Supervised learning is sensitive to weak signals; given enough examples, even tiny correlations can produce statistically detectable patterns. The work in Project 33 found that Writers cluster around weak-Mars placements (p=0.011) and Filmmakers around strong-Sun charts (p=0.027). Project 20 identified Mars in Libra and Moon in Scorpio as frequency peaks in celebrity charts. These findings are real. But they describe small, specific correlations that don't necessarily imply that birth charts as a whole organize themselves around professional identity.

Unsupervised learning asks a fundamentally different question. It removes the labels entirely and simply asks: *do these charts naturally group together?* If the answer is yes — if physicians' charts spontaneously cluster apart from athletes' charts, if musicians' planetary configurations form a natural cloud in feature space — that would be far stronger evidence for astrological influence than any supervised result. It would mean the structure is real enough that an algorithm can find it without being shown what to look for.

This is the "fair" test because it grants astrology no interpretive assistance. The algorithm cannot cherry-pick which planets to emphasize, cannot lean on culturally transmitted associations between Saturn and discipline or Venus and beauty. It receives only numbers and is asked whether those numbers contain hidden structure that corresponds to human categories of meaning.

The answer, across six different algorithms applied to 766 professionals, is an unambiguous no.

---

## Data

| Field | Detail |
|---|---|
| **Sample** | 766 verified professionals (deduplicated from 771 initial entries) |
| **Source** | Astro-Databank (birth dates verified for biographical subjects) |
| **Professional categories** | 8: Entertainer, Scientist, Athlete, Writer, Musician, Artist, Politician, Business |
| **Feature Set 1** | 7 planetary longitudes (Sun through Saturn, 0–360°) |
| **Feature Set 2** | 66 pairwise cosine interactions (all pairs of 12 bodies) |
| **Dimensionality reduction** | PCA (49% variance in 2 components), t-SNE, UMAP |
| **Cluster algorithms** | K-means, HDBSCAN, GMM, Spectral, Agglomerative, DBSCAN |

### Sample Distribution

| Profession | Count | Percentage |
|---|---|---|
| Entertainer | 130 | 17.0% |
| Scientist | 115 | 15.0% |
| Athlete | 115 | 15.0% |
| Writer | 104 | 13.6% |
| Musician | 91 | 11.9% |
| Artist | 74 | 9.7% |
| Politician | 70 | 9.1% |
| Business | 67 | 8.7% |
| **TOTAL** | **766** | **100%** |

---

## Results

### Phase 1: K-Means and Hierarchical Clustering on Raw Planetary Positions

The initial analysis used K-means and agglomerative hierarchical clustering on the raw planetary longitude coordinates (converted to continuous 0–360° values for Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn). The number of clusters was varied from K=2 to K=8 and validated via Silhouette Score — a measure of how well-separated the resulting clusters are (scores above 0.5 indicate meaningful structure; scores below 0.25 indicate near-random partitioning).

| K (clusters) | Silhouette Score | Interpretation |
|---|---|---|
| 2 | 0.222 | Best — still weak |
| 3 | 0.169 | Poor separation |
| 4 | 0.147 | Poor separation |
| 5 | 0.147 | Poor separation |
| 6 | 0.145 | Poor separation |
| 7 | 0.140 | Poor separation |
| 8 | 0.141 | Poor separation |

The maximum Silhouette Score of 0.222 is achieved with just two clusters — essentially the algorithm splitting the dataset in half. Even this best case falls well below the 0.5 threshold for meaningful clustering. More revealing still, when those clusters are cross-tabulated against actual profession:

| Test | Statistic | p-value | Result |
|---|---|---|---|
| K-Means (K=2) vs. Profession | χ² = 8.69 | p = 0.276 | Not significant |
| Hierarchical (K=2) vs. Profession | χ² = 5.25 | p = 0.630 | Not significant |
| K-Means (K=8, matched) vs. Profession | χ² = 36.08 | p = 0.915 | Not significant |

The Adjusted Rand Index — the gold-standard measure of clustering alignment — tells the same story:

| Configuration | Adjusted Rand Index | Cramér's V |
|---|---|---|
| K-Means (optimal) | 0.0009 | 0.107 |
| Hierarchical (K=2) | −0.0012 | — |
| K-Means (K=8 matched) | −0.0015 | 0.082 |

An ARI of zero means the clustering is no better than random assignment. Negative values mean it is literally worse than random. Cramér's V of 0.082 indicates negligible association. The profession distribution across eight K-means clusters shows every profession present in roughly equal proportions in every cluster — a perfectly undifferentiated mixture:

| Profession | C0 | C1 | C2 | C3 | C4 | C5 | C6 | C7 |
|---|---|---|---|---|---|---|---|---|
| Artist | 7 | 13 | 7 | 7 | 10 | 13 | 9 | 8 |
| Athlete | 13 | 13 | 7 | 11 | 16 | 22 | 19 | 14 |
| Business | 6 | 10 | 8 | 7 | 8 | 9 | 10 | 9 |
| Entertainer | 16 | 16 | 12 | 6 | 22 | 15 | 23 | 20 |
| Musician | 13 | 13 | 8 | 8 | 10 | 19 | 9 | 11 |
| Politician | 7 | 9 | 13 | 4 | 7 | 8 | 13 | 9 |
| Scientist | 15 | 18 | 10 | 7 | 19 | 17 | 21 | 8 |
| Writer | 10 | 13 | 16 | 10 | 13 | 18 | 11 | 13 |

This is what randomness looks like. There is no cluster that is predominantly musicians, no cluster populated mainly by athletes. The numbers vary somewhat, as random fluctuations always will, but none of the variations approach significance.

### Phase 2: Cosine Interaction Clustering — Testing Aspect Geometry

The second analysis phase switched from raw planetary positions to the 66 pairwise cosine interactions — the cosine of the angular difference between every pair of the twelve main celestial bodies. This feature set encodes the *relational geometry* of the chart: how conjunct or opposed each planet is to every other planet. It effectively asks not "where are the planets?" but "what aspects do they make?"

Testing both Tropical and Vedic (sidereal) zodiac systems:

| System | Adjusted Rand Index |
|---|---|
| Tropical (pairwise cosines) | 0.0386 |
| Vedic/Sidereal (pairwise cosines) | 0.0355 |
| Cosine interactions (zodiac-invariant) | 0.0124 |

These values are technically higher than the Phase 1 results, but all remain functionally zero — no system of astrological features produced clusters that meaningfully corresponded to professional categories. Notably, the zodiac-invariant interaction score (0.0124) is the weakest of the three, suggesting that even the small amount of residual signal in the Tropical and Vedic results may derive from generational cohort effects (different professionals born in different eras having different outer planet configurations) rather than from genuine astrological structuring.

### Phase 3: Advanced Algorithms — Exhausting the Hypothesis Space

The third phase expanded to a full battery of algorithms capable of detecting non-spherical, overlapping, or density-based clusters that K-means would miss. The input was the 66-dimensional cosine feature space, reduced via PCA to the number of components preserving 95% of variance:

| Algorithm | Adjusted Rand Index | Interpretation |
|---|---|---|
| Gaussian Mixture Models (GMM) | 0.009 | Near zero |
| Spectral Clustering | 0.004 | Near zero |
| Agglomerative (Ward linkage) | 0.006 | Near zero |
| DBSCAN | −0.000 | Found only noise |

DBSCAN — a density-based algorithm that identifies high-density regions in feature space — classified essentially all points as noise, meaning the data has no regions of elevated planetary density at all. The GMM, which can detect probabilistic overlapping clusters with ellipsoidal shapes (more flexible than K-means's spherical assumption), produced an ARI of 0.009. Spectral Clustering, which maps data onto a graph manifold and is capable of finding arbitrarily shaped clusters, managed 0.004.

These results collectively exhaust the methodological hypothesis space. K-means assumes spherical clusters; GMM assumes ellipsoidal; Spectral assumes manifold structure; DBSCAN assumes arbitrary density shapes; Agglomerative assumes hierarchical tree structure. All of them, applied to the same data, produced the same answer: nothing.

---

## What Absence of Structure Means

The chart space of 766 professionals is, in the language of machine learning, *flat*. PCA retains only 49% of variance in two dimensions, and even the full high-dimensional space offers no detectable concentrations of professionals with shared astrological features.

What would a positive result have required? It would require that, for instance, musicians tend to have Moon-Mercury conjunctions while scientists tend to have Saturn-Sun conjunctions — not just slightly elevated frequencies of these configurations (which supervised analysis might detect), but elevated enough that the clusters become visually and algorithmically apparent. It would require that when you map 766 charts into a 66-dimensional aspect space, distinct clouds emerge around professional identities.

The data shows no such clouds. The musicians and scientists and athletes are distributed through the same undifferentiated fog, indistinguishable from one another by any algorithmic tool.

### The Hardship Hypothesis and Unsupervised Learning

This result does not contradict the supervised findings in other chapters of this book. Project 33 found that Writers cluster around weak-Mars charts — a small frequency elevation that a supervised classifier can detect when told to look for it. Project 20 identified specific placements with elevated rates in the celebrity population as a whole. These weak signals exist; they are not artifacts.

But here is the crucial distinction: a weak signal in a supervised context does not guarantee detectable structure in an unsupervised context. To illustrate: imagine that exactly 20% of musicians have Moon-Mercury conjunctions, while the general celebrity population has 15%. That is a real, statistically detectable signal in a supervised framework. But in unsupervised clustering, that 5% frequency difference is swamped by the 80% of musicians who do *not* have that placement, and the 15% of non-musicians who do. The algorithm cannot find a clean cluster because the "signal" musicians are distributed among the noise musicians, indistinguishable at the individual chart level.

The Hardship Hypothesis — the book's most persistent theme, that successful people tend to have tense rather than harmonious charts — might actually explain part of this null result. If all professionals tend toward somewhat difficult placements, regardless of field, there would be no field-specific clustering to find. Difficulty is the uniform condition; the specific flavor of difficulty is the minor variation. Unsupervised learning cannot detect minor variations in a uniformly turbulent landscape.

---

## Statistical Caveats

**The null is strong.** With N=766 across 8 categories and six different algorithms all producing ARI values below 0.01, the probability of missing a genuine medium-strength effect (d > 0.3) is extremely low. This is a well-powered null result, not a merely underpowered one.

**Feature choice matters.** These analyses used planetary longitudes and cosine interaction features. They did not include house placements (which require birth time), aspects with midpoints, or harmonic series. A future analysis with full birth time data and richer features might yield different results — though Projects 13 and 23 suggest this is unlikely to change the fundamental picture dramatically.

**Generational confound suppressed but not eliminated.** The slow outer planets (Jupiter, Saturn, Uranus, Neptune, Pluto) encode birth year rather than individual astrological character. Removing them from the feature set might reduce noise in some dimensions but would also remove features that astrologers do use in career assessment. The analysis in Phase 2 using only pairwise cosine interactions (which are zodiac-invariant but still include slow-planet aspects) shows no improvement over raw coordinates.

**Sample composition.** The 766 professionals come from Astro-Databank, a database of historically notable individuals — a population already filtered for celebrity and historical significance. This population may already be more homogeneous astrologically (due to the Hardship Hypothesis uniformity noted above) than a random sample of working professionals would be.

---

## Conclusion

Unsupervised machine learning applied to 766 verified professionals across 8 career categories finds no evidence that birth charts cluster by profession. The Adjusted Rand Index across six algorithms and three feature sets ranges from −0.002 to 0.039 — all functionally zero. Silhouette scores peak at 0.222, well below the 0.5 threshold for meaningful cluster structure. All eight professions distribute uniformly across all generated clusters.

This does not mean astrology has no information about profession — the supervised results elsewhere in this book suggest it may have a little. But it does mean that information is too weak, too diffuse, and too much overwhelmed by individual variation to produce the kind of natural grouping that would make a birth chart function as a vocational fingerprint. If the planets say something about what a person becomes, they are whispering, not shouting — and the whispers are inaudible to any algorithm listening without prior assumptions about what to hear.

---

*Archived source data and raw outputs preserved in `backup/`.*
