"""
Schema Validator
Validates data against expected schema
"""

import pandas as pd
import logging
from typing import Tuple, List

class SchemaValidator:
    """Validate DataFrame schema against expected structure"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('SchemaValidator')
        self.expected_schema = self.config.get('schema', {})
    
    def validate(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate DataFrame schema
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Expected columns for financial transactions
        expected_columns = [
            'transaction_id', 'timestamp', 'amount', 'currency',
            'customer_id', 'merchant_id', 'transaction_type', 'status'
        ]
        
        # Check required columns
        missing_columns = set(expected_columns) - set(df.columns)
        if missing_columns:
            errors.append(f"Missing required columns: {missing_columns}")
        
        # Check data types
        if 'amount' in df.columns:
            if not pd.api.types.is_numeric_dtype(df['amount']):
                errors.append("Column 'amount' must be numeric")
        
        if 'timestamp' in df.columns:
            try:
                pd.to_datetime(df['timestamp'])
            except:
                errors.append("Column 'timestamp' must be valid datetime")
        
        is_valid = len(errors) == 0
        
        if is_valid:
            self.logger.info("Schema validation passed")
        else:
            self.logger.warning(f"Schema validation failed with {len(errors)} errors")
        
        return is_valid, errors
