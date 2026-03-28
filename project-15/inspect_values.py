import pandas as pd

f = '../wls_b_15_2.dta'
print(f"--- Values in {f} ---")
try:
    # Remove 'sex' add 'bor'
    df = pd.read_stata(f, columns=['idpub', 'brdxdy', 'bor', 'sibcount'])
    print(df.head(10))
    print("\nValue Counts for brdxdy:")
    print(df['brdxdy'].value_counts().sort_index())
except Exception as e:
    print(e)
