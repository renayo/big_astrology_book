import pandas as pd
import os

def clean_file(filename):
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    print(f"Cleaning {filename}...")
    try:
        df = pd.read_csv(filename)
        original_count = len(df)

        # Get first 3 columns
        subset_cols = df.columns[:3].tolist()
        print(f"  Deduplicating based on: {subset_cols}")

        df_clean = df.drop_duplicates(subset=subset_cols, keep='first')
        new_count = len(df_clean)

        print(f"  Removed {original_count - new_count} duplicates. {new_count} records remain.")
        df_clean.to_csv(filename, index=False)

    except Exception as e:
        print(f"  Error cleaning {filename}: {e}")

if __name__ == "__main__":
    # Clean wealthy_birthdata_v2.csv
    clean_file("wealthy_birthdata_v2.csv")

    # Clean 1000_richest_people_in_the_world.csv
    clean_file("1000_richest_people_in_the_world.csv")
