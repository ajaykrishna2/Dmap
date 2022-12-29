import logging

import pandas as pd
import sys
import os
import operator as op
import numpy as np
import openpyxl

def Exception_report(df,book_to_facs,writer):

    try:
        print(df)
        df['Total']=df['Pd to Agency']+df['Pd to You']
        df['Difference']=df['Total']-book_to_facs['PRN']
        print(df['Difference'])
        df['Book_To_Facs_PRN']=book_to_facs['PRN']
        df['Over Paid Validation'] = np.where(df['Total'] == df['Book_To_Facs_PRN'], 'True', 'False')
        df1 = df[[ 'Client #','Pd to Agency', 'Pd to You','Total','Book_To_Facs_PRN','Difference', 'Over Paid Validation']]
        print(df1)
        df['flag_bill']=df['Clients Acct #'].astype(str)+df['Total'].astype(str)
        df['flag_bill']= pd.to_numeric(df['flag_bill'] ,errors='coerce').astype(float)
        print((df['flag_bill']))
        book_to_facs['flag_book_to_FACS']=book_to_facs['Acct#'].astype(str)+book_to_facs['Total'].astype(str)
        book_to_facs['flag_book_to_FACS']=pd.to_numeric(df['flag_bill'] ,errors='coerce').astype(float)
        print(book_to_facs['flag_book_to_FACS'])
        df['flag_book_to_FACS']=book_to_facs['flag_book_to_FACS']
        print(df['flag_book_to_FACS'])
        df['Book_To_Facs_O/P Amt'] = book_to_facs['O/P Amt']
        df2=df[(df['flag_bill'] != df['flag_book_to_FACS'])]
        print(df2)
        df3=df2[['Clients Acct #', 'Client #', 'Pmt Amt Applied', 'Pd to Agency', 'Pd to You', 'Due Agency', 'Due You', 'Book_To_Facs_PRN', 'Book_To_Facs_O/P Amt']]
        df1.to_excel(writer, index=False, sheet_name='Amount Validation')
        df3.to_excel(writer, index=False, sheet_name='Exception')
        workbook = writer.book
        worksheet1 = writer.sheets['Amount Validation']
        worksheet2 = writer.sheets['Exception']
        header_format= workbook.add_format({'text_wrap': False})
        header_format1 = workbook.add_format({'fg_color': '#6B6565'})
        for col_num, value in enumerate(df1.columns.values):
            worksheet1.write(0, col_num , value, header_format1)
        for col_num, value in enumerate(df3.columns.values):
            worksheet2.write(0, col_num , value, header_format1)
        worksheet1.set_column('B:B', 9, header_format)
        worksheet1.set_column('E:E', 18, header_format)
        worksheet1.set_column('F:F', 9, header_format)
        worksheet1.set_column('G:G', 18, header_format)
        worksheet2.set_column('A:A', 11, header_format)
        worksheet2.set_column('B:B', 9, header_format)
        worksheet2.set_column('E:E', 18, header_format)
        worksheet2.set_column('F:F', 9, header_format)
        worksheet2.set_column('I:I', 20, header_format)
    except Exception as e:
        print("Error in creating exception report for deaconess hospital")

