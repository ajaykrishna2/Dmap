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
        df=df.round(0)
        decimals=1
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
        med1_df.round(1)
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
        cff["AVG AGE AT LIST_y"]=cff["AVG AGE AT LIST_y"].round(0)
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
        dff["AVG AGE AT LIST_y"] = dff["AVG AGE AT LIST_y"].round(0)
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
        Sheet2["adjusted %"] = Sheet2["adjusted %"].apply(lambda x: round(x, decimals))
        Sheet2["Unadjusted %"] = Sheet2["Unadjusted %"].apply(lambda x: round(x, decimals))
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
            (df['CLIENT'].isin(['201AWP', '202AWP'])), ["NAME", "CLIENT", "Year", "Month", "NUM_ACCTS_LISTED", "LISTED",
                                                        "COLLECTED", "ADJUSTED", "RECALLED", "VOL_CANCELLED", "FEES",
                                                        "AVG AGE AT LIST", "Inventory Remaining", "Unadjusted %",
                                                        "adjusted %"]]


        med1_df1.columns = ["NAME", "CLIENT", "Year", "Month", "# of Accts Listed", "Amt Listed", "Recovered",
                           "Adjustments", "RECALLED", "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining",
                           "Unadjusted %", "adjusted %"]
        med1_df1["Inventory Remaining"] = med1_df1["Inventory Remaining"].astype(int)
        med1_pivot1 = pd.pivot_table(med1_df1, index=index1)
        med1_pivot1.round(0)
        med1_pivot1.reset_index(inplace=True)
        data3 = med1_pivot1[
            ["NAME", "CLIENT", "Month", "# of Accts Listed", "Amt Listed", "Recovered", "Adjustments", "RECALLED",
             "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining"]].groupby(
            ["NAME", "CLIENT"], as_index=False)
        d22 = data3.sum().stb.subtotal()
        print(type(d22))
        d22["Unadjusted %"] = ((d22["Recovered"] / d22["Amt Listed"]) * 100)
        d22["adjusted %"] = ((d22["Recovered"] / (
                    d22["Amt Listed"] + d22["Adjustments"] - d22["RECALLED"] - d22["Returned"])) * 100)
        db1 = d22["Unadjusted %"]
        db2 = d22["adjusted %"]
        db3 = pd.concat([db1, db2], axis=1)
        d3 = pd.merge(d22, db3)
        print(d3)
        d4 = data.mean()
        dd3 = med1_pivot1["AVG AGE AT LIST"].mean()
        column_list = list(d4.columns)
        print((column_list))
        data_list = []
        for i in range(len(column_list)):
            # print(i)
            if i == len(column_list) - 2:
                data_list.insert(i, dd3)
            else:
                data_list.insert(i, np.nan)
        print(data_list)
        d4.loc[len(d4)] = data_list
        cff1 = pd.merge(d3, d4, on=["NAME", "CLIENT"])
        cff1["AVG AGE AT LIST_y"]=cff1["AVG AGE AT LIST_y"].round(0)
        print(cff1.to_string())
        df3 = cff1[cff1.columns.difference(
            ["AVG AGE AT LIST_x", "# of Accts Listed_y", "Amt Listed_y",
             "Recovered_y", "Adjustments_y",
             "RECALLED_y", "Returned_y", "FEES_y", "Inventory Remaining_y"])]

        df3.columns = ["# of Accts Listed", "AVG AGE AT LIST", "Adjustments", "Amt Listed", "CLIENT", "FEES",
                       "Inventory Remaining", "NAME", "RECALLED", "Recovered", "Returned", "Unadjusted %", "adjusted %"]
        Sheet3 = pd.concat([med1_pivot1, df3])
        print(Sheet1)
        data4 = Sheet3[
            ["NAME", "CLIENT", "Year", "Month", "# of Accts Listed", "Amt Listed", "Recovered", "Adjustments",
             "RECALLED", "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining"]].groupby(
            ["NAME", "CLIENT", "Year"], as_index=False)

        c22 = data4.sum()
        c22["Unadjusted %"] = ((c22["Recovered"] / c22["Amt Listed"]) * 100)
        c22["adjusted %"] = ((c22["Recovered"] / (
                c22["Amt Listed"] + c22["Adjustments"] - c22["RECALLED"] - c22["Returned"])) * 100)
        cb1 = c22["Unadjusted %"]
        cb3 = c22["adjusted %"]
        cb2 = pd.concat([cb1, cb3], axis=1)
        c3 = pd.merge(c22, cb2)
        c4 = data4.mean()
        dff1 = pd.merge(c3, c4, on=["CLIENT", "Year"])
        dff1["AVG AGE AT LIST_y"] = dff1["AVG AGE AT LIST_y"].round(0)
        print(dff1.to_string())
        df4 = dff1[dff1.columns.difference(
            ["AVG AGE AT LIST_x", "NAME_y", "# of Accts Listed_y", "Amt Listed_y",
             "Recovered_y", "Adjustments_y",
             "RECALLED_y", "Returned_y", "FEES_y", "Inventory Remaining_y"])]
        print(df4.to_string())
        df4.columns = ["# of Accts Listed", "AVG AGE AT LIST", "Adjustments", "Amt Listed", "CLIENT", "FEES",
                       "Inventory Remaining", "NAME", "RECALLED", "Recovered", "Returned", "Unadjusted %", "Year",
                       "adjusted %"]
        Sheet4 = pd.concat([Sheet3, df4])
        Sheet4['Month'] = Sheet4['Month'].astype(cat_month)
        Sheet4.set_index(index1, inplace=True)
        Sheet4 = Sheet4.sort_values(index1)
        column_order1 = ["# of Accts Listed", "Amt Listed", "Recovered", "Unadjusted %", "Adjustments", "RECALLED",
                         "Returned", "adjusted %", "Inventory Remaining", "FEES", "AVG AGE AT LIST"]
        Sheet4 = Sheet4[
            ["# of Accts Listed", "Amt Listed", "Recovered", "Unadjusted %", "Adjustments", "RECALLED", "Returned",
             "adjusted %", "Inventory Remaining", "FEES", "AVG AGE AT LIST"]].apply(lambda x: round(x, 2))
        Sheet4["adjusted %"] = Sheet4["adjusted %"].apply(lambda x: round(x, decimals))
        Sheet4["Unadjusted %"] = Sheet4["Unadjusted %"].apply(lambda x: round(x, decimals))
        Sheet4["adjusted %"] = Sheet4["adjusted %"].fillna(0)
        Sheet4["Unadjusted %"] = Sheet4["Unadjusted %"].apply(str) + "%"
        Sheet4["adjusted %"] = Sheet4["adjusted %"].apply(str) + "%"
        # print(Sheet2.to_string())
        table4 = Sheet4.reindex(column_order1, axis=1)
        table4.reset_index(inplace=True)
        table4['Month'] = np.where(table4['Month'].isna(), "Total_" + table4['Year'].astype('str'), table4['Month']);
        table4['Month'] = np.where((table4['Year'].isna()), "Total_" + table4['CLIENT'], table4['Month'])
        table4['Month'] = table4['Month'].astype(str).str.split('.', expand=True)[0]
        shape = list(table4.shape)
        table4.at[shape[0] - 1, "Month"] = "Grand Total"
        table4.set_index(index1, inplace=True)
        #
        # # for CBS Work Comp_Accident
        med1_df2 = df.loc[
            (df['CLIENT'].isin(['201ERP', '201WCP', '202ERP', '202WCP'])), ["NAME", "CLIENT", "Year", "Month", "NUM_ACCTS_LISTED", "LISTED",
                                                        "COLLECTED", "ADJUSTED", "RECALLED", "VOL_CANCELLED", "FEES",
                                                        "AVG AGE AT LIST", "Inventory Remaining", "Unadjusted %",
                                                        "adjusted %"]]
        med1_df2.columns = ["NAME", "CLIENT", "Year", "Month", "# of Accts Listed", "Amt Listed", "Recovered",
                            "Adjustments", "RECALLED", "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining",
                            "Unadjusted %", "adjusted %"]
        med1_df2["Inventory Remaining"] = med1_df2["Inventory Remaining"]
        med1_pivot2 = pd.pivot_table(med1_df2, index=index1)
        med1_pivot2.reset_index(inplace=True)
        data5 = med1_pivot2[
            ["NAME", "CLIENT", "Month", "# of Accts Listed", "Amt Listed", "Recovered", "Adjustments", "RECALLED",
             "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining"]].groupby(
            ["NAME", "CLIENT"], as_index=False)
        d33 = data5.sum().stb.subtotal()
        print(type(d33))
        d33["Unadjusted %"] = ((d33["Recovered"] / d33["Amt Listed"]) * 100)
        d33["adjusted %"] = ((d33["Recovered"] / (
                d33["Amt Listed"] + d33["Adjustments"] - d33["RECALLED"] - d33["Returned"])) * 100)
        dc1 = d33["Unadjusted %"]
        dc2 = d33["adjusted %"]
        dc3 = pd.concat([dc1, dc2], axis=1)
        d5 = pd.merge(d33, dc3)
        print(d5)
        d6 = data5.mean()
        dd5 = med1_pivot2["AVG AGE AT LIST"].mean()
        column_list = list(d6.columns)
        print((column_list))
        data_list = []
        for i in range(len(column_list)):
            # print(i)
            if i == len(column_list) - 2:
                data_list.insert(i, dd5)
            else:
                data_list.insert(i, np.nan)
        print(data_list)
        d6.loc[len(d4)] = data_list
        cff2 = pd.merge(d5, d6, on=["NAME", "CLIENT"])
        cff2["AVG AGE AT LIST_y"]=cff2["AVG AGE AT LIST_y"].round(0)
        print(cff2.to_string())
        df5 = cff2[cff2.columns.difference(
            ["AVG AGE AT LIST_x", "# of Accts Listed_y", "Amt Listed_y",
             "Recovered_y", "Adjustments_y",
             "RECALLED_y", "Returned_y", "FEES_y", "Inventory Remaining_y"])]
        df5.columns = ["# of Accts Listed", "AVG AGE AT LIST", "Adjustments", "Amt Listed", "CLIENT", "FEES",
                       "Inventory Remaining", "NAME", "RECALLED", "Recovered", "Returned", "Unadjusted %", "adjusted %"]
        Sheet5 = pd.concat([med1_pivot2, df5])
        print(Sheet5)
        data6 = Sheet5[
            ["NAME", "CLIENT", "Year", "Month", "# of Accts Listed", "Amt Listed", "Recovered", "Adjustments",
             "RECALLED", "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining"]].groupby(
            ["NAME", "CLIENT", "Year"], as_index=False)
        c33 = data6.sum()
        c33["Unadjusted %"] = ((c33["Recovered"] / c33["Amt Listed"]) * 100)
        c33["adjusted %"] = ((c33["Recovered"] / (
                c33["Amt Listed"] + c33["Adjustments"] - c33["RECALLED"] - c33["Returned"])) * 100)
        cc1 = c33["Unadjusted %"]
        cc3 = c33["adjusted %"]
        cc2 = pd.concat([cc1, cc3], axis=1)
        c5 = pd.merge(c33, cc2)
        print(c5.to_string())
        c6 = data6.mean()
        print(c6.to_string())
        dff2 = pd.merge(c5, c6, on=["CLIENT", "Year"])
        dff2["AVG AGE AT LIST_y"] = dff2["AVG AGE AT LIST_y"].round(0)
        print(dff2.to_string())
        df6 = dff2[dff2.columns.difference(
            ["AVG AGE AT LIST_x", "NAME_y", "# of Accts Listed_y", "Amt Listed_y",
             "Recovered_y", "Adjustments_y",
             "RECALLED_y", "Returned_y", "FEES_y", "Inventory Remaining_y"])]
        print(df6.to_string())
        df6.columns = ["# of Accts Listed", "AVG AGE AT LIST", "Adjustments", "Amt Listed", "CLIENT", "FEES",
                       "Inventory Remaining", "NAME", "RECALLED", "Recovered", "Returned", "Unadjusted %", "Year",
                       "adjusted %"]
        Sheet6 = pd.concat([Sheet5, df6])
        Sheet6['Month'] = Sheet6['Month'].astype(cat_month)
        Sheet6.set_index(index1, inplace=True)
        Sheet6 = Sheet6.sort_values(index1)
        column_order1 = ["# of Accts Listed", "Amt Listed", "Recovered", "Unadjusted %", "Adjustments", "RECALLED",
                         "Returned", "adjusted %", "Inventory Remaining", "FEES", "AVG AGE AT LIST"]
        Sheet6 = Sheet6[
            ["# of Accts Listed", "Amt Listed", "Recovered", "Unadjusted %", "Adjustments", "RECALLED", "Returned",
             "adjusted %", "Inventory Remaining", "FEES", "AVG AGE AT LIST"]].apply(lambda x: round(x, 2))
        Sheet6["adjusted %"] = Sheet6["adjusted %"].apply(lambda x: round(x, decimals))
        Sheet6["Unadjusted %"] = Sheet6["Unadjusted %"].apply(lambda x: round(x, decimals))
        Sheet6["adjusted %"] = Sheet6["adjusted %"].fillna(0)
        Sheet6["Unadjusted %"] = Sheet6["Unadjusted %"].apply(str) + "%"
        Sheet6["adjusted %"] = Sheet6["adjusted %"].apply(str) + "%"
        # print(Sheet2.to_string())
        table5 = Sheet6.reindex(column_order1, axis=1)
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
    writer = pd.ExcelWriter('/home/ajay/PDS1_Riverview1.xlsx', engine='openpyxl')
    xls = pd.ExcelFile('/home/ajay/Downloads/Riverview.xlsx', engine='openpyxl')
    df_facs1 = pd.read_excel(xls, 'Details')
    Riverview(df_facs1,writer)
    writer.save()
