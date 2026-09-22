import pandas as pd

df = pd.read_csv("raw_sales.csv")
# print(df.head())

df = df.dropna()

df['date'] = pd.to_datetime(df['date'], format='mixed', dayfirst=True).dt.strftime('%Y-%m-%d')
# print(df['date'].head())