# # def Deaconess():
# #     try:
# #         all_dfs1 = pd.read_excel('/home/ajay/Downloads/April/deaconess_dsp.xlsx', sheet_name=None)
# #         df1 = pd.concat(all_dfs1, ignore_index=True)
# #         all_dfs2 = pd.read_excel('/home/ajay/Downloads/April/deaconess_gibson.xlsx', sheet_name=None)
# #         df2 = pd.concat(all_dfs2, ignore_index=True)
# #         all_dfs3 = pd.read_excel('/home/ajay/Downloads/April/deaconess_health_heart.xlsx', sheet_name=None)
# #         df3 = pd.concat(all_dfs3, ignore_index=True)
# #         all_dfs4 = pd.read_excel('/home/ajay/Downloads/April/deaconess_health_sys.xlsx', sheet_name=None)
# #         df4 = pd.concat(all_dfs4, ignore_index=True)
# #         all_dfs5 = pd.read_excel('/home/ajay/Downloads/April/deaconess_heart_hospital.xlsx', sheet_name=None)
# #         df5 = pd.concat(all_dfs5, ignore_index=True)
# #         all_dfs6 = pd.read_excel('/home/ajay/Downloads/April/deaconess_henderson.xlsx', sheet_name=None)
# #         df6 = pd.concat(all_dfs6, ignore_index=True)
# #         all_dfs7 = pd.read_excel('/home/ajay/Downloads/April/deaconess_union_county.xlsx', sheet_name=None)
# #         df7 = pd.concat(all_dfs7, ignore_index=True)
# #         frames = [df1, df2, df3, df4, df5, df6, df7]
# #         df8 = pd.concat(frames, ignore_index=True)
# #         return df8
# #
# #     except Exception as e:
# #         logging.exception("error")
# #
# #
# # def book_to_facs1():
# #     try:
# #         df = pd.read_excel('/home/ajay/Downloads/book_to_facs.xlsx', sheet_name='NON_STV')
# #         rslt_df = df[(df['Client Name'] == 'Deaconess Gibson Hospital')|(df['Client Name'] == 'Deaconess Health System')|(df['Client Name'] == 'Deaconess Henderson Hospital')|(df['Client Name'] == 'Deaconess Specialty Physicians')|(df['Client Name'] == 'Deaconess Union County Hospital')|(df['Client Name'] == 'THE HEART HOSPITAL')]
# #         print(rslt_df)
# #
# #
# #     except Exception as e:
# #         logging.exception("error")
#
# if __name__ == "__main__":
#     writer = pd.ExcelWriter('/home/ajay/deconess_hospital_exception_report.xlsx', engine='xlsxwriter')
#     all_dfs1 = pd.read_excel('/home/ajay/Downloads/April/deaconess_dsp.xlsx', sheet_name=None)
#     df1 = pd.concat(all_dfs1, ignore_index=True)
#     all_dfs2 = pd.read_excel('/home/ajay/Downloads/April/deaconess_gibson.xlsx', sheet_name=None)
#     df2 = pd.concat(all_dfs2, ignore_index=True)
#     all_dfs3 = pd.read_excel('/home/ajay/Downloads/April/deaconess_health_heart.xlsx', sheet_name=None)
#     df3 = pd.concat(all_dfs3, ignore_index=True)
#     all_dfs4 = pd.read_excel('/home/ajay/Downloads/April/deaconess_health_sys.xlsx', sheet_name=None)
#     df4 = pd.concat(all_dfs4, ignore_index=True)
#     all_dfs5 = pd.read_excel('/home/ajay/Downloads/April/deaconess_heart_hospital.xlsx', sheet_name=None)
#     df5 = pd.concat(all_dfs5, ignore_index=True)
#     all_dfs6 = pd.read_excel('/home/ajay/Downloads/April/deaconess_henderson.xlsx', sheet_name=None)
#     df6 = pd.concat(all_dfs6, ignore_index=True)
#     all_dfs7 = pd.read_excel('/home/ajay/Downloads/April/deaconess_union_county.xlsx', sheet_name=None)
#     df7 = pd.concat(all_dfs7, ignore_index=True)
#     frames = [df1, df2, df3, df4, df5, df6, df7]
#     deaconess = pd.concat(frames, ignore_index=True)
#     dff = pd.read_excel('/home/ajay/Downloads/book_to_facs.xlsx', sheet_name='NON_STV')
#     book_to_facs = dff[
#         (dff['Client Name'] == 'Deaconess Gibson Hospital') | (dff['Client Name'] == 'Deaconess Health System') | (
#                     dff['Client Name'] == 'Deaconess Henderson Hospital') | (
#                     dff['Client Name'] == 'Deaconess Specialty Physicians') | (
#                     dff['Client Name'] == 'Deaconess Union County Hospital') | (
#                     dff['Client Name'] == 'THE HEART HOSPITAL')]
#     Exception_report(deaconess,book_to_facs,writer)
#     writer.save()


if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/deconess_hospital_exception_report1.xlsx', engine='xlsxwriter')
    deaconess = pd.read_excel('/home/ajay/Deaconess2.xlsx', sheet_name='deaconess')
    book_to_facs1 = pd.read_excel('/home/ajay/Deaconess_book_facs.xlsx', sheet_name='book_to_facs')
    Exception_report(deaconess, book_to_facs1, writer)
    writer.save()
