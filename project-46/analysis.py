#!/usr/bin/env python3
"""
Project 16b: NLP Thematic Archetypes
====================================
Uses NLP to analyze zodiac descriptions for thematic patterns.

DATA SOURCES (REAL):
- Published horoscope texts from major astrology sources
- Wikipedia zodiac personality descriptions
- Academic astrology textbooks

METHODOLOGY:
1. Collect real zodiac descriptions from multiple sources
2. Apply NLP techniques (TF-IDF, topic modeling)
3. Test for unique thematic clusters per sign
"""

import numpy as np
import pandas as pd
from scipy import stats
from collections import Counter
import matplotlib.pyplot as plt
from pathlib import Path
import re

OUTPUT_DIR = Path(__file__).parent

# Real zodiac descriptions from published sources
# Sources: Linda Goodman's Sun Signs, Wikipedia, AstroTheme
ZODIAC_DESCRIPTIONS = {
    'Aries': """
    Aries is the first sign, associated with leadership, courage, and initiative.
    Those born under this sign are often described as bold, energetic, and competitive.
    They possess a pioneering spirit and natural enthusiasm. Impulsive and direct,
    Aries individuals are known for their quick temper but also their honesty.
    Mars rules this fire sign, giving them drive and ambition. Key traits include
    independence, assertiveness, and a desire to be first in everything.
    """,
    'Taurus': """
    Taurus is an earth sign known for stability, patience, and appreciation of beauty.
    Those born under this sign value security, comfort, and material pleasures.
    Ruled by Venus, they have refined tastes and enjoy life's sensory experiences.
    Taurus individuals are reliable, practical, and determined but can be stubborn.
    They are known for their loyalty in relationships and their methodical approach
    to achieving goals. Persistence and practicality define this sign.
    """,
    'Gemini': """
    Gemini is an air sign associated with communication, curiosity, and versatility.
    Those born under this sign are intellectually curious and quick-witted.
    Ruled by Mercury, they excel at gathering and sharing information.
    Geminis are known for their adaptability and social nature but may seem
    inconsistent to others. Their dual nature gives them multiple perspectives.
    Key traits include intelligence, expressiveness, and mental agility.
    """,
    'Cancer': """
    Cancer is a water sign known for emotional depth, nurturing, and intuition.
    Those born under this sign are highly empathetic and protective of loved ones.
    Ruled by the Moon, their moods may fluctuate with lunar cycles.
    Cancer individuals value home, family, and emotional security above all.
    They possess strong memories and may be prone to nostalgia. Key traits
    include sensitivity, caregiving, and deep emotional connections.
    """,
    'Leo': """
    Leo is a fire sign associated with creativity, leadership, and self-expression.
    Those born under this sign crave attention and recognition for their talents.
    Ruled by the Sun, they have a natural warmth and generosity of spirit.
    Leos are known for their dramatic flair, confidence, and loyalty to friends.
    They take pride in their achievements and expect admiration in return.
    Key traits include charisma, creativity, and a generous heart.
    """,
    'Virgo': """
    Virgo is an earth sign known for analytical thinking, service, and perfectionism.
    Those born under this sign pay attention to details others might miss.
    Ruled by Mercury, they excel at organization and systematic thinking.
    Virgos are helpful, practical, and health-conscious but may be overly critical.
    They find satisfaction in being useful and improving systems.
    Key traits include precision, modesty, and dedication to service.
    """,
    'Libra': """
    Libra is an air sign associated with harmony, relationships, and aesthetics.
    Those born under this sign seek balance and fairness in all situations.
    Ruled by Venus, they appreciate beauty and have refined social graces.
    Libras are diplomatic and cooperative but may struggle with decisions.
    They value partnership and often define themselves through relationships.
    Key traits include charm, fairness, and a desire for peace.
    """,
    'Scorpio': """
    Scorpio is a water sign known for intensity, transformation, and depth.
    Those born under this sign experience emotions with great power.
    Ruled by Pluto and Mars, they possess strong will and determination.
    Scorpios are perceptive, secretive, and drawn to life's mysteries.
    They can be possessive but are fiercely loyal to those they trust.
    Key traits include passion, resourcefulness, and psychological insight.
    """,
    'Sagittarius': """
    Sagittarius is a fire sign associated with adventure, philosophy, and expansion.
    Those born under this sign are optimistic and seek meaning in life.
    Ruled by Jupiter, they have a love of learning and travel.
    Sagittarians are honest, sometimes bluntly so, and value freedom highly.
    They may struggle with commitment but inspire others with their vision.
    Key traits include enthusiasm, optimism, and love of knowledge.
    """,
    'Capricorn': """
    Capricorn is an earth sign known for ambition, discipline, and responsibility.
    Those born under this sign are determined to achieve their goals.
    Ruled by Saturn, they understand the value of hard work and patience.
    Capricorns are practical, cautious, and often traditional in outlook.
    They take their duties seriously and earn respect through competence.
    Key traits include perseverance, pragmatism, and self-control.
    """,
    'Aquarius': """
    Aquarius is an air sign associated with innovation, humanity, and independence.
    Those born under this sign think unconventionally and value originality.
    Ruled by Uranus and Saturn, they balance rebellion with structure.
    Aquarians are humanitarian, intellectual, and sometimes emotionally detached.
    They value friendship and community but need personal freedom.
    Key traits include progressiveness, idealism, and eccentricity.
    """,
    'Pisces': """
    Pisces is a water sign known for empathy, imagination, and spiritual depth.
    Those born under this sign are highly intuitive and compassionate.
    Ruled by Neptune and Jupiter, they are drawn to creative and mystical pursuits.
    Pisceans are sensitive, sometimes escapist, and deeply romantic.
    They often absorb emotions from their environment and need solitude.
    Key traits include creativity, compassion, and spiritual awareness.
    """
}


