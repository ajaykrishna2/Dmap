import pandas as pd
df=pd.read_csv('/home/ajay/example4.csv',sep='[:, |_]',engine='python')
print(df)