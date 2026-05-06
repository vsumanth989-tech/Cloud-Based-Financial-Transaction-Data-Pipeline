"""
Data Quality Checker
Performs comprehensive data quality validation
"""

import pandas as pd
import logging

class DataQualityChecker:
    """Run data quality checks on DataFrame"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('DataQualityChecker')
        self.thresholds = config.get('quality_thresholds', {
            'null_rate_max': 0.05,
            'duplicate_rate_max': 0.01
        })
    
    def run_checks(self, df: pd.DataFrame) -> dict:
        """
        Run all quality checks
        
        Returns:
            dict: Quality report with metrics
        """
        report = {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'checks': {},
            'total_issues': 0
        }
        
        # Check for null values
        null_check = self._check_nulls(df)
        report['checks']['nulls'] = null_check
        
        # Check for duplicates
        duplicate_check = self._check_duplicates(df)
        report['checks']['duplicates'] = duplicate_check
        
        # Check data ranges
        range_check = self._check_ranges(df)
        report['checks']['ranges'] = range_check
        
        # Calculate total issues
        report['total_issues'] = sum(
            check.get('issues_found', 0) 
            for check in report['checks'].values()
        )
        
        # Calculate quality score
        report['quality_score'] = self._calculate_quality_score(report)
        
        return report
    
    def _check_nulls(self, df: pd.DataFrame) -> dict:
        """Check for null values"""
        null_counts = df.isnull().sum()
        null_percentages = (null_counts / len(df)) * 100
        
        issues_found = sum(null_percentages > self.thresholds['null_rate_max'] * 100)
        
        return {
            'check_type': 'null_values',
            'total_nulls': int(null_counts.sum()),
            'columns_with_nulls': int((null_counts > 0).sum()),
            'issues_found': issues_found,
            'passed': issues_found == 0
        }
    
    def _check_duplicates(self, df: pd.DataFrame) -> dict:
        """Check for duplicate records"""
        duplicate_count = df.duplicated().sum()
        duplicate_rate = duplicate_count / len(df)
        
        return {
            'check_type': 'duplicates',
            'duplicate_records': int(duplicate_count),
            'duplicate_rate': float(duplicate_rate),
            'issues_found': int(duplicate_count),
            'passed': duplicate_rate <= self.thresholds['duplicate_rate_max']
        }
    
    def _check_ranges(self, df: pd.DataFrame) -> dict:
        """Check if numeric values are within expected ranges"""
        issues = 0
        
        if 'amount' in df.columns:
            negative_amounts = (df['amount'] < 0).sum()
            zero_amounts = (df['amount'] == 0).sum()
            issues += negative_amounts
        
        return {
            'check_type': 'ranges',
            'issues_found': int(issues),
            'passed': issues == 0
        }
    
    def _calculate_quality_score(self, report: dict) -> float:
        """Calculate overall quality score (0-100)"""
        passed_checks = sum(1 for check in report['checks'].values() if check['passed'])
        total_checks = len(report['checks'])
        
        if total_checks == 0:
            return 100.0
        
        return round((passed_checks / total_checks) * 100, 2)
