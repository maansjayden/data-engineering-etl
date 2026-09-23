# Sales ETL Script

Simple local ETL script for retail sales data.

## Setup
Install dependencies:
```bash
pip install -r requirements.txt
```

Run ETL:
```bash
python etl.py
```

The script cleans `raw_sales.csv` and loads valid records into `warehouse.db`.
