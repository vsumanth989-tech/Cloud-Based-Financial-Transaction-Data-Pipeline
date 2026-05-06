"""
Data Transformer
Applies business logic and transformations
"""

import pandas as pd
import logging
import numpy as np

class DataTransformer:
    """Transform data according to business rules"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('DataTransformer')
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply transformations to DataFrame
        
        Args:
            df: Input DataFrame
            
        Returns:
            pd.DataFrame: Transformed DataFrame
        """
        self.logger.info("Starting data transformation")
        
        df = df.copy()
        
        # Add derived columns
        df = self._add_derived_columns(df)
        
        # Apply business rules
        df = self._apply_business_rules(df)
        
        # Normalize values
        df = self._normalize_values(df)
        
        self.logger.info("Data transformation completed")
        
        return df
    
    def _add_derived_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add calculated/derived columns"""
        
        # Extract date components from timestamp
        if 'timestamp' in df.columns:
            df['transaction_date'] = df['timestamp'].dt.date
            df['transaction_hour'] = df['timestamp'].dt.hour
            df['transaction_day_of_week'] = df['timestamp'].dt.dayofweek
            df['transaction_month'] = df['timestamp'].dt.month
            df['transaction_year'] = df['timestamp'].dt.year
        
        # Add transaction categorization
        if 'amount' in df.columns:
            df['amount_category'] = pd.cut(
                df['amount'],
                bins=[0, 100, 1000, 10000, float('inf')],
                labels=['Small', 'Medium', 'Large', 'Very Large']
            )
        
        # Add flags
        if 'amount' in df.columns:
            df['is_high_value'] = df['amount'] > df['amount'].quantile(0.90)
        
        return df
    
    def _apply_business_rules(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply business logic rules"""
        
        # Flag suspicious transactions
        if 'amount' in df.columns:
            # Transactions above 10,000 are flagged for review
            df['needs_review'] = df['amount'] > 10000
        
        # Standardize status codes
        if 'status' in df.columns:
            status_mapping = {
                'COMPLETED': 'COMPLETE',
                'SUCCESS': 'COMPLETE',
                'FAILED': 'FAIL',
                'REJECTED': 'FAIL'
            }
            df['status'] = df['status'].replace(status_mapping)
        
        return df
    
    def _normalize_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize and standardize values"""
        
        # Convert all amounts to USD (simplified example)
        if 'amount' in df.columns and 'currency' in df.columns:
            # In real implementation, use actual exchange rates
            exchange_rates = {'EUR': 1.10, 'GBP': 1.25, 'USD': 1.0}
            df['amount_usd'] = df.apply(
                lambda row: row['amount'] * exchange_rates.get(row['currency'], 1.0),
                axis=1
            )
        
        return df
