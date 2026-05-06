"""
Configuration management
"""

import yaml
from pathlib import Path

def load_config(config_path: str) -> dict:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config file
    
    Returns:
        dict: Configuration dictionary
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        # Return default config
        return get_default_config()
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    return config

def get_default_config() -> dict:
    """Get default configuration"""
    return {
        'pipeline': {
            'name': 'financial_transaction_pipeline',
            'version': '1.0.0'
        },
        'logging': {
            'level': 'INFO'
        },
        'quality_thresholds': {
            'null_rate_max': 0.05,
            'duplicate_rate_max': 0.01
        },
        'schema': {
            'required_columns': [
                'transaction_id', 'timestamp', 'amount', 
                'customer_id', 'merchant_id'
            ]
        }
    }
