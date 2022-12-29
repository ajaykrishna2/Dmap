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
        print(len(df))
        print(len(book_to_facs))
        # print(book_to_facs['PRN'])
        # print(df['Client #'].astype(str).to_string())
        df['Client #']=df['Client #'].str.replace('e+','E').astype(str)
        df['Client #'].fillna("132E55", inplace = True)
        # df['Client'] = df['Client'].replace({np.nan:''})
        # print(df['Client #'].astype(str).to_string())

        df.reset_index(inplace=True)
        book_to_facs.reset_index(inplace=True)
        index_names = book_to_facs[book_to_facs['PRN'] ==0.00].index
        # book_to_facs['Client#'].str.contains('132E55').astype(float)

        print(book_to_facs['Client#'])
        print(((df['Pmt Amt Applied']==0)&(df['Pmt Code']==0)&(df['New Bal']==0)&(df['Pd to Agency']==0)&(df['Pd to You']==0)&(df['Due You']==0))==True)
        index_names1=df[((df['Pd to Agency']==0.00)&(df['Pd to You']==0.00)&(df['Due Agency']==0.00)&(df['Due You']==0.00))].index
        book_to_facs.drop(index_names,inplace=True)
        print(book_to_facs['PRN'] ==0.00)
        df.drop(index_names1, inplace=True)
        print(book_to_facs['PRN'])
        d1=df.groupby(['Client #']).agg({ 'Pd to Agency': 'sum', 'Pd to You': 'sum'})

        # d1.drop(d1.loc[1.32E+57])
        d1.reset_index(inplace=True)
        d2 = book_to_facs.groupby(['Client#']).agg({'PRN': 'sum'})
        # d2.loc=d2
        # pd.to_numeric((d2['Client#'] == 132E55), errors='coerce').astype(float)
        d2.reset_index(inplace=True)
        # print(d1)
        # print(d2.to_string())
        d1['Total']=d1['Pd to Agency']+d1['Pd to You']
        # print(d2.info())
        # print(d1['Total'])
        d1['book_to_fac']=d2['PRN']
        d1['Difference']=(d1['Total'] - d2['PRN'])
        d1["Difference"] = d1["Difference"].apply(lambda x: round(x, decimals))
        df1=d1

        df['Total'] = df['Pd to Agency'] + df['Pd to You']
        # d1['Difference'] = d1['Total'].set_index('Client #').subtract(d2[['PRN']].set_index('Client#')).reset_index()
        # d1['Difference']=d1['Total']-book_to_facs['PRN']
        # d1['Book_To_Facs_PRN']=book_to_facs['PRN']
        # d1['Over Paid Validation'] = np.where(d1['Total'] ==d1['Book_To_Facs_PRN'], 'True', 'False')
        # df1 = d1[[ 'Client #','Pd to Agency', 'Pd to You','Total','Book_To_Facs_PRN','Difference', 'Over Paid Validation']]
        # print(df1)
        df.reset_index(inplace=True)
        # print(df.info())
        df['flag_bill']=df['Clients Acct #'].astype(str)+(df['Total'].abs()).astype(str)
        # print(df[['Clients Acct #','Total','flag_bill']].head(5))
        # # print(df.info())
        # df['flag_bill']= pd.to_numeric(df['flag_bill'] ,errors='coerce')
        # # df['flag_bill']=df['flag_bill'].astype(float)
        # # df['flag_bill'] = df['flag_bill'].apply('{:.2f}'.format)
        # df['flag_bill']=df['flag_bill'].astype(float)
        # # print(df[['Clients Acct #','Total','flag_bill']].head(5))
        # print(df.head(5).to_string())
        # print(df['flag_bill'])
        # df['flag_bill'] = df['flag_bill'].apply('{:.2f}'.format)
        # df['flag_bill'] = df['flag_bill'].apply(lambda x: round(x, 2))
        # df['flag_bill']=round(df['flag_bill'],2)
        # print(df['Clients Acct #'].head(5),df['Total'].head(5),df['flag_bill'].head(5))
        # print(df.info())
        book_to_facs.reset_index(inplace=True)
        book_to_facs['Acct#']=book_to_facs['Acct#'].astype(int)
        book_to_facs['flag_book_to_FACS']=book_to_facs['Acct#'].astype(str)+(book_to_facs['PRN'].abs()).astype(str)
        # book_to_facs['flag_book_to_FACS']=pd.to_numeric(book_to_facs['flag_book_to_FACS'] ,errors='coerce')
        # book_to_facs['flag_book_to_FACS']=book_to_facs['flag_book_to_FACS'].astype(float)



        # book_to_facs['flag_book_to_FACS']=pd.concat(book_to_facs['flag_book_to_FACS'],)
        # book_to_facs['flag_book_to_FACS']=pd.to_numeric(book_to_facs['flag_book_to_FACS'] ,errors='coerce')
        #
        # book_to_facs['flag_book_to_FACS'] = book_to_facs['flag_book_to_FACS'].apply('{:.2f}'.format)
        # print(book_to_facs.info())
        # book_to_facs['flag_book_to_FACS'] =  book_to_facs['flag_book_to_FACS'].apply(lambda x: round(x, 2))
        # print(book_to_facs['flag_book_to_FACS'])



        df['Year'] = DatetimeIndex(df['Pmt Date']).year
        df['Month'] = DatetimeIndex(df['Pmt Date']).month
        df['Day'] = DatetimeIndex(df['Pmt Date']).day
        # print(df['Year'])

        df['flag_id'] = df['Clients Acct #'].astype(str) + df['Year'].astype(str)+df['Month'].astype(str)+df['Day'].astype(str)
        # df['flag_id'] = pd.to_numeric(df['flag_id'], errors='coerce').astype(int)
        print(df['flag_id'])

        book_to_facs['Year'] = DatetimeIndex(book_to_facs['Date']).year
        book_to_facs['Month'] = DatetimeIndex(book_to_facs['Date']).month
        book_to_facs['Day'] = DatetimeIndex(book_to_facs['Date']).day
        # print(book_to_facs.info())
        book_to_facs['Acct#'] = pd.to_numeric(book_to_facs['Acct#'], errors='coerce').astype(int)

        book_to_facs['flag_id'] = book_to_facs['Acct#'].astype(str) + book_to_facs['Year'].astype(str)+book_to_facs['Month'].astype(str)+book_to_facs['Day'].astype(str)
        # book_to_facs['flag_id'] = pd.to_numeric(book_to_facs['flag_id'], errors='coerce').astype(int)
        print((book_to_facs['flag_id']))
        # print(book_to_facs[['PRN', 'O/P Amt']])
        # df.reset_index()
        # book_to_facs.reset_index(inplace=True)
        result = pd.merge(df[['Clients Acct #',  'Pmt Amt Applied', 'Pd to Agency', 'Pd to You', 'Due Agency','Due You','Client #','Total','flag_bill','flag_id']], book_to_facs[['PRN','Int','Atty','Misc','CC','PJI','Total Pay', 'O/P Amt','flag_book_to_FACS','flag_id']],on='flag_id',how='outer')
        print(result.head(5).to_string())
        result.reset_index(drop=True,inplace=True)
        df2=result[~result['flag_bill'].isin(result['flag_book_to_FACS'])]
        # df4=df2[~((df2['flag_bill']-(df2['flag_book_to_FACS'])<=0.5)&(df2['flag_bill']-(df2['flag_book_to_FACS'])>-0.5))]
        # df4 = df2[((df2['flag_bill'] - (df2['flag_book_to_FACS']) != 0))]
        print(df2)
        df2.reset_index(drop=True,inplace=False)
        print(df2.head(5).to_string())
        # print(df2.head(10).to_string())
        df3=df2[['Clients Acct #', 'Client #', 'Pmt Amt Applied', 'Pd to Agency', 'Pd to You', 'Due Agency', 'Due You','Total','flag_bill', 'PRN', 'O/P Amt','Int','Atty','Misc','CC','PJI','Total Pay','flag_book_to_FACS']]
        df1.to_excel(writer, index=False, sheet_name='Amount Validation')
        df3.to_excel(writer, index=False, sheet_name='Exception')
        workbook = writer.book
        worksheet1 = writer.sheets['Amount Validation']
        # worksheet2 = writer.sheets['Exception']
        header_format= workbook.add_format({'text_wrap': False})
        # header_format1 = workbook.add_format({'fg_color': '#6B6565'})
        # for col_num, value in enumerate(df1.columns.values):
        #     worksheet1.write(0, col_num , value, header_format1)
        # for col_num, value in enumerate(df3.columns.values):
        #     worksheet2.write(0, col_num , value, header_format1)
        # worksheet1.set_column('B:B', 9, header_format)
        # worksheet1.set_column('E:E', 18, header_format)
        worksheet1.set_column('F:F', 24, header_format)
        # worksheet1.set_column('G:G', 18, header_format)
        # worksheet2.set_column('A:A', 11, header_format)
        # worksheet2.set_column('B:B', 9, header_format)
        # worksheet2.set_column('E:E', 18, header_format)
        # worksheet2.set_column('F:F', 9, header_format)
        # worksheet2.set_column('I:I', 20, header_format)
    except Exception as e:
        print("Error in creating exception report for deaconess hospital")

