"""
Data Loader Module
Handles data ingestion from multiple sources
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Union

class DataLoader:
    """Load data from various file formats"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('DataLoader')
        self.supported_formats = ['csv', 'json', 'parquet', 'xlsx']
    
    def load_data(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from file
        
        Args:
            file_path: Path to data file
            
        Returns:
            pd.DataFrame: Loaded data
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = file_path.suffix.lower().replace('.', '')
        
        if file_extension not in self.supported_formats:
            raise ValueError(
                f"Unsupported file format: {file_extension}. "
                f"Supported formats: {self.supported_formats}"
            )
        
        self.logger.info(f"Loading data from {file_path}")
        
        try:
            if file_extension == 'csv':
                df = pd.read_csv(file_path)
            elif file_extension == 'json':
                df = pd.read_json(file_path)
            elif file_extension == 'parquet':
                df = pd.read_parquet(file_path)
            elif file_extension == 'xlsx':
                df = pd.read_excel(file_path)
            
            self.logger.info(f"Successfully loaded {len(df)} records, {len(df.columns)} columns")
            return df
            
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise
    
    def save_data(self, df: pd.DataFrame, output_path: Union[str, Path], 
                  format: str = None):
        """
        Save DataFrame to file
        
        Args:
            df: DataFrame to save
            output_path: Output file path
            format: Output format (csv, parquet, json). If None, inferred from path
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format is None:
            format = output_path.suffix.lower().replace('.', '')
        
        self.logger.info(f"Saving {len(df)} records to {output_path}")
        
        try:
            if format == 'csv':
                df.to_csv(output_path, index=False)
            elif format == 'parquet':
                df.to_parquet(output_path, index=False)
            elif format == 'json':
                df.to_json(output_path, orient='records', indent=2)
            elif format == 'xlsx':
                df.to_excel(output_path, index=False)
            else:
                raise ValueError(f"Unsupported output format: {format}")
            
            self.logger.info(f"Data saved successfully to {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving data: {str(e)}")
            raise
    
    def load_batch(self, file_pattern: str, directory: Path) -> pd.DataFrame:
        """
        Load multiple files matching a pattern
        
        Args:
            file_pattern: File pattern (e.g., '*.csv')
            directory: Directory to search
            
        Returns:
            pd.DataFrame: Combined data from all files
        """
        directory = Path(directory)
        files = list(directory.glob(file_pattern))
        
        if not files:
            raise FileNotFoundError(f"No files found matching {file_pattern} in {directory}")
        
        self.logger.info(f"Loading {len(files)} files")
        
        dfs = []
        for file in files:
            try:
                df = self.load_data(file)
                dfs.append(df)
            except Exception as e:
                self.logger.warning(f"Error loading {file}: {str(e)}")
        
        combined_df = pd.concat(dfs, ignore_index=True)
        self.logger.info(f"Combined {len(dfs)} files into {len(combined_df)} total records")
        
        return combined_df
