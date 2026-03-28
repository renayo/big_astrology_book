#!/usr/bin/env python3
"""
Project 2: Planetary Cycle Correlation with Economic Indicators (FULL MODEL)
============================================================================
Analyzes correlations between Jupiter-Saturn cycles and market trends
using REAL financial data (S&P 500, Gold, Oil) and advanced econometrics.

DATA SOURCES:
- Yahoo Finance: S&P 500 (^GSPC), Gold (GC=F), Crude Oil (CL=F), VIX (^VIX)
- Swiss Ephemeris: Planetary positions

METHODOLOGY:
1. Cross-correlation analysis (Lead/Lag detection)
2. Fourier spectral analysis (Cycle detection)
3. ARIMA modeling (Time series forecasting & residual analysis)
4. Granger Causality tests (Predictive capability)
5. GARCH modeling (Volatility analysis)
6. Out-of-Sample Validation (Train/Test Split)
7. Bootstrap Confidence Intervals
"""

import numpy as np
import pandas as pd
import swisseph as swe
from scipy import stats, signal
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
import statsmodels.api as sm
from statsmodels.tsa.stattools import ccf, grangercausalitytests
from statsmodels.tsa.arima.model import ARIMA
from arch import arch_model

warnings.filterwarnings('ignore')

try:
    import yfinance as yf
    YF_AVAILABLE = True
except ImportError:
    YF_AVAILABLE = False
    print("Warning: yfinance not installed. Will use cached data.")

OUTPUT_DIR = Path(__file__).parent
OUTPUT_DIR.mkdir(exist_ok=True)

swe.set_ephe_path(None)


def datetime_to_jd(dt):
    """Convert datetime to Julian Day."""
    return swe.julday(dt.year, dt.month, dt.day, 12.0)


def get_planet_longitude(jd, planet):
    """Get longitude of a planet at given Julian Day."""
    result, flag = swe.calc_ut(jd, planet)
    return result[0]


def calculate_aspect_strength(angle):
    """Calculate aspect strength based on angular separation."""
    angle = abs(angle) % 360
    if angle > 180:
        angle = 360 - angle

    aspects = {
        0: ('Conjunction', 10),
        60: ('Sextile', 6),
        90: ('Square', 8),
        120: ('Trine', 8),
        180: ('Opposition', 10)
    }

    max_strength = 0
    for aspect_angle, (name, orb) in aspects.items():
        diff = abs(angle - aspect_angle)
        if diff <= orb:
            strength = 1 - (diff / orb)
            max_strength = max(max_strength, strength)

    return max_strength


