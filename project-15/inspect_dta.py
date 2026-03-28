import pandas as pd
import os

files = ['../wls_bl_15_2.dta']

for f in files:
    print(f"--- Inspecting {f} ---")
    try:
        reader = pd.read_stata(f, iterator=True)
        labels = reader.variable_labels()

        print("Searching for Birth/Year/Month/Day variables:")
        for col, label in labels.items():
            l_lower = label.lower()
            if 'birth' in l_lower and ('year' in l_lower or 'month' in l_lower or 'day' in l_lower):
                print(f"{col}: {label}")

        print("\nSearching for variables starting with 'brd' (birth date prefixes?):")
        for col, label in labels.items():
             if col.startswith('brd') or col.startswith('birth'):
                 print(f"{col}: {label}")

    except Exception as e:
        print(f"Error reading {f}: {e}")
    print("\n")
