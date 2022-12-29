import pandas as pd
df = pd.read_csv("/home/ajay/inputJan2021.csv",)
print(df['Batch start date'])
print(df['Batch end date'])
df[(df['Batch start date'] > '2020-01-01') & (df['Batch end date'] <= '2020-01-31 ')]
print(df)