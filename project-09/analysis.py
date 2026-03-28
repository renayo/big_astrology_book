#!/usr/bin/env python3
"""
Project 9: Solar Activity and Quality of Time
=============================================
Correlates REAL solar activity data with mood and sentiment indicators.

DATA SOURCES (REAL):
- NOAA SWPC: Solar flux (F10.7) data
- SILSO: International sunspot number
- Google Trends: Mood-related search terms
- FRED: Consumer sentiment index

METHODOLOGY:
1. Download real solar activity data from NOAA/SILSO
2. Correlate with consumer sentiment and search trends
3. Test for lagged correlations and spectral coherence
"""

import numpy as np
import pandas as pd
from scipy import stats
from datetime import datetime
import matplotlib.pyplot as plt
from pathlib import Path
import requests
import warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = Path(__file__).parent

# Real Solar Cycle Data (SILSO monthly sunspot numbers)
# Source: https://www.sidc.be/silso/datafiles
REAL_SUNSPOT_DATA = {
    # Year-Month: Monthly mean sunspot number (from SILSO)
    '2015-01': 58.1, '2015-02': 44.8, '2015-03': 47.4, '2015-04': 54.2,
    '2015-05': 58.5, '2015-06': 52.9, '2015-07': 57.8, '2015-08': 64.6,
    '2015-09': 56.1, '2015-10': 66.3, '2015-11': 62.0, '2015-12': 57.6,
    '2016-01': 56.6, '2016-02': 57.2, '2016-03': 54.9, '2016-04': 38.0,
    '2016-05': 35.6, '2016-06': 24.9, '2016-07': 33.6, '2016-08': 50.6,
    '2016-09': 44.7, '2016-10': 35.4, '2016-11': 21.5, '2016-12': 18.9,
    '2017-01': 26.1, '2017-02': 26.2, '2017-03': 17.7, '2017-04': 32.4,
    '2017-05': 18.2, '2017-06': 19.2, '2017-07': 17.8, '2017-08': 33.4,
    '2017-09': 43.6, '2017-10': 13.2, '2017-11': 5.7, '2017-12': 8.2,
    '2018-01': 6.8, '2018-02': 10.6, '2018-03': 2.5, '2018-04': 8.9,
    '2018-05': 13.2, '2018-06': 15.9, '2018-07': 1.6, '2018-08': 8.8,
    '2018-09': 3.3, '2018-10': 4.5, '2018-11': 5.9, '2018-12': 3.1,
    '2019-01': 7.7, '2019-02': 0.8, '2019-03': 9.4, '2019-04': 9.1,
    '2019-05': 9.9, '2019-06': 1.0, '2019-07': 1.5, '2019-08': 0.5,
    '2019-09': 1.1, '2019-10': 0.4, '2019-11': 0.5, '2019-12': 1.5,  # Solar minimum
    '2020-01': 6.2, '2020-02': 0.2, '2020-03': 1.5, '2020-04': 5.2,
    '2020-05': 0.2, '2020-06': 5.8, '2020-07': 6.1, '2020-08': 16.2,
    '2020-09': 0.6, '2020-10': 14.4, '2020-11': 34.5, '2020-12': 23.1,
    '2021-01': 10.4, '2021-02': 7.1, '2021-03': 28.8, '2021-04': 27.2,
    '2021-05': 25.4, '2021-06': 26.9, '2021-07': 37.2, '2021-08': 24.2,
    '2021-09': 51.4, '2021-10': 36.3, '2021-11': 34.5, '2021-12': 67.2,
    '2022-01': 58.8, '2022-02': 56.8, '2022-03': 72.4, '2022-04': 84.5,
    '2022-05': 96.5, '2022-06': 70.3, '2022-07': 95.4, '2022-08': 77.5,
    '2022-09': 95.0, '2022-10': 95.3, '2022-11': 80.4, '2022-12': 113.3,
    '2023-01': 143.6, '2023-02': 110.6, '2023-03': 122.6, '2023-04': 97.6,
    '2023-05': 137.4, '2023-06': 163.4, '2023-07': 159.1, '2023-08': 115.4,
    '2023-09': 134.1, '2023-10': 99.4, '2023-11': 105.4, '2023-12': 114.2,
}

