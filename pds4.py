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

        df = pd.read_excel('/home/ajay/Downloads/Jessica Sims Sample Report_Riverview Collections Report FEB 2021 (1).xlsx',sheet_name='Details')

        df["COLLECTED"] = df["COLLECTED"].fillna(0)
        df["ADJUSTED"] = df["ADJUSTED"].fillna(0)
        df["RECALLED"] = df["RECALLED"].fillna(0)
        df["VOL_CANCELLED"] = df["VOL_CANCELLED"].fillna(0)
        df["FEES"] = df["FEES"].fillna(0)
        df['Unadjusted %'] = (((df['COLLECTED'] / df['LISTED']) * 100))
        df['adjusted %'] = ((((df['COLLECTED']) / (df['LISTED'] + df['ADJUSTED'] - df['RECALLED'] - df['VOL_CANCELLED'])) * 100))
        df['Unadjusted %'] = df['Unadjusted %'].fillna(0)
        df['adjusted %'] = df['adjusted %'].fillna(0)
        df['Inventory Remaining'] = ((df['LISTED']) - (df['COLLECTED']) + (df['ADJUSTED']) - (df['RECALLED']) - (df['VOL_CANCELLED']))
        index1=["NAME", "CLIENT", "Year", "Month"]
        Column1=["NAME", "CLIENT", "Year", "Month", "NUM_ACCTS_LISTED", "LISTED","COLLECTED", "ADJUSTED", "RECALLED", "VOL_CANCELLED", "FEES",
                                                        "AVG AGE AT LIST", "Inventory Remaining", "Unadjusted %",
                                                        "adjusted %"]
        Column2=["NAME", "CLIENT", "Year", "Month", "# of Accts Listed", "Amt Listed", "Recovered","Adjustments", "RECALLED", "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining","Unadjusted %", "adjusted %"]
        sub = ["AVG AGE AT LIST_x", "Unadjusted %_x", "adjusted %_x", "# of Accts Listed_y", "Amt Listed_y",
               "Recovered_y", "Adjustments_y", "RECALLED_y", "Returned_y", "FEES_y", "Inventory Remaining_y","Year_x","Year_y"]
        sub2 = ["AVG AGE AT LIST_x", "Unadjusted %_x", "adjusted %_x", "NAME_y","# of Accts Listed_y", "Amt Listed_y",
               "Recovered_y", "Adjustments_y", "RECALLED_y", "Returned_y", "FEES_y", "Inventory Remaining_y"]
        Column3=["# of Accts Listed", "AVG AGE AT LIST", "Adjustments", "Amt Listed", "CLIENT", "FEES",
                       "Inventory Remaining", "NAME", "RECALLED", "Recovered", "Returned", "Unadjusted %","adjusted %"]
        Column4=[ "# of Accts Listed","AVG AGE AT LIST","Adjustments", "Amt Listed", "CLIENT", "FEES","Inventory Remaining","NAME","RECALLED","Recovered", "Returned",   "Unadjusted %", "Year","adjusted %"]

        column_order = ["# of Accts Listed", "Amt Listed", "Recovered", "Unadjusted %", "Adjustments", "RECALLED",
                        "Returned", "adjusted %", "Inventory Remaining", "FEES", "AVG AGE AT LIST"]
        cat_month = CategoricalDtype(
            ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC'], ordered=True)
        # for Med1 collections

        med1_df = df.loc[(df['CLIENT'].isin(['201ECA', '202ECA'])), Column1]
        med1_df.columns = Column2
        med1_df["Inventory Remaining"] = med1_df["Inventory Remaining"].astype(int)
        med1_pivot = pd.pivot_table(med1_df, index=index1)
        med1_pivot.reset_index(inplace=True)
        data=med1_pivot[Column2].groupby(["NAME", "CLIENT"], as_index=False)
        d1 = data.sum().stb.subtotal()
        d2= data.mean()
        dd2 = med1_pivot["AVG AGE AT LIST"].mean()
        dd3 = med1_pivot["Unadjusted %"].mean()
        dd4 = med1_pivot["adjusted %"].mean()
        column_list=list(d2.columns)
        print((column_list))
        data_list=[]
        for i in range(len(column_list)):
            print(i)
            if i == len(column_list)-4:
                data_list.insert(i,dd2)
            elif i == len(column_list)-2:
                data_list.insert(i,dd3)
            elif i == len(column_list)-1:
                data_list.insert(i,dd4)
            else:
                data_list.insert(i,np.nan)
        print(data_list)
        d2.loc[len(d2)] = data_list

        cff = pd.merge(d1, d2, on=["NAME", "CLIENT"])
        df1 = cff[cff.columns.difference(sub)]
        df1.columns = Column3
        Sheet1 = pd.concat([med1_pivot, df1])
        data2=Sheet1[Column2].groupby(["NAME", "CLIENT", "Year"], as_index=False)
        c1 = data2.sum()
        c2 = data2.mean()
        dff = pd.merge(c1, c2,on=["CLIENT", "Year"])
        df2 = dff[dff.columns.difference(sub2)]
        df2.columns=Column4
        Sheet2 = pd.concat([Sheet1, df2])
        Sheet2['Month'] = Sheet2['Month'].astype(cat_month)
        Sheet2.set_index(["NAME", "CLIENT", "Year", "Month"], inplace=True)
        Sheet2 = Sheet2.sort_values(["NAME", "CLIENT", "Year", "Month"])
        Sheet2 = Sheet2[column_order].apply(lambda x: round(x, 2))
        Sheet2["Unadjusted %"]=Sheet2["Unadjusted %"].apply(str)+"%"
        Sheet2["adjusted %"] = Sheet2["adjusted %"].apply(str) + "%"
        print(Sheet2.to_string())
        table3 = Sheet2.reindex(column_order, axis=1)
        table3.reset_index(inplace=True)
        table3['Month'] = np.where(table3['Month'].isna(), "Total_" + table3['Year'].astype('str'), table3['Month']);
        table3['Month'] = np.where((table3['Year'].isna()), "Total_" + table3['CLIENT'], table3['Month'])
        table3['Month'] = table3['Month'].astype(str).str.split('.', expand=True)[0]
        shape = list(table3.shape)
        table3.at[shape[0] - 1, "Month"] = "Grand Total"
        table3.set_index(index1, inplace=True)

        # for CBS Early Out

        med1_df1 = df.loc[
            (df['CLIENT'].isin(['201AWP', '202AWP'])), Column1]
        med1_df1.columns = Column2
        med1_df1["Inventory Remaining"] = med1_df1["Inventory Remaining"].astype(int)
        med1_pivot1 = pd.pivot_table(med1_df1, index=index1)
        med1_pivot1.reset_index(inplace=True)
        data3=med1_pivot1[Column2].groupby(["NAME", "CLIENT"], as_index=False)
        d3 = data3.sum().stb.subtotal()
        d4 = data3.mean()
        dd5 = med1_pivot1["AVG AGE AT LIST"].mean()
        dd6 = med1_pivot1["Unadjusted %"].mean()
        dd7 = med1_pivot1["adjusted %"].mean()
        column_list = list(d4.columns)
        print((column_list))
        data_list = []
        for i in range(len(column_list)):
            print(i)
            if i == len(column_list) - 4:
                data_list.insert(i, dd5)
            elif i == len(column_list) - 2:
                data_list.insert(i, dd6)
            elif i == len(column_list) - 1:
                data_list.insert(i, dd7)
            else:
                data_list.insert(i, np.nan)
        print(data_list)
        d4.loc[len(d4)] = data_list
        print(d4.to_string())
        cff1 = pd.merge(d3, d4, on=["NAME", "CLIENT"])
        df3 = cff1[cff1.columns.difference(sub)]
        df3.columns =Column3
        Sheet3 = pd.concat([med1_pivot1, df3])
        data4=Sheet3[Column2].groupby(["NAME", "CLIENT", "Year"], as_index=False)
        c3 = data4.sum()
        c4 = data4.mean()
        dff1 = pd.merge(c3, c4, on=["CLIENT", "Year"])
        df4 = dff1[dff1.columns.difference(sub2)]
        df4.columns = Column4
        Sheet4 = pd.concat([Sheet3, df4])
        Sheet4['Month'] = Sheet4['Month'].astype(cat_month)
        Sheet4.set_index(index1, inplace=True)
        Sheet4 = Sheet4.sort_values(index1)
        Sheet4 = Sheet4[column_order].apply(lambda x: round(x, 2))
        Sheet4["Unadjusted %"] = Sheet4["Unadjusted %"].apply(str) + "%"
        Sheet4["adjusted %"] = Sheet4["adjusted %"].apply(str) + "%"
        print(Sheet4.to_string())
        table4 = Sheet4.reindex(column_order, axis=1)
        table4.reset_index(inplace=True)
        table4['Month'] = np.where(table4['Month'].isna(), "Total_" + table4['Year'].astype('str'), table4['Month']);
        table4['Month'] = np.where((table4['Year'].isna()), "Total_" + table4['CLIENT'], table4['Month'])
        table4['Month'] = table4['Month'].astype(str).str.split('.', expand=True)[0]
        shape = list(table4.shape)
        table4.at[shape[0] - 1, "Month"] = "Grand Total"
        table4.set_index(index1, inplace=True)
        #
        # # for CBS Work Comp_Accident
        med1_df2 = df.loc[(df['CLIENT'].isin(['201ERP', '201WCP', '202ERP', '202WCP'])), Column1]
        med1_df2.columns = Column2
        med1_df2["Inventory Remaining"] = med1_df2["Inventory Remaining"]
        med1_pivot2 = pd.pivot_table(med1_df2, index=index1)
        med1_pivot2.reset_index(inplace=True)
        data5=med1_pivot2[Column2].groupby(["NAME", "CLIENT"], as_index=False)
        d5 = data5.sum().stb.subtotal()
        d6 = data5.mean()
        dd8 = med1_pivot2["AVG AGE AT LIST"].mean()
        dd9 = med1_pivot2["Unadjusted %"].mean()
        dd10 = med1_pivot2["adjusted %"].mean()
        column_list = list(d6.columns)
        print((column_list))
        data_list = []
        for i in range(len(column_list)):
            print(i)
            if i == len(column_list) - 4:
                data_list.insert(i, dd8)
            elif i == len(column_list) - 2:
                data_list.insert(i, dd9)
            elif i == len(column_list) - 1:
                data_list.insert(i, dd10)
            else:
                data_list.insert(i, np.nan)
        print(data_list)
        d6.loc[len(d6)] = data_list
        print(d6.to_string())
        cff2 = pd.merge(d5, d6, on=["NAME", "CLIENT"])
        df5 = cff2[cff2.columns.difference(sub)]
        df5.columns = Column3
        Sheet5 = pd.concat([med1_pivot2, df5])
        data6=Sheet5[Column2].groupby(["NAME", "CLIENT", "Year"], as_index=False)
        c5 = data6.sum()
        c6 = data6.mean()
        dff2 = pd.merge(c5, c6, on=["CLIENT", "Year"])
        df6 = dff2[dff2.columns.difference(sub2)]
        df6.columns = Column4
        Sheet6 = pd.concat([Sheet5, df6])
        Sheet6['Month'] = Sheet6['Month'].astype(cat_month)
        Sheet6.set_index(index1, inplace=True)
        Sheet6 = Sheet6.sort_values(index1)
        Sheet6 = Sheet6[column_order].apply(lambda x: round(x, 2))
        Sheet6["Unadjusted %"] = Sheet6["Unadjusted %"].apply(str) + "%"
        Sheet6["adjusted %"] = Sheet6["adjusted %"].apply(str) + "%"
        print(Sheet6.to_string())
        table5 = Sheet6.reindex(column_order, axis=1)
        table5.reset_index(inplace=True)
        table5['Month'] = np.where(table5['Month'].isna(), "Total_" + table5['Year'].astype('str'), table5['Month']);
        table5['Month'] = np.where((table5['Year'].isna()), "Total_" + table5['CLIENT'], table5['Month'])
        table5['Month'] = table5['Month'].astype(str).str.split('.', expand=True)[0]
        shape = list(table5.shape)
        table5.at[shape[0] - 1, "Month"] = "Grand Total"
        table5.set_index(index1, inplace=True)

        table3.to_excel(writer, index=True, sheet_name='MED-12 Collections')
        table4.to_excel(writer, index=True, sheet_name='CBS Early Out.xlsx')
        table5.to_excel(writer, index=True, sheet_name='CBS Work Comp_Accident.xlsx')

    except Exception as e:
        logging.exception("error")




if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/PDS_Riverview1.xlsx', engine='openpyxl')
    xls = pd.ExcelFile('/home/ajay/Downloads/Riverview.xlsx', engine='openpyxl')
    df_facs1 = pd.read_excel(xls, 'Details')
    Riverview(df_facs1,writer)
    writer.save()
