# Cloud-Scale Financial Transaction Data Pipeline

See `project1-README.md` for full documentation.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Generate sample data:
```bash
python generate_sample_data.py
```

3. Run the pipeline:
```bash
python src/main.py --input data/sample_transactions.csv --output data/processed_transactions.csv
```

## Project Structure
```
financial-transaction-pipeline/
├── src/
│   ├── main.py                 # Main pipeline orchestrator
│   ├── ingestion/             
│   │   └── data_loader.py      # Data loading from multiple sources
│   ├── validation/
│   │   ├── schema_validator.py # Schema validation
│   │   └── data_quality_checks.py  # Quality checks
│   ├── transformation/
│   │   ├── data_cleaner.py     # Data cleaning
│   │   └── data_transformer.py # Business logic transformations
│   └── utils/
│       ├── logger.py           # Logging configuration
│       └── config.py           # Configuration management
├── config/
│   └── pipeline_config.yaml    # Pipeline configuration
├── data/                       # Data directory
├── tests/                      # Unit tests
├── requirements.txt            # Python dependencies
└── generate_sample_data.py     # Sample data generator
```