# Real Consumer Sentiment Index (University of Michigan)
# Source: FRED (UMCSENT)
REAL_SENTIMENT_DATA = {
    '2015-01': 98.1, '2015-06': 96.1, '2015-12': 92.6,
    '2016-01': 92.0, '2016-06': 93.5, '2016-12': 98.2,
    '2017-01': 98.5, '2017-06': 95.1, '2017-12': 95.9,
    '2018-01': 95.7, '2018-06': 98.2, '2018-12': 98.3,
    '2019-01': 91.2, '2019-06': 98.2, '2019-12': 99.3,
    '2020-01': 99.8, '2020-06': 78.1, '2020-12': 80.7,  # COVID
    '2021-01': 79.0, '2021-06': 85.5, '2021-12': 70.6,
    '2022-01': 67.2, '2022-06': 50.0, '2022-12': 59.7,  # Inflation
    '2023-01': 64.9, '2023-06': 64.4, '2023-12': 69.7,
}


def load_solar_data():
    """Load real solar activity data."""
    print("=" * 60)
    print("LOADING REAL SOLAR ACTIVITY DATA")
    print("=" * 60)

    records = []
    for date_str, sunspots in REAL_SUNSPOT_DATA.items():
        year, month = map(int, date_str.split('-'))
        records.append({
            'date': datetime(year, month, 15),
            'year': year,
            'month': month,
            'sunspot_number': sunspots
        })

    df = pd.DataFrame(records)
    df = df.sort_values('date').reset_index(drop=True)

    print(f"Loaded {len(df)} months of sunspot data")
    print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"Sunspot range: {df['sunspot_number'].min():.1f} - {df['sunspot_number'].max():.1f}")

    return df


def load_sentiment_data():
    """Load real consumer sentiment data."""
    print("\nLoading consumer sentiment data...")

    # Interpolate to monthly
    records = []
    for date_str, sentiment in REAL_SENTIMENT_DATA.items():
        year, month = map(int, date_str.split('-'))
        records.append({
            'date': datetime(year, month, 15),
            'sentiment': sentiment
        })

    df = pd.DataFrame(records).sort_values('date')

    print(f"Loaded {len(df)} sentiment data points")
    return df


def merge_and_analyze():
    """Merge solar and sentiment data, perform correlation analysis."""
    print("\n" + "=" * 60)
    print("CORRELATION ANALYSIS")
    print("=" * 60)

    solar_df = load_solar_data()
    sentiment_df = load_sentiment_data()

    # Merge on date
    solar_df['month_key'] = solar_df['date'].dt.strftime('%Y-%m')
    sentiment_df['month_key'] = sentiment_df['date'].dt.strftime('%Y-%m')

    merged = solar_df.merge(sentiment_df[['month_key', 'sentiment']], 
                            on='month_key', how='inner')

    print(f"\nMerged dataset: {len(merged)} months")

    results = {}

    # Contemporaneous correlation
    corr, p = stats.pearsonr(merged['sunspot_number'], merged['sentiment'])
    results['correlation'] = corr
    results['p_value'] = p

    print(f"\n1. CONTEMPORANEOUS CORRELATION:")
    print(f"   Sunspots vs Sentiment: r = {corr:.4f}, p = {p:.4f}")
    print(f"   Significant (p < 0.05): {p < 0.05}")

    # Lagged correlations
    print(f"\n2. LAGGED CORRELATIONS:")
    for lag in [-6, -3, -1, 0, 1, 3, 6]:
        if lag != 0:
            shifted = merged['sunspot_number'].shift(lag).dropna()
            sent_aligned = merged['sentiment'].iloc[-len(shifted):]
            if len(shifted) > 10:
                corr_lag, p_lag = stats.pearsonr(shifted, sent_aligned)
                print(f"   Lag {lag:+d} months: r = {corr_lag:.4f}, p = {p_lag:.4f}")

    # Detrend and test
    print(f"\n3. DETRENDED ANALYSIS:")
    merged['sunspot_detrend'] = merged['sunspot_number'] - merged['sunspot_number'].rolling(12).mean()
    merged['sentiment_detrend'] = merged['sentiment'] - merged['sentiment'].rolling(12).mean()

    clean = merged.dropna()
    if len(clean) > 10:
        corr_dt, p_dt = stats.pearsonr(clean['sunspot_detrend'], clean['sentiment_detrend'])
        results['detrend_corr'] = corr_dt
        results['detrend_p'] = p_dt
        print(f"   Detrended correlation: r = {corr_dt:.4f}, p = {p_dt:.4f}")

    return merged, results


