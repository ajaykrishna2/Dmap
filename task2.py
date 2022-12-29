import pandas as pd
df = pd.read_csv("/home/ajay/inputJan2021.csv")

df1=df[(df['Batch start date'] >= '2021-01-01') & (df['Batch end date'] <= '2021-01-31 ')]
d=df1.groupby(['State']).agg({'Collection id':'nunique','Total enrolments By State':'sum','Total completion By State':'sum'})
print(d)
pivot=d.pivot_table(index=['State'], values=['Collection id','Total enrolments By State','Total completion By State'])
print(d)
pivot.to_csv ('export_dataframe.csv', index = True, header=True)
