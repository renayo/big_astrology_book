import pandas as pd

f = 'person_2025_update.csv'
print(f"--- Inspecting {f} ---")
try:
    # Read first few rows
    df = pd.read_csv(f, nrows=5)
    print("Columns:", df.columns.tolist())
    print("\nSample Data:")
    print(df.head())

    # Check for keywords like 'sib', 'brother', 'sister', 'family', 'order'
    potential_cols = []
    for col in df.columns:
        c_lower = col.lower()
        if any(x in c_lower for x in ['sib', 'brother', 'sister', 'family', 'order', 'child', 'num']):
            potential_cols.append(col)

    print("\nPotential Sibling Columns:", potential_cols)

except Exception as e:
    print(e)