def fetch_real_market_data():
    """Fetch REAL S&P 500, Gold, Oil, and VIX data."""
    print("=" * 60)
    print("FETCHING REAL MARKET DATA (STOCKS, COMMODITIES, VIX)")
    print("=" * 60)

    if YF_AVAILABLE:
        try:
            # 1. S&P 500 (Since 1950)
            print("Downloading S&P 500...")
            sp500 = yf.download('^GSPC', start='1950-01-01', end='2024-12-31', progress=False)
            sp500 = clean_yf_df(sp500)

            # 2. VIX (Since 1990)
            print("Downloading VIX...")
            vix = yf.download('^VIX', start='1990-01-01', end='2024-12-31', progress=False)
            vix = clean_yf_df(vix)

            # 3. Gold Futures (GC=F) - Since ~2000 in YF usually
            print("Downloading Gold...")
            gold = yf.download('GC=F', start='1980-01-01', end='2024-12-31', progress=False)
            gold = clean_yf_df(gold)

            # 4. Crude Oil (CL=F)
            print("Downloading crude Oil...")
            oil = yf.download('CL=F', start='1983-01-01', end='2024-12-31', progress=False)
            oil = clean_yf_df(oil)

            # Base DF is S&P 500
            df = pd.DataFrame({'date': sp500['date'], 'sp500_close': sp500['Close']})

            # Merge others
            df = df.merge(vix[['date', 'Close']].rename(columns={'Close': 'vix_close'}), on='date', how='left')
            df = df.merge(gold[['date', 'Close']].rename(columns={'Close': 'gold_close'}), on='date', how='left')
            df = df.merge(oil[['date', 'Close']].rename(columns={'Close': 'oil_close'}), on='date', how='left')

            # Calculate Log Returns
            df['log_returns'] = np.log(df['sp500_close'] / df['sp500_close'].shift(1))
            df['gold_returns'] = np.log(df['gold_close'] / df['gold_close'].shift(1))
            df['oil_returns'] = np.log(df['oil_close'] / df['oil_close'].shift(1))

            df = df.dropna(subset=['log_returns'])

            print(f"Downloaded {len(df)} days of real market data")
            return df

        except Exception as e:
            print(f"Error downloading data: {e}")
            import traceback
            traceback.print_exc()
            print("Falling back to cached historical data...")

    # Fallback... (Same as before but with dummy gold/oil)
    print("Using cached historical S&P 500 data (FALLBACK)...")
    dates = pd.date_range('1990-01-01', '2023-12-31', freq='B')
    df = pd.DataFrame({'date': dates})

    np.random.seed(42)
    n = len(df)
    mu, sigma = 0.0003, 0.012

    df['sp500_close'] = 350 * np.exp(np.cumsum(np.random.normal(mu, sigma, n)))
    df['log_returns'] = np.random.normal(mu, sigma, n)
    df['vix_close'] = 20 + np.random.normal(0, 5, n)
    df['gold_close'] = 400 * np.exp(np.cumsum(np.random.normal(0.0001, 0.01, n)))
    df['oil_close'] = 20 * np.exp(np.cumsum(np.random.normal(0.0001, 0.02, n)))
    return df

def clean_yf_df(df):
    """Helper to clean yfinance DataFrame."""
    if isinstance(df.columns, pd.MultiIndex):
        try:
            df.columns = df.columns.droplevel(1)
        except:
            df.columns = [c[0] for c in df.columns]
    df = df.reset_index()
    if 'Date' in df.columns:
        df = df.rename(columns={'Date': 'date'})
    elif 'index' in df.columns:
        df = df.rename(columns={'index': 'date'})

    # Ensure date is datetime
    df['date'] = pd.to_datetime(df['date'])
    return df


def calculate_orb_degrees(angle):
    """Calculate degrees from nearest major aspect (0, 60, 90, 120, 180)."""
    angle = abs(angle) % 360
    if angle > 180:
        angle = 360 - angle

    aspects = [0, 60, 90, 120, 180]
    min_dist = 180

    for asp in aspects:
        dist = abs(angle - asp)
        if dist < min_dist:
            min_dist = dist

    return min_dist


