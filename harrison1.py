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
class Harrison:
    def Harrison(self,df,inf, writer):
        try:
            # dfw =df[df.groupby(['CLIENT ACCOUNT #'])['FACS #'].transform('nunique') > 1]
            # df.drop(df[df.groupby(['CLIENT ACCOUNT #'])['FACS #'].transform('nunique') > 1].index,inplace=True)
            print(len(df))
            df.drop('Last Payment Date.1', axis=1, inplace=True)
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
            df['year2'] = pd.DatetimeIndex(df['List Date']).year
            df['month2'] = pd.DatetimeIndex(df['List Date']).month
            df['day2'] = pd.DatetimeIndex(df['List Date']).day
            index_name = df[(df['year2'] >= df['year1']) & (df['month2'] >= df['month1']) & (df['day2'] > df['day1'])].index
            df.drop(index_name, inplace=True)
            df.drop('year1', axis=1, inplace=True)
            df.drop('year2', axis=1, inplace=True)
            df.drop('month1', axis=1, inplace=True)
            df.drop('month2', axis=1, inplace=True)
            df.drop('day1', axis=1, inplace=True)
            df.drop('day2', axis=1, inplace=True)
            df.drop('Date', axis=1, inplace=True)

            df1 = df[df.duplicated(['CLIENT ACCOUNT #'], keep=False)].sort_values('CLIENT ACCOUNT #')
            df2 = df[df.duplicated(['CLIENT ACCOUNT #'])].sort_values('CLIENT ACCOUNT #')
            dfw = df1[df1.groupby(['CLIENT ACCOUNT #'])['FACS #'].transform('nunique') > 1]
            dfw1=dfw[dfw['Recon file (Harrison) balance'].isna()]
            dfw2=dfw[~dfw['Recon file (Harrison) balance'].isna()]
            # df1.drop(df1[df1.groupby(['CLIENT ACCOUNT #'])['FACS #'].transform('nunique') > 1].index, inplace=True)
            i=df2.index
            df.drop(i, inplace=True)
            df3 = df1[df1['Recon file (Harrison) balance'].isna()]

            df4= df1[~df1['Recon file (Harrison) balance'].isna()]

            df3 = df3.reset_index(drop=True)
            df4 = df4.reset_index(drop=True)

            df3["Recon file (Harrison) balance"] = df4["Recon file (Harrison) balance"]
            df3['Match?'] = np.where(df3['Med-1 Balance'] == df3['Recon file (Harrison) balance'], 'True', 'False')
            print(df3.to_string())
            df3['Issue Detected'] = df3['Match?'].apply(lambda x: 'Balance Match' if x == 'True' else 'Balance Mismatch')
            df3.drop('Match?', axis=1, inplace=True)

            print(df1)

            # dfw1 = df1[df1.groupby(['CLIENT ACCOUNT #'])['FACS #'].transform('nunique') > 1]
            df5 = pd.concat([df,df3])
            df5=df5[['Issue Detected','FACS #','CLIENT ACCOUNT #','Client ID','First Name','Last Name','Disposition','Phase','List Date','Med-1 Balance','Amount Cancelled','Recon file (Harrison) balance','Cancel Code','Cancel Description','Cancel Date','Last Payment Date','Harrison F/C','Send Dt/Tm']]
            df6 = df5[df5['Issue Detected'] == "Acct is in Harrison file but closed in FACS"]
            df7=df5[df5['Issue Detected'] == "Account is in FACS, but not in the Harrison file"]

            df8=df5[df5['Issue Detected'] == "Account is in Harrison CO File, but it is not in FACS."]
            df9=df5[df5['Issue Detected'] == "The balance in FACS is greater than the bal in the Harrison file"]
            df10=df5[df5['Issue Detected'] == "The balance in the Harrison file is greater than the bal in FACS"]
            df11=df3[df3['Issue Detected'] == "Balance Mismatch"]
            df12=df5[df5['Issue Detected'] == "The balances in FACS and the Harrison file match"]
            df13=df3[df3['Issue Detected'] == "Balance Match"]
            df14=pd.concat([df9, df10])
            df15=pd.concat([df14, df11])
            df16=pd.concat([df12, df13])

            inf_dup=inf[inf.duplicated(['Client REF #'])].sort_values('Client REF #').index
            inf.drop(inf_dup, inplace=True)


            inf['Issue Deteched']=''
            inf['Phase'] = ''
            inf['send dt/tm'] = ''
            inf.drop(labels=['Unnamed: 15','Last Pay DTE','Unnamed: 20'], axis="columns", inplace=True)
            inf = inf.rename(columns={'Unnamed: 17': 'Last Pay DTE', 'Current BAL': 'Med1 BAL'},inplace=False)
            date_sr4 = pd.to_datetime(pd.Series(inf['Last Pay DTE']))
            inf['Last Pay DTE'] = date_sr4.dt.strftime('%m-%d-%Y')
            inf = inf[['Issue Deteched','FACS Acct','Client REF #','Client ID','First Name','Last Name','Disposition','Phase','List DTE',	'Med1 BAL',	'AMT Cancelled','Recon File BAL','Cancel Code',	'Cancel Description', 'Cancel DTE',	'Last Pay DTE','Client Name','send dt/tm']]
            inf = inf.drop(inf[inf['Cancel Code'] == 11].index)
            inf = inf.drop(inf[inf['Cancel Code'] == 71].index)
            # inf = inf.drop(inf[inf['Cancel Code'] == 75].index)



            inf1 = inf[inf.duplicated(['Client REF #'], keep=False)].sort_values('Client REF #')

            inf=inf.drop(inf1[inf1['Cancel Code'] == 75].index)


            inf2=inf.sort_values(by="List DTE").drop_duplicates(subset=["Client REF #"], keep="last")
            inf2= inf2.rename(columns={'Issue Deteched':'Issue Detected','FACS Acct': 'FACS #', 'Client REF #': 'CLIENT ACCOUNT #','List DTE': 'List Date','AMT Cancelled':'Amount Cancelled','Med1 BAL':'Med-1 Balance','Recon File BAL':'Recon file (Harrison) balance','Cancel DTE':'Cancel Date','Last Pay DTE':'Last Payment Date','send dt/tm':'Send Dt/Tm'}, inplace=False)
            inf2.drop(labels=['Client Name'], axis="columns", inplace=True)
            inf2['CLIENT ACCOUNT #'] = inf2['CLIENT ACCOUNT #'].astype(str)
            print(len(df8))
            print(len(inf2))
            inf3 = pd.merge(df8, inf2, on='CLIENT ACCOUNT #')

            inf3=inf3[['Issue Detected_x','CLIENT ACCOUNT #','Harrison F/C','Send Dt/Tm_x','FACS #_y','Client ID_y','First Name_y','Last Name_y','Disposition_y','Phase_y','List Date_y','Med-1 Balance_y','Amount Cancelled_y','Recon file (Harrison) balance_y','Cancel Code_y','Cancel Description_y','Cancel Date_y','Last Payment Date_y']]
            inf3 = inf3.rename(columns={'Issue Detected_x':'Issue Detected',  'Send Dt/Tm_x':'Send Dt/Tm', 'FACS #_y':'FACS #', 'Client ID_y':'Client ID',
                 'First Name_y':'First Name', 'Last Name_y':'Last Name', 'Disposition_y':'Disposition', 'Phase_y':'Phase', 'List Date_y':'List Date', 'Med-1 Balance_y':'Med-1 Balance',
                 'Amount Cancelled_y':'Amount Cancelled', 'Recon file (Harrison) balance_y':'Recon file (Harrison) balance', 'Cancel Code_y':'Cancel Code','Cancel Description_y': 'Cancel Description',
                 'Cancel Date_y':'Cancel Date','Last Payment Date_y':'Last Payment Date'}, inplace=False)
            inf3=inf3[['Issue Detected', 'FACS #', 'CLIENT ACCOUNT #', 'Client ID', 'First Name', 'Last Name', 'Disposition',
                 'Phase', 'List Date', 'Med-1 Balance', 'Amount Cancelled', 'Recon file (Harrison) balance',
                 'Cancel Code', 'Cancel Description', 'Cancel Date', 'Last Payment Date', 'Harrison F/C', 'Send Dt/Tm']]
            # print(inf3.to_string())
            # inf3["Issue Detected"].replace({"Account is in Harrison CO File, but it is not in FACS.": "Acct is in Harrison file but closed in FACS"}, inplace=True)
            inf4 = inf3[inf3.duplicated(['CLIENT ACCOUNT #'], keep=False)].sort_values('CLIENT ACCOUNT #')
            df18=pd.concat([df6,inf4])
            df19=inf3[((inf3['Disposition'] == '9000')|(inf3['Disposition'] == '9999'))]
            df19["Issue Detected"].replace({"Account is in Harrison CO File, but it is not in FACS.": "Acct is in Harrison file but closed in FACS"}, inplace=True)
            df20=pd.concat([df18,df19])#closed facs
            inf3=inf3.drop(inf3[((inf3['Disposition'] == '9000')|(inf3['Disposition'] == '9999'))].index)
            inf3['Match?'] = np.where(inf3['Med-1 Balance'] == inf3['Recon file (Harrison) balance'], 'True', 'False')
            inf3['Issue Detected'] = inf3['Match?'].apply(
                lambda x: 'Balance Match' if x == 'True' else 'Balance Mismatch')
            # print(df3)
            inf3.drop('Match?', axis=1, inplace=True)
            df21 = inf3[inf3['Issue Detected'] == "Balance Match"]
            df22 = inf3[inf3['Issue Detected'] == "Balance Mismatch"]
            df23 = pd.concat([df16, df21])
            df24 = pd.concat([df15, df22])

            inf3=inf3.drop(inf3[((inf3['Issue Detected'] == 'Balance Match') | (inf3['Issue Detected'] == 'Balance Mismatch'))].index)
            # print(df7.to_string())


            index_names5 = df7[df7['CLIENT ACCOUNT #'].str.startswith("F", na=False)].index
            df7.drop(index_names5, inplace=True)
            index_names6=df7[df7['Med-1 Balance']==0].index
            df7.drop(index_names6, inplace=True)
            df7 = df7.drop(df7[~( (df7['Phase'] == 10))].index)
            # df7 = df7.drop(df7[~(df7['Phase'] == 30)].index)
            df25=pd.concat([inf3,dfw2])


            df7['Cancel Code']=''
            df15['Cancel Code'] = ''
            df16['Cancel Code'] = ''
            # dfw1['Cancel Code'] = ''
            df7['Cancel Description'] = ''
            df15['Cancel Description'] = ''
            df16['Cancel Description'] = ''
            # dfw1['Cancel Description'] = ''


            df20.to_excel(writer, index=False, sheet_name='Closed in FACS')
            df7.to_excel(writer, index=False, sheet_name='FACS not RECON')
            df25.to_excel(writer, index=False, sheet_name='RECON not FACS')
            df24.to_excel(writer, index=False, sheet_name='Balance Mismatch')
            df23.to_excel(writer, index=False, sheet_name='Balance Match')
            dfw1.to_excel(writer, index=False, sheet_name='Multiples')


        except Exception as e:
            logging.exception("error")





if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/harison1.xlsx', engine='xlsxwriter',options={'strings_to_numbers':True} )
    df_facs1 = pd.read_csv("/home/ajay/Downloads/HA2_EO_HOSP_PHY_RECON_060321_57559.TXT",delimiter="\t")
    info_facs1 = pd.read_csv("/home/ajay/Downloads/info-out_EO NOT_in_FACS.TXT",delimiter="|")
    # print(info_facs1.to_string())
    reconcilation=Harrison()
    reconcilation.Harrison(df_facs1,info_facs1,writer)
    writer.save()