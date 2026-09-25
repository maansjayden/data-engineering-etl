# Retail Sales Data Engineering ETL Pipeline

A local, modular ETL pipeline built in Python with pandas and SQLite, implementing a Medallion Architecture (Bronze -> Silver -> Gold).

## Architecture Overview
1. **Bronze Layer (Raw Ingestion):** Ingests raw transactional retail data from `raw_sales.csv`.
2. **Silver Layer (Clean & Conformed):** 
   - Identifies corrupted records and isolates them into `rejected_records.csv` with full audit reasoning.
   - Normalizes inconsistent date formats into ISO 8601 (`YYYY-MM-DD`).
   - Standardizes customer names with whitespace trimming and uniform uppercase formatting.
   - Stores valid transactional records into the `sales` table in `warehouse.db`.
3. **Gold Layer (Business Analytics):** Aggregates product revenue, transaction counts, and average order values into the `product_performance_summary` table.

## Quickstart

### 1. Requirements
Ensure pandas is installed:
```bash
pip install -r requirements.txt
```

### 2. Run the ETL Pipeline
```bash
python etl.py
```

### 3. Run Automated Pipeline Tests
Verify data integrity, zero nulls, and schema constraints:
```bash
python test_pipeline.py
```

## Demo Video
- [YouTube Demo Video](https://youtu.be/) *(Link your unlisted 5–10 min demo video here)*
