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
df["Month"]=df["Month"].fillna(0)
df["COLLECTED"]=df["COLLECTED"].fillna(0)
df["ADJUSTED"]=df["ADJUSTED"].fillna(0)
df["RECALLED"]=df["RECALLED"].fillna(0)
df["VOL_CANCELLED"]=df["VOL_CANCELLED"].fillna(0)
df["FEES"]=df["FEES"].fillna(0)


df['Unadjusted %'] = ((df['COLLECTED'] / df['LISTED']) * 100)
df['adjusted %'] = (((df['COLLECTED']) / (df['LISTED'] + df['ADJUSTED'] - df['RECALLED'] - df['VOL_CANCELLED'])) * 100)
df['Inventory Remaining'] = ((df['LISTED']) -(df['COLLECTED']) +(df['ADJUSTED']) -(df['RECALLED']) -(df['VOL_CANCELLED']))

med1_df2 = df.loc[(df['CLIENT'].isin(['201ERP' , '201WCP','202ERP','202WCP'])),["NAME","CLIENT","Year","Month","NUM_ACCTS_LISTED","LISTED","COLLECTED","ADJUSTED","RECALLED","VOL_CANCELLED","FEES","Inventory Remaining","Unadjusted %","adjusted %"]]
med1_df2.columns = [ "NAME", "CLIENT","Year", "Month", "# of Accts Listed","Amt Listed","Recovered","Adjustments","RECALLED","Returned","FEES","Inventory Remaining","Unadjusted %","adjusted %"]
med1_df2["Inventory Remaining"]=med1_df2["Inventory Remaining"]
med1_pivot2= pd.pivot_table(med1_df2,index=["NAME","CLIENT","Year","Month"])

med1_pivot2.reset_index(inplace=True)
cat_month = CategoricalDtype(['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC'],ordered=True)
df5 = med1_pivot2[["NAME","CLIENT","Month","# of Accts Listed","Amt Listed","Recovered","Adjustments","RECALLED","Returned","FEES","Inventory Remaining","Unadjusted %","adjusted %"]] \
            .groupby(["NAME","CLIENT"], as_index=False).sum().stb.subtotal().reset_index()


Sheet5 = pd.concat([med1_pivot2, df5])
df6 = Sheet5[["NAME","CLIENT","Year","Month","# of Accts Listed","Amt Listed","Recovered","Adjustments","RECALLED","Returned","FEES","Inventory Remaining","Unadjusted %","adjusted %"]] \
            .groupby(["NAME","CLIENT","Year"], as_index=False).sum()

Sheet6 = pd.concat([Sheet5,df6])
Sheet6['Month'] = Sheet6['Month'].astype(cat_month)
Sheet6.set_index(["NAME","CLIENT","Year","Month"], inplace=True)
Sheet6 = Sheet6.sort_values(["NAME","CLIENT","Year","Month"])
column_order = ["# of Accts Listed","Amt Listed","Recovered","Unadjusted %","Adjustments","RECALLED","Returned","adjusted %","Inventory Remaining","FEES"]

table5 = Sheet6.reindex(column_order, axis=1)
table5.reset_index(inplace=True)
# table3['Year']  = np.where((table3['Year'].isna()),"total_"+table3['CLIENT'],table3['Year'])
table5['Month'] = np.where(table5['Month'].isna(),"Total_"+table5['Year'].astype('str'),table5['Month']);

table5['Month'] = np.where((table5['Year'].isna()),"Total_"+table5['CLIENT'],table5['Month'])
table5['Month'] = table5['Month'].astype(str).str.split('.', expand = True)[0]

shape=list(table5.shape)

table5.at[shape[0]-1,"Month"]="Grand Total"
# table3[shape[0]-1,"Month"] ="Grand Total"
table5.set_index(["NAME","CLIENT","Year","Month"], inplace=True)



table5.to_excel('CBS Work Comp_Accident.xlsx',sheet_name='MED-1 Collections')