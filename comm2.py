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




class Communityhospital:
    def communityhospital(self,df, writer):
        try:
            pd.set_option('display.float_format', lambda x: '%.0f' % x)
            date_sr = pd.to_datetime(pd.Series(df['List Date']))
            df['List Date'] = date_sr.dt.strftime('%m-%d-%Y')
            date_sr1 = pd.to_datetime(pd.Series(df['Last Payment Date']))
            df['Last Payment Date'] = date_sr1.dt.strftime('%m-%d-%Y')
            date_sr2 = pd.to_datetime(pd.Series(df['Cancel Date']))
            df['Cancel Date'] = date_sr2.dt.strftime('%m-%d-%Y')
            df['Date'] = pd.datetime.now().date()
            df['year1'] = pd.DatetimeIndex(df['Date']).year
            df['month1'] = pd.DatetimeIndex(df['Date']).month
            df['day1'] = pd.DatetimeIndex(df['Date']).day
            df['year2'] = pd.DatetimeIndex(df['Last Payment Date']).year
            df['month2'] = pd.DatetimeIndex(df['Last Payment Date']).month
            df['day2'] = pd.DatetimeIndex(df['Last Payment Date']).day
            index_name = df[
                (df['year2'] >= df['year1']) & (df['month2'] >= df['month1']) & (df['day2'] >= df['day1'])].index
            df.drop(index_name, inplace=True)
            df.drop('year1', axis=1, inplace=True)
            df.drop('year2', axis=1, inplace=True)
            df.drop('month1', axis=1, inplace=True)
            df.drop('month2', axis=1, inplace=True)
            df.drop('day1', axis=1, inplace=True)
            df.drop('day2', axis=1, inplace=True)
            df.drop('Date', axis=1, inplace=True)

            print(df)
            df1 = df[df.duplicated(['EPIC #'], keep=False)].sort_values('EPIC #')
            df2 = df[df.duplicated(['EPIC #'])].sort_values('EPIC #')
            df2.drop(df2[(df2['FACS #'].isna())].index, inplace=True)
            df3 = df1.merge(df2, indicator=True, how='left').loc[lambda x: x['_merge'] != 'both']
            df = df.merge(df1, indicator=True, how='left').loc[lambda x: x['_merge'] != 'both']
            df3.drop('_merge', axis=1, inplace=True)
            df.drop('_merge', axis=1, inplace=True)
            df2 = df2.reset_index()
            df3 = df3.reset_index()
            df2["Recon file (EPIC) balance"] = df3["Recon file (EPIC) balance"]
            df2['Match?'] = np.where(df2['Med-1 Balance'] == df2['Recon file (EPIC) balance'], 'True', 'False')
            df2['Issue Detected'] = df2['Match?'].apply(
                lambda x: 'Balance Match' if x == 'True' else 'Balance Mismatch')
            df2.drop('Match?', axis=1, inplace=True)
            df2.drop('index', axis=1, inplace=True)
            df4 = df[df['Issue Detected'] == "Account Closed in FACS, But in Recon File."]
            df5 = df[df['Issue Detected'] == "Account is in Recon File but not in FACS."]
            df6 = df[df['Issue Detected'] == "Account is in FACS, But not in Recon File."]
            df7 = df[df['Issue Detected'] == "The balance in EPIC is greater than the balance in FACS."]
            df8 = df[df['Issue Detected'] == "The balance in FACS is greater than the balance in EPIC."]
            df9 = df2[df2['Issue Detected'] == "Balance Mismatch"]
            df10 = pd.concat([df7, df8, df9])
            df11 = df[df['Issue Detected'] == "The balance in EPIC match with the balance in FACS."]
            df12 = df2[df2['Issue Detected'] == "Balance Match"]
            df13 = pd.concat([df11, df12])
            # df4.drop(df4[(df4['Disposition']=='9000')].index,inplace=True)
            df4['Date'] = pd.datetime.now().date()
            df4['year1'] = pd.DatetimeIndex(df4['Date']).year
            df4['month1'] = pd.DatetimeIndex(df4['Date']).month
            df4['day1'] = pd.DatetimeIndex(df4['Date']).day
            df4['year2'] = pd.DatetimeIndex(df4['Last Payment Date']).year
            df4['month2'] = pd.DatetimeIndex(df4['Last Payment Date']).month
            df4['day2'] = pd.DatetimeIndex(df4['Last Payment Date']).day
            df4['year3'] = pd.DatetimeIndex(df4['Cancel Date']).year
            df4['month3'] = pd.DatetimeIndex(df4['Cancel Date']).month
            df4['day3'] = pd.DatetimeIndex(df4['Cancel Date']).day
            index_name1 = df4[
                (df4['Cancel Code'].isna()) & (df4['year2'] >= df4['year1']) & (df4['month2'] >= df4['month1']) & (
                            df4['day2'] > df4['day1'])].index
            df4.drop(index_name1, inplace=True)
            # ad=df4[df4['Cancel Code']==7]
            # df4.drop(ad.index,inplace=True)
            index_name2 = df4[
                ((df4['Cancel Code'] == 2) | (df4['Cancel Code'] == 4)) & (df4['year3'] >= df4['year1']) & (
                            df4['month3'] >= df4['month1']) & (
                        df4['day3'] > df4['day1'])].index
            df4.drop(index_name1, inplace=True)
            df4.drop(index_name2, inplace=True)

            df4.drop('year1', axis=1, inplace=True)
            df4.drop('year2', axis=1, inplace=True)
            df4.drop('year3', axis=1, inplace=True)
            df4.drop('month1', axis=1, inplace=True)
            df4.drop('month2', axis=1, inplace=True)
            df4.drop('month3', axis=1, inplace=True)
            df4.drop('day1', axis=1, inplace=True)
            df4.drop('day2', axis=1, inplace=True)
            df4.drop('day3', axis=1, inplace=True)
            df4.drop('Date', axis=1, inplace=True)
            # df6.drop(df6[df6['Client ID']=='5019HH'].index,inplace=True)
            # df6.drop(df6[(df6['Disposition'] == '3TEM')|(df6['Disposition'] == '3CCR')].index, inplace=True)
            df10['Date'] = pd.datetime.now().date()
            df10['year1'] = pd.DatetimeIndex(df10['Date']).year
            df10['month1'] = pd.DatetimeIndex(df10['Date']).month
            df10['day1'] = pd.DatetimeIndex(df10['Date']).day
            df10['year2'] = pd.DatetimeIndex(df10['Last Payment Date']).year
            df10['month2'] = pd.DatetimeIndex(df10['Last Payment Date']).month
            df10['day2'] = pd.DatetimeIndex(df10['Last Payment Date']).day
            index_name3 = df10[(df10['year2'] >= df10['year1']) & (df10['month2'] >= df10['month1']) & (
                        df10['day2'] > df10['day1'])].index
            df10.drop(index_name3, inplace=True)
            df10.drop('year1', axis=1, inplace=True)
            df10.drop('year2', axis=1, inplace=True)
            df10.drop('month1', axis=1, inplace=True)
            df10.drop('month2', axis=1, inplace=True)
            df10.drop('day1', axis=1, inplace=True)
            df10.drop('day2', axis=1, inplace=True)
            df10.drop('Date', axis=1, inplace=True)
            # index_13 = df10[(df10['Med-1 Balance'] < 0) | (df10['Med-1 Balance'].isna())].index
            # df10.drop(index_13, inplace=True)

            df4.to_excel(writer, index=False, sheet_name='Closed in FACS')
            df6.to_excel(writer, index=False, sheet_name='FACS not RECON')
            df5.to_excel(writer, index=False, sheet_name='RECON not FACS')
            df10.to_excel(writer, index=False, sheet_name='Balance Mismatch')
            df13.to_excel(writer, index=False, sheet_name='Balance Match')
            # ad.to_excel(writer, index=False, sheet_name='Adjustments')
        except Exception as e:
            logging.exception("error")





