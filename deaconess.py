import pandas as pd
import sys
import logging
from pandas.api.types import CategoricalDtype
from natsort import index_natsorted
import xlrd
import os
import openpyxl
from openpyxl.workbook import Workbook
import xlsxwriter
import sys
import logging
import xlrd
import os
from openpyxl.workbook import Workbook
import xlsxwriter
import numpy as np
import sidetable
from datetime import date
import locale
import numpy as np
from pandas import DatetimeIndex
import datetime
class deaconess:
    def Deaconess(self,df,inf, writer):
        try:
            pd.set_option('display.float_format', lambda x: '%.0f' % x)
            date_sr = pd.to_datetime(pd.Series(df['List Date']))
            df['List Date'] = date_sr.dt.strftime('%m-%d-%Y')
            date_sr1 = pd.to_datetime(pd.Series(df['Last Payment Date']))
            df['Last Payment Date'] = date_sr1.dt.strftime('%m-%d-%Y')
            date_sr1 = pd.to_datetime(pd.Series(df['Cancel Date']))
            df['Cancel Date'] = date_sr1.dt.strftime('%m-%d-%Y')
            df['Date'] = pd.datetime.now().date()
            df['year1'] = pd.DatetimeIndex(df['Date']).year
            df['month1'] = pd.DatetimeIndex(df['Date']).month
            df['day1'] = pd.DatetimeIndex(df['Date']).day
            df['year2'] = pd.DatetimeIndex(df['Cancel Date']).year
            df['month2'] = pd.DatetimeIndex(df['Cancel Date']).month
            df['day2'] = pd.DatetimeIndex(df['Cancel Date']).day
            index_name = df[(df['year2'] >= df['year1']) & (df['month2'] >= df['month1']) & (df['day2'] >= df['day1'])].index
            df.drop(index_name, inplace=True)
            df.drop('year1', axis=1, inplace=True)
            df.drop('year2', axis=1, inplace=True)
            df.drop('month1', axis=1, inplace=True)
            df.drop('month2', axis=1, inplace=True)
            df.drop('day1', axis=1, inplace=True)
            df.drop('day2', axis=1, inplace=True)
            df.drop('Date', axis=1, inplace=True)
            print(df[df['Issue Detected'] == "EPIC has this account in Med1 Bad Debt, but the account is in the 1000 phase."].to_string())
            df1 = df[df.duplicated(['EPIC #'], keep=False)].sort_values('EPIC #')
            ph1 = df1[df1['Issue Detected'] == 'EPIC has this account in Early Out, but the account is in the 3000 phase.'].index
            ph2 = df1[df1['Issue Detected'] == 'EPIC has this account in Med1 Bad Debt, but the account is in the 1000 phase.'].index
            ph3 = df1[df1['Issue Detected'] == 'EPIC has this account in Med1 Bad Debt, but the account is in the 3000 phase.'].index
            ph4 = df1[df1['Issue Detected'] == "EPIC has this account in Med1 Outsource, but the account is in the 1000 phase."].index
            ph5 = df1[df1['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 128ERP client ID."].index
            ph6 = df1[df1['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 128WCP client ID."].index
            ph7 = df1[df1['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 132INS client ID."].index
            df1.drop(ph1, inplace=True)
            df1.drop(ph2,inplace=True)
            df1.drop(ph3,inplace=True)
            df1.drop(ph4,inplace=True)
            df1.drop(ph5,inplace=True)
            df1.drop(ph6,inplace=True)
            df1.drop(ph7,inplace=True)
            df1.drop(df1[df1['Issue Detected'] == 'The balance in FACS and EPIC match'].index, inplace=True)
            dfw = df1[df1.groupby(['EPIC #'])['FACS #'].transform('nunique') > 1]
            df1.drop(dfw[(dfw['FACS #'].isna())].index,inplace=True)
            df2 = df[df.duplicated(['EPIC #'])].sort_values('EPIC #')
            df2.drop(df2[df2['Issue Detected'] == 'The balance in FACS and EPIC match'].index, inplace=True)


            # df2.drop(df2[df2.groupby(['EPIC #'])['FACS #'].transform('nunique') > 1].index, inplace=True)

            print(df2[df2['Issue Detected'] == 'EPIC has this account in Med1 Bad Debt, but the account is in the 3000 phase.'])
            p1 = df2[df2['Issue Detected'] == 'EPIC has this account in Early Out, but the account is in the 3000 phase.'].index
            p2 =  df2[df2['Issue Detected'] == 'EPIC has this account in Med1 Bad Debt, but the account is in the 1000 phase.'].index
            p3 = df2[df2['Issue Detected'] == 'EPIC has this account in Med1 Bad Debt, but the account is in the 3000 phase.'].index
            p4 = df2[df2['Issue Detected'] == "EPIC has this account in Med1 Outsource, but the account is in the 1000 phase."].index
            p5 = df2[df2['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 128ERP client ID."].index
            p6 = df2[df2['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 128WCP client ID."].index
            p7 = df2[df2['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 132INS client ID."].index
            df2.drop(df2[df2['Issue Detected'] == 'The balance in FACS and EPIC match'].index,inplace=True)

            df2.drop(p1,inplace=True)
            df2.drop(p2, inplace=True)
            df2.drop(p3, inplace=True)
            df2.drop(p4, inplace=True)
            df2.drop(p5, inplace=True)
            df2.drop(p6, inplace=True)
            df2.drop(p7, inplace=True)

            i = df2.index
            df.drop(i, inplace=True)

            print(df[df['Issue Detected'] == 'EPIC has this account in Med1 Bad Debt, but the account is in the 1000 phase.'])
            df3=df1.merge(df2)

            print(len(df2))
            print(len(df3))
            df2 = df2.reset_index()
            df3 = df3.reset_index()
            # print(len(df2))

            df2["Recon file (EPIC) balance"] = df3["Recon file (EPIC) balance"]
            df2['Match?'] = np.where(df2['Med-1 Balance'] == df2['Recon file (EPIC) balance'], 'True', 'False')
            df2['Issue Detected'] = df2['Match?'].apply(lambda x: 'Balance Match' if x == 'True' else 'Balance Mismatch')
            df2.drop('Match?', axis=1, inplace=True)


            df4 = df[df['Issue Detected'] == "Account is closed in FACS, but open in EPIC."]
            df5= df[df['Issue Detected'] == "Account is in FACS, but not in Deaconess EPIC."]
            df6 = df[df['Issue Detected'] == "Account is in EPIC, but it is either not in FACS, or does not have EPIC flag."]


            df71=df[df['Issue Detected'] == "EPIC has this account in Early Out, but the account is in the 3000 phase."]
            print(len(df71))
            df72 = df[df['Issue Detected'] == "EPIC has this account in Med1 Bad Debt, but the account is in the 1000 phase."]
            print(len(df72))
            df73 = df[df['Issue Detected'] == "EPIC has this account in Med1 Bad Debt, but the account is in the 3000 phase."]
            print(len(df73))
            df74 = df[df['Issue Detected'] == "EPIC has this account in Med1 Outsource, but the account is in the 1000 phase."]
            print(len(df74))
            df75 = df[df['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 128ERP client ID."]
            print(len(df75))
            df76 = df[df['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 128WCP client ID."]
            print(len(df76))
            df77 = df[df['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 132INS client ID."]
            print(len(df77))
            df7=pd.concat([df71,df72,df73,df74,df75,df76,df77])
            print(len(df7))
            df8 = df[df['Issue Detected'] == "The balance in EPIC is greater than the balance in FACS."]
            df9 = df[df['Issue Detected'] == "The balance in FACS is greater than the balance in EPIC."]
            df11 = df2[df2['Issue Detected'] == "Balance Mismatch"]
            df12 =pd.concat([df8,df9])
            df13 =pd.concat([df12,df11])
            df10 = df[df['Issue Detected'] == "The balance in FACS and EPIC Match."]
            df14 = df2[df2['Issue Detected'] == "Balance Match"]
            df15=pd.concat([df10,df14])
            print(df4.info())
            print(df4.head(10).to_string())
            df4.drop(df4[(df4['Disposition']=='9000')&(df4['Cancel Code']=='4')].index,inplace=True)
            df4.drop(df4[df4['Cancel Code'].isna()].index,inplace=True)
            print(inf.head(20).to_string())
            inf['Issue Deteched'] = ''
            inf['Phase'] = ''
            inf['Payment Date']=''
            inf['Days in Dispo']=np.NAN
            inf['PMT TO PRN']=np.NAN
            inf.drop(labels=['Unnamed: 15', 'Unnamed: 17', 'Unnamed: 20'], axis="columns", inplace=True)
            date_sr = pd.to_datetime(pd.Series(inf['List DTE']))
            inf['List DTE'] = date_sr.dt.strftime('%d-%m-%Y')
            inf = inf[['Issue Deteched', 'FACS Acct', 'Client REF #', 'Client ID', 'First Name', 'Last Name', 'Disposition','Phase', 'List DTE','Current BAL',  'Recon File BAL','AMT Cancelled','Payment Date', 'Cancel Code','Last Pay DTE', 'Days in Dispo', 'Cancel DTE','PMT TO PRN']]
            inf2 = inf.rename(columns={'Issue Deteched': 'Issue Detected', 'FACS Acct': 'FACS #', 'Client REF #': 'EPIC #',
                         'List DTE': 'List Date', 'AMT Cancelled': 'Amount Cancelled', 'Current BAL': 'Med-1 Balance',
                         'Recon File BAL': 'Recon file (EPIC) balance', 'Cancel DTE': 'Cancel Date','Last Pay DTE': 'Last Payment Date'}, inplace=False)
            inf2['Cancel Code']=pd.to_numeric(inf2['Cancel Code'] ,errors='coerce').astype(float)
            print(len(inf2))
            index11=inf2[(inf2['Cancel Code']==71)|(inf2['Cancel Code']==11)].index
            inf2.drop(index11,inplace=True)
            # inf2['EPIC #'] = inf2['EPIC #'].astype(str)
            # inf3=pd.concat([df6,inf2])
            print(len(inf2))
            inf3 = pd.merge(df6, inf2, on='EPIC #', how='left')
            indexd=inf3[inf3.duplicated(['EPIC #'])].sort_values('EPIC #')
            inf3.drop(indexd.index,inplace=True)
            inf3=inf3.rename(columns={'Issue Detected_x':'Issue Detected','Recon file (EPIC) balance_x':'Recon file (EPIC) balance','FACS #_y':'FACS #','Client ID_y':'Client ID','First Name_y':'First Name','Last Name_y':'Last Name','Disposition_y':'Disposition','Phase_y':'Phase','List Date_y':'List Date','Med-1 Balance_y':'Med-1 Balance','Amount Cancelled_y':'Amount Cancelled','Payment Date_y':'Payment Date','Cancel Code_y':'Cancel Code','Last Payment Date_y':'Last Payment Date','Days in Dispo_y':'Days in Dispo','Cancel Date_y':'Cancel Date' ,'PMT TO PRN_y':'PMT TO PRN' }, inplace=False)
            inf3=inf3[['Issue Detected','FACS #','EPIC #','Client ID','First Name','Last Name','Disposition','Phase','List Date','Med-1 Balance','Recon file (EPIC) balance','Amount Cancelled','Payment Date','Cancel Code','Last Payment Date','Days in Dispo','Cancel Date','PMT TO PRN']]
            print('hi')
            indexn=inf3[~inf3['FACS #'].isna()].index
            print(len(indexn))
            inf3.drop(indexn,inplace=True)
            print(len(inf3))
            indexg=df5[(df5['Phase']==10)&((df5['Disposition']=='1TEM')|(df5['Disposition'] =='1MCB')|(df5['Disposition'] =='1700')|(df5['Disposition'] == '3700')|(df5['Disposition']=='2TEM')|(df5['Disposition']=='3TEM')|(df5['Disposition']=='5TEM'))].index
            df5.drop(indexg,inplace=True)
            indexbkr = df5[(df5['Disposition'] == '1BKR')].index
            df5.drop(indexbkr, inplace=True)
            indexmex=df7[df7['Med-1 Balance']<=0].index
            df7.drop(indexmex,inplace=True)


            df13['Date1'] = pd.datetime.now().date()
            df13['year1'] = pd.DatetimeIndex(df13['Date1']).year
            df13['month1'] = pd.DatetimeIndex(df13['Date1']).month
            df13['day1'] = pd.DatetimeIndex(df13['Date1']).day
            df13['year2'] = pd.DatetimeIndex(df13['Payment Date']).year
            df13['month2'] = pd.DatetimeIndex(df13['Payment Date']).month
            df13['day2'] = pd.DatetimeIndex(df13['Payment Date']).day
            index_name13 = df13[(df13['year2'] >= df13['year1']) & (df13['month2'] >= df13['month1']) & (df13['day2'] >= df13['day1'])].index
            df13.drop('year1', axis=1, inplace=True)
            df13.drop('year2', axis=1, inplace=True)
            df13.drop('month1', axis=1, inplace=True)
            df13.drop('month2', axis=1, inplace=True)
            df13.drop('day1', axis=1, inplace=True)
            df13.drop('day2', axis=1, inplace=True)
            df13.drop('Date1', axis=1, inplace=True)

            df13.drop(index_name13, inplace=True)
            index_13=df13[(df13['Recon file (EPIC) balance']<0)|(df13['Recon file (EPIC) balance'].isna())].index
            df13.drop(index_13,inplace=True)
            print(len(df7))
            df4.to_excel(writer, index=False, sheet_name='Closed in FACS')
            df5.to_excel(writer, index=False, sheet_name='FACS not RECON')
            inf3.to_excel(writer, index=False, sheet_name='RECON not FACS')
            df7.to_excel(writer, index=False, sheet_name='Phase Mismatch')
            df13.to_excel(writer, index=False, sheet_name='Balance Mismatch')
            df15.to_excel(writer, index=False, sheet_name='Balance Match')
            dfw.to_excel(writer, index=False, sheet_name='Multiples')
        except Exception as e:
            logging.exception("error")




if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/EPC_RECON_052621_48227_DEF.xlsx', engine='xlsxwriter',options={'strings_to_numbers':True} )
    df_facs1 = pd.read_csv("/home/ajay/Downloads/Deaconess_DEF11/EPC_RECON_052621_48227.TXT",delimiter="\t")
    info_facs1 = pd.read_csv("/home/ajay/Downloads/Deaconess_DEF11/info-out_PUT_in_FACS.TXT", delimiter="|")
    reconcilation=deaconess()
    reconcilation.Deaconess(df_facs1,info_facs1,writer)
    writer.save()
