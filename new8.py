import pandas as pd
df1=pd.read_csv('/home/ajay/input1.csv')
df2=pd.read_csv('/home/ajay/input2.csv')
# df3=df2[['course_id']]
# df3.columns=[['Collection_id']]
df2['exists'] = df1.Collection_id.isin(df2.course_id)
print(df2)
df2.to_csv('/home/ajay/todayout3.csv', index=False)


df3=df2[df2.exists==False]
df4=df3[['course_id','exists']]
df4.columns = ['Collection_id','exists']
print(df4)
d1=pd.DataFrame(df1)
d2=pd.DataFrame(df4)
df5=pd.merge(d2,d1,how='inner',on=['Collection_id'])
print(df5)
df6=df5[['Collection_id','Total enrolments By State','Total completion By State','Total Certificate issued by State']]
df6.to_csv('/home/ajay/nisthaout.csv',index=False)
