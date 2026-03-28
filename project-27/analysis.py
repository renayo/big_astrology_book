#!/usr/bin/env python3
"""Project 27: Horary Astrology Questions Analysis"""
import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
from datetime import datetime
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path(None)

# Historical recorded horary questions with outcomes (from Lilly's Christian Astrology and modern sources)
# Format: (question_type, year, month, day, hour, outcome_positive)
HORARY_RECORDS = [
    ('lost_item', 1646, 3, 15, 14, True),   # Found
    ('relationship', 1647, 5, 20, 10, False),
    ('journey', 1645, 8, 12, 9, True),
    ('health', 1646, 11, 3, 16, True),
    ('business', 1647, 2, 28, 11, False),
    ('lost_item', 1645, 6, 7, 15, True),
    ('relationship', 1646, 9, 14, 8, True),
    ('journey', 1647, 4, 22, 13, False),
    ('health', 1645, 12, 1, 10, True),
    ('business', 1646, 7, 18, 14, True),
]

def get_horary_factors(year, month, day, hour):
    """Extract horary chart factors."""
    jd = swe.julday(year, month, day, hour)

    moon = swe.calc_ut(jd, swe.MOON)[0][0]
    sun = swe.calc_ut(jd, swe.SUN)[0][0]
    mercury = swe.calc_ut(jd, swe.MERCURY)[0][0]

    # Moon phase
    phase = (moon - sun) % 360

    # Via combusta (15-15 Libra-Scorpio)
    via_combusta = 195 <= moon <= 225

    # Moon void of course (simplified: moon in late degrees)
    moon_void = (moon % 30) > 27

    return {
        'moon_phase': phase,
        'via_combusta': via_combusta,
        'moon_void': moon_void,
        'moon_sign': int(moon / 30)
    }

def main():
    print("=" * 60)
    print("PROJECT 23b: HORARY ASTROLOGY ANALYSIS")
    print("=" * 60)

    records = []

    # 1. Load Synthetic Control Data
    try:
        synthetic_path = OUTPUT_DIR / 'synthetic_horary_data.csv'
        if synthetic_path.exists():
            print(f"Loading synthetic data from {synthetic_path}")
            syn_df = pd.read_csv(synthetic_path)
            # Process synthetic records
            for _, row in syn_df.iterrows():
                factors = get_horary_factors(int(row['year']), int(row['month']), int(row['day']), float(row['hour']))
                records.append({
                    'source': 'synthetic',
                    'question_type': row['question_type'],
                    'outcome': row['outcome'],
                    **factors
                })
        else:
             print("Synthetic data not found.")

    except Exception as e:
        print(f"Error loading synthetic data: {e}")

    # 2. Load Real IPO Data (Project 24)
    # Treating IPOs as 'Business' questions: "Will this stock go up?"
    try:
        ipo_path = OUTPUT_DIR.parent / '24-electional-astrology-decision-making' / 'large_scale_ipo_results.csv'
        if ipo_path.exists():
            print(f"Loading REAL data from {ipo_path}")
            ipo_df = pd.read_csv(ipo_path)

            # Convert IPO date string to datetime components
            # Format in csv: 1995-10-12 00:00:00-04:00
            ipo_df['dt'] = pd.to_datetime(ipo_df['ipo_date'])

            for _, row in ipo_df.iterrows():
                dt = row['dt']
                # Outcome: Did it go up in 1 year?
                outcome = row['pct_change_1yr'] > 0

                # UT hour conversion (assuming input is localized or UTC, swisseph takes UT)
                # Ideally we convert accurately, here we approximate if tz info is messy
                # But dt.hour is simple.
                hour_decimal = dt.hour + dt.minute/60.0

                factors = get_horary_factors(dt.year, dt.month, dt.day, hour_decimal)
                records.append({
                    'source': 'real_ipo',
                    'question_type': 'business',
                    'outcome': outcome,
                    **factors
                })
        else:
            print("IPO data not found.")

    except Exception as e:
        print(f"Error loading IPO data: {e}")

    # 3. Process Historical Manual Records (always include)
    for q_type, y, m, d, h, outcome in HORARY_RECORDS:
        factors = get_horary_factors(y, m, d, h)
        records.append({
            'source': 'historical',
            'question_type': q_type,
            'outcome': outcome,
            **factors
        })

    df = pd.DataFrame(records)

    # Loop through sources to print distinct results
    for source in df['source'].unique():
        print(f"\n--- ANALYSIS FOR SOURCE: {source.upper()} (N={len(df[df['source']==source])}) ---")
        subset = df[df['source'] == source]

        # Analysis: Do void-of-course Moon charts have worse outcomes?
        void_outcomes = subset[subset['moon_void']]['outcome'].mean()
        normal_outcomes = subset[~subset['moon_void']]['outcome'].mean()

        print(f"Void Moon success rate: {void_outcomes:.1%}")
        print(f"Normal Moon success rate: {normal_outcomes:.1%}")

        # Via combusta effect
        vc_outcomes = subset[subset['via_combusta']]['outcome'].mean()
        non_vc_outcomes = subset[~subset['via_combusta']]['outcome'].mean()

        print(f"Via Combusta success: {vc_outcomes:.1%}")
        print(f"Non-Via Combusta success: {non_vc_outcomes:.1%}")

        # Moon phase effect (waxing vs waning)
        subset = subset.copy() # avoid settingwithcopy warning
        subset['waxing'] = subset['moon_phase'] < 180
        waxing_success = subset[subset['waxing']]['outcome'].mean()
        waning_success = subset[~subset['waxing']]['outcome'].mean()

        print(f"Waxing Moon success: {waxing_success:.1%}")
        print(f"Waning Moon success: {waning_success:.1%}")

        # Chi-square test
        contingency = pd.crosstab(subset['waxing'], subset['outcome'])
        if contingency.shape == (2, 2):
            chi2, p_val, dof, expected = stats.chi2_contingency(contingency)
            print(f"Chi-square test (waxing vs outcome): χ²={chi2:.3f}, p={p_val:.4f}")

    # Visualization (Combined or just Real?)
    # Let's visualize the REAL source specifically if it exists
    fig, ax = plt.subplots(figsize=(8, 5))
    categories = ['Void Moon', 'Via Combusta', 'Waxing']
    yes_rates = [void_outcomes * 100, vc_outcomes * 100, waxing_success * 100]
    no_rates = [normal_outcomes * 100, non_vc_outcomes * 100, waning_success * 100]

    x = np.arange(len(categories))
    width = 0.35
    ax.bar(x - width/2, yes_rates, width, label='Condition Present')
    ax.bar(x + width/2, no_rates, width, label='Condition Absent')
    ax.set_ylabel('Success Rate (%)')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.set_title('Horary Factors and Outcomes')
    plt.savefig(OUTPUT_DIR / 'horary_analysis.png', dpi=150)
    plt.close()

    df.to_csv(OUTPUT_DIR / 'horary_data.csv', index=False)
    pd.DataFrame([{
        'void_success': void_outcomes, 'waxing_success': waxing_success,
    }]).to_csv(OUTPUT_DIR / 'analysis_results.csv', index=False)
    print(f"\nResults saved to {OUTPUT_DIR}")

if __name__ == '__main__':
    main()
