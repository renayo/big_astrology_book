import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from datetime import datetime
import concurrent.futures
import time

def process_weather_chunk(args):
    """
    Process a list of weather files and return aggregation.
    args: (file_list, valid_dates_set)
    """
    files, valid_dates_list = args
    # Create valid_dates_set for fast lookup
    # Actually, we want to align to a common index.
    # Let's create a local series for alignment

    # Initialize accumulators
    # We use a dictionary for sparse accumulation then convert to Series
    # Or just use a common index if we pass it? Passing index is heavy.
    # Let's return a dict: {date: [sum_p, count_p, sum_t, count_t]}
    # Or better: {date: (sum_p, count_p, sum_t, count_t)}

    local_data = {}

    valid_dates = set(valid_dates_list)

    for f in files:
        try:
            # Read only needed cols
            df = pd.read_csv(f, usecols=['DATE', 'PRCP', 'TMAX'])
            df = df.dropna(subset=['DATE'])

            # Filter rows
            df = df[df['DATE'].isin(valid_dates)]
            if df.empty:
                continue

            # Iterate rows is slow. Vectorized?
            # Group by DATE and sum (handle duplicates if any)
            # Actually simplest: set index date.

            # Prcp
            p_df = df[['DATE', 'PRCP']].dropna().set_index('DATE')
            t_df = df[['DATE', 'TMAX']].dropna().set_index('DATE')

            # Iterate unique dates present in this file
            # This is the slow part in Python loop. 
            # But accumulating into a big aligned DF is fast if we use add.
            # But we can't create a big DF in every worker.

            # Optimization: Return the raw summed frames for this chunk? 
            # If chunk is 500 files.
            # We can aggregate inside the chunk using a DataFrame.
            pass
        except:
            continue

    # BETTER APPROACH for Chunking:
    # Initialize a DF with the index
    chunk_idx = pd. Index(valid_dates_list)
    chunk_agg = pd.DataFrame(0.0, index=chunk_idx, columns=['sum_p', 'count_p', 'sum_t', 'count_t'])

    for f in files:
        try:
            df = pd.read_csv(f, usecols=['DATE', 'PRCP', 'TMAX'])
            df = df[df['DATE'].isin(valid_dates)]

            p = df[['DATE', 'PRCP']].dropna().set_index('DATE')
            if not p.empty:
                # Group by date to handle dups
                p = p.groupby('DATE')['PRCP'].sum() # Sum duplicates? Or mean? daily summary implies one.
                # Actually, duplicate dates in one file is rare/error.

                # Align and add
                # Reindex to ensure alignment (fast if mostly aligned)
                # Intersection logic
                common = p.index.intersection(chunk_agg.index)
                if not common.empty:
                    chunk_agg.loc[common, 'sum_p'] += p.loc[common]
                    chunk_agg.loc[common, 'count_p'] += 1

            t = df[['DATE', 'TMAX']].dropna().set_index('DATE')
            if not t.empty:
                # Rename to avoid confusion with agg cols
                common_t = t.index.intersection(chunk_agg.index)
                if not common_t.empty:
                    chunk_agg.loc[common_t, 'sum_t'] += t.loc[common_t]['TMAX']
                    chunk_agg.loc[common_t, 'count_t'] += 1

        except Exception:
            continue

    return chunk_agg