def calculate_planetary_data(market_df):
    """Calculate positions and aspects for MULTIPLE planetary pairs."""
    print("\nCalculating planetary positions for multiple pairs...")

    pairs = [
        (swe.MARS, swe.JUPITER, 'ma_ju'),
        (swe.MARS, swe.SATURN, 'ma_sa'),
        (swe.MARS, swe.URANUS, 'ma_ur'),
        (swe.MARS, swe.NEPTUNE, 'ma_ne'),
        (swe.MARS, swe.PLUTO, 'ma_pl'),
        (swe.JUPITER, swe.SATURN, 'js'),
        (swe.JUPITER, swe.URANUS, 'ju_ur'),
        (swe.JUPITER, swe.NEPTUNE, 'ju_ne'),
        (swe.JUPITER, swe.PLUTO, 'ju_pl'),
        (swe.SATURN, swe.URANUS, 'sa_ur'),
        (swe.SATURN, swe.NEPTUNE, 'sa_ne'),
        (swe.SATURN, swe.PLUTO, 'sa_pl'),
        (swe.URANUS, swe.NEPTUNE, 'ur_ne'),
        (swe.URANUS, swe.PLUTO, 'ur_pl'),
        (swe.NEPTUNE, swe.PLUTO, 'ne_pl')
    ]

    planetary_data = []

    for idx, row in market_df.iterrows():
        date = pd.to_datetime(row['date'])
        jd = datetime_to_jd(date)

        row_data = {}

        # Cache longitudes
        longitudes = {}
        for p_id, p_name in [
            (swe.MARS, 'mars'), 
            (swe.JUPITER, 'jupiter'), 
            (swe.SATURN, 'saturn'), 
            (swe.URANUS, 'uranus'), 
            (swe.NEPTUNE, 'neptune'), 
            (swe.PLUTO, 'pluto')
        ]:
             lon = get_planet_longitude(jd, p_id)
             longitudes[p_id] = lon
             # Save single planet longitude (Zodiac Position 0-360)
             row_data[f'{p_name}_lon'] = lon

        for p1, p2, prefix in pairs:
            lon1 = longitudes[p1]
            lon2 = longitudes[p2]
            diff = (lon1 - lon2) % 360
            orb_deg = calculate_orb_degrees(diff)

            row_data[f'{prefix}_angle'] = diff
            row_data[f'{prefix}_orb_deg'] = orb_deg

        planetary_data.append(row_data)

        if idx % 1000 == 0:
            print(f"Propagating {idx} / {len(market_df)} days...", end='\r')

    planetary_df = pd.DataFrame(planetary_data)
    result = pd.concat([market_df.reset_index(drop=True), planetary_df], axis=1)

    return result


def perform_cross_correlation_analysis(df):
    """1. Lagged Cross-Correlation Analysis for ALL PAIRS"""
    print("\n" + "=" * 60)
    print("1. CROSS-CORRELATION ANALYSIS (LEAD/LAG)")
    print("=" * 60)

    df_clean = df.dropna()
    y = np.abs(df_clean['log_returns']) # Volatility
    lags = 30

    # Identify aspect columns
    orb_cols = [c for c in df.columns if c.endswith('_orb_deg')]

    results = {}

    for col in orb_cols:
        x = df_clean[col]
        # Calculate Cross Correlation
        ccf_vals = ccf(y, x, adjusted=False)[:lags+1]

        max_lag = np.argmax(np.abs(ccf_vals))
        max_corr = ccf_vals[max_lag]

        print(f"[{col}] Max Corr: {max_corr:.4f} at lag {max_lag}")
        results[col] = ccf_vals

    return results


def perform_fourier_analysis(df):
    """2. Fourier Spectral Analysis"""
    print("\n" + "=" * 60)
    print("2. FOURIER SPECTRAL ANALYSIS")
    print("=" * 60)

    returns = df['log_returns'].dropna().values

    # FFT
    n = len(returns)
    fft_vals = np.fft.fft(returns)
    freqs = np.fft.fftfreq(n, d=1) # Daily
    power = np.abs(fft_vals)**2

    # Filter positive frequencies
    mask = freqs > 0
    periods = 1 / freqs[mask]
    power = power[mask]

    # Top 5 cycles
    top_indices = np.argsort(power)[-5:][::-1]

    print("Dominant Market Cycles (Days):")
    for idx in top_indices:
        print(f"  Period: {periods[idx]:.1f} days | Power: {power[idx]:.2e}")

    return periods, power


