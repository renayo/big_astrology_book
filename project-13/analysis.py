#!/usr/bin/env python3
"""
Project 13: Circular Statistics and Personality Traits
======================================================
Tests zodiac sign distribution and continuous planetary interactions 
using REAL celebrity data.

Methodology:
1. Parse celebrity birth dates.
2. Calculate positions for 12 bodies (Sun-Pluto + Nodes).
   - Tropical Zodiac
   - Sidereal Zodiac (Lahiri)
3. Calculate Zodiac Signs for ALL 12 bodies.
4. Calculate Cosine Similarity features for ALL pairs (Interactions).
5. Compare "Performers" vs "Scientists" vs "Writers".
6. Calculate Effect Magnitudes (Cramer's V & Cohen's d).
"""

import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
from datetime import datetime
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path(None)

# CELEBRITY DATA from previous version
CELEBRITY_DATA = [
     # PERFORMERS (Actors, Musicians, Comedians) - High Extraversion proxy
    ('Marilyn Monroe', '1926-06-01', 'performer'),
    ('Elvis Presley', '1935-01-08', 'performer'),
    ('Michael Jackson', '1958-08-29', 'performer'),
    ('Prince', '1958-06-07', 'performer'),
    ('David Bowie', '1947-01-08', 'performer'),
    ('Freddie Mercury', '1946-09-05', 'performer'),
    ('Whitney Houston', '1963-08-09', 'performer'),
    ('Amy Winehouse', '1983-09-14', 'performer'),
    ('Kurt Cobain', '1967-02-20', 'performer'),
    ('Jimi Hendrix', '1942-11-27', 'performer'),
    ('Janis Joplin', '1943-01-19', 'performer'),
    ('Jim Morrison', '1943-12-08', 'performer'),
    ('John Lennon', '1940-10-09', 'performer'),
    ('George Harrison', '1943-02-25', 'performer'),
    ('Frank Sinatra', '1915-12-12', 'performer'),
    ('Dean Martin', '1917-06-07', 'performer'),
    ('Sammy Davis Jr', '1925-12-08', 'performer'),
    ('Lucille Ball', '1911-08-06', 'performer'),
    ('Robin Williams', '1951-07-21', 'performer'),
    ('John Belushi', '1949-01-24', 'performer'),
    ('Chris Farley', '1964-02-15', 'performer'),
    ('Richard Pryor', '1940-12-01', 'performer'),
    ('George Carlin', '1937-05-12', 'performer'),
    ('Bob Hope', '1903-05-29', 'performer'),
    ('Johnny Carson', '1925-10-23', 'performer'),
    ('Joan Rivers', '1933-06-08', 'performer'),
    ('Betty White', '1922-01-17', 'performer'),
    ('Audrey Hepburn', '1929-05-04', 'performer'),
    ('Elizabeth Taylor', '1932-02-27', 'performer'),
    ('Grace Kelly', '1929-11-12', 'performer'),
    ('Marlon Brando', '1924-04-03', 'performer'),
    ('James Dean', '1931-02-08', 'performer'),
    ('Humphrey Bogart', '1899-12-25', 'performer'),
    ('Clark Gable', '1901-02-01', 'performer'),
    ('Cary Grant', '1904-01-18', 'performer'),
    ('James Stewart', '1908-05-20', 'performer'),
    ('John Wayne', '1907-05-26', 'performer'),
    ('Bette Davis', '1908-04-05', 'performer'),
    ('Katharine Hepburn', '1907-05-12', 'performer'),
    ('Judy Garland', '1922-06-10', 'performer'),
    ('Gene Kelly', '1912-08-23', 'performer'),
    ('Fred Astaire', '1899-05-10', 'performer'),
    ('Ginger Rogers', '1911-07-16', 'performer'),
    ('Bing Crosby', '1903-05-03', 'performer'),
    ('Nat King Cole', '1919-03-17', 'performer'),
    ('Ella Fitzgerald', '1917-04-25', 'performer'),
    ('Billie Holiday', '1915-04-07', 'performer'),
    ('Louis Armstrong', '1901-08-04', 'performer'),
    ('Duke Ellington', '1899-04-29', 'performer'),
    ('Count Basie', '1904-08-21', 'performer'),
    ('Charlie Parker', '1920-08-29', 'performer'),
    ('Miles Davis', '1926-05-26', 'performer'),
    ('John Coltrane', '1926-09-23', 'performer'),
    ('Thelonious Monk', '1917-10-10', 'performer'),
    ('Ray Charles', '1930-09-23', 'performer'),
    ('James Brown', '1933-05-03', 'performer'),
    ('Aretha Franklin', '1942-03-25', 'performer'),
    ('Otis Redding', '1941-09-09', 'performer'),
    ('Marvin Gaye', '1939-04-02', 'performer'),
    ('Stevie Wonder', '1950-05-13', 'performer'),
    ('Bob Marley', '1945-02-06', 'performer'),
    ('Johnny Cash', '1932-02-26', 'performer'),
    ('Hank Williams', '1923-09-17', 'performer'),
    ('Patsy Cline', '1932-09-08', 'performer'),
    ('Buddy Holly', '1936-09-07', 'performer'),
    ('Ritchie Valens', '1941-05-13', 'performer'),
    ('Eddie Cochran', '1938-10-03', 'performer'),
    ('Chuck Berry', '1926-10-18', 'performer'),
    ('Little Richard', '1932-12-05', 'performer'),
    ('Fats Domino', '1928-02-26', 'performer'),
    ('Jerry Lee Lewis', '1935-09-29', 'performer'),
    ('Roy Orbison', '1936-04-23', 'performer'),
    ('Sam Cooke', '1931-01-22', 'performer'),
    ('Jackie Wilson', '1934-06-09', 'performer'),
    ('Etta James', '1938-01-25', 'performer'),
    ('Tina Turner', '1939-11-26', 'performer'),
    ('Donna Summer', '1948-12-31', 'performer'),
    ('Barry White', '1944-09-12', 'performer'),
    ('Isaac Hayes', '1942-08-20', 'performer'),
    ('Curtis Mayfield', '1942-06-03', 'performer'),
    ('George Michael', '1963-06-25', 'performer'),
    ('Tom Petty', '1950-10-20', 'performer'),
    ('Glenn Frey', '1948-11-06', 'performer'),
    ('Don Henley', '1947-07-22', 'performer'),
    ('Gregg Allman', '1947-12-08', 'performer'),
    ('Duane Allman', '1946-11-20', 'performer'),
    ('Ronnie Van Zant', '1948-01-15', 'performer'),
    ('Stevie Ray Vaughan', '1954-10-03', 'performer'),
    ('BB King', '1925-09-16', 'performer'),
    ('Muddy Waters', '1913-04-04', 'performer'),
    ('Howlin Wolf', '1910-06-10', 'performer'),
    ('John Lee Hooker', '1912-08-22', 'performer'),
    ('Albert King', '1923-04-25', 'performer'),
    ('Freddie King', '1934-09-03', 'performer'),
    ('Rory Gallagher', '1948-03-02', 'performer'),
    ('Gary Moore', '1952-04-04', 'performer'),
    ('Jeff Beck', '1944-06-24', 'performer'),
    ('Eddie Van Halen', '1955-01-26', 'performer'),
    ('Dimebag Darrell', '1966-08-20', 'performer'),
    ('Lemmy Kilmister', '1945-12-24', 'performer'),

    # SCIENTISTS/MATHEMATICIANS/INVENTORS - Lower Extraversion proxy
    ('Albert Einstein', '1879-03-14', 'scientist'),
    ('Isaac Newton', '1643-01-04', 'scientist'),
    ('Charles Darwin', '1809-02-12', 'scientist'),
    ('Marie Curie', '1867-11-07', 'scientist'),
    ('Nikola Tesla', '1856-07-10', 'scientist'),
    ('Thomas Edison', '1847-02-11', 'scientist'),
    ('Stephen Hawking', '1942-01-08', 'scientist'),
    ('Richard Feynman', '1918-05-11', 'scientist'),
    ('Carl Sagan', '1934-11-09', 'scientist'),
    ('Alan Turing', '1912-06-23', 'scientist'),
    ('Ada Lovelace', '1815-12-10', 'scientist'),
    ('Galileo Galilei', '1564-02-15', 'scientist'),
    ('Johannes Kepler', '1571-12-27', 'scientist'),
    ('Niels Bohr', '1885-10-07', 'scientist'),
    ('Werner Heisenberg', '1901-12-05', 'scientist'),
    ('Erwin Schrodinger', '1887-08-12', 'scientist'),
    ('Max Planck', '1858-04-23', 'scientist'),
    ('Enrico Fermi', '1901-09-29', 'scientist'),
    ('Robert Oppenheimer', '1904-04-22', 'scientist'),
    ('Linus Pauling', '1901-02-28', 'scientist'),
    ('Jonas Salk', '1914-10-28', 'scientist'),
    ('Alexander Fleming', '1881-08-06', 'scientist'),
    ('Louis Pasteur', '1822-12-27', 'scientist'),
    ('Gregor Mendel', '1822-07-20', 'scientist'),
    ('Sigmund Freud', '1856-05-06', 'scientist'),
    ('Carl Jung', '1875-07-26', 'scientist'),
    ('Ivan Pavlov', '1849-09-26', 'scientist'),
    ('BF Skinner', '1904-03-20', 'scientist'),
    ('Abraham Maslow', '1908-04-01', 'scientist'),
    ('Jean Piaget', '1896-08-09', 'scientist'),
    ('Noam Chomsky', '1928-12-07', 'scientist'),
    ('Claude Shannon', '1916-04-30', 'scientist'),
    ('John von Neumann', '1903-12-28', 'scientist'),
    ('Kurt Godel', '1906-04-28', 'scientist'),
    ('Bertrand Russell', '1872-05-18', 'scientist'),
    ('Alfred North Whitehead', '1861-02-15', 'scientist'),
    ('Ludwig Wittgenstein', '1889-04-26', 'scientist'),
    ('Blaise Pascal', '1623-06-19', 'scientist'),
    ('Rene Descartes', '1596-03-31', 'scientist'),
    ('Gottfried Leibniz', '1646-07-01', 'scientist'),
    ('Leonhard Euler', '1707-04-15', 'scientist'),
    ('Carl Friedrich Gauss', '1777-04-30', 'scientist'),
    ('Bernhard Riemann', '1826-09-17', 'scientist'),
    ('Henri Poincare', '1854-04-29', 'scientist'),
    ('David Hilbert', '1862-01-23', 'scientist'),
    ('Emmy Noether', '1882-03-23', 'scientist'),
    ('Srinivasa Ramanujan', '1887-12-22', 'scientist'),
    ('Paul Erdos', '1913-03-26', 'scientist'),
    ('John Nash', '1928-06-13', 'scientist'),
    ('Andrew Wiles', '1953-04-11', 'scientist'),

    # WRITERS/POETS - Mixed
    ('William Shakespeare', '1564-04-23', 'writer'),
    ('Charles Dickens', '1812-02-07', 'writer'),
    ('Jane Austen', '1775-12-16', 'writer'),
    ('Emily Bronte', '1818-07-30', 'writer'),
    ('Charlotte Bronte', '1816-04-21', 'writer'),
    ('Virginia Woolf', '1882-01-25', 'writer'),
    ('Oscar Wilde', '1854-10-16', 'writer'),
    ('Mark Twain', '1835-11-30', 'writer'),
    ('Ernest Hemingway', '1899-07-21', 'writer'),
    ('F Scott Fitzgerald', '1896-09-24', 'writer'),
    ('William Faulkner', '1897-09-25', 'writer'),
    ('John Steinbeck', '1902-02-27', 'writer'),
    ('Edgar Allan Poe', '1809-01-19', 'writer'),
    ('HP Lovecraft', '1890-08-20', 'writer'),
    ('Franz Kafka', '1883-07-03', 'writer'),
    ('Fyodor Dostoevsky', '1821-11-11', 'writer'),
    ('Leo Tolstoy', '1828-09-09', 'writer'),
    ('Anton Chekhov', '1860-01-29', 'writer'),
    ('Marcel Proust', '1871-07-10', 'writer'),
    ('James Joyce', '1882-02-02', 'writer'),
    ('Samuel Beckett', '1906-04-13', 'writer'),
    ('Albert Camus', '1913-11-07', 'writer'),
    ('Jean-Paul Sartre', '1905-06-21', 'writer'),
    ('Simone de Beauvoir', '1908-01-09', 'writer'),
    ('George Orwell', '1903-06-25', 'writer'),
    ('Aldous Huxley', '1894-07-26', 'writer'),
    ('Ray Bradbury', '1920-08-22', 'writer'),
    ('Isaac Asimov', '1920-01-02', 'writer'),
    ('Arthur C Clarke', '1917-12-16', 'writer'),
    ('Philip K Dick', '1928-12-16', 'writer'),
    ('Kurt Vonnegut', '1922-11-11', 'writer'),
    ('JD Salinger', '1919-01-01', 'writer'),
    ('Jack Kerouac', '1922-03-12', 'writer'),
    ('Allen Ginsberg', '1926-06-03', 'writer'),
    ('William S Burroughs', '1914-02-05', 'writer'),
    ('Hunter S Thompson', '1937-07-18', 'writer'),
    ('Truman Capote', '1924-09-30', 'writer'),
    ('Tennessee Williams', '1911-03-26', 'writer'),
    ('Arthur Miller', '1915-10-17', 'writer'),
    ('Eugene ONeill', '1888-10-16', 'writer'),
    ('Sylvia Plath', '1932-10-27', 'writer'),
    ('Anne Sexton', '1928-11-09', 'writer'),
    ('Emily Dickinson', '1830-12-10', 'writer'),
    ('Walt Whitman', '1819-05-31', 'writer'),
    ('Robert Frost', '1874-03-26', 'writer'),
    ('TS Eliot', '1888-09-26', 'writer'),
    ('Ezra Pound', '1885-10-30', 'writer'),
    ('WB Yeats', '1865-06-13', 'writer'),
    ('Dylan Thomas', '1914-10-27', 'writer'),
    ('Langston Hughes', '1901-02-01', 'writer'),
    ('Maya Angelou', '1928-04-04', 'writer'),
    ('Toni Morrison', '1931-02-18', 'writer'),
    ('James Baldwin', '1924-08-02', 'writer'),
    ('Ralph Ellison', '1913-03-01', 'writer'),
    ('Richard Wright', '1908-09-04', 'writer'),
    ('Zora Neale Hurston', '1891-01-07', 'writer'),
    ('Flannery OConnor', '1925-03-25', 'writer'),
    ('Carson McCullers', '1917-02-19', 'writer'),
    ('Harper Lee', '1926-04-28', 'writer'),
    ('Agatha Christie', '1890-09-15', 'writer'),
    ('Dorothy Parker', '1893-08-22', 'writer'),
]

