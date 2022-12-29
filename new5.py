import pandas as pd
df = pd.read_json('/home/ajay/today.json',lines=True)
export_csv = df.to_csv (r'/home/ajay/sample.csv', index = None, header=True)
df1=pd.read_csv('/home/ajay/sample.csv')
df2=df1[(df1.contentorg=="['Delhi']")&(df1['state']=="Delhi")]
df3=df2[['contentorg','state','batchid','courseid','enrolleduserscount','completionuserscount','certificateissuedcount','startdate','enddate','hascertified','batchid']]
print(df3)
df4=df3.groupby(['courseid']).agg({'courseid':'first','enrolleduserscount':'sum','completionuserscount':'sum','certificateissuedcount':'sum','contentorg':'first','state':'first','enddate':'first','startdate':'first','hascertified':'first'})
df5=df4[['courseid','contentorg','batchid','enrolleduserscount','completionuserscount','certificateissuedcount','startdate','enddate','hascertified']]
df5.to_csv('/home/ajay/today3.csv')
df6=pd.read_csv('/home/ajay/today3.csv')
df7=df6[['courseid','contentorg','enrolleduserscount','completionuserscount','certificateissuedcount','startdate','enddate','hascertified']]
# df5.columns = ['tenant_name','courseid','Total_Enrollment','Total_Completion','Total_Certifications','start_date','end_date','Has certificate']
df8=pd.read_csv("/home/ajay/today2.csv")
df9=df8[(df8['State Name/Org Name']=="Delhi")]
df10=df9[['course name','course_id']]
# df10.columns = ['course_name','course_id']
df11=pd.merge(df7,df10,left_on='courseid', right_on='course_id')
df12=df11[['contentorg','courseid','course name','startdate','enddate','enrolleduserscount','completionuserscount','hascertified','certificateissuedcount']]
df12.columns = ['tenant_name', 'courseid','course name','start_date', 'end_date', 'Total_Enrollment', 'Total_Completion',  'Has certificate','Total_Certifications',]
print(df12)
df12.to_csv('/home/ajay/final.csv')
