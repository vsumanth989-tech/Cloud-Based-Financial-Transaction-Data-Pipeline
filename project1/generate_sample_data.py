"""
Generate sample financial transaction data for testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data(n_records=10000, output_file='data/sample_transactions.csv'):
    """Generate sample financial transaction data"""
    
    np.random.seed(42)
    random.seed(42)
    
    # Generate data
    data = {
        'transaction_id': [f'TXN{str(i).zfill(8)}' for i in range(1, n_records + 1)],
        'timestamp': [
            datetime.now() - timedelta(days=random.randint(0, 365), 
                                      hours=random.randint(0, 23))
            for _ in range(n_records)
        ],
        'amount': np.random.lognormal(mean=4, sigma=1.5, size=n_records).round(2),
        'currency': np.random.choice(['USD', 'EUR', 'GBP'], size=n_records, p=[0.7, 0.2, 0.1]),
        'customer_id': [f'CUST{random.randint(1000, 9999)}' for _ in range(n_records)],
        'merchant_id': [f'MERCH{random.randint(100, 999)}' for _ in range(n_records)],
        'transaction_type': np.random.choice(
            ['PURCHASE', 'REFUND', 'TRANSFER'], 
            size=n_records, 
            p=[0.85, 0.10, 0.05]
        ),
        'status': np.random.choice(
            ['COMPLETE', 'PENDING', 'FAILED'], 
            size=n_records, 
            p=[0.90, 0.05, 0.05]
        )
    }
    
    df = pd.DataFrame(data)
    
    # Add some noise (nulls, duplicates)
    null_indices = np.random.choice(df.index, size=int(n_records * 0.02), replace=False)
    df.loc[null_indices, 'customer_id'] = None
    
    # Add some duplicates
    duplicate_rows = df.sample(n=int(n_records * 0.01))
    df = pd.concat([df, duplicate_rows], ignore_index=True)
    
    # Save
    df.to_csv(output_file, index=False)
    print(f"Generated {len(df)} sample transactions and saved to {output_file}")
    
    return df

if __name__ == "__main__":
    generate_sample_data()
