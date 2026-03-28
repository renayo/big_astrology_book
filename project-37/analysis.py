#!/usr/bin/env python3
"""Project 21b: Planetary Cycles and Mood Surveys"""
import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats
from datetime import datetime
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
swe.set_ephe_path(None)

# University of Michigan Consumer Sentiment (real monthly data)
SENTIMENT_DATA = {
    '2020-01': 99.8, '2020-02': 101.0, '2020-03': 89.1, '2020-04': 71.8,
    '2020-05': 72.3, '2020-06': 78.1, '2020-07': 72.5, '2020-08': 74.1,
    '2020-09': 80.4, '2020-10': 81.8, '2020-11': 76.9, '2020-12': 80.7,
    '2021-01': 79.0, '2021-02': 76.8, '2021-03': 84.9, '2021-04': 88.3,
    '2021-05': 82.9, '2021-06': 85.5, '2021-07': 81.2, '2021-08': 70.3,
}

def datetime_to_jd(dt):
    return swe.julday(dt.year, dt.month, dt.day, 12.0)

def main():
    print("=" * 60)
    print("PROJECT 21b: PLANETARY CYCLES AND MOOD")
    print("=" * 60)
    
    records = []
    for month_str, sentiment in SENTIMENT_DATA.items():
        dt = datetime.strptime(month_str + '-15', '%Y-%m-%d')
        jd = datetime_to_jd(dt)
        
        jupiter = swe.calc_ut(jd, swe.JUPITER)[0][0]
        saturn = swe.calc_ut(jd, swe.SATURN)[0][0]
        
        js_angle = abs(jupiter - saturn) % 360
        if js_angle > 180: js_angle = 360 - js_angle
        
        records.append({
            'month': month_str,
            'sentiment': sentiment,
            'jupiter_saturn_angle': js_angle,
            'jupiter_lon': jupiter
        })
    
    df = pd.DataFrame(records)
    
    # Correlation analysis
    corr, p_val = stats.pearsonr(df['jupiter_saturn_angle'], df['sentiment'])
    print(f"Jupiter-Saturn angle vs Sentiment: r={corr:.3f}, p={p_val:.4f}")
    
    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    axes[0].plot(range(len(df)), df['sentiment'], 'b-o')
    axes[0].set_xticks(range(len(df)))
    axes[0].set_xticklabels(df['month'], rotation=45, ha='right')
    axes[0].set_ylabel('Consumer Sentiment')
    axes[0].set_title('U Michigan Sentiment Index')
    
    axes[1].scatter(df['jupiter_saturn_angle'], df['sentiment'])
    axes[1].set_xlabel('Jupiter-Saturn Angle')
    axes[1].set_ylabel('Sentiment')
    axes[1].set_title(f'Correlation: r={corr:.3f}')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'mood_analysis.png', dpi=150)
    plt.close()
    
    df.to_csv(OUTPUT_DIR / 'mood_data.csv', index=False)
    pd.DataFrame([{'correlation': corr, 'p_value': p_val}]).to_csv(
        OUTPUT_DIR / 'analysis_results.csv', index=False)
    print(f"Results saved to {OUTPUT_DIR}")

if __name__ == '__main__':
    main()