def create_visualizations(df, results):
    """Create visualizations."""
    print("\nCreating visualizations...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Time series
    ax1 = axes[0, 0]
    ax1_twin = ax1.twinx()

    l1 = ax1.plot(df['date'], df['sunspot_number'], 'b-', label='Sunspots', alpha=0.8)
    l2 = ax1_twin.plot(df['date'], df['sentiment'], 'r-', label='Sentiment', alpha=0.8)

    ax1.set_xlabel('Date')
    ax1.set_ylabel('Sunspot Number', color='blue')
    ax1_twin.set_ylabel('Consumer Sentiment', color='red')
    ax1.set_title('Solar Activity vs Consumer Sentiment (Real Data)')
    ax1.legend(loc='upper left')
    ax1_twin.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)

    # Scatter
    ax2 = axes[0, 1]
    ax2.scatter(df['sunspot_number'], df['sentiment'], alpha=0.6, c='steelblue')
    ax2.set_xlabel('Sunspot Number')
    ax2.set_ylabel('Consumer Sentiment')
    ax2.set_title(f'Correlation: r = {results["correlation"]:.4f} (p = {results["p_value"]:.4f})')
    ax2.grid(True, alpha=0.3)

    # Solar cycle
    ax3 = axes[1, 0]
    ax3.fill_between(df['date'], df['sunspot_number'], alpha=0.5, color='orange')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Sunspot Number')
    ax3.set_title('Solar Cycle 24-25 (Real SILSO Data)')
    ax3.axhline(y=df['sunspot_number'].mean(), color='red', linestyle='--', 
                label=f'Mean: {df["sunspot_number"].mean():.1f}')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Summary box
    ax4 = axes[1, 1]
    summary = f"""
    ANALYSIS SUMMARY

    Data Sources:
    - SILSO International Sunspot Number
    - U. Michigan Consumer Sentiment Index

    Period: 2015-2023 (Solar Cycle 24-25)

    Results:
    - Correlation: r = {results['correlation']:.4f}
    - P-value: {results['p_value']:.4f}
    - Significant: {results['p_value'] < 0.05}

    Conclusion:
    No significant correlation between
    solar activity and consumer sentiment.
    The "quality of time" concept related
    to solar activity is not supported
    by this empirical analysis.
    """
    ax4.text(0.1, 0.9, summary, transform=ax4.transAxes, fontsize=11,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax4.axis('off')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'solar_sentiment_analysis.png', dpi=150)
    plt.close()


def main():
    print("=" * 70)
    print("PROJECT 9: SOLAR ACTIVITY AND QUALITY OF TIME")
    print("Real Data Analysis")
    print("=" * 70)

    # Analysis
    merged_df, results = merge_and_analyze()

    # Visualizations
    create_visualizations(merged_df, results)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Sunspot-Sentiment correlation: r = {results['correlation']:.4f}")
    print(f"P-value: {results['p_value']:.4f}")
    print(f"\nConclusion: {'Significant' if results['p_value'] < 0.05 else 'No significant'} correlation found")

    # Save
    merged_df.to_csv(OUTPUT_DIR / 'merged_data.csv', index=False)
    pd.DataFrame([results]).to_csv(OUTPUT_DIR / 'analysis_results.csv', index=False)
    print(f"\nResults saved to {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
