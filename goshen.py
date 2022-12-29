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
def Goshen(df,writer):
    date_sr = pd.to_datetime(pd.Series(df['List Date']))
    df['List Date'] = date_sr.dt.strftime('%d-%m-%Y')
    df1 = df[df.duplicated(['Goshen #'], keep=False)].sort_values('Goshen #')
    print(df1.to_string())
    df2 = df[df.duplicated(['Goshen #'])].sort_values('Goshen #')
    rdf=df1.merge(df2, indicator=True, how='left')
    rdf1=rdf[rdf['_merge'] == 'left_only']
    rdf1.drop('_merge', axis=1, inplace=True)
    df4 = df.merge(df1, indicator=True, how='left')
    df4.drop('_merge', axis=1, inplace=True)
    df4['Goshen #'] = df4['Goshen #'].apply(str)
    # df4['Disposition'] = pd.to_numeric(df4['Disposition'], errors='coerce')
    df10 = df4[df4['Issue Detected'] == "Account is in Goshen File, but it is not in FACS."]
    df3 = df4[df4['Goshen #'].str.contains("-",regex=True)]
    index_names = df4[df4['Goshen #'].str.contains("-",regex=True)].index
    df4.drop(index_names, inplace=True)
    df4['Year'] = DatetimeIndex(df4['List Date']).year
    index_name = df4[df4['Year'] < 2018].index
    df4.drop(index_name, inplace=True)
    df4.drop('Year', axis=1, inplace=True)
    df4=df4[["Issue Detected","FACS #","Goshen #","Client ID","First Name","Last Name","Disposition","Phase","List Date","FACS Balance","Recon file (Goshen) Balance","Amount Cancelled","Cancel Date","Cancel Code","Cancel Code Desc","Last Payment Date","Goshen Status"]]
    print(df4.info())
    # today = date.today()
    # today_date = today.strftime('%d-%m-%Y')
    # dt = datetime.datetime(today)
    # rows = df4['List Date'].apply(
    #     lambda x: x.year > dt.year and x.month > dt.month and x.day > dt.day
    # )
    # print(df4[rows])
    # today_date=today.strftime('%d-%m-%Y')
    # print(today_date)
    # index_name1 = df4[df4['List Date'] > today].index
    # df4.drop(index_name1, inplace=True)


    df5 = df4[df4['Issue Detected'] == "Account is closed in FACS, but open at Goshen."]
    df7 = df4[df4['Issue Detected'] == "Account is in FACS, but not in Goshen File."]
    df81 = df4[(df4['Issue Detected'] == "The balance in FACS is greater than the balance at Goshen.")]
    df82 = df4[(df4['Issue Detected'] == "The balance at Goshen is greater than the balance in FACS.")]
    df8=pd.concat([df81,df82])
    df9 = df4[(df4['Issue Detected'] == "Balance Match")]
    fdf=df7[(df7['Disposition'] == '9000')|(df7['Disposition'] == '9999')]
    index_names0 = df7[(df7['Disposition'] == '9000')|(df7['Disposition'] == '9999')].index
    df7.drop(index_names0, inplace=True)
    df6 = pd.concat([df5, rdf1,fdf])
    index_names1 = df6[df6['Cancel Code'] == 11].index
    df6.drop(index_names1, inplace=True)
    df6.loc[((df6['Disposition'] != '9000') & (df6['Disposition'] != '9999')), 'Cancel Code'] = ''
    df6.loc[((df6['Disposition'] != '9000') & (df6['Disposition'] != '9999')), 'Cancel Code Desc'] = ''
    index_names2 = df7[df7['Cancel Code'] == 11].index
    df7.drop(index_names2, inplace=True)
    df7.loc[((df7['Disposition'] != '9000') & (df7['Disposition'] != '9999')), 'Cancel Code'] = ''
    df7.loc[((df7['Disposition'] != '9000') & (df7['Disposition'] != '9999')), 'Cancel Code Desc'] = ''
    index_names3 = df3[df3['Cancel Code'] == 11].index
    df3.drop(index_names3, inplace=True)
    index_names4 = df8[df8['Cancel Code'] == 11].index
    df8.drop(index_names4, inplace=True)
    df8.loc[((df8['Disposition'] != '9000') & (df8['Disposition'] != '9999')), 'Cancel Code'] = ''
    df8.loc[((df8['Disposition'] != '9000') & (df8['Disposition'] != '9999')), 'Cancel Code Desc'] = ''
    index_names5 = df9[df9['Cancel Code'] == 11].index
    df9.drop(index_names5, inplace=True)
    df9.loc[((df9['Disposition'] != '9000') & (df9['Disposition'] != '9999')), 'Cancel Code'] = ''
    df9.loc[((df9['Disposition'] != '9000') & (df9['Disposition'] != '9999')), 'Cancel Code Desc'] = ''
    df6.to_excel(writer, index=False, sheet_name='Closed in FACS')
    df7.to_excel(writer, index=False, sheet_name='FACS not RECON')
    df10.to_excel(writer, index=False, sheet_name='RECON not FACS')
    df3.to_excel(writer, index=False, sheet_name='Recurring Accounts')
    df8.to_excel(writer, index=False, sheet_name='Balance Mismatch')
    df9.to_excel(writer, index=False, sheet_name='Balance Match')



if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/Goshen-N_Recon_040621.xlsx', engine='xlsxwriter',options={'strings_to_numbers':True} )
    df_facs1 = pd.read_csv("/home/ajay/Downloads/Goshen-N_Recon_040621_42026.TXT",delimiter="\t")
    Goshen(df_facs1,writer)
    writer.save()
