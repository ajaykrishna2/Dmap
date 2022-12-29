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
                 "AVG AGE AT LIST",    "Inventory Remaining", "Unadjusted %","adjusted %"]
        Column2=["NAME", "CLIENT", "Year", "Month", "# of Accts Listed", "Amt Listed", "Recovered","Adjustments", "RECALLED", "Returned", "FEES", "AVG AGE AT LIST","Inventory Remaining","Unadjusted %", "adjusted %"]
        sub = [ "AVG AGE AT LIST_x",  "# of Accts Listed_y", "Amt Listed_y",
             "Recovered_y", "Adjustments_y", "RECALLED_y", "Returned_y", "FEES_y", "Inventory Remaining_y","Year_x","Year_y","Unadjusted %_y","adjusted %_y"]
        sub2 = ["AVG AGE AT LIST_x",  "NAME_y", "# of Accts Listed_y", "Amt Listed_y",
             "Recovered_y", "Adjustments_y","RECALLED_y", "Returned_y", "FEES_y", "Inventory Remaining_y","Unadjusted %_y","adjusted %_y"]
        Column3=["# of Accts Listed", "AVG AGE AT LIST", "Adjustments", "Amt Listed", "CLIENT", "FEES",
                       "Inventory Remaining", "NAME", "RECALLED", "Recovered", "Returned", "Unadjusted %", "adjusted %"]
        Column4=[ "# of Accts Listed", "AVG AGE AT LIST", "Adjustments", "Amt Listed", "CLIENT", "FEES",
                       "Inventory Remaining", "NAME", "RECALLED", "Recovered", "Returned", "Unadjusted %", "Year",
                       "adjusted %"]

        column_order = ["# of Accts Listed", "Amt Listed", "Recovered", "Unadjusted %", "Adjustments", "RECALLED",
                        "Returned", "adjusted %", "Inventory Remaining", "FEES", "AVG AGE AT LIST" ]
        cat_month = CategoricalDtype(
            ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC'], ordered=True)
        # for Med1 collections

        med1_df = df.loc[
            (df['CLIENT'].isin(['201ECA', '202ECA'])), ["NAME", "CLIENT", "Year", "Month", "NUM_ACCTS_LISTED", "LISTED",
                                                        "COLLECTED", "ADJUSTED", "RECALLED", "VOL_CANCELLED", "FEES",
                                                        "AVG AGE AT LIST", "Inventory Remaining", "Unadjusted %",
                                                        "adjusted %"]]
        med1_df.columns = ["NAME", "CLIENT", "Year", "Month", "# of Accts Listed", "Amt Listed", "Recovered",
                           "Adjustments", "RECALLED", "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining",
                           "Unadjusted %", "adjusted %"]
        med1_df["Inventory Remaining"] = med1_df["Inventory Remaining"].astype(int)
        med1_pivot = pd.pivot_table(med1_df, index=index1)
        med1_pivot.reset_index(inplace=True)
        data=med1_pivot[["NAME", "CLIENT", "Month", "# of Accts Listed", "Amt Listed", "Recovered", "Adjustments", "RECALLED",
         "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining"]].groupby(
        ["NAME", "CLIENT"], as_index = False)
        d11 = data.sum().stb.subtotal()
        print(type(d11))
        d11["Unadjusted %"]=((d11["Recovered"]/d11["Amt Listed"])*100)
        d11["adjusted %"] = ((d11["Recovered"] / (d11["Amt Listed"]+d11["Adjustments"]-d11["RECALLED"]-d11["Returned"])) * 100)
        da1 =d11["Unadjusted %"]
        da2=d11["adjusted %"]
        da3 = pd.concat([da1, da2],axis=1)
        d1=pd.merge(d11,da3)
        print(d1)
        d2 = data.mean()
        dd2 = med1_pivot["AVG AGE AT LIST"].mean()
        column_list = list(d2.columns)
        print((column_list))
        data_list = []
        for i in range(len(column_list)):
            # print(i)
            if i == len(column_list) - 2:
                data_list.insert(i, dd2)
            else:
                data_list.insert(i, np.nan)
        print(data_list)
        d2.loc[len(d2)] = data_list
        cff = pd.merge(d1, d2, on=["NAME", "CLIENT"])
        print(cff.to_string())
        df1 = cff[cff.columns.difference(
            ["AVG AGE AT LIST_x",  "# of Accts Listed_y", "Amt Listed_y",
             "Recovered_y", "Adjustments_y",
             "RECALLED_y", "Returned_y", "FEES_y", "Inventory Remaining_y"])]
        df1.columns = ["# of Accts Listed", "AVG AGE AT LIST", "Adjustments", "Amt Listed", "CLIENT", "FEES",
                       "Inventory Remaining", "NAME", "RECALLED", "Recovered", "Returned", "Unadjusted %", "adjusted %"]
        Sheet1 = pd.concat([med1_pivot, df1])
        print(Sheet1)
        data2=Sheet1[["NAME", "CLIENT", "Year", "Month", "# of Accts Listed", "Amt Listed", "Recovered", "Adjustments",
                     "RECALLED", "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining"]].groupby(["NAME", "CLIENT", "Year"], as_index=False)
        c11 = data2.sum()
        c11["Unadjusted %"] = ((c11["Recovered"] / c11["Amt Listed"]) * 100)
        c11["adjusted %"] = ((c11["Recovered"] / (
                    c11["Amt Listed"] + c11["Adjustments"] - c11["RECALLED"] - c11["Returned"])) * 100)
        ca1 = c11["Unadjusted %"]
        ca3 = c11["adjusted %"]
        ca2 = pd.concat([ca1, ca3],axis=1)
        c1 = pd.merge(c11, ca2)
        c2 = data2.mean()
        dff = pd.merge(c1, c2, on=["CLIENT", "Year"])
        print(dff.to_string())
        df2 = dff[dff.columns.difference(
            ["AVG AGE AT LIST_x",  "NAME_y", "# of Accts Listed_y", "Amt Listed_y",
             "Recovered_y", "Adjustments_y",
             "RECALLED_y", "Returned_y", "FEES_y", "Inventory Remaining_y"])]
        print(df2.to_string())
        df2.columns = ["# of Accts Listed", "AVG AGE AT LIST", "Adjustments", "Amt Listed", "CLIENT", "FEES",
                       "Inventory Remaining", "NAME", "RECALLED", "Recovered", "Returned", "Unadjusted %", "Year",
                       "adjusted %"]
        Sheet2 = pd.concat([Sheet1, df2])
        Sheet2['Month'] = Sheet2['Month'].astype(cat_month)
        Sheet2.set_index(index1, inplace=True)
        Sheet2 = Sheet2.sort_values(index1)
        column_order1 = ["# of Accts Listed", "Amt Listed", "Recovered", "Unadjusted %", "Adjustments", "RECALLED",
                        "Returned", "adjusted %", "Inventory Remaining", "FEES", "AVG AGE AT LIST"]
        Sheet2 = Sheet2[
            ["# of Accts Listed", "Amt Listed", "Recovered", "Unadjusted %", "Adjustments", "RECALLED", "Returned",
             "adjusted %", "Inventory Remaining", "FEES", "AVG AGE AT LIST"]].apply(lambda x: round(x, 2))
        Sheet2["adjusted %"] = Sheet2["adjusted %"].fillna(0)
        Sheet2["Unadjusted %"] = Sheet2["Unadjusted %"].apply(str) + "%"
        Sheet2["adjusted %"] = Sheet2["adjusted %"].apply(str) + "%"
        # print(Sheet2.to_string())
        table3 = Sheet2.reindex(column_order1, axis=1)
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
        d3["Unadjusted %"] = ((d3["Recovered"] / d3["Amt Listed"]) * 100)
        d3["adjusted %"] = ((d3["Recovered"] / (
                    d3["Amt Listed"] + d3["Adjustments"] - d3["RECALLED"] - d3["Returned"])) * 100)
        da4 = d3["Unadjusted %"]
        da5 = d3["adjusted %"]
        da6 = pd.concat([da4, da5], axis=1)
        d33 = pd.merge(d3, da6)
        print(d33)
        d4 = data3.mean()
        dd5 = med1_pivot1["AVG AGE AT LIST"].mean()
        data_list1 = []
        column_list = list(d4.columns)
        print((column_list))
        for i in range(len(column_list)):
            print(i)
            if i == len(column_list) - 2:
                data_list1.insert(i, dd5)
            else:
                data_list1.insert(i, np.nan)
        print(data_list)
        d4.loc[len(d4)] = data_list1

        cff1 = pd.merge(d33, d4, on=["NAME", "CLIENT"])
        df3 = cff1[cff1.columns.difference(sub)]

        df3.columns =Column3
        Sheet3 = pd.concat([med1_pivot1, df3])
        print("S",Sheet3)
        print(Column2)
        data4=Sheet3["NAME", "CLIENT", "Year", "Month", "# of Accts Listed", "Amt Listed", "Recovered", "Adjustments",
                     "RECALLED", "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining"].groupby(["NAME", "CLIENT", "Year"], as_index=False)
        print(data4)
        c3 = data4.sum()
        c3["Unadjusted %"] = ((c3["Recovered"] / c3["Amt Listed"]) * 100)
        c3["adjusted %"] = ((c3["Recovered"] / (
                c3["Amt Listed"] + c3["Adjustments"] - c3["RECALLED"] - c3["Returned"])) * 100)
        ca4 = c3["Unadjusted %"]
        ca5 = c3["adjusted %"]
        ca6 = pd.concat([ca4, ca5], axis=1)
        c33 = pd.merge(d3, ca6)
        c4 =data4.mean()
        dff1 = pd.merge(c33, c4, on=["NAME", "CLIENT"])
        print(dff1)
        df4 = dff1[dff1.columns.difference(sub2)]
        print(df4)
        df4.columns = Column4
        Sheet4 = pd.concat([Sheet3, df4])
        Sheet4['Month'] = Sheet4['Month'].astype(cat_month)
        Sheet4.set_index(index1, inplace=True)
        Sheet4 = Sheet4.sort_values(index1)
        Sheet4 = Sheet4[column_order].apply(lambda x: round(x, 2))
        Sheet4["adjusted %"] = Sheet4["adjusted %"].fillna(0)
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
        d6 =data5.mean()
        d5["Unadjusted %"] = ((d5["Recovered"] / d5["Amt Listed"]) * 100)
        d5["adjusted %"] = ((d5["Recovered"] / (
                d5["Amt Listed"] + d5["Adjustments"] - d5["RECALLED"] - d5["Returned"])) * 100)
        da7 = d5["Unadjusted %"]
        da8 = d5["adjusted %"]
        da9 = pd.concat([da7, da8], axis=1)
        d55 = pd.merge(d5, da9)
        dd6 = med1_pivot1["AVG AGE AT LIST"].mean()
        data_list = []
        for i in range(len(column_list)):
            print(i)
            if i == len(column_list) - 4:
                data_list.insert(i, dd6)
            else:
                data_list.insert(i, np.nan)
        print(data_list)
        d6.loc[len(d4)] = data_list
        print(d6.to_string())
        cff2 =  pd.merge(d55, d6, on=["NAME", "CLIENT"])
        df5 = cff2[cff2.columns.difference(sub)]
        df5.columns = Column3
        Sheet5 = pd.concat([med1_pivot2, df5])
        data6=Sheet5[Column2].groupby(["NAME", "CLIENT", "Year"], as_index=False)
        c5 = data6.sum()
        c5["Unadjusted %"] = ((c5["Recovered"] / c5["Amt Listed"]) * 100)
        c5["adjusted %"] = ((c5["Recovered"] / (
                c5["Amt Listed"] + c5["Adjustments"] - c5["RECALLED"] - c5["Returned"])) * 100)
        ca7 = c5["Unadjusted %"]
        ca8 = c5["adjusted %"]
        ca9 = pd.concat([ca7, ca8], axis=1)
        c55 = pd.merge(c5, ca9)
        c6=data6.mean()
        dff2= pd.merge(c55, c6, on=["NAME", "CLIENT"])
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
    writer = pd.ExcelWriter('/home/ajay/PDS1_Riverview132.xlsx', engine='openpyxl')
    xls = pd.ExcelFile('/home/ajay/Downloads/Riverview.xlsx', engine='openpyxl')
    df_facs1 = pd.read_excel(xls, 'Details')
    Riverview(df_facs1,writer)
    writer.save()
