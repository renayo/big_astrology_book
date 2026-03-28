import pandas as pd
import numpy as np
import swisseph as swe
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy.stats import f_oneway, spearmanr

# Setup
swe.set_ephe_path(None)
DATA_FILE = Path("37-planetary-cycles-mood-surveys/umcsent.csv")
OUTPUT_DIR = Path("37-planetary-cycles-mood-surveys")

def get_monthly_astro_features(year, month):
    """
    Calculates astrological features for a given month.
    Uses the 15th of the month as the representative 'center' for slow moving points.
    For fast moving (Merc Rx), calculates the fraction of the month.
    """
    # Mid-month date
    dt_mid = datetime(year, month, 15)
    jd_mid = swe.julday(year, month, 15, 12.0)
    
    # Mercury Rx Fraction
    # Check every 2 days
    rx_days = 0
    total_samples = 0
    
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
    days_in_month = (end_date - start_date).days + 1
    
    # Sampling for Rx
    for d in range(1, days_in_month + 1, 2): # Check every other day for speed
        d_jd = swe.julday(year, month, d, 12.0)
        res = swe.calc_ut(d_jd, swe.MERCURY, swe.FLG_SWIEPH | swe.FLG_SPEED)
        if res[0][3] < 0: # Speed negative
            rx_days += 1
        total_samples += 1
        
    rx_fraction = rx_days / total_samples
    
    # Slow Moving Features (at mid-month)
    # 1. Vedic Sun Sign (Sidereal)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags_sid = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    
    sun_sid = swe.calc_ut(jd_mid, swe.SUN, flags_sid)[0][0]
    vedic_sun_sign = int(sun_sid / 30)
    
    # 2. Jupiter - Saturn Angle (Tropical/Sidereal same for angle)
    jup = swe.calc_ut(jd_mid, swe.JUPITER, swe.FLG_SWIEPH)[0][0]
    sat = swe.calc_ut(jd_mid, swe.SATURN, swe.FLG_SWIEPH)[0][0]
    
    # Shortest arc
    angle = abs(jup - sat)
    if angle > 180: angle = 360 - angle
    
    # 3. Mars Position (Sidereal)
    mars_sid = swe.calc_ut(jd_mid, swe.MARS, flags_sid)[0][0]
    
    # 4. Vedic Lunar Month (Approximation based on Sun Sign + Moon constellational theory? 
    # Actually, simpler: Vedic Solar Month is just the Sun Sign)
    
    return {
        'vedic_sun_sign': vedic_sun_sign, # 0=Mesha/Aries
        'jup_sat_angle': angle,
        'merc_rx_fraction': rx_fraction,
        'is_merc_rx_dominant': 1 if rx_fraction > 0.5 else 0,
        'mars_sign': int(mars_sid / 30)
    }

def main():
    print("Loading Real Mood Data (UMCSENT)...")
    if not DATA_FILE.exists():
        print(f"File {DATA_FILE} not found. Run the curl command.")
        return

    df = pd.read_csv(DATA_FILE)
    df = df.dropna(subset=['UMCSENT']) # Drop missing quarters
    # Convert . to NaN just in case
    df['UMCSENT'] = pd.to_numeric(df['UMCSENT'], errors='coerce')
    df = df.dropna()
    
    print(f"Loaded {len(df)} monthly records (1952-Present).")
    
    astro_rows = []
    
    for _, row in df.iterrows():
        dt = datetime.strptime(row['observation_date'], "%Y-%m-%d")
        feats = get_monthly_astro_features(dt.year, dt.month)
        astro_rows.append(feats)
        
    astro_df = pd.DataFrame(astro_rows)
    full_df = pd.concat([df.reset_index(drop=True), astro_df.reset_index(drop=True)], axis=1)
    
    print("\n--- Analysis of REAL Data ---")
    
    # 1. Mercury Retrograde
    # Do months with heavy Mercury Rx have lower sentiment?
    print("\n1. Mercury Retrograde Effect")
    rx_mean = full_df[full_df['is_merc_rx_dominant'] == 1]['UMCSENT'].mean()
    norx_mean = full_df[full_df['is_merc_rx_dominant'] == 0]['UMCSENT'].mean()
    print(f"Rx Dominant Month Mean: {rx_mean:.2f}")
    print(f"Direct Month Mean: {norx_mean:.2f}")
    t_stat, p_rx = f_oneway(full_df[full_df['is_merc_rx_dominant'] == 1]['UMCSENT'], 
                            full_df[full_df['is_merc_rx_dominant'] == 0]['UMCSENT'])
    print(f"ANOVA p-value: {p_rx:.4f}")
    
    # 2. Vedic Sun Sign (Seasonality + Precession)
    print("\n2. Vedic Sun Sign (Mesha=0 to Meena=11)")
    print(full_df.groupby('vedic_sun_sign')['UMCSENT'].mean())
    # Plot
    plt.figure(figsize=(10, 5))
    sign_means = full_df.groupby('vedic_sun_sign')['UMCSENT'].mean()
    sns.barplot(x=sign_means.index, y=sign_means.values, palette='viridis')
    plt.ylim(sign_means.min() - 5, sign_means.max() + 5)
    plt.title("Consumer Sentiment by Vedic Sun Sign")
    plt.xlabel("Sign (0=Aries, 11=Pisces)")
    plt.ylabel("Sentiment Index")
    plt.savefig(OUTPUT_DIR / "real_mood_vedic_sun.png")
    
    # 3. Jupiter-Saturn Cycle (Economic Cycle)
    # Correlation
    corr, p_corr = spearmanr(full_df['jup_sat_angle'], full_df['UMCSENT'])
    print(f"\n3. Jupiter-Saturn Angle Correlation: r={corr:.4f}, p={p_corr:.4f}")
    
    # Plot Jupiter-Saturn
    plt.figure(figsize=(10, 5))
    sns.scatterplot(x=full_df['jup_sat_angle'], y=full_df['UMCSENT'], alpha=0.5)
    sns.regplot(x=full_df['jup_sat_angle'], y=full_df['UMCSENT'], scatter=False, color='red')
    plt.title(f"Jupiter-Saturn Angle vs Consumer Sentiment (r={corr:.2f})")
    plt.xlabel("Angle (0 = Conjunction, 180 = Opposition)")
    plt.ylabel("Sentiment Index")
    plt.savefig(OUTPUT_DIR / "real_mood_jup_sat.png")
    
    # Save processed
    full_df.to_csv(OUTPUT_DIR / "real_data_processed.csv", index=False)
    print("Completed.")

if __name__ == "__main__":
    main()