PLANETS = [
    (swe.SUN, 'Sun'), (swe.MOON, 'Moon'), (swe.MERCURY, 'Mercury'),
    (swe.VENUS, 'Venus'), (swe.MARS, 'Mars'), (swe.JUPITER, 'Jupiter'),
    (swe.SATURN, 'Saturn'), (swe.URANUS, 'Uranus'), (swe.NEPTUNE, 'Neptune'),
    (swe.PLUTO, 'Pluto'), (swe.MEAN_NODE, 'North Node')
]

def get_positions(jd, sidereal=False):
    """Calculate planetary positions for a given Julian Day."""
    if sidereal:
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
        flags = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL
    else:
        flags = swe.FLG_SWIEPH | swe.FLG_SPEED

    positions = {}
    for pid, name in PLANETS:
        pos, _ = swe.calc_ut(jd, pid, flags)[:2]
        positions[name] = pos[0] # Longitude

    # Calculate South Node (opposite North Node)
    positions['South Node'] = (positions['North Node'] + 180) % 360

    return positions

def get_interactions(positions):
    """Calculate cosine of angle difference for all pairs."""
    interactions = {}
    names = list(positions.keys())

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            p1, p2 = names[i], names[j]
            diff = (positions[p1] - positions[p2]) % 360
            interactions[f"{p1}_{p2}"] = np.cos(np.radians(diff))

    return interactions

