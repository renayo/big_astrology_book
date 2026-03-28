#!/usr/bin/env python3
"""
Couples Data Collector from Wikidata
------------------------------------
Fetches couples (spouses) where both partners have known birth dates.
Used for Projects 10, 26, 36.
"""

import requests
import pandas as pd
import time
from pathlib import Path

OUTPUT_FILE = Path("couples_data_wikidata.csv")

def fetch_wikidata_couples():
    print("Querying Wikidata for couples...")
    
    # SPARQL Query
    # Logic: Person1 has Spouse Person2. Get Birthdates and Deathdates.
    # Filter: ID(P1) < ID(P2) to avoid A-B and B-A duplicates.
    # Filter: Birth year > 1800 for data quality.
    query = """
    SELECT DISTINCT 
        ?person1 ?person1Label ?birth1 ?death1
        ?person2 ?person2Label ?birth2 ?death2
        ?start ?end
    WHERE {
      ?person1 wdt:P31 wd:Q5;         # P1 is Human
               wdt:P569 ?birth1.      # P1 has Birth Date
      OPTIONAL { ?person1 wdt:P570 ?death1. } # P1 Death
               
      ?person1 p:P26 ?stmt.           # P1 has Spouse Statement
      ?stmt ps:P26 ?person2.          # Spouse is P2
      
      ?person2 wdt:P31 wd:Q5;         # P2 is Human
               wdt:P569 ?birth2.      # P2 has Birth Date
      OPTIONAL { ?person2 wdt:P570 ?death2. } # P2 Death
      
      OPTIONAL { ?stmt pq:P580 ?start. } # Marriage Start
      OPTIONAL { ?stmt pq:P582 ?end. }   # Marriage End (Divorce/Death)

      # Filter for modern-ish history (better documentation)
      FILTER(YEAR(?birth1) > 1800 && YEAR(?birth2) > 1800)
      
      # Semantic constraint: Only pair them once
      FILTER(STR(?person1) < STR(?person2))
      
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 4000
    """
    
    url = "https://query.wikidata.org/sparql"
    headers = {
        'User-Agent': 'AstrologyResearch/1.0 (academic research attempt)',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(url, params={'query': query, 'format': 'json'}, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

    results = []
    for item in data['results']['bindings']:
        try:
            p1_name = item['person1Label']['value']
            p1_birth = item['birth1']['value'].split('T')[0]
            
            p1_death = item.get('death1', {}).get('value', '').split('T')[0]
            
            p2_name = item['person2Label']['value']
            p2_birth = item['birth2']['value'].split('T')[0]
            
            p2_death = item.get('death2', {}).get('value', '').split('T')[0]
            
            start_date = item.get('start', {}).get('value', '').split('T')[0]
            end_date = item.get('end', {}).get('value', '').split('T')[0]
            
            # Status Logic
            # Just pass raw dates; let analysis decide status
            
            results.append({
                'p1_name': p1_name,
                'p1_birth_date': p1_birth,
                'p1_birth_time': None, 
                'p1_death_date': p1_death,
                'p2_name': p2_name,
                'p2_birth_date': p2_birth,
                'p2_birth_time': None, 
                'p2_death_date': p2_death,
                'start_date': start_date,
                'end_date': end_date
            })
        except Exception as e:
            continue

            
    df = pd.DataFrame(results)
    
    # Filter out entries where names are Q-ids (label fetch failed) or numeric
    # Usually label service handles this, but sometimes glitches.
    
    print(f"Fetched {len(df)} couples.")
    return df

if __name__ == "__main__":
    df = fetch_wikidata_couples()
    if df is not None and not df.empty:
        # Save to Project 10 folder
        proj10_path = Path("10-synastry-relationship-longevity/new_couples_wikidata.csv")
        df.to_csv(proj10_path, index=False)
        print(f"Saved to {proj10_path}")
        
        # Also save to Project 26
        proj26_path = Path("26-compatibility-relationship-satisfaction/new_couples_wikidata.csv")
        # Ensure dir exists
        proj26_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(proj26_path, index=False)
        print(f"Saved to {proj26_path}")
        
        # Also save to Project 36
        proj36_path = Path("36-synastry-harmonics-logistic/new_couples_wikidata.csv")
        proj36_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(proj36_path, index=False)
        print(f"Saved to {proj36_path}")

