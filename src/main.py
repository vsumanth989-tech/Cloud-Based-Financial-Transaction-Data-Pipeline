"""
Cloud-Scale Financial Transaction Data Pipeline
Main ETL Pipeline Orchestrator
"""

import logging
from datetime import datetime
from pathlib import Path
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from ingestion.data_loader import DataLoader
from validation.schema_validator import SchemaValidator
from validation.data_quality_checks import DataQualityChecker
from transformation.data_cleaner import DataCleaner
from transformation.data_transformer import DataTransformer
from utils.logger import setup_logger
from utils.config import load_config

class FinancialTransactionPipeline:
    """
    Main ETL pipeline for processing financial transactions
    Handles ingestion, validation, transformation, and loading
    """
    
    def __init__(self, config_path='config/pipeline_config.yaml'):
        """Initialize the pipeline with configuration"""
        self.config = load_config(config_path)
        self.logger = setup_logger('FinancialPipeline', self.config['logging']['level'])
        
        # Initialize components
        self.loader = DataLoader(self.config)
        self.schema_validator = SchemaValidator(self.config)
        self.quality_checker = DataQualityChecker(self.config)
        self.cleaner = DataCleaner(self.config)
        self.transformer = DataTransformer(self.config)
        
        self.logger.info("Pipeline initialized successfully")
    
    def run(self, input_path, output_path=None, stage='all'):
        """
        Execute the ETL pipeline
        
        Args:
            input_path: Path to input data file/directory
            output_path: Path to output processed data
            stage: Pipeline stage to run ('ingestion', 'validation', 'transformation', 'all')
        
        Returns:
            dict: Pipeline execution results and metrics
        """
        start_time = datetime.now()
        results = {
            'status': 'success',
            'records_processed': 0,
            'errors': [],
            'execution_time': None,
            'metrics': {}
        }
        
        try:
            self.logger.info(f"Starting pipeline execution for {input_path}")
            
            # Stage 1: Data Ingestion
            if stage in ['ingestion', 'all']:
                self.logger.info("Stage 1: Data Ingestion")
                df = self.loader.load_data(input_path)
                results['records_processed'] = len(df)
                results['metrics']['ingestion'] = {
                    'records_loaded': len(df),
                    'columns': len(df.columns),
                    'file_size_mb': Path(input_path).stat().st_size / (1024 * 1024)
                }
                self.logger.info(f"Loaded {len(df)} records")
            
            # Stage 2: Schema Validation
            if stage in ['validation', 'all']:
                self.logger.info("Stage 2: Schema Validation")
                schema_valid, schema_errors = self.schema_validator.validate(df)
                
                if not schema_valid:
                    results['errors'].extend(schema_errors)
                    self.logger.warning(f"Schema validation found {len(schema_errors)} issues")
                
                # Data Quality Checks
                self.logger.info("Running data quality checks")
                quality_report = self.quality_checker.run_checks(df)
                results['metrics']['quality'] = quality_report
                
                # Log quality issues
                if quality_report['total_issues'] > 0:
                    self.logger.warning(
                        f"Found {quality_report['total_issues']} data quality issues"
                    )
            
            # Stage 3: Data Transformation
            if stage in ['transformation', 'all']:
                self.logger.info("Stage 3: Data Cleaning")
                df = self.cleaner.clean(df)
                
                self.logger.info("Stage 4: Data Transformation")
                df = self.transformer.transform(df)
                
                results['metrics']['transformation'] = {
                    'records_after_cleaning': len(df),
                    'columns_after_transformation': len(df.columns)
                }
            
            # Stage 4: Load to destination
            if stage == 'all' and output_path:
                self.logger.info(f"Loading data to {output_path}")
                self.loader.save_data(df, output_path)
                results['metrics']['output'] = {
                    'output_path': output_path,
                    'final_record_count': len(df)
                }
            
            # Calculate metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            results['execution_time'] = execution_time
            results['throughput'] = results['records_processed'] / execution_time if execution_time > 0 else 0
            
            self.logger.info(
                f"Pipeline completed successfully. "
                f"Processed {results['records_processed']} records in {execution_time:.2f}s "
                f"({results['throughput']:.0f} records/sec)"
            )
            
            return results
            
        except Exception as e:
            self.logger.error(f"Pipeline execution failed: {str(e)}", exc_info=True)
            results['status'] = 'failed'
            results['errors'].append(str(e))
            return results
    
    def get_pipeline_stats(self):
        """Get pipeline statistics and health metrics"""
        return {
            'config': self.config['pipeline'],
            'status': 'healthy',
            'last_run': datetime.now().isoformat()
        }


def main():
    """Main entry point for pipeline execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Financial Transaction ETL Pipeline')
    parser.add_argument('--input', required=True, help='Input data path')
    parser.add_argument('--output', help='Output data path')
    parser.add_argument('--config', default='config/pipeline_config.yaml', 
                       help='Configuration file path')
    parser.add_argument('--stage', default='all', 
                       choices=['ingestion', 'validation', 'transformation', 'all'],
                       help='Pipeline stage to execute')
    
    args = parser.parse_args()
    
    # Initialize and run pipeline
    pipeline = FinancialTransactionPipeline(config_path=args.config)
    results = pipeline.run(
        input_path=args.input,
        output_path=args.output,
        stage=args.stage
    )
    
    # Print results
    print("\n" + "="*50)
    print("PIPELINE EXECUTION RESULTS")
    print("="*50)
    print(f"Status: {results['status']}")
    print(f"Records Processed: {results['records_processed']}")
    print(f"Execution Time: {results['execution_time']:.2f} seconds")
    print(f"Throughput: {results['throughput']:.0f} records/second")
    
    if results['errors']:
        print(f"\nErrors: {len(results['errors'])}")
        for error in results['errors'][:5]:  # Show first 5 errors
            print(f"  - {error}")
    
    print("="*50 + "\n")


if __name__ == "__main__":
    main()
