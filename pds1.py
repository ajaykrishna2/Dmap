import pandas as pd
import openpyxl
import xlsxwriter
xls = pd.ExcelFile('/home/ajay/Downloads/Community_Apps_Nov.xlsx',engine='openpyxl')
df1 = pd.read_excel(xls, 'COMAPP',engine='openpyxl')
xls = pd.ExcelFile('/home/ajay/Downloads/WellFundMonthlyActivityDetails.HB.PB.202011.xlsx',engine='openpyxl')
df2 = pd.read_excel(xls, 'Details',engine='openpyxl')

# writer = pd.ExcelWriter('/home/ajay/pds/COMAPP1.xlsx', index_col=0, engine='xlsxwriter')
# df1.to_excel(writer, sheet_name='Sheet1')
# df2.to_excel(writer, sheet_name='Sheet2')
# writer.save()
df3=df1[['DATE LISTED','FIRST NAME','LAST NAME','DISPOSITION','ACCT# FROM CLT','MRN NUM','BABY GRAM APPR','HIP APPROVED','INSURANCE FOUND','HPE APPROVED','HPE DENIED','HHW APPROVED','MK APPROVED','DATE APP COMP','MSP LVL','MK EFF DATE','RECERTIFICATION','MSP APPROVED','COBRA','ACCOUNT #','DATE DISP CHANGE','CLIENT','PREVIOUS DISPO','ACCT CLASS']]
df3.columns=['DATE LISTED','FIRST NAME','LAST NAME','DISPOSITION','HAR','MRN NUM','BABY GRAM APPR','HIP APPROVED','INSURANCE FOUND','HPE APPROVED','HPE DENIED','HHW APPROVED','MK APPROVED','DATE APP COMP','MSP LVL','MK EFF DATE','RECERTIFICATION','MSP APPROVED','COBRA','ACCOUNT #','DATE DISP CHANGE','CLIENT','PREVIOUS DISPO','ACCT CLASS']
# common=pd.merge(df3,df2,left_on='ACCT# FROM CLT', right_on='HAR')
common=pd.merge(df3,df2,how='inner',on=['HAR'])
# print(common)
df4= df3[(~df3.HAR.isin(common.HAR))]

print(df4)

df5= df2[(~df2.HAR.isin(common.HAR))]
# df5.columns=['Patient MRN','HAR','Column1','HAR Type','Patient','Base Class','BI Add Date','BI Added User','Billing Indicator Customer','BI Description','Admit Date','Discharge Date','Sum of Fee','Department','Location']
print(df5)
path = '/home/ajay/COMMAPP1.xlsx'

with pd.ExcelWriter(path,engine="openpyxl",mode='a') as writer:
    writer.book = openpyxl.load_workbook(path)
    df5.to_excel(writer, sheet_name='In Epic not in Facs', index=False)
    df4.to_excel(writer, sheet_name='In FACS not in EPIC',index=False)
