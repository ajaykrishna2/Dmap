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
    df['List Date'] = date_sr.dt.strftime('%m/%d/%Y')
    date_sr1 = pd.to_datetime(pd.Series(df['Last Payment Date']))
    df['Last Payment Date'] = date_sr1.dt.strftime('%m/%d/%Y')
    date_sr1 = pd.to_datetime(pd.Series(df['Cancel Date']))
    df['Cancel Date'] = date_sr1.dt.strftime('%m/%d/%Y')
    df["Last Payment Date.1"] = df["Cancel Description"]
    df.drop(labels=["Cancel Description"], axis="columns", inplace=True)
    df = df.rename(columns={'Last Payment Date.1': 'Cancel Description'}, inplace=False)
    print(df.to_string())
    df1 = df[df.duplicated(['Client #'], keep=False)].sort_values('Client #')
    df2 = df[df.duplicated(['Client #'])].sort_values('Client #')
    df4 = df.merge(df1, indicator=True, how='left').loc[lambda x: x['_merge'] != 'both']
    print(df4.to_string())
    df4.drop('_merge', axis=1, inplace=True)
    df2 = df2.reset_index(drop=True)
    # df['Match?'] = np.where(df['Med-1 Balance'] == df['Recon file (EPIC) balance'], 'True', 'False')
    # df2['Match?'] = np.where(df2['Med-1 Balance'] == df2['Recon file (EPIC) balance'], 'True', 'False')
    # df2['Issue Detected'] = df2['Match?'].apply(lambda x: 'Balance Match' if x == 'True' else 'Balance Mismatch')
    # df2.drop('Match?', axis=1, inplace=True)
    # print(df.to_string())
    df2['Client #'] = df2['Client #'].apply(str)
    df4['Client #'] = df4['Client #'].apply(str)
    df5 = df4[df4['Issue Detected'] == "Account is closed in FACS, but open in KDH File."]
    df6 = df4[df4['Issue Detected'] == "CANNOT REMOVE CBCSo DUE TO PENDING  PYMT"]
    df7 = df4[df4['Issue Detected'] == "CBSo REMOVED"]
    frames1 = [ df5, df6, df7]
    df8 = pd.concat(frames1)
    df9 = df4[df4['Issue Detected'] == "UNABLE TO ADD CBSo DUE TO CLIENT SYS"]
    df10 = df4[df4['Issue Detected'] == "Account is in FACS, but not in KDH File."]
    df11 = df4[df4['Issue Detected'] == "RECURRING ACCT UNABLE TO ADD CBSo"]
    df12 = df4[df4['Issue Detected'] == "CBSo ADDED TO ACCT"]
    frames2 = [df9, df10, df11,df12]
    df13=pd.concat(frames2)
    df14 = df2[(df2['Issue Detected'] == "Account is in KDH File, but it is not in FACS.")]
    print(df14)
    df15 = df4[df4['Issue Detected'] == "BAL DIFF IS WC ADJ NOT POSTING TO FACS"]
    df16 = df4[(df4['Issue Detected'] == "BAL DIFF NEEDS TIME TO POST TO FACS")]
    df17 = df4[(df4['Issue Detected'] == "The balance in FACS is greater than the balance in KDH File.")]
    df18 = df4[(df4['Issue Detected'] == "The balance in KDH File is greater than the balance in FACS.")]
    df19= df4[(df4['Issue Detected'] == "BAL DIFF IS ON PYMT SHEET TO POST")]
    df20 = df2[df2['Issue Detected'] == "Balance Mismatch"]
    frames3 = [df15, df16, df17, df18,df19,df20]
    df21 = pd.concat(frames3)

    df22 = df4[df4['Issue Detected'] == "The balances in FACS and KDH File are same."]
    df23 = df2[df2['Issue Detected'] == "Balance Match"]
    df24 = pd.concat([df22, df23])
    df8.to_excel(writer, index=False, sheet_name='Closed in FACS')
    df13.to_excel(writer, index=False, sheet_name='FACS not RECON')
    df14.to_excel(writer, index=False, sheet_name='RECON not FACS')
    df21.to_excel(writer, index=False, sheet_name='Balance Mismatch')
    df24.to_excel(writer, index=False, sheet_name='Balance Match')
    # workbook = writer.book
    # worksheet1 = writer.sheets['Closed in FACS']
    # worksheet2 = writer.sheets['FACS not RECON']
    # worksheet3 = writer.sheets['RECON not FACS']
    # worksheet4 = writer.sheets['Balance Mismatch']
    # worksheet5 = writer.sheets['Balance Match']





if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/KDH_CBSO_REC_041521.xlsx', engine='xlsxwriter',options={'strings_to_numbers':True} )
    df_facs1 = pd.read_csv("/home/ajay/Downloads/KDH_CBSO_REC_041521_54134.TXT",delimiter="\t")
    KingsDaughter(df_facs1,writer)
    writer.save()







