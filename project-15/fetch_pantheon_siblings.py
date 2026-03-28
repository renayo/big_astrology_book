import pandas as pd
import requests
import time
import sys

# Settings
INPUT_FILE = 'person_2025_update.csv'
OUTPUT_FILE = 'pantheon_with_birth_order.csv'
BATCH_SIZE = 50
LIMIT = 500  # Process top 500 famous people for now to avoid timeout
SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

def get_sparql_query(qids):
    values = " ".join([f"wd:{qid}" for qid in qids])
    query = f"""
    SELECT ?person ?personLabel ?birthDate ?sibling ?siblingBirthDate WHERE {{
      VALUES ?person {{ {values} }}
      ?person wdt:P31 wd:Q5 .
      ?person wdt:P569 ?birthDate . 
      OPTIONAL {{ 
        ?person wdt:P3373 ?sibling .
        ?sibling wdt:P569 ?siblingBirthDate .
      }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    """
    return query

def fetch_data(df):
    results = []

    # Sort by HPI to get most famous
    df = df.sort_values(by='hpi', ascending=False).head(LIMIT)
    qids = df['wd_id'].tolist()

    print(f"Fetching data for top {len(qids)} people...")

    for i in range(0, len(qids), BATCH_SIZE):
        batch = qids[i:i+BATCH_SIZE]
        print(f"Processing batch {i} to {i+len(batch)}...")

        try:
            query = get_sparql_query(batch)
            response = requests.get(SPARQL_ENDPOINT, params={'query': query, 'format': 'json'})

            if response.status_code == 429:
                print("Rate limited, waiting...")
                time.sleep(10)
                continue

            data = response.json()

            # Process bindings
            family_map = {} # QID -> {birth: date, siblings: [(qid, date)]}

            for item in data['results']['bindings']:
                p_url = item['person']['value']
                p_qid = p_url.split('/')[-1]
                p_bdate = item['birthDate']['value']

                if p_qid not in family_map:
                    family_map[p_qid] = {'birth': p_bdate, 'siblings': []}

                if 'sibling' in item and 'siblingBirthDate' in item:
                    s_url = item['sibling']['value']
                    s_qid = s_url.split('/')[-1]
                    s_bdate = item['siblingBirthDate']['value']
                    family_map[p_qid]['siblings'].append({'id': s_qid, 'birth': s_bdate})

            # Calculate birth order
            for qid, info in family_map.items():
                my_birth = info['birth']
                sibs = info['siblings']

                if not sibs:
                    # No siblings found in Wikidata implies either Only Child OR missing data.
                    # We can't be sure. But let's mark as "Unknown" or skip.
                    # User asked to "isolate rows that have sibling information".
                    # If siblings list is empty, we don't have INFO about siblings (existence or non-existence is ambiguous).
                    # Actually, if P3373 is missing, it's ambiguous.
                    # But the query returns a row if birthdate exists.
                    continue

                # Filter valid dates
                valid_sibs = [s for s in sibs if s['birth'] and not s['birth'].startswith('t')] # simple check

                # Count older siblings
                older_count = 0
                for s in valid_sibs:
                    if s['birth'] < my_birth:
                        older_count += 1

                birth_order = older_count + 1
                total_siblings = len(valid_sibs) + 1

                results.append({
                    'wd_id': qid,
                    'birth_order': birth_order,
                    'total_siblings': total_siblings,
                    'sibling_data_count': len(valid_sibs)
                })

            time.sleep(1) # Be nice to API

        except Exception as e:
            print(f"Error in batch: {e}")

    # Merge with original data
    if not results:
        print("No sibling data found.")
        return

    res_df = pd.DataFrame(results)
    final_df = df.merge(res_df, on='wd_id', how='inner')

    print(f"Enriched {len(final_df)} records with birth order.")
    final_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    df = pd.read_csv(INPUT_FILE)
    fetch_data(df)
