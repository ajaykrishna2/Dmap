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
from datetime import datetime
import numpy as np

class parkview:
    def Parkview(self,df,writer):
        try:
            column_indexes = list(df.columns)
            df.reset_index(inplace=True)
            column_indexes = dict(zip(list(df.columns), column_indexes))
            df = df.rename(columns={'Cancel Description': ''})
            df.rename(columns=column_indexes, inplace=True)
            pd.set_option('display.float_format', lambda x: '%.0f' % x)
            date_sr = pd.to_datetime(pd.Series(df['List Date']))
            df['List Date'] = date_sr.dt.strftime('%m-%d-%Y')
            date_sr1 = pd.to_datetime(pd.Series(df['Last Payment Date']))
            df['Last Payment Date'] = date_sr1.dt.strftime('%m-%d-%Y')
            date_sr1 = pd.to_datetime(pd.Series(df['Cancel Date']))
            df['Cancel Date'] = date_sr1.dt.strftime('%m-%d-%Y')
            df["Last Payment Date.1"]=df["Cancel Description"]
            df.drop(labels=["Cancel Description"], axis="columns", inplace=True)
            df= df.rename(columns = {'Last Payment Date.1':'Cancel Description'},inplace=False)
            df['Date']=pd.datetime.now().date()

            df['year1'] = pd.DatetimeIndex(df['Date']).year
            df['month1'] = pd.DatetimeIndex(df['Date']).month
            df['day1'] = pd.DatetimeIndex(df['Date']).day
            df['year2'] = pd.DatetimeIndex(df['List Date']).year
            df['month2'] = pd.DatetimeIndex(df['List Date']).month
            df['day2'] = pd.DatetimeIndex(df['List Date']).day
            df['day1']=df['day1'].sub(1)
            print(df['day1'])
            index_name=df[(df['year2']>=df['year1'])&(df['month2']>=df['month1'])&(df['day2']>df['day1'])].index
            df.drop(index_name, inplace=True)
            df.drop('year1',axis=1, inplace=True)
            df.drop('year2', axis=1, inplace=True)
            df.drop('month1', axis=1, inplace=True)
            df.drop('month2', axis=1, inplace=True)
            df.drop('day1', axis=1, inplace=True)
            df.drop('day2', axis=1, inplace=True)
            df.drop('Date', axis=1, inplace=True)
            df1 = df[df.duplicated(['EPIC #'], keep=False)].sort_values('EPIC #')
            df2 = df[df.duplicated(['EPIC #'])].sort_values('EPIC #')
            df3 = df1.merge(df2, indicator=True, how='left').loc[lambda x: x['_merge'] != 'both']
            df4 = df.merge(df1, indicator=True, how='left').loc[lambda x: x['_merge'] != 'both']
            df2["Recon file (EPIC) balance"] = df2["Recon file (EPIC) balance"]
            df4.drop('_merge', axis=1, inplace=True)
            # print(df4.to_string())
            # print(len(df4))
            df2 = df2.reset_index(drop=True)
            df3 = df3.reset_index(drop=True)
            # print(df2.to_string())
            df2["Recon file (EPIC) balance"] = df3["Recon file (EPIC) balance"]
            # print(df2.to_string())
            df2['Match?'] = np.where(df2['Med-1 Balance'] == df2['Recon file (EPIC) balance'], 'True', 'False')
            # create new column in df1 to check if prices match
            df2['Issue Detected'] = df2['Match?'].apply(lambda x: 'Balance Match' if x == 'True' else 'Balance Mismatch')
            df2.drop('Match?', axis=1, inplace=True)
            # print(df4.to_string())
            df2['EPIC #'] = df2['EPIC #'].apply(str)
            df4['EPIC #'] = df4['EPIC #'].apply(str)
            df4['regex'] = df4['Client ID'].str.contains('IFU', regex=True)
            df2['regex'] = df2['Client ID'].str.contains('IFU', regex=True)

            df5 = df4[df4['Issue Detected'] == "Account is closed in FACS, but open in PV File."]
            df6 = df4[df4['Issue Detected'] == "Account is in FACS, but not in Park View File."]
            df7 = df4[df4['Issue Detected'] == "Account is in PV File, but it is not in FACS."]
            df8 = df4[(df4['Issue Detected'] == "The balance in FACS is greater than the balance in PV File.")]
            df9 = df4[(df4['Issue Detected'] == "The balance in PV File is greater than the balance in FACS.")]
            df10 = pd.concat([df8, df9])
            df11 = df2[df2['Issue Detected'] == "Balance Mismatch"]
            df12 = pd.concat([df10, df11])
            df13 = df4[df4['Issue Detected'] == "The balances in FACS and PV File are same."]
            df14 = df2[df2['Issue Detected'] == "Balance Match"]
            df15 = pd.concat([df13, df14])
            # df12['Cancel Code'] = ''
            # df15['Cancel Code'] = ''
            # df12['Cancel Description'] = ''
            # df15['Cancel Description'] = ''
            df16=df5[df5['regex']==True]
            df17 = df5[df5['regex'] == False]
            df18 = df6[df6['regex'] == True]
            df19 = df6[df6['regex'] == False]
            df22 = df12[df12['regex'] == True]
            df23 = df12[df12['regex'] == False]
            df24 = df15[df15['regex'] == True]
            df25 = df15[df15['regex'] == False]
            df7.drop('regex', axis=1, inplace=True)
            df16.drop('regex', axis=1, inplace=True)
            df17.drop('regex', axis=1, inplace=True)
            df18.drop('regex', axis=1, inplace=True)
            df19.drop('regex', axis=1, inplace=True)
            df22.drop('regex', axis=1, inplace=True)
            df23.drop('regex', axis=1, inplace=True)
            df24.drop('regex', axis=1, inplace=True)
            df25.drop('regex', axis=1, inplace=True)
            df16.to_excel(writer, index=False, sheet_name='IFU Closed in FACS')
            df17.to_excel(writer, index=False, sheet_name='WCP Closed in FACS')
            df18.to_excel(writer, index=False, sheet_name='IFU FACS not RECON')
            df19.to_excel(writer, index=False, sheet_name='WCP FACS not RECON')
            df7.to_excel(writer, index=False, sheet_name='RECON not FACS')
            df22.to_excel(writer, index=False, sheet_name='IFU Balance Mismatch')
            df23.to_excel(writer, index=False, sheet_name='WCP Balance Mismatch')
            df24.to_excel(writer, index=False, sheet_name='IFU Balance Match')
            df25.to_excel(writer, index=False, sheet_name='WCP Balance Match')




        except Exception as e:
            logging.exception("error")




if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/PARKVIEW_EPIC_RECON_010522_6005.xlsx')
    excel = '/home/ajay/Downloads/PARKVIEW_EPIC_RECON_010522_6005.TXT'
    df = pd.read_csv(excel, sep='\t')
    df_facs1=df
    reconcilation=parkview()
    reconcilation.Parkview(df_facs1,writer)
    writer.save()