if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/COMMUNITY_EPIC_LGL_RECON_041221_61571_.xlsx', engine='xlsxwriter',options={'strings_to_numbers':True} )
    # mylist=[]
    # ChunkSize = 10
    # for chunk in pd.read_csv("/home/ajay/Downloads/EnableFiles/Community/Outgoing/COMMUNITY_EPIC_LGL_RECON_111521_60406.TXT" ,sep='\t',chunksize=ChunkSize):
    #     mylist.append(chunk)
    # print(len(mylist))
    df = pd.read_csv('/home/ajay/Downloads/COMMUNITY_EPIC_LGL_RECON_041221_61571.TXT', sep='\t',names=['Issue Detected', 'FACS #', 'EPIC #', 'Client ID', 'First Name', 'Last Name', 'Disposition',
                            'Phase', 'List Date', 'Med-1 Balance', 'Amount Cancelled', 'Recon file (EPIC) balance',
                            'Last Payment Date', 'Cancel Code', 'Cancel Date', 'Cancel Description', 'Legal Flag',
                            'samp'], skiprows=1)
    # df=pd.read_csv("/home/ajay/Downloads/EnableFiles/Community/Outgoing/COMMUNITY_EPIC_LGL_RECON_111521_60406.TXT",delimiter='\t')
    # print(df.shape)
    # df.columns = ['Issue Detected', 'FACS #', 'EPIC #', 'Client ID', 'First Name', 'Last Name', 'Disposition', 'Phase',
    #               'List Date', 'Med-1 Balance', 'Amount Cancelled', 'Recon file (EPIC) balance', 'Last Payment Date',
    #               'Cancel Code', 'Cancel Date', 'Cancel Description', 'Legal Flag']
    # df=pd.concat(mylist,axis=0)
    df_facs1 = df
    reconcilation = Communityhospital()
    reconcilation.communityhospital(df_facs1, writer)
    writer.save()