import pandas as pd
import sys
import logging
import xlrd
import os
from openpyxl.workbook import Workbook
import xlsxwriter
import numpy as np
import sidetable
from datetime import date
from pandas.api.types import CategoricalDtype
df = pd.read_excel('/home/ajay/Downloads/Jessica Sims Sample Report_Riverview Collections Report FEB 2021 (1).xlsx',sheet_name='Details')

df["COLLECTED"]=df["COLLECTED"].fillna(0)
df["ADJUSTED"]=df["ADJUSTED"].fillna(0)
df["RECALLED"]=df["RECALLED"].fillna(0)
df["VOL_CANCELLED"]=df["VOL_CANCELLED"].fillna(0)
df["FEES"]=df["FEES"].fillna(0)


df['Unadjusted %'] = ((df['COLLECTED'] / df['LISTED']) * 100)
df['adjusted %'] = (((df['COLLECTED']) / (df['LISTED'] + df['ADJUSTED'] - df['RECALLED'] - df['VOL_CANCELLED'])) * 100)
df['Inventory Remaining'] = ((df['LISTED']) -(df['COLLECTED']) +(df['ADJUSTED']) -(df['RECALLED']) -(df['VOL_CANCELLED']))

med1_df = df.loc[(df['CLIENT'].isin(['201ECA' , '202ECA'])),["NAME","CLIENT","Year","Month","NUM_ACCTS_LISTED","LISTED","COLLECTED","ADJUSTED","RECALLED","VOL_CANCELLED","FEES","AVG AGE AT LIST","Inventory Remaining","Unadjusted %","adjusted %"]]
med1_df.columns = [ "NAME", "CLIENT","Year", "Month", "# of Accts Listed","Amt Listed","Recovered","Adjustments","RECALLED","Returned","FEES","AVG AGE AT LIST","Inventory Remaining","Unadjusted %","adjusted %"]

med1_pivot = pd.pivot_table(med1_df,index=["NAME","CLIENT","Year","Month"]).astype(int)

med1_pivot.reset_index(inplace=True)
cat_month = CategoricalDtype(['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC'],ordered=True)
df1 = med1_pivot[["NAME","CLIENT","Month","# of Accts Listed","Amt Listed","Recovered","Adjustments","RECALLED","Returned","FEES","AVG AGE AT LIST","Inventory Remaining","Unadjusted %","adjusted %"]] \
            .groupby(["NAME","CLIENT"], as_index=False).sum().stb.subtotal()


Sheet1 = pd.concat([med1_pivot, df1])
df2 = Sheet1[["NAME","CLIENT","Year","Month","# of Accts Listed","Amt Listed","Recovered","Adjustments","RECALLED","Returned","FEES","AVG AGE AT LIST","Inventory Remaining","Unadjusted %","adjusted %"]] \
            .groupby(["NAME","CLIENT","Year"], as_index=False).sum()
Sheet2 = pd.concat([Sheet1,df2])
Sheet2['Month'] = Sheet2['Month'].astype(cat_month)
Sheet2.set_index(["NAME","CLIENT","Year","Month"], inplace=True)
Sheet2 = Sheet2.sort_values(["NAME","CLIENT","Year","Month"])
column_order = ["# of Accts Listed","Amt Listed","Recovered","Unadjusted %","Adjustments","RECALLED","Returned","adjusted %","Inventory Remaining","FEES","AVG AGE AT LIST"]
table3 = Sheet2.reindex(column_order, axis=1)
table3.to_excel('med1.xlsx',sheet_name='MED-1 Collections')