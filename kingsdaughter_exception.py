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
def KingsDaughter(df,writer):
    date_sr = pd.to_datetime(pd.Series(df['List Date']))
    df['List Date'] = date_sr.dt.strftime('%m-%d-%Y')
    date_sr1 = pd.to_datetime(pd.Series(df['Last Payment Date']))
    df['Last Payment Date'] = date_sr1.dt.strftime('%m-%d-%Y')
    date_sr1 = pd.to_datetime(pd.Series(df['Cancel Date']))
    df['Cancel Date'] = date_sr1.dt.strftime('%m-%d-%Y')
    df["Last Payment Date.1"] = df["Cancel Description"]
    df.drop(labels=["Cancel Description"], axis="columns", inplace=True)
    df = df.rename(columns={'Last Payment Date.1': 'Cancel Description'}, inplace=False)
    df2 = df[df.duplicated(['Client #'])].sort_values('Client #')
    df4 = df.merge(df2, indicator=True, how='left')
    df4=df4.sort_values('Client #')
    df4['Disposition'] = pd.to_numeric(df4['Disposition'], errors='coerce')
    df4.loc[((df4['Disposition']!= 9000)&(df4['Disposition']!= 9999)), 'Cancel Code'] = ''
    df4.loc[((df4['Disposition'] != 9000) & (df4['Disposition'] != 9999)), 'Cancel Description'] = ''
    print(df4.to_string())
    df4.drop('_merge', axis=1, inplace=True)
    df2 = df2.reset_index(drop=True)
    df2['Client #'] = df2['Client #'].apply(str)
    df4['Client #'] = df4['Client #'].apply(str)
    df5 = df4[df4['Issue Detected'] == "Account is closed in FACS, but open in KDH File."]
    df6 = df4[df4['Issue Detected'] == "Account is in FACS, but not in KDH File."]
    df7 = df4[(df4['Issue Detected'] == "Account is in KDH File, but it is not in FACS.")]
    df8 = df4[(df4['Issue Detected'] == "The balance in FACS is greater than the balance in KDH File.")]
    df9 = df4[(df4['Issue Detected'] == "The balance in KDH File is greater than the balance in FACS.")]
    frames3 = [df8,df9]
    df10 = pd.concat(frames3)
    df11 = df4[df4['Issue Detected'] == "The balances in FACS and KDH File are same."]
    df5.to_excel(writer, index=False, sheet_name='Closed in FACS')
    df6.to_excel(writer, index=False, sheet_name='FACS not RECON')
    df7.to_excel(writer, index=False, sheet_name='RECON not FACS')
    df10.to_excel(writer, index=False, sheet_name='Balance Mismatch')
    df11.to_excel(writer, index=False, sheet_name='Balance Match')

if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/KDH_CBSO_REC_0415211.xlsx', engine='xlsxwriter',options={'strings_to_numbers':True} )
    df_facs1 = pd.read_csv("/home/ajay/Downloads/KDH_CBSO_REC_041521_54134.TXT",delimiter="\t")
    KingsDaughter(df_facs1,writer)
    writer.save()