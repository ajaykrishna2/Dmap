import logging
from timeit import timeit

import pandas as pd
import sys
import os
import operator as op
import numpy as np
import openpyxl
from pandas import DatetimeIndex


def Exception_report(writer):

    try:
        decimals = 2
        df=Deaconess()

        book_to_facs=book_to_facs1()
        df.reset_index(inplace=True)
        book_to_facs.reset_index(inplace=True)
        # Amount Validation
        d1=df.groupby(['Client #']).agg({ 'Pd to Agency': 'sum', 'Pd to You': 'sum'})
        d1.reset_index(inplace=True)
        d2 = book_to_facs.groupby(['Client#']).agg({'PRN': 'sum'})
        d2.reset_index(inplace=True)
        d1['Total']=d1['Pd to Agency']+d1['Pd to You']
        d1['book_to_fac_PRN']=d2['PRN']
        d1['Difference']=(d1['Total'] - d2['PRN'])
        d1["Difference"] = d1["Difference"].apply(lambda x: round(x, decimals))
        df1=d1
        df['Year'] = DatetimeIndex(df['Pmt Date']).year
        df['Month'] = DatetimeIndex(df['Pmt Date']).month
        df['Day'] = DatetimeIndex(df['Pmt Date']).day
        df['Total'] = df['Pd to Agency'] + df['Pd to You']
        df['Total'] = df['Total'].apply(lambda x: round(x, decimals))

        df.reset_index(inplace=True)
        df['flag_bill']=df['Clients Acct #'].astype(str)+ df['Year'].astype(str)+df['Month'].astype(str)+df['Day'].astype(str)+(df['Total']).astype(str)
        book_to_facs.reset_index(inplace=True)
        book_to_facs['Acct#']=book_to_facs['Acct#'].astype(int)
        book_to_facs['Year'] = DatetimeIndex(book_to_facs['Date']).year
        book_to_facs['Month'] = DatetimeIndex(book_to_facs['Date']).month
        book_to_facs['Day'] = DatetimeIndex(book_to_facs['Date']).day
        book_to_facs['flag_book_to_FACS']=book_to_facs['Acct#'].astype(str)+ book_to_facs['Year'].astype(str)+book_to_facs['Month'].astype(str)+book_to_facs['Day'].astype(str)+(book_to_facs['PRN']).astype(str)
        df['flag_id'] = df['Clients Acct #'].astype(str) + df['Year'].astype(str)+df['Month'].astype(str)+df['Day'].astype(str)+df['Pmt Type'].astype(str)
        book_to_facs['Acct#'] = pd.to_numeric(book_to_facs['Acct#'], errors='coerce').astype(int)
        book_to_facs['flag_id'] = book_to_facs['Acct#'].astype(str) + book_to_facs['Year'].astype(str)+book_to_facs['Month'].astype(str)+book_to_facs['Day'].astype(str)+book_to_facs['Pmt Type'].astype(str)
        result = pd.merge(df[['Clients Acct #',  'Pmt Amt Applied', 'Pd to Agency', 'Pd to You', 'Due Agency','Due You','Client #','Total','flag_bill','flag_id']], book_to_facs[['PRN','CC','PJI', 'O/P Amt','flag_book_to_FACS','flag_id']],on='flag_id',how='outer')
        result.reset_index(drop=True,inplace=True)
        df2=result[~result['flag_bill'].isin(result['flag_book_to_FACS'])]
        df2.reset_index(drop=True,inplace=False)
        df3=df2[['Clients Acct #', 'Client #', 'Pmt Amt Applied', 'Pd to Agency', 'Pd to You', 'Due Agency', 'Due You','Total' ,'PRN', 'O/P Amt','CC','PJI']]
        df1.to_excel(writer, index=False, sheet_name='Amount Validation')
        df3.to_excel(writer, index=False, sheet_name='Exception')
        workbook = writer.book
        worksheet1 = writer.sheets['Amount Validation']
        worksheet2 = writer.sheets['Exception']
        header_format= workbook.add_format({'text_wrap': False})
        worksheet1.set_column('B:B', 11, header_format)
        worksheet2.set_column('A:A', 11, header_format)
    except Exception as e:
        print("Error in creating exception report for deaconess hospital")

def Deaconess():
    try:
        all_dfs1 = pd.read_excel('/home/ajay/Downloads/Deaconess/deaconess_dsp.xlsx', sheet_name=None,
                                 converters={'Client #':str})
        df1 = pd.concat(all_dfs1, ignore_index=True)

        all_dfs2 = pd.read_excel('/home/ajay/Downloads/Deaconess/deaconess_gibson.xlsx', sheet_name=None,
                                 converters={'Client #':str})
        df2 = pd.concat(all_dfs2, ignore_index=True)
        all_dfs3 = pd.read_excel('/home/ajay/Downloads/Deaconess/deaconess_health_heart.xlsx', sheet_name=None,
                                 converters={'Client #':str})
        df3 = pd.concat(all_dfs3, ignore_index=True)
        all_dfs4 = pd.read_excel('/home/ajay/Downloads/Deaconess/deaconess_health_sys.xlsx', sheet_name=None,
                                 converters={'Client #':str})
        df4 = pd.concat(all_dfs4, ignore_index=True)
        all_dfs5 = pd.read_excel('/home/ajay/Downloads/Deaconess/deaconess_heart_hospital.xlsx', sheet_name=None,
                                 converters={'Client #':str})
        df5 = pd.concat(all_dfs5, ignore_index=True)
        all_dfs6 = pd.read_excel('/home/ajay/Downloads/Deaconess/deaconess_henderson.xlsx', sheet_name=None,
                                 converters={'Client #':str})
        df6 = pd.concat(all_dfs6, ignore_index=True)
        all_dfs7 = pd.read_excel('/home/ajay/Downloads/Deaconess/deaconess_union_county.xlsx', sheet_name=None,
                                 converters={'Client #':str})
        df7 = pd.concat(all_dfs7, ignore_index=True)
        frames = [df1, df2, df3, df4, df5, df6, df7]
        df8 = pd.concat(frames, ignore_index=True)
        print(df8)
        return df8

    except Exception as e:
        logging.exception("error")


def book_to_facs1():
    try:
        df = pd.read_excel('/home/ajay/Downloads/Book_to_Facs/book_to_facs.xlsx', sheet_name='NON_STV')
        rslt_df = df[(df['Client Name'] == 'Deaconess Gibson Hospital')|(df['Client Name'] == 'Deaconess Health System')|(df['Client Name'] == 'Deaconess Henderson Hospital')|(df['Client Name'] == 'Deaconess Specialty Physicians')|(df['Client Name'] == 'Deaconess Union County Hospital')|(df['Client Name'] == 'THE HEART HOSPITAL')]
        return rslt_df


    except Exception as e:
        logging.exception("error")

if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/Deconess_exception_report.xlsx', engine='xlsxwriter')
    Exception_report(writer)
    writer.save()

