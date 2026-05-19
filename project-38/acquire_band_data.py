import requests
import pandas as pd
import time
from datetime import datetime

WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"
REQUEST_TIMEOUT = 60

# Query logic:
# Select bands with > 2 members
# Get start date, end date (optional)
# Get members and their birth dates
# Limit to reasonable number to avoid timeout, maybe 500-1000 bands

SPARQL_QUERY = """
SELECT ?band ?bandLabel ?genreLabel ?start ?end ?member ?memberLabel ?birthdate WHERE {
  {
    SELECT ?band ?start ?end WHERE {
      ?band wdt:P31/wdt:P279* wd:Q215380. # Instance of musical group
      ?band wdt:P571 ?start.             # Start date
      OPTIONAL { ?band wdt:P576 ?end. }  # End date (optional)
      ?band wdt:P136 ?genre.             # Genre
    }
    LIMIT 5000
  }
  
  ?band wdt:P527 ?member.     # Has part (member)
  ?member wdt:P569 ?birthdate. # Date of birth
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""

def fetch_data():
    print("Querying Wikidata for bands and members...")
    headers = {'User-Agent': 'AstrologyResearchBot/1.0 (rko@example.com)'}
    
    try:
        response = requests.get(
            WIKIDATA_ENDPOINT,
            params={'query': SPARQL_QUERY, 'format': 'json'},
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

    results = []
    bindings = data['results']['bindings']
    
    print(f"Received {len(bindings)} rows. Processing...")
    
    for item in bindings:
        try:
            band_name = item['bandLabel']['value']
            band_id = item['band']['value'].split('/')[-1]
            member_name = item['memberLabel']['value']
            
            # Dates in Wiki are ISO8601 like 1980-01-01T00:00:00Z
            start_str = item['start']['value']
            end_str = item.get('end', {}).get('value', None)
            birth_str = item['birthdate']['value']
            
            start_yr = int(start_str[:4])
            end_yr = int(end_str[:4]) if end_str else 2024 # Assume active if no end
            birth_dt = birth_str.split('T')[0]
            
            # Simple validation
            if start_yr < 1900: continue 
            
            results.append({
                'band_id': band_id,
                'band_name': band_name,
                'start_year': start_yr,
                'end_year': end_yr,
                'member_name': member_name,
                'birth_date': birth_dt
            })
        except Exception as e:
            continue
            
    df = pd.DataFrame(results)
    return df

if __name__ == "__main__":
    df = fetch_data()
    if df is not None:
        # Filter for bands with at least 3 members with birthdates
        # Deduplicate first
        df = df.drop_duplicates(subset=['band_id', 'member_name'])
        
        counts = df.groupby('band_name')['member_name'].count()
        valid_bands = counts[counts >= 3].index
        
        final_df = df[df['band_name'].isin(valid_bands)]
        
        # Determine lifespan
        # We need lifespan per band, so let's deduplicate band info
        # But here we just save the flat file
        
        output_path = "38-composite-charts-group-dynamics/bands_data.csv"
        final_df.to_csv(output_path, index=False)
        print(f"Saved {len(final_df)} rows of member data for {final_df['band_name'].nunique()} bands to {output_path}")
        print(final_df.head())
