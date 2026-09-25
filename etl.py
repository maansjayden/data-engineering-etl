import pandas as pd
import sqlite3
import os

RAW_DATA_PATH = "raw_sales.csv"
REJECTED_DATA_PATH = "rejected_records.csv"
DB_PATH = "warehouse.db"

def extract(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file {file_path} not found.")
    return pd.read_csv(file_path)

def transform(df):
    # Data Quality Validation: Identify rejection reasons
    reasons = []
    is_valid = []

    for _, row in df.iterrows():
        row_issues = []
        if pd.isna(row['customer_name']) or str(row['customer_name']).strip() == "":
            row_issues.append("Missing Customer Name")
        if pd.isna(row['date']) or str(row['date']).strip() == "":
            row_issues.append("Missing Transaction Date")
        if pd.isna(row['amount']) or str(row['amount']).strip() == "":
            row_issues.append("Missing Amount")
        
        if row_issues:
            is_valid.append(False)
            reasons.append("; ".join(row_issues))
        else:
            is_valid.append(True)
            reasons.append("VALID")

    # Split into clean and rejected datasets
    df_eval = df.copy()
    df_eval['validation_status'] = reasons

    rejected_df = df_eval[~pd.Series(is_valid)].copy()
    clean_df = df_eval[pd.Series(is_valid)].copy()
    clean_df = clean_df.drop(columns=['validation_status'])

    # Standardize Dates to ISO YYYY-MM-DD
    clean_df['date'] = pd.to_datetime(clean_df['date'], format='mixed', dayfirst=True).dt.strftime('%Y-%m-%d')

    # Normalize Customer Names (uppercase and whitespace trimmed)
    clean_df['customer_name'] = clean_df['customer_name'].astype(str).str.strip().str.upper()

    # Ensure amount is proper float
    clean_df['amount'] = clean_df['amount'].astype(float).round(2)

    # Business Analytics (Gold layer aggregation): Product performance summary
    summary_df = clean_df.groupby('product').agg(
        total_revenue=('amount', 'sum'),
        total_transactions=('transaction_id', 'count'),
        avg_order_value=('amount', 'mean')
    ).reset_index()
    summary_df['total_revenue'] = summary_df['total_revenue'].round(2)
    summary_df['avg_order_value'] = summary_df['avg_order_value'].round(2)

    return clean_df, rejected_df, summary_df

def load(clean_df, rejected_df, summary_df):
    # Save rejection audit log
    rejected_df.to_csv(REJECTED_DATA_PATH, index=False)

    # Load into local SQLite Data Warehouse
    conn = sqlite3.connect(DB_PATH)
    clean_df.to_sql("sales", conn, if_exists="replace", index=False)
    summary_df.to_sql("product_performance_summary", conn, if_exists="replace", index=False)
    conn.close()

def main():
    print("=" * 55)
    print("        RETAIL SALES ETL PIPELINE EXECUTION")
    print("=" * 55)
    
    raw_df = extract(RAW_DATA_PATH)
    total_raw = len(raw_df)
    
    clean_df, rejected_df, summary_df = transform(raw_df)
    
    load(clean_df, rejected_df, summary_df)
    
    print(f"[*] Ingested Records:      {total_raw}")
    print(f"[*] Valid Clean Records:   {len(clean_df)} (loaded into 'sales')")
    print(f"[*] Rejected Records:      {len(rejected_df)} (logged to '{REJECTED_DATA_PATH}')")
    print(f"[*] Gold Mart Generated:   {len(summary_df)} products summarized into 'product_performance_summary'")
    print(f"[*] Database Status:       Saved to '{DB_PATH}'")
    print("=" * 55)
    print("Pipeline execution completed successfully.")

if __name__ == "__main__":
    main()