def get_zodiac_sign(lon):
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
             'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    return signs[int(lon / 30)]

def run_analysis():
    print("Processing celebrity data...")
    records = []

    for name, date_str, profession in CELEBRITY_DATA:
        try:
            # Assume Noon UTC for birth time
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            jd = swe.julday(dt.year, dt.month, dt.day, 12.0)

            # Tropical Calculations
            trop_pos = get_positions(jd, sidereal=False)
            trop_int = get_interactions(trop_pos)

            # Sidereal Calculations
            sid_pos = get_positions(jd, sidereal=True)
            sid_int = get_interactions(sid_pos)

            record = {
                'name': name,
                'profession': profession,
            }

            # Add Tropical features (Signs & Positions)
            for p, v in trop_pos.items(): 
                record[f"Trop_Pos_{p}"] = v
                record[f"Trop_Sign_{p}"] = get_zodiac_sign(v)

            # Add Tropical Interactions
            for k, v in trop_int.items(): record[f"Trop_Int_{k}"] = v

            # Add Sidereal features (Signs & Positions)
            for p, v in sid_pos.items(): 
                record[f"Sid_Pos_{p}"] = v
                record[f"Sid_Sign_{p}"] = get_zodiac_sign(v)

            # Add Sidereal Interactions
            for k, v in sid_int.items(): record[f"Sid_Int_{k}"] = v

            records.append(record)

        except Exception as e:
            print(f"Error processing {name}: {e}")

    df = pd.DataFrame(records)
    print(f"Processed {len(df)} records.")

    # ANALYSIS
    professions = ['performer', 'scientist']
    sub_df = df[df['profession'].isin(professions)]

    results = {}

    print("\n" + "="*50)
    print("STATISTICAL ANALYSIS: Performers vs Scientists")
    print("="*50)

    # 1. ZODIAC SIGN DISTRIBUTIONS (Chi-Square + Cramer's V)
    print("\n--- ZODIAC SIGN DISTRIBUTION (Chi-Square) ---")
    print(f"{'Feature':<25} | {'p-value':<10} | {'V':<8} | {'Sig?'}")
    print("-" * 65)

    sign_cols = [c for c in sub_df.columns if '_Sign_' in c]

    for col in sign_cols:
        ct = pd.crosstab(sub_df['profession'], sub_df[col])
        if ct.size > 0:
            chi2, p, dof, ex = stats.chi2_contingency(ct)
            # Cramer's V calculation: sqrt(chi2 / (n * min(k-1, r-1)))
            n = ct.sum().sum()
            min_dim = min(ct.shape[0]-1, ct.shape[1]-1)
            cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0

            sig = "**" if p < 0.05 else ""
            print(f"{col:<25} | {p:.4f}     | {cramers_v:.4f}   | {sig}")
            results[f'{col}_Chi2'] = p
            results[f'{col}_V'] = cramers_v
        else:
             results[f'{col}_Chi2'] = 1.0
             results[f'{col}_V'] = 0.0

    # 2. CONTINUOUS INTERACTIONS (T-Tests + Cohen's d)
    print("\n--- CONTINUOUS INTERACTIONS (T-Test, Top 5) ---")

    int_cols = [c for c in sub_df.columns if '_Int_' in c]
    int_results = []

    for col in int_cols:
        perf_vals = sub_df[sub_df['profession']=='performer'][col]
        sci_vals = sub_df[sub_df['profession']=='scientist'][col]

        if perf_vals.nunique() > 1 and sci_vals.nunique() > 1:
            # T-test
            t_stat, p_val = stats.ttest_ind(perf_vals, sci_vals, equal_var=False)

            # Cohen's d: (mean1 - mean2) / pooled_std
            m1, m2 = perf_vals.mean(), sci_vals.mean()
            s1, s2 = perf_vals.std(), sci_vals.std()
            n1, n2 = len(perf_vals), len(sci_vals)
            pooled_std = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
            cohens_d = (m1 - m2) / pooled_std

            int_results.append((col, p_val, m1, m2, cohens_d))
            results[f'{col}_Ttest'] = p_val

    int_results.sort(key=lambda x: x[1])

    print(f"{'Feature':<30} | {'P-Value':<10} | {'d (Eff)':<8} | {'Mean Diff'}")
    print("-" * 80)
    for col, p, m1, m2, d in int_results[:10]:
        sig = "**" if p < 0.05 else ""
        diff = m2 - m1 # Sci - Perf
        print(f"{col.replace('Trop_Int_', 'Tr_').replace('Sid_Int_', 'Sd_'):<30} | {p:.4f} {sig:<3} | {d:.4f}   | {diff:.3f}")

    # SAVE RESULTS
    with open(OUTPUT_DIR / 'RESULTS.md', 'w') as f:
        f.write("# Project 13 Results: Circular Statistics & Personality\n\n")
        f.write("## Overview\n")
        f.write(f"Analyzed {len(df)} celebrities (Performers vs Scientists).\n")
        f.write("Computed 12 Planetary positions (Sun-Pluto + Nodes) for both **Tropical** and **Sidereal (Vedic)** zodiacs.\n")
        f.write("Performed statistical tests including Effect Size (Magnitude).\n\n")
        f.write("- **Cramer's V**: Effect size for Categorical (Signs). 0.1=Small, 0.3=Medium, 0.5=Large.\n")
        f.write("- **Cohen's d**: Effect size for Continuous (Aspects). 0.2=Small, 0.5=Medium, 0.8=Large. (Positive = Scientists higher, Negative = Performers higher).\n\n")

        f.write("## 1. Zodiac Sign Distributions (Chi-Square)\n")
        f.write("| Feature | System | P-Value | Cramer's V | Significance |\n|---|---|---|---|---|\n")

        sorted_signs = sorted([(k, v) for k, v in results.items() if '_Sign_' in k and '_V' not in k], key=lambda x: x[1])
        for k, p in sorted_signs:
            sys = "Tropical" if "Trop" in k else "Sidereal"
            feat = k.replace("Trop_Sign_", "").replace("Sid_Sign_", "").replace("_Chi2", "")
            sig = "**SIGNIFICANT**" if p < 0.05 else "ns"
            v = results.get(k.replace('_Chi2', '_V'), 0)
            f.write(f"| {feat} | {sys} | {p:.4f} | {v:.4f} | {sig} |\n")

        f.write("\n## 2. Planetary Interactions (Top Differences)\n")
        f.write("Comparing cosine similarity (aspect strength). Direction indicates which group favors the aspect.\n\n")
        f.write("| Feature | System | P-Value | Cohen's d | Perf Mean | Sci Mean |\n|---|---|---|---|---|---|\n")

        for col, p, m1, m2, d in int_results[:10]:
            sys = "Tropical" if "Trop" in col else "Sidereal"
            feat = col.replace("Trop_Int_", "").replace("Sid_Int_", "")
            # Recalculate d to be Sci - Perf relative
            # If d is positive, Performer mean was higher?
            # My d calc was (m1 - m2) where m1=Perf, m2=Sci. 
            # So Positive d = Performer High. Negative d = Sci High.
            # Let's standardize in display for Sci - Perf.
            d_sci_minus_perf = -d 

            f.write(f"| {feat} | {sys} | {p:.4f} | {d_sci_minus_perf:.4f} | {m1:.3f} | {m2:.3f} |\n")

    print(f"\nResults saved to {OUTPUT_DIR / 'RESULTS.md'}")

if __name__ == "__main__":
    run_analysis()
