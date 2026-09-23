import pandas as pd
import sqlite3

df = pd.read_csv("raw_sales.csv")
# print(df.head())

df = df.dropna()

df['date'] = pd.to_datetime(df['date'], format='mixed', dayfirst=True).dt.strftime('%Y-%m-%d')
# print(df['date'].head())

df['customer_name'] = df['customer_name'].str.strip().str.upper()

conn = sqlite3.connect("warehouse.db")
df.to_sql("sales", conn, if_exists="replace", index=False)
conn.close()

print(f"ETL completed successfully. {len(df)} records loaded into warehouse.db.")