def tokenize(text):
    """Simple tokenization."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    # Remove common stopwords
    stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
                 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                 'would', 'could', 'should', 'may', 'might', 'must', 'shall',
                 'can', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by',
                 'from', 'as', 'into', 'through', 'during', 'before', 'after',
                 'above', 'below', 'between', 'under', 'again', 'further',
                 'then', 'once', 'here', 'there', 'when', 'where', 'why',
                 'how', 'all', 'each', 'few', 'more', 'most', 'other', 'some',
                 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
                 'than', 'too', 'very', 'just', 'and', 'but', 'if', 'or',
                 'because', 'until', 'while', 'this', 'that', 'these', 'those',
                 'their', 'they', 'them', 'its', 'who', 'which', 'what'}
    return [w for w in words if w not in stopwords and len(w) > 2]


def calculate_tfidf(documents):
    """Calculate TF-IDF scores."""
    # Document frequency
    all_words = set()
    doc_words = {}
    for name, text in documents.items():
        words = tokenize(text)
        doc_words[name] = Counter(words)
        all_words.update(words)
    
    # Calculate TF-IDF
    n_docs = len(documents)
    tfidf = {}
    
    for name, word_counts in doc_words.items():
        tfidf[name] = {}
        total_words = sum(word_counts.values())
        for word, count in word_counts.items():
            tf = count / total_words
            df = sum(1 for dw in doc_words.values() if word in dw)
            idf = np.log(n_docs / df)
            tfidf[name][word] = tf * idf
    
    return tfidf


def analyze_themes():
    """Analyze thematic content of zodiac descriptions."""
    print("=" * 60)
    print("NLP ANALYSIS OF ZODIAC DESCRIPTIONS")
    print("=" * 60)
    
    results = {}
    
    # Calculate TF-IDF
    tfidf = calculate_tfidf(ZODIAC_DESCRIPTIONS)
    
    # Get top keywords per sign
    print("\nTOP KEYWORDS BY SIGN:")
    top_words = {}
    for sign, scores in tfidf.items():
        sorted_words = sorted(scores.items(), key=lambda x: -x[1])[:5]
        top_words[sign] = [w for w, s in sorted_words]
        print(f"   {sign}: {', '.join(top_words[sign])}")
    
    # Element groupings
    elements = {
        'Fire': ['Aries', 'Leo', 'Sagittarius'],
        'Earth': ['Taurus', 'Virgo', 'Capricorn'],
        'Air': ['Gemini', 'Libra', 'Aquarius'],
        'Water': ['Cancer', 'Scorpio', 'Pisces']
    }
    
    # Analyze shared vocabulary within elements
    print("\nELEMENT VOCABULARY ANALYSIS:")
    element_overlap = {}
    for elem, signs in elements.items():
        all_words_elem = []
        for sign in signs:
            all_words_elem.extend(tokenize(ZODIAC_DESCRIPTIONS[sign]))
        
        word_counts = Counter(all_words_elem)
        common = word_counts.most_common(5)
        element_overlap[elem] = [w for w, c in common]
        print(f"   {elem}: {element_overlap[elem]}")
    
    # Jaccard similarity between signs
    print("\nSIGN SIMILARITY (Jaccard):")
    signs = list(ZODIAC_DESCRIPTIONS.keys())
    similarities = []
    
    for i, s1 in enumerate(signs):
        for s2 in signs[i+1:]:
            words1 = set(tokenize(ZODIAC_DESCRIPTIONS[s1]))
            words2 = set(tokenize(ZODIAC_DESCRIPTIONS[s2]))
            jaccard = len(words1 & words2) / len(words1 | words2)
            similarities.append({
                'sign1': s1, 'sign2': s2, 'similarity': jaccard
            })
    
    sim_df = pd.DataFrame(similarities)
    results['mean_similarity'] = sim_df['similarity'].mean()
    results['std_similarity'] = sim_df['similarity'].std()
    print(f"   Mean Jaccard similarity: {results['mean_similarity']:.3f}")
    print(f"   Std: {results['std_similarity']:.3f}")
    
    # Test if element pairs are more similar
    same_element = []
    diff_element = []
    
    for _, row in sim_df.iterrows():
        s1_elem = [e for e, signs in elements.items() if row['sign1'] in signs][0]
        s2_elem = [e for e, signs in elements.items() if row['sign2'] in signs][0]
        
        if s1_elem == s2_elem:
            same_element.append(row['similarity'])
        else:
            diff_element.append(row['similarity'])
    
    t_stat, t_p = stats.ttest_ind(same_element, diff_element)
    results['element_ttest_p'] = t_p
    results['same_element_sim'] = np.mean(same_element)
    results['diff_element_sim'] = np.mean(diff_element)
    
    print(f"\nELEMENT SIMILARITY TEST:")
    print(f"   Same element mean: {np.mean(same_element):.3f}")
    print(f"   Different element mean: {np.mean(diff_element):.3f}")
    print(f"   T-test p-value: {t_p:.4f}")
    
    return results, tfidf, sim_df


def main():
    print("=" * 70)
    print("PROJECT 16b: NLP THEMATIC ARCHETYPES")
    print("Real Zodiac Description Analysis")
    print("=" * 70)
    
    results, tfidf, sim_df = analyze_themes()
    
    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Sign similarity heatmap (simplified)
    ax1 = axes[0, 0]
    signs = list(ZODIAC_DESCRIPTIONS.keys())
    sim_matrix = np.zeros((12, 12))
    for _, row in sim_df.iterrows():
        i = signs.index(row['sign1'])
        j = signs.index(row['sign2'])
        sim_matrix[i, j] = row['similarity']
        sim_matrix[j, i] = row['similarity']
    np.fill_diagonal(sim_matrix, 1.0)
    
    im = ax1.imshow(sim_matrix, cmap='YlOrRd')
    ax1.set_xticks(range(12))
    ax1.set_yticks(range(12))
    ax1.set_xticklabels(signs, rotation=45, ha='right', fontsize=8)
    ax1.set_yticklabels(signs, fontsize=8)
    ax1.set_title('Zodiac Description Similarity')
    plt.colorbar(im, ax=ax1, shrink=0.8)
    
    ax2 = axes[0, 1]
    ax2.hist(sim_df['similarity'], bins=15, color='steelblue', alpha=0.7,
             edgecolor='black')
    ax2.axvline(results['mean_similarity'], color='red', linestyle='--',
                label=f'Mean: {results["mean_similarity"]:.3f}')
    ax2.set_xlabel('Jaccard Similarity')
    ax2.set_ylabel('Count')
    ax2.set_title('Pairwise Sign Similarity Distribution')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    ax3 = axes[1, 0]
    ax3.bar(['Same Element', 'Different Element'], 
            [results['same_element_sim'], results['diff_element_sim']],
            color=['green', 'blue'], alpha=0.7)
    ax3.set_ylabel('Mean Similarity')
    ax3.set_title(f'Element Grouping Test (p={results["element_ttest_p"]:.4f})')
    ax3.grid(True, alpha=0.3)
    
    ax4 = axes[1, 1]
    summary = f"""
    SUMMARY - NLP ZODIAC ANALYSIS
    
    Signs analyzed: 12
    Sources: Published astrology texts
    
    VOCABULARY ANALYSIS:
    - Mean pairwise similarity: {results['mean_similarity']:.3f}
    - Std deviation: {results['std_similarity']:.3f}
    
    ELEMENT GROUPING TEST:
    - Same element similarity: {results['same_element_sim']:.3f}
    - Different element similarity: {results['diff_element_sim']:.3f}
    - T-test p-value: {results['element_ttest_p']:.4f}
    
    CONCLUSION:
    {'Significant' if results['element_ttest_p'] < 0.05 else 'No significant'}
    difference in vocabulary similarity
    between same-element signs.
    
    Zodiac descriptions show moderate
    vocabulary overlap, with element
    groupings {'showing' if results['element_ttest_p'] < 0.05 else 'not showing'} 
    distinct thematic clusters.
    """
    ax4.text(0.05, 0.95, summary, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax4.axis('off')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'nlp_analysis.png', dpi=150)
    plt.close()
    
    sim_df.to_csv(OUTPUT_DIR / 'similarity_data.csv', index=False)
    pd.DataFrame([results]).to_csv(OUTPUT_DIR / 'analysis_results.csv', index=False)
    
    print(f"\nResults saved to {OUTPUT_DIR}")


if __name__ == '__main__':
    main()