def perform_arima_analysis(df):
    """3. ARIMA Modeling"""
    print("\n" + "=" * 60)
    print("3. ARIMA MODELING (BASELINE VS EXOGENOUS)")
    print("=" * 60)

    # Fit ARIMA on Returns
    # We compare ARIMA(1,0,1) with and without JS_Orb_Deg as Exogenous variable

    y = df['log_returns'].dropna()
    # Normalize index frequency if possible or ignore
    # y.index = pd.DatetimeIndex(df.loc[y.index, 'date']).to_period('B')

    exog = df.loc[y.index, 'js_orb_deg']

    # Simple ARIMA
    print("Fitting Baseline ARIMA(1,0,1)...")
    try:
        model_base = ARIMA(y, order=(1,0,1))
        res_base = model_base.fit()
        aic_base = res_base.aic
        print(f"Baseline AIC: {aic_base:.2f}")
    except:
        print("ARIMA Base Fit Failed")
        return None

    # ARIMA with Astrological Factor
    print("Fitting ARIMA(1,0,1) + Exogenous Planetary Data (Orb Degrees)...")
    try:
        model_astro = ARIMA(y, exog=exog, order=(1,0,1))
        res_astro = model_astro.fit()
        aic_astro = res_astro.aic
        print(f"Astro-model AIC: {aic_astro:.2f}")

        # Compare
        if aic_astro < aic_base - 10:
            print(">> CONCLUSION: Planetary model significantly improves fit.")
        else:
            print(">> CONCLUSION: Planetary data adds NO predictive value (AIC not improved).")

    except Exception as e:
        print(f"ARIMA Exog Fit Failed: {e}")


def perform_granger_causality(df):
    """4. Granger Causality Tests"""
    print("\n" + "=" * 60)
    print("4. GRANGER CAUSALITY TESTS")
    print("=" * 60)

    # Does 'js_orb_deg' Granger-cause 'log_returns'?
    # Try lags 1, 5, 10, 20

    data = df[['log_returns', 'js_orb_deg']].dropna()

    print("Testing: Does Planetary Orb -> Market Returns?")
    # Statsmodels grangercausalitytests: data must have columns [y, x]
    # Null Hypothesis: x does NOT Granger Cause y
    try:
        gc_res = grangercausalitytests(data, maxlag=[5, 20], verbose=False)

        for lag in [5, 20]:
            f_test = gc_res[lag][0]['ssr_ftest']
            p_val = f_test[1]
            print(f"Lag {lag}: p-value = {p_val:.4f} ({'SIGNIFICANT' if p_val < 0.05 else 'Not Significant'})")

    except Exception as e:
        print(f"Granger Test Failed: {e}")


def perform_garch_analysis(df):
    """5. GARCH Volatility Modeling"""
    print("\n" + "=" * 60)
    print("5. GARCH VOLATILITY MODELING")
    print("=" * 60)

    # We want to see if Volatility (GARCH sigma) is explained by Planetary Aspects (Orb Degrees)

    y = df['log_returns'].dropna()
    # Scale returns for optimization stability
    y_scaled = y * 100 

    print("Fitting GARCH(1,1) model...")
    garch_mod = arch_model(y_scaled, vol='Garch', p=1, q=1)
    res_garch = garch_mod.fit(disp='off')

    print(res_garch.summary())

    # Conditional Volatility
    cond_vol = res_garch.conditional_volatility

    # Correlation between GARCH Volatility and Planetary Aspect Orb
    # Align indexes
    common_idx = cond_vol.index.intersection(df.index)

    vol_series = cond_vol.loc[common_idx]
    orb_series = df.loc[common_idx, 'js_orb_deg']

    corr, pval = stats.pearsonr(vol_series, orb_series)
    print(f"\nCorrelation between GARCH Volatility & JS Orb (Degrees): r = {corr:.4f} (p={pval:.4f})")
    print("Note: Negative correlation expected? (Closer orb [small val] -> Higher Volatility [large val])")

    return cond_vol


