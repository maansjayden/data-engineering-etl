import pandas as pd

df = pd.read_csv("raw_sales.csv")
# print(df.head())

df = df.dropna()

# date parsing keeps breaking on mixed formats
df['date'] = pd.to_datetime(df['date'], errors='coerce')
print(df['date'])
