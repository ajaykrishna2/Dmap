import pandas as pd

data = pd.read_csv("/home/ajay/15tmarch.csv")

d=data.groupby(['Collection id']).agg({'Total enrolments By State':'sum','Total completion By State':'sum','Total Certificate issued by State':'sum'})
print(d)
pivot=d.pivot_table(index=['Collection id'], values=['Total enrolments By State','Total completion By State','Total Certificate issued by State'])
print(pivot)
pivot.to_csv ('/home/ajay/abc.csv', index = True, header=True)