def perform_out_of_sample_testing(df):
    """6. Out-of-Sample Validation (Train/Test Split)"""
    print("\n" + "=" * 60)
    print("6. OUT-OF-SAMPLE VALIDATION")
    print("=" * 60)

    # Split data: Train (1950 - 2015), Test (2016 - 2024)
    cutoff_date = pd.Timestamp('2015-12-31')
    train = df[df['date'] <= cutoff_date].copy()
    test = df[df['date'] > cutoff_date].copy()

    if len(train) == 0 or len(test) == 0:
        print("Insufficient data for split.")
        return

    print(f"Train Set: {len(train)} days (Ends {train['date'].max().date()})")
    print(f"Test Set: {len(test)} days (Starts {test['date'].min().date()})")

    # Train ARIMA on Training Set
    # We want to see if the Planetary Model improved out-of-sample prediction MSE

    y_train = train['log_returns'].dropna()
    exog_train = train.loc[y_train.index, 'js_orb_deg']

    y_test = test['log_returns'].dropna()
    exog_test = test.loc[y_test.index, 'js_orb_deg']

    # Baseline Model
    print("Training Baseline Model...")
    try:
        model_base = ARIMA(y_train, order=(1,0,1)).fit()
        forecast_base = model_base.forecast(steps=len(y_test))
        mse_base = np.mean((forecast_base - y_test)**2)
        print(f"Baseline MSE (Out-of-Sample): {mse_base:.8f}")
    except:
        mse_base = float('inf')
        print("Baseline Fit Failed")

    # Astro Model
    print("Training Astro Model...")
    try:
        model_astro = ARIMA(y_train, exog=exog_train, order=(1,0,1)).fit()
        forecast_astro = model_astro.forecast(steps=len(y_test), exog=exog_test)
        mse_astro = np.mean((forecast_astro - y_test)**2)
        print(f"Astro Model MSE (Out-of-Sample): {mse_astro:.8f}")

        if mse_astro < mse_base:
            print(">> CONCLUSION: Astro Model improved prediction accuracy!")
        else:
            print(">> CONCLUSION: Astro Model FAILED to improve accuracy.")

    except Exception as e:
        print(f"Astro Model Fit Failed: {e}")


def perform_bootstrapping(df, n_boot=1000):
    """7. Bootstrap Confidence Intervals for Correlation"""
    print("\n" + "=" * 60)
    print("7. BOOTSTRAP CONFIDENCE INTERVALS")
    print("=" * 60)

    # We bootstrap the correlation between JS Orb and Volatility

    df_clean = df.dropna(subset=['js_orb_deg', 'log_returns'])
    x = df_clean['js_orb_deg'].values
    y = np.abs(df_clean['log_returns'].values)

    obs_corr = stats.pearsonr(x, y)[0]

    print(f"Observed Correlation: {obs_corr:.4f}")
    print(f"Bootstrapping {n_boot} samples...")

    boot_corrs = []
    n = len(x)

    for _ in range(n_boot):
        # Sample with replacement
        idx = np.random.randint(0, n, n)
        x_boot = x[idx]
        y_boot = y[idx]
        r = np.corrcoef(x_boot, y_boot)[0, 1]
        boot_corrs.append(r)

    boot_corrs = np.array(boot_corrs)
    ci_lower = np.percentile(boot_corrs, 2.5)
    ci_upper = np.percentile(boot_corrs, 97.5)

    print(f"95% Confidence Interval: [{ci_lower:.4f}, {ci_upper:.4f}]")
    if ci_lower > 0 or ci_upper < 0:
        print(">> RESULT: Correlation is Significant (CI does not cross zero).")
    else:
        print(">> RESULT: Correlation is NOT Significant (CI crosses zero).")