class GlobalWeatherAnalyzer:
    def __init__(self, data_dir, astro_file, metadata_file=None):
        self.data_dir = data_dir
        self.astro_file = astro_file
        self.metadata_file = metadata_file
        self.astro_df = None
        self.weather_df = None
        self.station_latitudes = {}

    def load_metadata(self):
        if not self.metadata_file or not os.path.exists(self.metadata_file):
            print("Metadata file not found. Skipping latitude filter.")
            return

        print(f"Loading station metadata from {self.metadata_file}...")
        # Dictionary id -> lat
        count = 0
        with open(self.metadata_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    st_id = parts[0]
                    try:
                        lat = float(parts[1])
                        self.station_latitudes[st_id] = lat
                        count += 1
                    except ValueError:
                        continue
        print(f"Loaded {count} station latitudes.")

    def load_astro_data(self):
        print("Loading astrological features...")
        self.astro_df = pd.read_csv(self.astro_file)
        # Ensure unique dates
        self.astro_df = self.astro_df.drop_duplicates(subset=['date'])

    def aggregate_weather_data(self, file_limit=None, hemisphere=None):
        # Determine prefix for checkpoint/output based on hemisphere
        hemisphere_tag = "Full"
        if hemisphere == 'north': hemisphere_tag = "North"
        if hemisphere == 'south': hemisphere_tag = "South"

        # Check for checkpoint if full run
        checkpoint_file = os.path.join(self.data_dir, f'../weather_data_{hemisphere_tag}_checkpoint.csv')
        if file_limit is None and os.path.exists(checkpoint_file):
             print(f"Loading {hemisphere_tag} data from checkpoint: {checkpoint_file}")
             self.weather_df = pd.read_csv(checkpoint_file)
             return

        files = glob.glob(os.path.join(self.data_dir, "*.csv"))

        if hemisphere and self.station_latitudes:
            print(f"Filtering stations for {hemisphere} hemisphere...")
            filtered_files = []
            for f in files:
                filename = os.path.basename(f)
                st_id = filename.replace('.csv', '')
                lat = self.station_latitudes.get(st_id)

                if lat is not None:
                    if hemisphere == 'north' and lat > 0:
                        filtered_files.append(f)
                    elif hemisphere == 'south' and lat < 0:
                        filtered_files.append(f)

            files = filtered_files
            print(f"Found {len(files)} stations in {hemisphere} hemisphere.")

        total_files = len(files)

        if file_limit:
            files = files[:file_limit]
            print(f"Processing subset of {len(files)} weather stations (User Limit)...")
        else:
            print(f"Processing ALL {len(files)} weather stations...")

        dates = self.astro_df['date'].values

        # Determine chunk size
        # 130k files. 
        # If we have 4 cores, we want maybe 20 chunks to keep load balanced?
        # Or just fixed size. 1000 files per chunk.
        chunk_size = 2000
        chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

        print(f"Split into {len(chunks)} chunks of ~{chunk_size} files.")
        print("Starting parallel aggregation...")

        # Accumulator
        grand_agg = pd.DataFrame(0.0, index=dates, columns=['sum_p', 'count_p', 'sum_t', 'count_t'])

        start_time = time.time()

        # Use ProcessPoolExecutor
        # Note: We pass dates list, which is pickled. It's not too big.

        # Function arguments must be picklable
        worker_args = [(chunk, dates) for chunk in chunks]

        with concurrent.futures.ProcessPoolExecutor() as executor:
            # Map returns results in order
            for i, chunk_result in enumerate(executor.map(process_weather_chunk, worker_args)):
                # Add to grand total
                # Indices match exactly because we passed dates
                grand_agg += chunk_result

                elapsed = time.time() - start_time
                progress = (i + 1) / len(chunks) if len(chunks) > 0 else 1
                print(f"Processed Chunk {i+1}/{len(chunks)} ({progress:.1%}) - Elapsed: {elapsed:.0f}s")

        print(f"Finished aggregation. Total time: {time.time() - start_time:.1f}s")

        # Calculate daily averages
        # Avoid division by zero
        grand_agg['avg_prcp'] = grand_agg['sum_p'].divide(grand_agg['count_p']).replace([np.inf, -np.inf], 0)
        grand_agg['avg_tmax'] = grand_agg['sum_t'].divide(grand_agg['count_t']).replace([np.inf, -np.inf], 0)

        self.weather_df = grand_agg.reset_index().rename(columns={'index': 'date'})

        # Save checkpoint
        self.weather_df.to_csv(checkpoint_file, index=False)
        print(f"Checkpoint saved to {checkpoint_file}")

    def analyze_correlations(self):
        print("Merging astro and weather data...")
        # Merge
        merged = pd.merge(self.weather_df, self.astro_df, on='date', how='inner')

        # Features to check
        # List of lists [Body, System]
        bodies = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 
                 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'NorthNode', 'SouthNode']
        systems = ['Trop', 'Vedic']

        results = []

        # Map for Elements
        # 0: Fire, 1: Earth, 2: Air, 3: Water
        # Sign % 4 gives: 0 (Aries-Fire), 1 (Taurus-Earth), 2 (Gem-Air), 3 (Can-Water) -> Wait.
        # Fire: 0, 4, 8. 0%4=0, 4%4=0, 8%4=0. Correct.
        # Earth: 1, 5, 9. 1%4=1. Correct.
        # Air: 2, 6, 10. 2%4=2. Correct.
        # Water: 3, 7, 11. 3%4=3. Correct.
        elements = ['Fire', 'Earth', 'Air', 'Water']

        print("Running statistical analysis...")

        for body in bodies:
            for sys in systems:
                sign_col = f'{body}_{sys}_Sign'

                if sign_col not in merged.columns:
                    continue

                # 1. Analyze by Sign (0-11)
                grp = merged.groupby(sign_col)[['avg_prcp', 'avg_tmax']].mean()

                # Check for "Water Sign" effect specifically
                # Water signs are 3, 7, 11
                water_signs = [3, 7, 11]
                water_mask = merged[sign_col].isin(water_signs)

                avg_p_water = merged[water_mask]['avg_prcp'].mean()
                avg_p_non_water = merged[~water_mask]['avg_prcp'].mean()

                avg_t_water = merged[water_mask]['avg_tmax'].mean()

                results.append({
                    'Feature': f'{body} ({sys})',
                    'Water_Prcp': avg_p_water,
                    'NonWater_Prcp': avg_p_non_water,
                    'Diff_Prcp': avg_p_water - avg_p_non_water,
                    'Effect_Type': 'Sign'
                })

                # 2. Analyze by Element
                # Create element column on the fly
                merged['temp_elem'] = merged[sign_col] % 4
                elem_grp = merged.groupby('temp_elem')[['avg_prcp', 'avg_tmax']].mean()

                for elem_id, row in elem_grp.iterrows():
                    elem_name = elements[int(elem_id)]
                    results.append({
                        'Feature': f'{body} ({sys})',
                        'Element': elem_name,
                        'Avg_Prcp': row['avg_prcp'],
                        'Avg_Tmax': row['avg_tmax'],
                        'Effect_Type': 'Element_Avg'
                    })

        return pd.DataFrame(results)

