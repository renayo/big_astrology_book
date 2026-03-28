import pandas as pd
import os

INPUT_FILE = '../temp_nyc_data.csv'
OUTPUT_FILE = 'nyc_daily_ed_visits.csv'

def process_data():
    print(f"Processing {INPUT_FILE}...")

    # Use chunks to handle large file
    chunk_size = 100000
    daily_sums = {}
    seen_entries = set() # To track (date, zip) pairs and avoid duplicates

    # Read only needed columns
    # date format in sample: 12/25/2021

    try:
        # First pass: map dates to sums
        for chunk in pd.read_csv(INPUT_FILE, usecols=['date', 'mod_zcta', 'total_ed_visits'], chunksize=chunk_size):
            # Convert date to datetime objects
            chunk['date'] = pd.to_datetime(chunk['date'], format='%m/%d/%Y', errors='coerce')

            # Iterate through rows to handle deduplication logic
            # (Doing this in pure python/iteration might be slower but safer for standard logic than complex pandas vectorization with sets)
            for _, row in chunk.iterrows():
                date_val = row['date']
                zcta_val = row['mod_zcta']
                visits_val = row['total_ed_visits']

                if pd.isna(date_val): continue

                # Create unique key for this daily zip code record
                # We assume the first one encountered is valid (or they are all identical)
                entry_key = (date_val, zcta_val)

                if entry_key not in seen_entries:
                    seen_entries.add(entry_key)

                    if date_val not in daily_sums:
                        daily_sums[date_val] = 0
                    daily_sums[date_val] += visits_val

        # Convert to DataFrame
        results = pd.DataFrame(list(daily_sums.items()), columns=['date', 'total_ed_visits'])
        results = results.sort_values('date')

        # Save
        print(f"Saving aggregated data to {OUTPUT_FILE}...")
        results.to_csv(OUTPUT_FILE, index=False)
        print("Done!")

        # Print stats
        print(f"Total days: {len(results)}")
        print(f"Date range: {results['date'].min()} to {results['date'].max()}")
        print(f"Total visits: {results['total_ed_visits'].sum()}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    process_data()