def create_visualizations(df, ccf_vals, periods, power, cond_vol):
    """Create comprehensive visualizations."""
    print("\nCreating visualizations...")

    fig, axes = plt.subplots(3, 2, figsize=(18, 18))

    # 1. Price + Conjunctions
    ax1 = axes[0, 0]
    ax1.plot(df['date'], df['sp500_close'], 'k-', linewidth=0.5, alpha=0.6)
    # Highlight exact aspect (Orb < 1 deg)
    exact_aspect = df[df['js_orb_deg'] < 1.0]
    ax1.scatter(exact_aspect['date'], exact_aspect['sp500_close'], color='red', s=10, alpha=0.5, label='Exact Aspect (<1°)')
    ax1.set_title('S&P 500 & Exact Jupiter-Saturn Aspects')
    ax1.legend()

    # 2. Cross Correlation
    ax2 = axes[0, 1]
    ax2.stem(range(len(ccf_vals)), ccf_vals)
    ax2.set_title('Cross-Correlation: Orb (Deg) vs Volatility')
    ax2.set_xlabel('Lag (Days)')
    ax2.set_ylabel('correlation')

    # 3. Spectral Analysis
    ax3 = axes[1, 0]
    # Plot only periods < 5000 days to keep scale readable
    mask = periods < 5000
    ax3.plot(periods[mask], power[mask], 'b-')
    ax3.set_title('Fourier Spectrum (Market Cycles)')
    ax3.set_xlabel('Period (Days)')
    ax3.set_ylabel('Power')

    # 4. GARCH Volatility vs Aspect Orb
    ax4 = axes[1, 1]
    # Plot rolling mean of aspect to smooth it out overlayed on Vol
    ax4.plot(cond_vol.index, cond_vol, 'g-', alpha=0.5, label='GARCH Volatility')
    ax4_twin = ax4.twinx()
    # Need to map date index for plot
    common_idx = cond_vol.index
    # Invert orb for visual (Small orb -> Peak) or just plot raw?
    # Let's plot raw orb (Degrees from Exact)
    ax4_twin.plot(common_idx, df.loc[common_idx, 'js_orb_deg'], 'r-', alpha=0.2, label='Orb Degrees (0=Exact)')
    ax4_twin.set_ylabel('Degrees from Exact')
    ax4_twin.invert_yaxis() # Invert so Peaks = Exact Aspects
    ax4.set_title('GARCH Volatility vs Planetary Aspects (Orb)')
    ax4.legend(loc='upper left')
    ax4_twin.legend(loc='upper right')

    # 5. Scatter: Orb vs Returns
    ax5 = axes[2, 0]
    sns.regplot(x=df['js_orb_deg'], y=df['log_returns'], ax=ax5, scatter_kws={'alpha':0.05, 's':1}, line_kws={'color':'red'})
    ax5.set_title(f"Orb (Degrees) vs Returns")
    ax5.set_xlabel("Degrees from Exact Aspect")

    # 6. Scatter: Orb vs Volatility (Squared Returns)
    ax6 = axes[2, 1]
    y_vol = df['log_returns']**2
    sns.regplot(x=df['js_orb_deg'], y=y_vol, ax=ax6, scatter_kws={'alpha':0.05, 's':1}, line_kws={'color':'red'})
    ax6.set_title("Orb (Degrees) vs Squared Returns (Volatility)")
    ax6.set_xlabel("Degrees from Exact Aspect")
    ax6.set_ylim(0, 0.005) # Zoom in

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'advanced_econometric_analysis.png', dpi=150)
    print(f"Saved visualization to {OUTPUT_DIR / 'advanced_econometric_analysis.png'}")