def main():
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, 'daily-summaries-latest')
    astro_file = os.path.join(current_dir, 'astro_weather_features.csv')
    metadata_file = os.path.join(current_dir, 'ghcnd-stations.txt')

    analyzer = GlobalWeatherAnalyzer(data_dir, astro_file, metadata_file)
    analyzer.load_astro_data()
    analyzer.load_metadata()

    # Run loop for hemispheres
    hemispheres = ['north', 'south']

    for hem in hemispheres:
        print(f"\n\n====================================")
        print(f"STARTING ANALYSIS: {hem.upper()} HEMISPHERE")
        print(f"====================================")

        # Reset weather_df to force reload/re-aggregate
        analyzer.weather_df = None

        # Using full data but filtered by hemisphere
        analyzer.aggregate_weather_data(file_limit=None, hemisphere=hem)

        results = analyzer.analyze_correlations()

        out_csv = os.path.join(current_dir, f'full_analysis_results_{hem}.csv')
        results.to_csv(out_csv, index=False)
        print(f"Results saved to {out_csv}")

        # Filter for Water Signals
        water_stats = results[results['Effect_Type'] == 'Sign'].sort_values('Diff_Prcp', ascending=False)
        print(f"\n--- Top Water Sign Precipitation Increases ({hem.upper()} Hemisphere) ---")
        print(water_stats[['Feature', 'Water_Prcp', 'Diff_Prcp']].head(5))

        # Filter for Element Averages
        elem_stats = results[results['Effect_Type'] == 'Element_Avg']
        # Pivot to see Body vs Element
        print(f"\n--- Element Precipitation Averages ({hem.upper()}) ---")
        pivot = elem_stats.pivot(index='Feature', columns='Element', values='Avg_Prcp')
        print(pivot)

        # Save pivot
        pivot.to_csv(os.path.join(current_dir, f'element_precipitation_pivot_{hem}.csv'))

if __name__ == "__main__":
    main()
