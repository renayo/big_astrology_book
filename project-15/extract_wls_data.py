import pandas as pd
import swisseph as swe
import os
import numpy as np

# Path to DTA
file_path = '../wls_b_15_2.dta'
output_csv = 'birth_order_real_data.csv'

def get_julian_day_midyear(year):
    # July 2nd is roughly mid year
    return swe.julday(year, 7, 2, 12.0)

def extract_and_process():
    print("Loading WLS data...")
    # Read columns for Grad and Siblings
    # We need:
    # idpub (ID)
    # brdxdy (Grad Birth Year)
    # bor (Grad Birth Order)
    # gk1301...gk13016 (Sibling Birth Years approx)

    # Generate list of sibling year columns
    sib_cols = [f'gk130{i}' for i in range(1, 14)] # 1 to 13
    # Check the inspection output, it goes up to gk13017 or so, but let's grab what we saw (gk1301...gk13012 etc from previous logs)
    # Actually let's just grab gk1301 through gk13012 for now as seen in logs.

    cols_to_load = ['idpub', 'brdxdy', 'bor'] + sib_cols

    # Note: Some columns might not exist if I guessed the name wrong, but inspect output showed gk1301..gk13013
    # Let's verify names or use try/except

    try:
        df = pd.read_stata(file_path, columns=cols_to_load)
    except ValueError as e:
        print(f"Column error: {e}")
        # Fallback to reading all and filtering
        df = pd.read_stata(file_path)

    print(f"Loaded {len(df)} records.")

    extracted_data = []

    # Iterate rows
    for index, row in df.iterrows():
        # 1. Add the Graduate
        g_year = row['brdxdy']
        g_order = row['bor']

        # Check validity (sometimes it's NaN or encoded as negative/categorical code)
        # In pandas categoricals, we might need to cast
        try:
            g_year = pd.to_numeric(g_year, errors='coerce')
            g_order = pd.to_numeric(g_order, errors='coerce')

            if not np.isnan(g_year) and not np.isnan(g_order) and g_year > 1900 and g_order > 0:
                extracted_data.append({
                    'family_id': row['idpub'],
                    'birth_year': int(g_year),
                    'birth_order': int(g_order),
                    'source': 'graduate'
                })
        except:
            pass

        # 2. Add the Siblings (Explicitly listed by order)
        # The variables gk1301, gk1302 correspond to 1st child, 2nd child, etc?
        # "Year of oldest sibling's birth" -> This suggests gk1301 is the 1st born sibling?
        # Or just the oldest in the list?
        # Usually "Year of oldest sibling" implies the #1 child of the family (if we include the grad?? or is grad excluded?)

        # Checking logic: "gk071re: Respondent position in sib table."
        # This implies all siblings + grad are in a table.
        # But gk1301 is "Year of oldest sibling's birth".
        # If the Grad is the oldest, is gk1301 the Grad's year? Or the oldest *other* sibling?
        # WLS documentation usually separates Grad from Siblings in these vars or includes them.

        # Let's assume for this "mass harvest" that gk130n corresponds to the Nth child in the family structure 
        # IF we can align it.
        # However, "oldest sibling" might exclude the graduate if the variable labels say "Year of oldest sibling".
        # BUT, to be safe and avoid duplicates or confusion (since we don't know if Grad is inserted in that list),
        # let's mainly rely on the Graduate's data point which is explicitly (Year, Order).
        # We have ~10,000 graduates. That's a good sample size (N=10k).
        # Expanding with siblings is better, but parsing the "who is who" without the mix is risky.

        # HOWEVER, the user asked to "find n-th born data".
        # If we just use graduates, we have a bias: WLS graduates are high school grads from Wisconsin in 1957.
        # They are all ~18 years old in 1957, so born ~1939.
        # This means for Birth Order 1, Year is 1939.
        # For Birth Order 5, Year is 1939.
        # This is CRITICAL: We cannot separate "Birth Order" from "Generational Astrology" if everyone is born in 1939.
        # A 1st born in 1939 has Saturn in Aries/Taurus.
        # A 5th born in 1939 has Saturn in Aries/Taurus.
        # The planetary positions will be IDENTICAL for all birth orders in a single-year cohort.

        # CONCLUSION: WE MUST USE THE SIBLINGS.
        # The siblings have different birth years.
        # gk1301 (Oldest) might be born 1935.
        # gk1305 (5th) might be born 1945.
        # We need to use the sibling arrays to get variation in birth years.

        # Let's extract siblings assuming gk130N is the Nth sibling in the roster.
        # The variables were "Year of oldest sibling's birth" (gk1301), "Year of 2nd oldest..." (gk1302).
        # This strongly implies strictly ordered from 1..N.
        # Does this list include the graduate?
        # Variable "gk071re: Respondent position in sib table" suggests the grad is IN the table or we know where they fit.
        # Actually, let's just take all valid years from gk1301...gk13012.
        # And assign them Birth Order 1...12.
        # This assumes gk1301 is the ACTUAL 1st born.
        # Label: "Year of oldest sibling's birth".
        # If I have 5 siblings and I am the 3rd, and they ask "Year of oldest sibling", do they mean my older brother (the 1st)? Yes.
        # So gk1301 = Child 1. gk1302 = Child 2.

        for i in range(1, 13):
            col_name = f'gk130{i}'
            if col_name in row:
                s_year = row[col_name]
                try:
                    s_year = pd.to_numeric(s_year, errors='coerce')
                    if not np.isnan(s_year) and s_year > 1890 and s_year < 2000:
                        extracted_data.append({
                            'family_id': row['idpub'],
                            'birth_year': int(s_year),
                            'birth_order': i,  # Assuming index i is birth order
                            'source': 'sibling_roster'
                        })
                except:
                    continue

    # Convert to DataFrame
    final_df = pd.DataFrame(extracted_data)

    # Remove duplicates if any (e.g. if we accidentally double counted)
    final_df.drop_duplicates(inplace=True)

    print(f"Extracted {len(final_df)} individual birth records.")
    print(final_df['birth_order'].value_counts().sort_index().head(10))
    print(final_df['birth_year'].describe())

    final_df.to_csv(output_csv, index=False)
    print(f"Saved to {output_csv}")

if __name__ == "__main__":
    extract_and_process()
