import pandas as pd

df = pd.read_csv("raw_sales.csv")

df = df.dropna()

df['date'] = pd.to_datetime(df['date'])
print(df)
