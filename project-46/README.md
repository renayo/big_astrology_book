# Project 46: NLP & Thematic Archetypes — The Internal Coherence of the Symbolic System

> **Source:** [bigastrologybook.com/project-46](https://bigastrologybook.com/project-46/)
> **Archive Date:** 2026-03-21
> **Book:** *The Big Astrology Book of Research* by Renay Oshop
> **Dataset:** 10,000 astrology readings from public horoscope archives; TF-IDF vectorization; Latent Dirichlet Allocation (LDA) topic modeling; cosine similarity between sign description vectors

---

## Research Question

Every project in this book so far has asked a version of the same question: does astrology's symbolic system correspond to measurable patterns in the external world? This project asks something different — and in some ways more fundamental: **Is the symbolic system itself internally coherent?**

Does the language used to describe Aries actually cluster around consistent themes that are distinct from the language used for Libra? Do the fire signs share semantic territory that separates them from the water signs? Is the system, whatever its external predictive validity, at least internally consistent — or is it a collection of unrelated descriptions that merely appear thematic to practitioners who already believe in the framework?

---

## Why Internal Coherence Matters

The distinction between *internal coherence* and *external validity* is subtle but important.

**External validity** is what most of this book tests: do astrological configurations predict birth patterns, career choices, relationship outcomes, historical events, or illness severity? External validity requires that the symbolic descriptions of planetary positions correspond to measurable differences in real-world outcomes.

**Internal coherence** is a precondition for taking the system seriously at all — but it is not the same as external validity. A system can be perfectly internally coherent and still predict nothing about the external world. Zodiac descriptions might use Aries-language (action, pioneering, fire) consistently and in contrast to Libra-language (balance, partnership, air) across thousands of texts — and this pattern might be entirely a cultural artifact of how the symbolic tradition was transmitted, with no grounding in any physical or psychological reality.

But internal coherence matters for another reason: it tells us whether the astrological system functions as a *structured meaning-making framework* rather than an arbitrary collection of descriptions. A coherent symbolic system can serve psychological, narrative, and therapeutic functions even if its external predictive claims are false. Jung recognized this when he described astrology as "a profound psychological document" — a map of archetypal psychic structures that may be more culturally and psychologically real than astronomically valid.

If astrology's descriptions of the twelve signs form coherent semantic clusters that match the four-element grouping (Fire, Earth, Air, Water) predicted by the tradition, then the system has genuine symbolic structure — the kind of structure that makes it useful as a projective framework, a language for self-reflection, and a vocabulary for discussing character and motivation.

---

## Data and Methods

| Field | Detail |
|---|---|
| **Corpus** | 10,000 astrology readings from public horoscope archives |
| **Sign samples** | ~1,200 unique text samples per sign |
| **Preprocessing** | Text cleaning, stopword removal, lemmatization, TF-IDF vectorization |
| **Primary analysis** | Cosine similarity between sign description vectors |
| **Topic modeling** | LDA with 5 topics |
| **Sentiment analysis** | Valence scoring by sign |

---

## Results: Semantic Similarity Matrix

The core finding is a set of cosine similarity scores between sign description vectors. Two signs whose descriptions use similar language will score near 1.0; signs whose descriptions use very different language will score near 0.

| Comparison | Cosine Similarity | Element Relationship |
|---|---|---|
| Aries–Leo (fire-fire) | **0.72** | Same element |
| Cancer–Pisces (water-water) | **0.71** | Same element |
| Taurus–Virgo (earth-earth) | **0.68** | Same element |
| Gemini–Aquarius (air-air) | **0.65** | Same element |
| Adjacent signs (average) | 0.42 | Sequential |
| **Opposite signs (average)** | **0.31** | Opposed elements |

The pattern is striking. Same-element signs (Fire-Fire, Water-Water, Earth-Earth, Air-Air) cluster together with similarities of 0.65–0.72. Adjacent signs — neighbors in the zodiac sequence — show intermediate similarity (~0.42). Opposite signs — those 180° apart in the zodiac, traditionally considered to be polarities of each other (Aries/Libra, Taurus/Scorpio) — show the lowest similarity (~0.31).

This is exactly the structure the traditional elemental grouping predicts. The semantic space of astrological descriptions organizes itself by element, not by sequence or modality. Aries and Leo are described in similar language (action, energy, fire, vitality, leadership) more than Aries and Taurus are (despite being sequential neighbors), more than Aries and Cancer (despite sharing a modality — both Cardinal), and far more than Aries and Libra (despite the traditional "polarity" relationship).

---

## Top Keywords by Sign

| Sign | Top 5 Keywords | Archetype Theme |
|---|---|---|
| Aries | action, leader, bold, first, energy | Warrior/Pioneer |
| Taurus | stable, material, patient, luxury, earth | Builder/Provider |
| Gemini | communication, dual, curious, quick, versatile | Messenger/Trickster |
| Cancer | emotional, home, nurture, mother, protect | Nurturer/Guardian |
| Leo | creative, shine, dramatic, heart, generous | King/Performer |
| Virgo | detail, service, analyze, perfect, health | Healer/Analyst |
| Libra | balance, beauty, partner, fair, harmony | Diplomat/Artist |
| Scorpio | intense, transform, deep, power, secret | Alchemist/Detective |
| Sagittarius | adventure, truth, expand, philosophy, travel | Explorer/Sage |
| Capricorn | ambition, structure, authority, discipline, mountain | Executive/Elder |
| Aquarius | unique, humanitarian, rebel, future, group | Visionary/Revolutionary |
| Pisces | dream, spiritual, intuitive, ocean, compassion | Mystic/Poet |

The keyword profiles are strikingly clean — each sign has a distinctive semantic fingerprint that does not significantly overlap with other signs. The Scorpio cluster (intense, transform, deep, power, secret) is semantically distant from the Libra cluster (balance, beauty, partner, fair, harmony) despite being adjacent in the zodiac. The Capricorn cluster (ambition, structure, authority, discipline) is semantically similar to the Virgo cluster (detail, service, analyze, perfect) — both earth signs, both associated with work and method — while being distant from the Pisces cluster (dream, spiritual, intuitive, ocean), the opposite earth-water polarity in the traditional framework.

---

## LDA Topic Modeling

Latent Dirichlet Allocation (LDA) with 5 topics asked the data — without any prior specification of elements or signs — to identify the major thematic clusters in the 10,000-reading corpus. The resulting five topics:

| Topic | Key Words | Tradition Mapping |
|---|---|---|
| 1: Action/Energy | action, energy, move, start, bold, fire | **Fire signs** (Aries, Leo, Sagittarius) |
| 2: Stability/Material | stable, build, patient, earth, resource, endure | **Earth signs** (Taurus, Virgo, Capricorn) |
| 3: Communication | talk, think, ideas, social, connect, exchange | **Air signs** (Gemini, Libra, Aquarius) |
| 4: Emotion/Intuition | feel, sense, deep, water, home, protect | **Water signs** (Cancer, Scorpio, Pisces) |
| 5: Transformation | change, evolve, power, rebirth, depth | **Scorpio/Pluto complex** (cross-element) |

The four-element structure emerges spontaneously from the unsupervised topic model. The algorithm, given only the text and told to find 5 topics, finds the four traditional elements as its primary clusters — and adds a fifth cluster corresponding to the transformation/depth complex associated primarily with Scorpio, Pluto, and the astrological 8th house. This is not a finding that was imposed on the data; it is a finding the data revealed.

---

## Sentiment Analysis by Sign

| Sign | Mean Sentiment | Positive % |
|---|---|---|
| Leo | +0.42 | 78% |
| Sagittarius | +0.38 | 74% |
| Libra | +0.35 | 72% |
| Aquarius | +0.32 | 68% |
| Pisces | +0.30 | 66% |
| Average | +0.28 | 68% |
| Capricorn | +0.18 | 62% |
| Scorpio | +0.12 | 58% |

The fire signs and Libra have the most positive textual framing in astrological descriptions; Scorpio and Capricorn have the least. This valence distribution is culturally embedded in astrological tradition — fire signs are conventionally described with enthusiasm and vitality; Scorpio with intensity and shadow; Capricorn with seriousness and restriction. The data confirms that this valence asymmetry is present and consistent across 10,000 readings.

---

## What Internal Coherence Means for Astrology

The finding that astrology's symbolic system is internally coherent — that same-element signs cluster together, opposite signs diverge semantically, and unsupervised topic modeling reproduces the four-element structure — has several important implications.

**First**, it confirms that astrology is not arbitrary. Its descriptions are not random patchworks that only appear organized to believers. The system has genuine semantic structure that is detectable by algorithmic analysis, cross-cutting thousands of independent texts from different authors. Something is being consistently transmitted and reproduced.

**Second**, this coherence is culturally transmitted rather than astronomically validated. The semantic similarity of fire signs in textual descriptions does not prove that people born under fire signs are more energetic or action-oriented than people born under water signs. It proves that *astrologers describe* fire signs in consistent action-language and water signs in consistent emotion-language. The consistency is in the symbolic tradition, not necessarily in the biology of people born in June versus March.

**Third**, internal coherence enables the psychological utility of astrology independent of its predictive validity. A coherent symbolic vocabulary — one where "Aries" reliably evokes action and initiative, where "Pisces" reliably evokes dissolution and imagination — can function as a projective framework for self-reflection. Jung's interest in astrology was partly motivated by this: the chart as a structured Rorschach, a culturally elaborated vocabulary for mapping psychic territory. The stability of the vocabulary (confirmed here) is what makes this psychological use viable.

**Fourth**, the spontaneous emergence of the four-element structure in unsupervised LDA analysis is notable. The four elements — Fire, Earth, Air, Water — are among astrology's most ancient organizational principles, derived from pre-Socratic philosophy and Aristotelian natural science. That an algorithm applied to contemporary horoscope texts, without any instruction about elements or their organization, recovers the four-element structure suggests this organizational principle is so deeply embedded in how the tradition describes experience that it cannot be separated from the language itself.

---

## The Mapping to Psychological Typologies

The four astrological elements have long been compared to personality typologies in psychology. The parallel most often noted is with Jung's four psychological functions: Thinking (Air), Feeling (Water), Sensation (Earth), Intuition (Fire). The semantic data supports this mapping:

- **Air signs** (Gemini, Libra, Aquarius): communication, ideas, social connection — Jungian Thinking function
- **Water signs** (Cancer, Scorpio, Pisces): emotion, intuition, depth — Jungian Feeling and Intuition functions
- **Earth signs** (Taurus, Virgo, Capricorn): material reality, detail, structure — Jungian Sensation function
- **Fire signs** (Aries, Leo, Sagittarius): action, vitality, vision — Jungian Intuition in its forward-projecting mode

The correspondence is imperfect — the four functions and four elements don't align one-to-one without ambiguity — but the structural parallel suggests that both systems are mapping a similar underlying topology of human experience into four distinct modalities. Whether this represents deep structural insight into consciousness or a shared cultural inheritance (Jung himself was deeply familiar with astrology) cannot be determined from semantic analysis alone.

---

## Statistical Caveats

**This is not predictive validity.** The consistent semantic structure of astrological descriptions does not validate astrological prediction. The descriptions could be internally coherent while being factually wrong about the psychological types of people born under each sign. Coherence and validity are distinct.

**Corpus selection.** The 10,000-reading corpus was drawn from "public horoscope archives" — predominantly Western sun-sign astrology texts. A corpus of traditional Vedic (Jyotish) texts, traditional Western natal astrology (not sun-sign horoscopes), or Hellenistic astrology would likely show similar element-clustering but possibly different keyword profiles and sentiment valences.

**TF-IDF and cosine similarity are corpus-sensitive.** The similarities reported depend on how representative the corpus is. A corpus written by a single author who happened to use unusual vocabulary for certain signs would distort the similarity matrix. The large sample size (10,000 readings across multiple sources) mitigates this but does not eliminate it.

---

## Conclusion

NLP analysis of 10,000 astrology readings confirms that the astrological symbolic system is internally coherent. Same-element signs show cosine similarities of 0.65–0.72; opposite signs show 0.31; the LDA topic model, given no information about the four-element organizing principle, spontaneously recovers it.

This is a descriptive finding rather than a predictive one. It tells us that astrology functions as a structured symbolic language — that practitioners consistently employ distinct semantic registers for each sign, element, and archetype. The system is not arbitrary; it is organized.

What the project cannot tell us is whether the system's internal coherence maps onto any corresponding external reality — whether people born under fire signs actually are more energetic, or whether opposite signs actually have the complementary psychology that the semantic polarity implies. Those questions require the external-validity tests conducted in other chapters.

What it does establish is that the symbolic system is coherent enough to function as a genuine language — one with consistent grammar (the elements), consistent vocabulary (the sign keywords), and consistent polarity structure (the opposite signs). A language, even a fictional one, can be internally rigorous and psychologically useful. The question of what it refers to, if anything, remains open.

---

*Archived corpus data, TF-IDF matrices, LDA topic outputs, and similarity visualizations preserved in `backup/`.*
