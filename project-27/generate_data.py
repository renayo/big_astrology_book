#!/usr/bin/env python3
"""
Generate synthetic horary data for testing the pipeline.
Generates 1000 random chart timestamps between 2000 and 2025.
Assigns random outcomes (50/50) to serve as a CONTROL group.
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_synthetic_data(n_samples=1000):
    start_date = datetime(2000, 1, 1)
    end_date = datetime(2025, 1, 1)
    range_days = (end_date - start_date).days

    records = []
    question_types = ['lost_item', 'relationship', 'job', 'health', 'journey', 'lawsuit']

    for _ in range(n_samples):
        # Random date
        random_days = random.randrange(range_days)
        random_seconds = random.randrange(86400)
        dt = start_date + timedelta(days=random_days, seconds=random_seconds)

        # Random outcome (Base rate 50%)
        # NOTE: In a real study, this column would be user-supplied truth.
        outcome = random.choice([True, False])

        # Random Question Type
        q_type = random.choice(question_types)

        records.append({
            'question_type': q_type,
            'year': dt.year,
            'month': dt.month,
            'day': dt.day,
            'hour': dt.hour + dt.minute/60.0, # Decimal hour for swisseph
            'outcome': outcome
        })

    df = pd.DataFrame(records)
    output_path = 'synthetic_horary_data.csv'
    df.to_csv(output_path, index=False)
    print(f"Generated {n_samples} synthetic records to {output_path}")

if __name__ == '__main__':
    generate_synthetic_data(600)
