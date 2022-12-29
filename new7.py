import pandas as pd
df1=pd.read_csv('/home/ajay/file1.csv')
df2=pd.read_csv('/home/ajay/file4.csv')
df1['exists'] = df1.course_id.isin(df2.course_id)
df1.to_csv('/home/ajay/todayout1.csv', index=False)
