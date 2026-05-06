"""
Data Cleaner
Cleans and prepares data for transformation
"""

import pandas as pd
import logging
import numpy as np

class DataCleaner:
    """Clean and prepare data"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('DataCleaner')
    
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the DataFrame
        
        Args:
            df: Input DataFrame
            
        Returns:
            pd.DataFrame: Cleaned DataFrame
        """
        self.logger.info(f"Starting data cleaning. Initial records: {len(df)}")
        
        df = df.copy()
        
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates()
        duplicates_removed = initial_count - len(df)
        if duplicates_removed > 0:
            self.logger.info(f"Removed {duplicates_removed} duplicate records")
        
        # Handle missing values
        df = self._handle_missing_values(df)
        
        # Clean text fields
        df = self._clean_text_fields(df)
        
        # Standardize formats
        df = self._standardize_formats(df)
        
        self.logger.info(f"Data cleaning completed. Final records: {len(df)}")
        
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values appropriately"""
        
        # For numeric columns, fill with median or 0
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if df[col].isnull().any():
                median_value = df[col].median()
                df[col].fillna(median_value, inplace=True)
                self.logger.debug(f"Filled missing values in {col} with median: {median_value}")
        
        # For categorical columns, fill with 'Unknown'
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if df[col].isnull().any():
                df[col].fillna('Unknown', inplace=True)
                self.logger.debug(f"Filled missing values in {col} with 'Unknown'")
        
        return df
    
    def _clean_text_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean text fields"""
        text_columns = df.select_dtypes(include=['object']).columns
        
        for col in text_columns:
            # Remove leading/trailing whitespace
            df[col] = df[col].str.strip()
            
            # Convert to consistent case if applicable
            if col in ['status', 'transaction_type', 'currency']:
                df[col] = df[col].str.upper()
        
        return df
    
    def _standardize_formats(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize data formats"""
        
        # Convert timestamp to datetime
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        # Ensure amount is numeric
        if 'amount' in df.columns:
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        return df
