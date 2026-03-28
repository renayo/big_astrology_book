import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import glob

def analyze_temperature(data_dir, lunar_file, max_files=100):
    print("Loading lunar data...")
    lunar_df = pd.read_csv(lunar_file)
    lunar_df['date'] = pd.to_datetime(lunar_df['date'])
    lunar_map = lunar_df.set_index('date')['tithi'].to_dict()

    # Accumulators for TMAX
    tithi_temp_sum = {i: 0.0 for i in range(1, 31)}
    tithi_temp_count = {i: 0 for i in range(1, 31)}

    # Get weather files
    files = glob.glob(os.path.join(data_dir, "*.csv"))
    # Picking a different subset or the same subset? 
    # Let's verify using more files if possible, or the same max_files
    files_to_process = files[:max_files]

    print(f"Found {len(files)} weather files. Processing first {len(files_to_process)}...")

    processed_count = 0
    total_records = 0

    for file_path in files_to_process:
        try:
            # Read TMAX. TMAX is in tenths of degrees C.
            # We filter for TMAX not null.
            df = pd.read_csv(file_path, usecols=['DATE', 'TMAX'])
            df['DATE'] = pd.to_datetime(df['DATE'])

            df = df.dropna(subset=['TMAX'])

            # Map Tithi
            df['tithi'] = df['DATE'].map(lunar_map)
            df = df.dropna(subset=['tithi'])

            if df.empty:
                continue

            # Group by tithi
            file_grouped = df.groupby('tithi')['TMAX'].agg(['sum', 'count'])

            for tithi, row in file_grouped.iterrows():
                tithi = int(tithi)
                if 1 <= tithi <= 30:
                    tithi_temp_sum[tithi] += row['sum']
                    tithi_temp_count[tithi] += row['count']

            total_records += len(df)
            processed_count += 1

            if processed_count % 10 == 0:
                print(f"Processed {processed_count} files...")

        except Exception as e:
            # Some files might not have TMAX column
            # print(f"Skipping {file_path}: {e}")
            continue

    print(f"Finished processing. Total records used: {total_records}")

    # Calculate averages
    results = []
    for tithi in range(1, 31):
        total_t = tithi_temp_sum[tithi]
        count_t = tithi_temp_count[tithi]
        avg_t = total_t / count_t if count_t > 0 else 0
        results.append({
            'tithi': tithi,
            'avg_tmax_tenths_c': avg_t,
            'avg_tmax_c': avg_t / 10.0,
            'count': count_t
        })

    results_df = pd.DataFrame(results)

    # Save results
    output_path = os.path.join(os.path.dirname(__file__), 'temperature_by_tithi.csv')
    results_df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(results_df['tithi'], results_df['avg_tmax_c'], marker='s', linestyle='-', color='red')
    plt.title(f'Average Max Temperature by Lunar Day (Tithi) - Sample of {processed_count} Stations')
    plt.xlabel('Lunar Day (Tithi) [1-30]')
    plt.ylabel('Avg Max Temp (°C)')
    plt.grid(True, alpha=0.3)
    plt.xticks(range(1, 31))

    # Add Moon Phases markers
    plt.axvline(x=1, color='k', linestyle='--', alpha=0.5, label='New Moon')
    plt.axvline(x=15, color='k', linestyle='--', alpha=0.5, label='Full Moon')
    plt.axvline(x=30, color='k', linestyle='--', alpha=0.5, label='New Moon')
    plt.legend()

    plot_path = os.path.join(os.path.dirname(__file__), 'temperature_plot.png')
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, 'daily-summaries-latest')
    lunar_file = os.path.join(current_dir, 'lunar_data.csv')

    analyze_temperature(data_dir, lunar_file, max_files=200)
