#for displaying particular details of the state
import pandas as pd
from pandas.io.json import json_normalize
df = pd.read_json('/home/ajay/today.json',lines=True)


export_csv = df.to_csv (r'/home/ajay/sample.csv', index = None, header=True)
df2=pd.read_csv('/home/ajay/sample.csv')
df3=df2.groupby(['courseid','contentorg']).agg({'courseid':'first','enrolleduserscount':'sum','completionuserscount':'sum','certificateissuedcount':'sum','contentorg':'first','state':'first','collectionname':'first'})
# print(df3)
# df3=df2.groupby(['contentorg','state','courseid','collectionname']).agg({'enrolleduserscount':'sum','completionuserscount':'sum','certificateissuedcount':'sum'})
print(df3)
# df4=df3[(df3['contentorg'] == "['Delhi']")&(df3['state']=="Delhi")]
df4=df3[(df3.contentorg=="['Delhi']")&(df3['state']=="Delhi")]
print(df4)
# df6=df4.query('df4[state]=="Delhi"')
# df5=df4.groupby('courseid')['contentorg','state','courseid','collectionname','enrolleduserscount','completionuserscount','certificateissuedcount']
# print(df5)
df5=df4[['contentorg','state','courseid','collectionname','enrolleduserscount','completionuserscount','certificateissuedcount']]
df4.to_csv('/home/ajay/output.csv',index=None,header=True )