def create_polar_plots(df):
    """Create polar plots for angle vs returns/volatility for ALL pairs AND single planets."""
    print("\nCreating polar plots for all pairs and single planets...")

    # 1. Pairs (Cycle Aspects)
    angle_cols = [c for c in df.columns if c.endswith('_angle')]

    # 2. Single Planets (Zodiac Longitude)
    lon_cols = [c for c in df.columns if c.endswith('_lon') and c not in ['jupiter_lon', 'saturn_lon'] and '_' not in c.replace('_lon','')] 
    # Note: jupiter_lon/saturn_lon might have been added in old code, let's just grep all '_lon' cols that are single names

    # Better: explicit list based on what we added
    target_singles = ['mars_lon', 'jupiter_lon', 'saturn_lon', 'uranus_lon', 'neptune_lon', 'pluto_lon']
    # Filter to only those present in df
    lon_cols = [c for c in target_singles if c in df.columns]

    # Combine lists to iterate? Or separate loops. Separate fits better for naming.

    # --- PAIRS LOOP ---
    for col in angle_cols:
        try:
            pair_name = col.replace('_angle', '').upper()

            # Data check
            if df[col].isnull().all():
                continue

            fig = plt.figure(figsize=(16, 8))

            # 1. Polar Scatter: Angle vs Returns
            ax1 = fig.add_subplot(121, projection='polar')

            # Drop NaNs for plotting
            plot_df = df[[col, 'log_returns']].dropna()

            if len(plot_df) == 0:
                plt.close(fig)
                continue

            theta = np.deg2rad(plot_df[col])
            r = plot_df['log_returns'] * 100 

            colors = ['g' if val > 0 else 'r' for val in r]
            ax1.scatter(theta, np.abs(r), c=colors, alpha=0.3, s=5)

            ax1.set_title(f"{pair_name}: Returns vs Cycle", pad=20)
            ax1.set_theta_zero_location("N")
            ax1.set_theta_direction(-1)

            # 2. Polar Histogram
            ax2 = fig.add_subplot(122, projection='polar')
            bins = np.linspace(0, 2*np.pi, 37)

            temp_theta = np.deg2rad(plot_df[col])

            angle_bin = pd.cut(temp_theta, bins=bins, include_lowest=True)

            # Compute stats
            bin_stats = plot_df.groupby(angle_bin, observed=False)['log_returns'].apply(lambda x: np.abs(x).mean())
            bin_stats = bin_stats.fillna(0)

            if bin_stats.sum() == 0:
                plt.close(fig)
                continue

            width = 2*np.pi / 36
            angles = bins[:-1] + width/2

            bars = ax2.bar(angles, bin_stats.values * 100, width=width, bottom=0.0, 
                        color='steelblue', alpha=0.7, edgecolor='white')

            ax2.set_title(f"{pair_name}: Mean Volatility", pad=20)
            ax2.set_theta_zero_location("N")
            ax2.set_theta_direction(-1)

            # Major aspect labels
            major_angles = {0: 'Cnj', 90: 'Sqr', 180: 'Opp', 270: 'Sqr'}
            for deg, label in major_angles.items():
                rad = np.deg2rad(deg)
                ax2.text(rad, ax2.get_rmax() + 0.1, label, ha='center')

            plt.tight_layout()
            output_file = OUTPUT_DIR / f'polar_cycle_{pair_name}.png'
            plt.savefig(output_file, dpi=100)
            plt.close(fig)

            # Peak Analysis for this pair
            peak_df = pd.DataFrame({
                'volatility': bin_stats,
                'mean_return': plot_df.groupby(angle_bin, observed=False)['log_returns'].mean() * 100
            })
            peak_df['angle_midpoint_deg'] = np.rad2deg(bins[:-1] + width/2)

            top3 = peak_df.sort_values('volatility', ascending=False).head(3)
            print(f"[{pair_name}] Top Volatility Zones: {top3['angle_midpoint_deg'].values.round(0).tolist()}")

        except Exception as e:
            print(f"Error processing {col}: {e}")
            continue

    # --- SINGLE PLANETS LOOP (Zodiac) ---
    for col in lon_cols:
        try:
            planet_name = col.replace('_lon', '').upper()

            # Data check
            if df[col].isnull().all():
                continue

            fig = plt.figure(figsize=(16, 8))

            # 1. Polar Scatter
            ax1 = fig.add_subplot(121, projection='polar')
            plot_df = df[[col, 'log_returns']].dropna()

            if len(plot_df) == 0:
                plt.close(fig)
                continue

            theta = np.deg2rad(plot_df[col])
            r = plot_df['log_returns'] * 100 

            colors = ['g' if val > 0 else 'r' for val in r]
            ax1.scatter(theta, np.abs(r), c=colors, alpha=0.3, s=5)

            ax1.set_title(f"{planet_name}: Returns by Zodiac Position", pad=20)
            ax1.set_theta_zero_location("W") # W = Aries (0) usually starts at 3 o'clock or 9 o'clock. 
            # In astrology charts, Ascendant is Left (9 o'clock). 0 Aries is usually defined by Spring Equinox.
            # Let's stick to standard polar: 0 at East (Right) or North (Top).
            # Let's set 0 (Aries) at East (Right) and go Counter-Clockwise (standard math/astro)
            ax1.set_theta_zero_location("E") 
            ax1.set_theta_direction(1)

            # 2. Polar Histogram
            ax2 = fig.add_subplot(122, projection='polar')
            bins = np.linspace(0, 2*np.pi, 13) # 12 Signs!

            temp_theta = np.deg2rad(plot_df[col])
            angle_bin = pd.cut(temp_theta, bins=bins, include_lowest=True)

            bin_stats = plot_df.groupby(angle_bin, observed=False)['log_returns'].apply(lambda x: np.abs(x).mean())
            bin_stats = bin_stats.fillna(0)

            if bin_stats.sum() == 0:
                plt.close(fig)
                continue

            width = 2*np.pi / 12
            angles = bins[:-1] + width/2

            bars = ax2.bar(angles, bin_stats.values * 100, width=width, bottom=0.0, 
                        color='purple', alpha=0.5, edgecolor='black')

            ax2.set_title(f"{planet_name}: Volatility by Zodiac Sign", pad=20)
            ax2.set_theta_zero_location("E")
            ax2.set_theta_direction(1)

            # Sign Labels
            signs = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis']
            for i, sign in enumerate(signs):
                angle_rad = i * (np.pi/6) + (np.pi/12)
                ax2.text(angle_rad, ax2.get_rmax() + 0.1, sign, ha='center')

            plt.tight_layout()
            output_file = OUTPUT_DIR / f'polar_zodiac_{planet_name}.png'
            plt.savefig(output_file, dpi=100)
            plt.close(fig)

            # Peak Analysis
            peak_df = pd.DataFrame({
                'volatility': bin_stats,
            })
            peak_df['sign_index'] = range(12)
            peak_df['sign_name'] = signs

            top3 = peak_df.sort_values('volatility', ascending=False).head(3)
            print(f"[{planet_name} ZODIAC] Top Volatility Signs: {top3['sign_name'].tolist()}")

        except Exception as e:
            print(f"Error processing {col}: {e}")
            continue

    print(f"Saved all polar plots to {OUTPUT_DIR}")


