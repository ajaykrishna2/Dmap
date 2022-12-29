import pandas as pd
df1=pd.read_csv("/home/ajay/today2.csv")
df4=df1[(df1['State Name/Org Name']=="Delhi")]
print(df4)

df2=pd.read_csv("/home/ajay/output1.csv")
df6=df4[['Course','course name','medium','course_id','State Name/Org Name']]
df5=df2[['courseid','enrolleduserscount','completionuserscount','certificateissuedcount','startdate']]
# df3=df5[df5.courseid.isin(df6.course_id)]
# print(df3)
# df7=pd.concat([df6,df5])
# print(df7)
df7=pd.merge(df5,df6,left_on='courseid', right_on='course_id')
df8=df7[['State Name/Org Name','course_id','Course','course name','medium','startdate','enrolleduserscount','completionuserscount','certificateissuedcount']]
df8.to_csv('/home/ajay/output2.csv',index=None,header=True )