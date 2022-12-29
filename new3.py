import pandas as pd
df = pd.read_json('/home/ajay/today.json',lines=True)
export_csv = df.to_csv (r'/home/ajay/sample.csv', index = None, header=True)
df2=pd.read_csv('/home/ajay/sample.csv')
df4=df2[(df2.contentorg=="['Delhi']")&(df2['state']=="Delhi")]
df5=df4[['contentorg','state','courseid','collectionname','enrolleduserscount','completionuserscount','certificateissuedcount','startdate']]
df6=df5.groupby('courseid').agg({'courseid':'first','enrolleduserscount':'sum','completionuserscount':'sum','certificateissuedcount':'sum','contentorg':'first','state':'first','collectionname':'first','startdate':'first'})

df6.to_csv('/home/ajay/output1.csv',index=None,header=True )
