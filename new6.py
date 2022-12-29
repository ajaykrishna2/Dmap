import pandas as pd
df=pd.read_csv('/home/ajay/file1.csv')
res = df.isin(['do_31315876717668761611109']).any().any()
if res:
    print('Element exists in Dataframe')
else:
    print('element doesnot exist')