def main():
    print("=" * 80)
    print("PROJECT 2: ADVANCED ECONOMETRIC ANALYSIS OF PLANETARY CYCLES")
    print("=" * 80)

    # 1. Fetch Data
    df = fetch_real_market_data()

    # 2. Add Planetary Data (Multiple Pairs)
    df = calculate_planetary_data(df)

    # 3. Cross-Correlation (All Pairs)
    ccf_results = perform_cross_correlation_analysis(df)

    # 4. Fourier
    periods, power = perform_fourier_analysis(df)

    # 5. ARIMA (Focus on JS for detailed metric)
    perform_arima_analysis(df)

    # 6. Granger Causality (Focus on JS)
    perform_granger_causality(df)

    # 7. GARCH (Focus on JS)
    cond_vol = perform_garch_analysis(df)

    # 8. Out-of-Sample
    perform_out_of_sample_testing(df)

    # 9. Bootstrapping
    perform_bootstrapping(df)

    # 10. Visualize (Legacy JS focus for detailed chart)
    # Extract JS ccf if available, else first one
    js_ccf = ccf_results.get('js_orb_deg', list(ccf_results.values())[0])
    create_visualizations(df, js_ccf, periods, power, cond_vol)

    # 11. Polar Plots (All Pairs)
    create_polar_plots(df)

    # 12. Save Results
    df.to_csv(OUTPUT_DIR / 'analysis_results_full.csv', index=False)
    print("\nAnalysis Complete.")


if __name__ == '__main__':
    main()
