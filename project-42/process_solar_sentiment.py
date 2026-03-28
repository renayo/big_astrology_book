import pandas as pd
import numpy as np

# Load Sunspots
# 1749;01;1749.042;  96.7; ...
# Columns: Year, Month, DecimalYear, Sunspots, StdDev, N, Prov
try:
    sunspots = pd.read_csv('temp_sunspots.csv', sep=';', header=None, 
                           names=['Year', 'Month', 'DecimalYear', 'Sunspots', 'StdDev', 'N', 'Prov'])
    
    # Create Date column
    sunspots['Date'] = pd.to_datetime(sunspots['Year'].astype(str) + '-' + sunspots['Month'].astype(str) + '-01').dt.strftime('%Y-%m')
    
    # Load Sentiment
    sentiment = pd.read_csv('temp_sentiment.csv')
    sentiment['Date'] = pd.to_datetime(sentiment['observation_date']).dt.strftime('%Y-%m')
    
    # Merge
    # We want 1960-01 to 2023-12
    dates = pd.date_range(start='1960-01-01', end='2023-12-01', freq='MS')
    df_dates = pd.DataFrame({'Date': dates.strftime('%Y-%m')})
    
    merged = df_dates.merge(sunspots[['Date', 'Sunspots']], on='Date', how='left')
    merged = merged.merge(sentiment[['Date', 'UMCSENT']], on='Date', how='left')
    
    merged.rename(columns={'UMCSENT': 'Sentiment'}, inplace=True)
    
    # Format
    merged['Date(YYYY-MM)'] = merged['Date']
    final_df = merged[['Date(YYYY-MM)', 'Sunspots', 'Sentiment']]
    
    # Save
    output_path = '42-solar-cycles-social-sentiment/solar_sentiment_data.csv'
    final_df.to_csv(output_path, index=False)
    
    print(f"Successfully created {output_path} with {len(final_df)} rows.")
    print(final_df.head())
    print(final_df.tail())

except Exception as e:
    print(e)

