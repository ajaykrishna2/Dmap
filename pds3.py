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
import numpy as np
def Riverview(facs,writer):
    try:


        df=facs[(facs.CLIENT=='201ECA')&((facs.Year==2016)|(facs.Year==2017)|(facs.Year==2018)|(facs.Year==2019)|(facs.Year==2020)|(facs.Year==2021))]

        df2=facs[(facs.CLIENT == '202ECA')&((facs.Year==2016)|(facs.Year==2017)|(facs.Year==2018)|(facs.Year==2019)|(facs.Year==2020)|(facs.Year==2021))]


        df1=df.append(df2)
        print(df1)
        df1["COLLECTED"] = df1["COLLECTED"].fillna(0)
        df1["ADJUSTED"] = df1["ADJUSTED"].fillna(0)
        df1["RECALLED"] = df1["RECALLED"].fillna(0)
        df1["VOL_CANCELLED"] = df1["VOL_CANCELLED"].fillna(0)
        df1["FEES"] = df1["FEES"].fillna(0)
        df1['Unadjusted %']=((df1['COLLECTED']/df1['LISTED'])*100)
        df1['adjusted %']=(((df1['COLLECTED'])/(df1['LISTED']+df1['ADJUSTED']-df1['RECALLED']-df1['VOL_CANCELLED']))*100)
        df1['Inventory Remaining']=((df1['LISTED'])-(df1['COLLECTED'])+(df1['ADJUSTED'])-(df1['RECALLED'])-(df1['VOL_CANCELLED']))
        df3 = df1[['CLIENT','NAME','Year','Month','NUM_ACCTS_LISTED','LISTED','NUM_ACCTS_ADJ_LIST','ADJUSTED','NUM_ACCTS_RECALLED','RECALLED','NUM_ACCTS_CANCELED','VOL_CANCELLED','COLLECTED','FEES','NET COLLECTIONS','Correspond_Clnt','CLASS','MTHLY COLLECTIONS','AVG AGE AT LIST','Unadjusted %','adjusted %','Inventory Remaining']]
        print(df1['Inventory Remaining'])

        df3.columns=['CLIENT','NAME','Year','Month','# of Accts Listed','Amt Listed','NUM_ACCTS_ADJ_LIST','Adjustments','NUM_ACCTS_RECALLED','Returned','NUM_ACCTS_CANCELED','RECALLED','Recovered','FEES','NET COLLECTIONS','Correspond_Clnt','CLASS','MTHLY COLLECTIONS','AVG AGE AT LIST','Unadjusted %','adjusted %','Inventory Remaining']
        table = df3.pivot_table(values=['# of Accts Listed','Amt Listed','Recovered','Adjustments','RECALLED','Returned','FEES','AVG AGE AT LIST','Unadjusted %','adjusted %','Inventory Remaining'], index=['NAME','CLIENT','Year','Month'])
        table.reset_index(inplace=True)
        cat_month = CategoricalDtype(
            ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC'],ordered=True)
        table1 = table[['NAME', 'CLIENT', 'Month', '# of Accts Listed','Amt Listed','Recovered','Adjustments','RECALLED','Returned','FEES','AVG AGE AT LIST','Unadjusted %','adjusted %','Inventory Remaining']].groupby(["NAME", "CLIENT"], as_index=False).sum().stb.subtotal()
        Sheet1 = pd.concat([table, table1])
        table2 = Sheet1[['NAME', 'CLIENT', 'Year', 'Month', '# of Accts Listed','Amt Listed','Recovered','Adjustments','RECALLED','Returned','FEES','AVG AGE AT LIST','Unadjusted %','adjusted %','Inventory Remaining']].groupby(["NAME", "CLIENT", "Year"], as_index=False).sum()
        Sheet2 = pd.concat([Sheet1, table2])
        Sheet2['Month'] = Sheet2['Month'].astype(cat_month)
        Sheet2 = Sheet2.sort_values(['NAME', 'CLIENT', 'Year', 'Month'])
        table.set_index(['NAME', 'CLIENT', 'Year', 'Month'], inplace=True)
        column_order =['NAME', 'CLIENT', 'Year', 'Month','# of Accts Listed','Amt Listed','Recovered','Adjustments','RECALLED','Returned','FEES','AVG AGE AT LIST','Unadjusted %','adjusted %','Inventory Remaining']
        table3 = Sheet2.reindex(column_order, axis=1)


        table3.to_excel(writer, index=True, sheet_name='MED-12 Collections')
    except Exception as e:
        logging.exception("error")




if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/Riverview1.xlsx', engine='openpyxl')
    xls = pd.ExcelFile('/home/ajay/Downloads/Riverview.xlsx', engine='openpyxl')
    df_facs1 = pd.read_excel(xls, 'Details')
    Riverview(df_facs1,writer)
    writer.save()