def Deaconess():
    try:
        all_dfs1 = pd.read_excel('/home/ajay/Downloads/April/deaconess_dsp.xlsx', sheet_name=None)
        df1 = pd.concat(all_dfs1, ignore_index=True)
        all_dfs2 = pd.read_excel('/home/ajay/Downloads/April/deaconess_gibson.xlsx', sheet_name=None)
        df2 = pd.concat(all_dfs2, ignore_index=True)
        all_dfs3 = pd.read_excel('/home/ajay/Downloads/April/deaconess_health_heart.xlsx', sheet_name=None)
        df3 = pd.concat(all_dfs3, ignore_index=True)
        all_dfs4 = pd.read_excel('/home/ajay/Downloads/April/deaconess_health_sys.xlsx', sheet_name=None)
        df4 = pd.concat(all_dfs4, ignore_index=True)
        all_dfs5 = pd.read_excel('/home/ajay/Downloads/April/deaconess_heart_hospital.xlsx', sheet_name=None)
        df5 = pd.concat(all_dfs5, ignore_index=True)
        all_dfs6 = pd.read_excel('/home/ajay/Downloads/April/deaconess_henderson.xlsx', sheet_name=None)
        df6 = pd.concat(all_dfs6, ignore_index=True)
        all_dfs7 = pd.read_excel('/home/ajay/Downloads/April/deaconess_union_county.xlsx', sheet_name=None)
        df7 = pd.concat(all_dfs7, ignore_index=True)
        frames = [df1, df2, df3, df4, df5, df6, df7]
        df8 = pd.concat(frames, ignore_index=True)
        return df8

    except Exception as e:
        logging.exception("error")


def book_to_facs1():
    try:
        df = pd.read_excel('/home/ajay/Downloads/book_to_facs.xlsx', sheet_name='NON_STV')
        rslt_df = df[(df['Client Name'] == 'Deaconess Gibson Hospital')|(df['Client Name'] == 'Deaconess Health System')|(df['Client Name'] == 'Deaconess Henderson Hospital')|(df['Client Name'] == 'Deaconess Specialty Physicians')|(df['Client Name'] == 'Deaconess Union County Hospital')|(df['Client Name'] == 'THE HEART HOSPITAL')]
        return rslt_df


    except Exception as e:
        logging.exception("error")

if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/deconess_hospital_exception_report.xlsx', engine='xlsxwriter')
    Exception_report(writer)
    writer.save()

