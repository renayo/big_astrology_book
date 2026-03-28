import pandas as pd
import numpy as np

f = '../wls_b_15_2.dta'
print(f"--- Inspecting CM variables in {f} ---")
try:
    reader = pd.read_stata(f, iterator=True)
    labels = reader.variable_labels()

    cm_vars = [col for col in labels.keys() if col.lower().startswith('cm')]
    print(f"Found {len(cm_vars)} variables starting with 'cm'")

    if cm_vars:
        df = pd.read_stata(f, columns=cm_vars)

        candidates = []
        for col in cm_vars:
            try:
                # Convert to numeric, forcing errors to NaN
                vals = pd.to_numeric(df[col], errors='coerce').dropna()

                if len(vals) > 0:
                    median = vals.median()
                    # Check range for 1937-1940 birth (444 to 492)
                    if 440 <= median <= 500:
                        candidates.append((col, labels[col], median))
            except Exception as e:
                pass

        print("\nCandidates for Birth Century Month (Median 440-500):")
        for c in candidates:
            print(f"{c[0]}: {c[1]} (Median: {c[2]})")

except Exception as e:
    print(e)
