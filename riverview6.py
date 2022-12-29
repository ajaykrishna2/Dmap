import itertools
from string import ascii_uppercase

import pandas as pd
import sys
import logging

from IPython.core.display import display
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


def Riverview(df, writer):
    try:
        def highlight_col1(x):
            r = 'background-color: #fad2b9'
            g = 'background-color: #bab8b6'
            w = 'color:white'
            lg = 'background-color: #d3d3d3'
            df2 = pd.DataFrame('', index=x.index, columns=x.columns)
            # df2.iloc[:, 0] = g
            # df2.iloc[:, 1] = lg
            df2.iloc[:, 7] = r
            df2.iloc[:, 11] = r
            x.fillna(9999)
            table3_2 = x.index[x['rank'] != 1.0]
            j = list(table3_2)
            i = x.index[(x.duplicated(['CLIENT']))]
            df2.iloc[j, 2] = w
            df2.iloc[i, 0] = w
            df2.iloc[:,1]=w
            df2.iloc[:, 15] = w
            df2.iloc[:, 16] = w

            return df2



        styles = [dict(selector="th", props=[("background-color", "#d3d3d3")])]
        decimals = 1
        df["NUM_ACCTS_LISTED"] = df["NUM_ACCTS_LISTED"].fillna(0)
        df["NUM_ACCTS_ADJ_LIST"] = df["NUM_ACCTS_ADJ_LIST"].fillna(0)
        df["LISTED"] = df["LISTED"].fillna(0)

        df["COLLECTED"] = df["COLLECTED"].fillna(0)
        df["ADJUSTED"] = df["ADJUSTED"].fillna(0)
        df["RECALLED"] = df["RECALLED"].fillna(0)
        df["NUM_ACCTS_RECALLED"] = df["NUM_ACCTS_RECALLED"].fillna(0)
        df["NUM_ACCTS_CANCELED"] = df["NUM_ACCTS_CANCELED"].fillna(0)
        df["NET COLLECTIONS"] = df["NET COLLECTIONS"].fillna(0)
        df["MTHLY COLLECTIONS"] = df["MTHLY COLLECTIONS"].fillna(0)
        df["AVG AGE AT LIST"] = df["AVG AGE AT LIST"].fillna(0)

        df["VOL_CANCELLED"] = df["VOL_CANCELLED"].fillna(0)
        df["FEES"] = df["FEES"].fillna(0)
        data_details = df

        #         print(data_details.to_string())
        df['Unadjusted %'] = (((df['COLLECTED'] / df['LISTED']) * 100))
        df['adjusted %'] = (
            (((df['COLLECTED']) / (df['LISTED'] + df['ADJUSTED'] - df['RECALLED'] - df['VOL_CANCELLED'])) * 100))
        df['Unadjusted %'] = df['Unadjusted %'].fillna(0)
        df['adjusted %'] = df['adjusted %'].fillna(0)
        df['Inventory Remaining'] = (
                (df['LISTED']) - (df['COLLECTED']) + (df['ADJUSTED']) - (df['RECALLED']) - (df['VOL_CANCELLED']))
        df["adjusted %"] = df["adjusted %"].fillna(0)
        df["Inventory Remaining"] = df["Inventory Remaining"].fillna(0)
        df["Unadjusted %"] = df["Unadjusted %"].fillna(0)
        # for col in df.columns[7:]:
        #     df[col] = df[col].apply(formatter)

        #         print(df['Inventory Remaining'])
        index1 = ["NAME", "CLIENT", "Year", "Month"]
        Column1 = ["NAME", "CLIENT", "Year", "Month", "NUM_ACCTS_LISTED", "LISTED", "COLLECTED", "ADJUSTED", "RECALLED",
                   "VOL_CANCELLED", "FEES", "AVG AGE AT LIST", "Inventory Remaining", "Unadjusted %", "adjusted %"]
        Column2 = ["NAME", "CLIENT", "Year", "Month", "# of Accts Listed", "Amt Listed", "Recovered", "Adjustments",
                   "RECALLED", "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining", "Unadjusted %",
                   "adjusted %"]
        Column3 = ["NAME", "CLIENT", "Month", "# of Accts Listed", "Amt Listed", "Recovered", "Adjustments", "RECALLED",
                   "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining"]
        Column4 = ["# of Accts Listed", "AVG AGE AT LIST", "Adjustments", "Amt Listed", "CLIENT", "FEES",
                   "Inventory Remaining", "NAME", "RECALLED", "Recovered", "Returned", "Unadjusted %", "adjusted %"]
        Column5 = ["NAME", "CLIENT", "Year", "Month", "# of Accts Listed", "Amt Listed", "Recovered", "Adjustments",
                   "RECALLED", "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining"]
        sub = ["AVG AGE AT LIST_x", "# of Accts Listed_y", "Amt Listed_y", "Recovered_y", "Adjustments_y", "RECALLED_y",
               "Returned_y", "FEES_y", "Inventory Remaining_y"]
        sub2 = ["AVG AGE AT LIST_x", "NAME_y", "# of Accts Listed_y", "Amt Listed_y", "Recovered_y", "Adjustments_y",
                "RECALLED_y", "Returned_y", "FEES_y", "Inventory Remaining_y"]
        Column6 = ["# of Accts Listed", "AVG AGE AT LIST", "Adjustments", "Amt Listed", "CLIENT", "FEES",
                   "Inventory Remaining", "NAME", "RECALLED", "Recovered", "Returned", "Unadjusted %", "Year",
                   "adjusted %"]
        Column7 = ["# of Accts Listed", "Amt Listed", "Recovered", "Unadjusted %", "Adjustments", "RECALLED",
                   "Returned", "adjusted %", "Inventory Remaining", "FEES", "AVG AGE AT LIST"]
        column_order = ["# of Accts Listed", "Amt Listed", "Recovered", "Unadjusted %", "Adjustments", "RECALLED",
                        "Returned", "adjusted %", "Inventory Remaining", "FEES", "AVG AGE AT LIST"]
        d = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUNE': 6, 'JULY': 7, 'AUG': 8, 'SEPT': 9, 'OCT': 10,
             'NOV': 11, 'DEC': 12}
        cat_month = CategoricalDtype(
            ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC','Total_2009','Total_2010','Total_2011','Total_2012','Total_2013','Total_2014','Total_2015','Total_2016','Total_2017','Total_2018','Total_2019','Total_2020','Total_2021','Total_2022','Total_2023'], ordered=True)
        # for Med1 collections

        med1_df = df.loc[
            (df['CLIENT'].isin(['201ECA', '202ECA'])), Column1]
        med1_df.round(1)
        med1_df.columns = Column2
        med1_df["Inventory Remaining"] = med1_df["Inventory Remaining"]
        med1_pivot = pd.pivot_table(med1_df, index=index1)
        med1_pivot.reset_index(inplace=True)
        data = med1_pivot[Column3].groupby(["NAME", "CLIENT"], as_index=False)
        d11 = data.sum().stb.subtotal()
        d11["Unadjusted %"] = ((d11["Recovered"] / d11["Amt Listed"]) * 100)
        d11["adjusted %"] = ((d11["Recovered"] / (
                d11["Amt Listed"] + d11["Adjustments"] - d11["RECALLED"] - d11["Returned"])) * 100)
        da1 = d11["Unadjusted %"]
        da2 = d11["adjusted %"]
        da3 = pd.concat([da1, da2], axis=1)
        d1 = pd.merge(d11, da3)
        d2 = data.mean()
        dd2 = med1_pivot["AVG AGE AT LIST"].mean()
        column_list = list(d2.columns)
        data_list = []
        for i in range(len(column_list)):
            if i == len(column_list) - 2:
                data_list.insert(i, dd2)
            else:
                data_list.insert(i, np.nan)
        d2.loc[len(d2)] = data_list
        cff = pd.merge(d1, d2, on=["NAME", "CLIENT"])
        df1 = cff[cff.columns.difference(sub)]
        df1.columns = Column4
        Sheet1 = pd.concat([med1_pivot, df1])
        Sheet1['Month'] = Sheet1['Month'].astype(cat_month)


        data2 = Sheet1[Column5].groupby(["NAME", "CLIENT", "Year"], as_index=False)

        c11 = data2.sum()
        c11["Unadjusted %"] = ((c11["Recovered"] / c11["Amt Listed"]) * 100)
        c11["adjusted %"] = ((c11["Recovered"] / (
                c11["Amt Listed"] + c11["Adjustments"] - c11["RECALLED"] - c11["Returned"])) * 100)
        ca1 = c11["Unadjusted %"]
        ca3 = c11["adjusted %"]
        ca2 = pd.concat([ca1, ca3], axis=1)
        c1 = pd.merge(c11, ca2)
        c2 = data2.mean()
        dff = pd.merge(c1, c2, on=["CLIENT", "Year"])
        df2 = dff[dff.columns.difference(sub2)]
        df2.columns = Column6
        df2['Month'] = "Total_" + df2['Year'].astype(str)
        df2['Month'] = df2['Month'].astype(str).str.split('.', expand=True)[0]
        df2=df2[['NAME', 'CLIENT', 'Year', 'Month', '# of Accts Listed','AVG AGE AT LIST', 'Adjustments', 'Amt Listed', 'FEES', 'Inventory Remaining', 'RECALLED', 'Recovered', 'Returned','Unadjusted %', 'adjusted %']]
        Sheet22 = pd.concat([Sheet1,df2],ignore_index=True)
        Sheet22['Month'] = Sheet22['Month'].astype(cat_month)
        Sheet2 = Sheet22.sort_values(index1)
        shape = list(Sheet2.shape)
        Sheet2['Month'] = np.where((Sheet2['Year'].isna()), "Total_" + Sheet2['CLIENT'], Sheet2['Month'])
        Sheet2.reset_index(drop=True,inplace=True)
        Sheet2.at[shape[0] - 1, "Month"] = "Grand Total"
        Sheet2["AVG AGE AT LIST"] = Sheet2["AVG AGE AT LIST"].apply(lambda x: round(x, 0))
        Sheet2["adjusted %"] = Sheet2["adjusted %"].apply(lambda x: round(x, decimals))
        Sheet2["Unadjusted %"] = Sheet2["Unadjusted %"].apply(lambda x: round(x, decimals))
        Sheet2["adjusted %"] = Sheet2["adjusted %"].fillna(0)
        Sheet2["Unadjusted %"] = Sheet2["Unadjusted %"].apply(str) + "%"
        Sheet2["adjusted %"] = Sheet2["adjusted %"].apply(str) + "%"
        Sheet2["Amt Listed"] = Sheet2.apply(lambda x: "{:,.0f}".format(x["Amt Listed"]), axis=1)
        Sheet2["Recovered"] = Sheet2.apply(lambda x: "{:,.0f}".format(x["Recovered"]), axis=1)
        Sheet2["Adjustments"] = np.rint(Sheet2["Adjustments"])
        Sheet2["RECALLED"] = Sheet2.apply(lambda x: "{:,.0f}".format(x["RECALLED"]), axis=1)
        Sheet2["Returned"] = Sheet2.apply(lambda x: "{:,.0f}".format(x["Returned"]), axis=1)
        Sheet2["Inventory Remaining"] = Sheet2.apply(lambda x: "{:,.0f}".format(x["Inventory Remaining"]), axis=1)
        Sheet2["FEES"] = Sheet2.apply(lambda x: "{:,.0f}".format(x["FEES"]), axis=1)
        column_order1 = ['NAME','CLIENT','Year','Month',"# of Accts Listed", "Amt Listed", "Recovered", "Unadjusted %", "Adjustments", "RECALLED","Returned", "adjusted %", "Inventory Remaining", "FEES", "AVG AGE AT LIST" ]
        table3 = Sheet2.reindex(column_order1, axis=1)
        table3['monthnumber'] = table3.Month.map(d)
        table3['rank'] = table3.groupby(['NAME', 'CLIENT', 'Year'])['monthnumber'].rank(ascending=True);
        tab1=table3.rename(columns={'adjusted %': 'Adjusted %'}, inplace=False)
        table6 = tab1.style.apply(highlight_col1, axis=None).set_properties(**{'text-align': 'right'}).set_table_styles(styles)
        # table6=table66([column_order1])

        # for CBS Early Out

        med1_df1 = df.loc[
            (df['CLIENT'].isin(['201AWP', '202AWP'])), Column1]
        med1_df1.round(1)
        med1_df1.columns = Column2
        med1_df1["Inventory Remaining"] = med1_df1["Inventory Remaining"]
        med1_pivot1 = pd.pivot_table(med1_df1, index=index1)
        med1_pivot1.reset_index(inplace=True)
        data3 = med1_pivot1[Column3].groupby(["NAME", "CLIENT"], as_index=False)
        d22 = data3.sum().stb.subtotal()
        d22["Unadjusted %"] = ((d22["Recovered"] / d22["Amt Listed"]) * 100)
        d22["adjusted %"] = ((d22["Recovered"] / (
                d22["Amt Listed"] + d22["Adjustments"] - d22["RECALLED"] - d22["Returned"])) * 100)
        db1 = d22["Unadjusted %"]
        db2 = d22["adjusted %"]
        db3 = pd.concat([db1, db2], axis=1)
        d3 = pd.merge(d22, db3)
        d4 = data3.mean()
        dd3 = med1_pivot1["AVG AGE AT LIST"].mean()
        column_list = list(d4.columns)
        data_list = []
        for i in range(len(column_list)):
            if i == len(column_list) - 2:
                data_list.insert(i, dd3)
            else:
                data_list.insert(i, np.nan)
        d4.loc[len(d4)] = data_list
        cff1 = pd.merge(d3, d4, on=["NAME", "CLIENT"])
        df3 = cff1[cff1.columns.difference(sub)]
        df3.columns = Column4
        Sheet3 = pd.concat([med1_pivot1, df3])
        data4 = Sheet3[Column5].groupby(["NAME", "CLIENT", "Year"], as_index=False)
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
        df4 = dff1[dff1.columns.difference(sub2)]
        df4.columns = Column6
        df4['Month'] = "Total_" + df4['Year'].astype(str)
        df4['Month'] = df4['Month'].astype(str).str.split('.', expand=True)[0]
        df4 = df4[
            ['NAME', 'CLIENT', 'Year', 'Month', '# of Accts Listed', 'AVG AGE AT LIST', 'Adjustments', 'Amt Listed',
             'FEES', 'Inventory Remaining', 'RECALLED', 'Recovered', 'Returned', 'Unadjusted %', 'adjusted %']]
        Sheet44 = pd.concat([Sheet3, df4], ignore_index=True)
        Sheet44['Month'] = Sheet44['Month'].astype(cat_month)
        Sheet4 = Sheet44.sort_values(index1)
        shape = list(Sheet4.shape)
        Sheet4['Month'] = np.where((Sheet4['Year'].isna()), "Total_" + Sheet4['CLIENT'], Sheet4['Month'])
        Sheet4.reset_index(drop=True, inplace=True)
        Sheet4.at[shape[0] - 1, "Month"] = "Grand Total"
        Sheet4["AVG AGE AT LIST"] = Sheet4["AVG AGE AT LIST"].apply(lambda x: round(x, 0))
        Sheet4["adjusted %"] = Sheet4["adjusted %"].apply(lambda x: round(x, decimals))
        Sheet4["Unadjusted %"] = Sheet4["Unadjusted %"].apply(lambda x: round(x, decimals))
        Sheet4["adjusted %"] = Sheet4["adjusted %"].fillna(0)
        Sheet4["Unadjusted %"] = Sheet4["Unadjusted %"].apply(str) + "%"
        Sheet4["adjusted %"] = Sheet4["adjusted %"].apply(str) + "%"
        Sheet4["Amt Listed"] = Sheet4.apply(lambda x: "{:,.0f}".format(x["Amt Listed"]), axis=1)
        Sheet4["Recovered"] = Sheet4.apply(lambda x: "{:,.0f}".format(x["Recovered"]), axis=1)
        Sheet4["Adjustments"] = np.rint(Sheet4["Adjustments"])
        Sheet4["RECALLED"] = Sheet4.apply(lambda x: "{:,.0f}".format(x["RECALLED"]), axis=1)
        Sheet4["Returned"] = Sheet4.apply(lambda x: "{:,.0f}".format(x["Returned"]), axis=1)
        Sheet4["Inventory Remaining"] = Sheet4.apply(lambda x: "{:,.0f}".format(x["Inventory Remaining"]), axis=1)
        Sheet4["FEES"] = Sheet4.apply(lambda x: "{:,.0f}".format(x["FEES"]), axis=1)
        column_order1 = ['NAME', 'CLIENT', 'Year', 'Month', "# of Accts Listed", "Amt Listed", "Recovered",
                         "Unadjusted %", "Adjustments", "RECALLED", "Returned", "adjusted %", "Inventory Remaining",
                         "FEES", "AVG AGE AT LIST"]
        table4 = Sheet4.reindex(column_order1, axis=1)
        table4['monthnumber'] = table4.Month.map(d)
        table4['rank'] = table4.groupby(['NAME', 'CLIENT', 'Year'])['monthnumber'].rank(ascending=True);
        tab2 = table4.rename(columns={'adjusted %': 'Adjusted %'}, inplace=False)
        table7 = tab2.style.apply(highlight_col1, axis=None).set_properties(**{'text-align': 'right'}).set_table_styles(styles)
        #

        # # for CBS Work Comp_Accident
        med1_df2 = df.loc[
            (df['CLIENT'].isin(['201ERP', '201WCP', '202ERP', '202WCP'])), Column1]
        med1_df2.columns = Column2
        med1_df2["Inventory Remaining"] = med1_df2["Inventory Remaining"]
        med1_pivot2 = pd.pivot_table(med1_df2, index=index1)
        med1_pivot2.reset_index(inplace=True)
        data5 = med1_pivot2[Column3].groupby(["NAME", "CLIENT"], as_index=False)
        d33 = data5.sum().stb.subtotal()
        d33["Unadjusted %"] = ((d33["Recovered"] / d33["Amt Listed"]) * 100)
        d33["adjusted %"] = ((d33["Recovered"] / (
                d33["Amt Listed"] + d33["Adjustments"] - d33["RECALLED"] - d33["Returned"])) * 100)
        dc1 = d33["Unadjusted %"]
        dc2 = d33["adjusted %"]
        dc3 = pd.concat([dc1, dc2], axis=1)
        d5 = pd.merge(d33, dc3)
        d6 = data5.mean()
        dd5 = med1_pivot2["AVG AGE AT LIST"].mean()
        column_list = list(d6.columns)
        data_list = []
        for i in range(len(column_list)):
            if i == len(column_list) - 2:
                data_list.insert(i, dd5)
            else:
                data_list.insert(i, np.nan)
        #         print(data_list)
        d6.loc[len(d6)] = data_list
        cff2 = pd.merge(d5, d6, on=["NAME", "CLIENT"])
        df5 = cff2[cff2.columns.difference(sub)]
        df5.columns = Column4
        Sheet5 = pd.concat([med1_pivot2, df5])
        data6 = Sheet5[Column5].groupby(["NAME", "CLIENT", "Year"], as_index=False)
        c33 = data6.sum()
        c33["Unadjusted %"] = ((c33["Recovered"] / c33["Amt Listed"]) * 100)
        c33["adjusted %"] = ((c33["Recovered"] / (
                c33["Amt Listed"] + c33["Adjustments"] - c33["RECALLED"] - c33["Returned"])) * 100)
        cc1 = c33["Unadjusted %"]
        cc3 = c33["adjusted %"]
        cc2 = pd.concat([cc1, cc3], axis=1)
        c5 = pd.merge(c33, cc2)
        c6 = data6.mean()
        dff2 = pd.merge(c5, c6, on=["CLIENT", "Year"])
        df6 = dff2[dff2.columns.difference(sub2)]
        df6.columns = Column6
        df6['Month'] = "Total_" + df6['Year'].astype(str)
        df6['Month'] = df6['Month'].astype(str).str.split('.', expand=True)[0]
        df6 = df6[
            ['NAME', 'CLIENT', 'Year', 'Month', '# of Accts Listed', 'AVG AGE AT LIST', 'Adjustments', 'Amt Listed',
             'FEES', 'Inventory Remaining', 'RECALLED', 'Recovered', 'Returned', 'Unadjusted %', 'adjusted %']]
        Sheet66 = pd.concat([Sheet5, df6], ignore_index=True)
        Sheet66['Month'] = Sheet66['Month'].astype(cat_month)
        Sheet6 = Sheet66.sort_values(index1)
        shape = list(Sheet6.shape)
        Sheet6['Month'] = np.where((Sheet6['Year'].isna()), "Total_" + Sheet6['CLIENT'], Sheet6['Month'])
        Sheet6.reset_index(drop=True, inplace=True)
        Sheet6.at[shape[0] - 1, "Month"] = "Grand Total"
        Sheet6["AVG AGE AT LIST"] = Sheet6["AVG AGE AT LIST"].apply(lambda x: round(x, 0))
        Sheet6["adjusted %"] = Sheet6["adjusted %"].apply(lambda x: round(x, decimals))
        Sheet6["Unadjusted %"] = Sheet6["Unadjusted %"].apply(lambda x: round(x, decimals))
        Sheet6["adjusted %"] = Sheet6["adjusted %"].fillna(0)
        Sheet6["Unadjusted %"] = Sheet6["Unadjusted %"].apply(str) + "%"
        Sheet6["adjusted %"] = Sheet6["adjusted %"].apply(str) + "%"
        Sheet6["Amt Listed"] = Sheet6.apply(lambda x: "{:,.0f}".format(x["Amt Listed"]), axis=1)
        Sheet6["Recovered"] = Sheet6.apply(lambda x: "{:,.0f}".format(x["Recovered"]), axis=1)
        Sheet6["Adjustments"] = np.rint(Sheet6["Adjustments"])
        Sheet6["RECALLED"] = Sheet6.apply(lambda x: "{:,.0f}".format(x["RECALLED"]), axis=1)
        Sheet6["Returned"] = Sheet6.apply(lambda x: "{:,.0f}".format(x["Returned"]), axis=1)
        Sheet6["Inventory Remaining"] = Sheet6.apply(lambda x: "{:,.0f}".format(x["Inventory Remaining"]), axis=1)
        Sheet6["FEES"] = Sheet6.apply(lambda x: "{:,.0f}".format(x["FEES"]), axis=1)
        column_order1 = ['NAME', 'CLIENT', 'Year', 'Month', "# of Accts Listed", "Amt Listed", "Recovered",
                         "Unadjusted %", "Adjustments", "RECALLED", "Returned", "adjusted %", "Inventory Remaining",
                         "FEES", "AVG AGE AT LIST"]
        table5 = Sheet6.reindex(column_order1, axis=1)
        table5['monthnumber'] = table5.Month.map(d)
        table5['rank'] = table5.groupby(['NAME', 'CLIENT', 'Year'])['monthnumber'].rank(ascending=True);
        tab3 = table5.rename(columns={'adjusted %': 'Adjusted %'}, inplace=False)
        table8 = tab3.style.apply(highlight_col1, axis=None).set_properties(**{'text-align': 'right'}).set_table_styles(styles)
        # details

        data_details["NUM_ACCTS_LISTED"] = data_details.apply(lambda x: "{:,.0f}".format(x["NUM_ACCTS_LISTED"]), axis=1)
        data_details["LISTED"] = data_details.apply(lambda x: "{:,.0f}".format(x["LISTED"]), axis=1)
        data_details["NUM_ACCTS_ADJ_LIST"] = data_details.apply(lambda x: "{:,.0f}".format(x["NUM_ACCTS_ADJ_LIST"]),
                                                                axis=1)
        data_details["ADJUSTED"] = data_details.apply(lambda x: "{:,.0f}".format(x["ADJUSTED"]), axis=1)
        data_details["NUM_ACCTS_RECALLED"] = data_details.apply(lambda x: "{:,.0f}".format(x["NUM_ACCTS_RECALLED"]),
                                                                axis=1)
        data_details["RECALLED"] = data_details.apply(lambda x: "{:,.0f}".format(x["RECALLED"]), axis=1)
        data_details["NUM_ACCTS_CANCELED"] = data_details.apply(lambda x: "{:,.0f}".format(x["NUM_ACCTS_CANCELED"]),
                                                                axis=1)
        data_details["VOL_CANCELLED"] = data_details.apply(lambda x: "{:,.0f}".format(x["VOL_CANCELLED"]), axis=1)
        data_details["COLLECTED"] = data_details.apply(lambda x: "{:,.0f}".format(x["COLLECTED"]), axis=1)
        data_details["FEES"] = data_details.apply(lambda x: "{:,.0f}".format(x["FEES"]), axis=1)
        data_details["NET COLLECTIONS"] = data_details.apply(lambda x: "{:,.0f}".format(x["NET COLLECTIONS"]), axis=1)
        data_details["MTHLY COLLECTIONS"] = data_details.apply(lambda x: "{:,.0f}".format(x["MTHLY COLLECTIONS"]),
                                                               axis=1)
        data_details["AVG AGE AT LIST"] = data_details.apply(lambda x: "{:,.0f}".format(x["AVG AGE AT LIST"]), axis=1)
        data_details1 = data_details[
            ["CLIENT", "NAME", "Year", "Month", "NUM_ACCTS_LISTED", "LISTED", "NUM_ACCTS_ADJ_LIST", "ADJUSTED",
             "NUM_ACCTS_RECALLED", "RECALLED", "NUM_ACCTS_CANCELED", "VOL_CANCELLED", "COLLECTED", "FEES",
             "NET COLLECTIONS", "Correspond_Clnt", "CLASS", "MTHLY COLLECTIONS", "AVG AGE AT LIST"]]
        table6.to_excel(writer, index=False, sheet_name='MED-1 Collections')
        table7.to_excel(writer, index=False, sheet_name='CBS Early Out')
        table8.to_excel(writer, index=False, sheet_name='CBS Work Comp_Accident')
        data_details1.to_excel(writer, index=False, sheet_name='Details')
        workbook = writer.book
        worksheet1 = writer.sheets['MED-1 Collections']
        worksheet2 = writer.sheets['CBS Early Out']
        worksheet3 = writer.sheets['CBS Work Comp_Accident']
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': False,
            'valign': 'top',
            'color': '#FFFFFF',
            'fg_color': '#6B6565',
            'border': 1})
        header_format2 = workbook.add_format({
            'bold': True,
            'text_wrap': False,
            'valign': 'top',
            'color': '#000000',
            'fg_color': '#FAD2B9',
            'border': 1})
        header_format3 = workbook.add_format({'color': '#F70000'})
        worksheet1.conditional_format('I2:I1000',
                                      {'type': 'cell', 'criteria': '<', 'value': 0, 'format': header_format3})
        worksheet2.conditional_format('I2:I1000',
                                      {'type': 'cell', 'criteria': '<', 'value': 0, 'format': header_format3})
        worksheet3.conditional_format('I2:I1000',
                                      {'type': 'cell', 'criteria': '<', 'value': 0, 'format': header_format3})
        format2 = workbook.add_format({'num_format': '	#,##,##0'})
        # format3=workbook.add_format({'color': 'white'})
        # worksheet1.conditional_format('A2:A1000',{'type': 'duplicate','format': format3})
        # worksheet1.conditional_format('B2:B1000',{'type': 'duplicate','format': format3})
        # worksheet2.conditional_format('A2:A1000', {'type': 'duplicate', 'format': format3})
        # worksheet2.conditional_format('B2:B1000', {'type': 'duplicate', 'format': format3})
        # worksheet3.conditional_format('A2:A1000',{'type': 'duplicate','format': format3})
        # worksheet3.conditional_format('B2:B1000',{'type': 'duplicate','format': format3})
        worksheet1.set_column('A:A', 18, format2)
        worksheet2.set_column('A:A', 18, format2)
        worksheet3.set_column('A:A', 18, format2)
        worksheet1.set_column('D:D', 12, format2)
        worksheet2.set_column('D:D', 12, format2)
        worksheet3.set_column('D:D', 12, format2)
        worksheet3.set_column('I:I',12, format2)
        number_rows1 = len(table6.index) + 1
        number_rows2 = len(table7.index) + 1
        number_rows3 = len(table8.index) + 1
        format1 = workbook.add_format({'bg_color': '#D3D3D3','bold': True})
        worksheet1.conditional_format("$C$1:$O$%d" % (number_rows1),
                                      {"type": "formula",
                                       "criteria": '=INDIRECT("D"&ROW())="Total_201ECA"',
                                       "format": format1
                                       }
                                      )
        worksheet1.conditional_format("$C$1:$O$%d" % (number_rows1),
                                      {"type": "formula",
                                       "criteria": '=INDIRECT("D"&ROW())="Total_202ECA"',
                                       "format": format1
                                       }
                                      )
        worksheet1.conditional_format("$C$1:$O$%d" % (number_rows1),
                                      {"type": "formula",
                                       "criteria": '=INDIRECT("D"&ROW())="Grand Total"',
                                       "format": format1
                                       }
                                      )
        worksheet2.conditional_format("$C$1:$O$%d" % (number_rows2),
                                      {"type": "formula",
                                       "criteria": '=INDIRECT("D"&ROW())="Total_201AWP"',
                                       "format": format1
                                       }
                                      )
        worksheet2.conditional_format("$C$1:$O$%d" % (number_rows2),
                                      {"type": "formula",
                                       "criteria": '=INDIRECT("D"&ROW())="Total_202AWP"',
                                       "format": format1
                                       }
                                      )
        worksheet2.conditional_format("$C$1:$O$%d" % (number_rows1),
                                      {"type": "formula",
                                       "criteria": '=INDIRECT("D"&ROW())="Grand Total"',
                                       "format": format1
                                       }
                                      )

        worksheet3.conditional_format("$C$1:$O$%d" % (number_rows3),
                                      {"type": "formula",
                                       "criteria": '=INDIRECT("D"&ROW())="Total_201ERP"',
                                       "format": format1
                                       }
                                      )
        worksheet3.conditional_format("$C$1:$O$%d" % (number_rows3),
                                      {"type": "formula",
                                       "criteria": '=INDIRECT("D"&ROW())="Total_201WCP"',
                                       "format": format1
                                       }
                                      )
        worksheet3.conditional_format("$C$1:$O$%d" % (number_rows3),
                                      {"type": "formula",
                                       "criteria": '=INDIRECT("D"&ROW())="Total_202ERP"',
                                       "format": format1
                                       }
                                      )
        worksheet3.conditional_format("$C$1:$O$%d" % (number_rows3),
                                      {"type": "formula",
                                       "criteria": '=INDIRECT("D"&ROW())="Total_202WCP"',
                                       "format": format1
                                       }
                                      )
        worksheet3.conditional_format("$C$1:$O$%d" % (number_rows1),
                                      {"type": "formula",
                                       "criteria": '=INDIRECT("D"&ROW())="Grand Total"',
                                       "format": format1
                                       }
                                      )
        white_format=workbook.add_format({'bg_color': '#FFFFFF','color': '#FFFFFF'})
        for col_num, value in enumerate(table6.columns.values):
            worksheet1.write(0, col_num , value, header_format)
            if ((value == 'Unadjusted %') | (value == 'Adjusted %')):
                worksheet1.write(0, col_num , value, header_format2)
            elif((value == 'monthnumber')|(value == 'rank')):
                worksheet1.write(0, col_num, value, white_format)
        for col_num, value in enumerate(table7.columns.values):
            worksheet2.write(0, col_num , value, header_format)
            if ((value == 'Unadjusted %') | (value == 'Adjusted %')):
                worksheet2.write(0, col_num , value, header_format2)
            elif ((value == 'monthnumber') | (value == 'rank')):
                worksheet2.write(0, col_num, value, white_format)
        for col_num, value in enumerate(table8.columns.values):
            worksheet3.write(0, col_num , value, header_format)
            if ((value == 'Unadjusted %') | (value == 'Adjusted %')):
                worksheet3.write(0, col_num , value, header_format2)
            elif ((value == 'monthnumber') | (value == 'rank')):
                worksheet3.write(0, col_num, value, white_format)
        format1 = workbook.add_format({'font_color': '#000000'})
        worksheet1.conditional_format("B2:B100",
                                      {'type': 'formula', 'criteria': '(COUNTIF($B$2:B2,B2)=1)', 'format': format1})
        worksheet2.conditional_format("B2:B100",
                                      {'type': 'formula', 'criteria': '(COUNTIF($B$2:B2,B2)=1)', 'format': format1})
        worksheet3.conditional_format("B2:B100",
                                      {'type': 'formula', 'criteria': '(COUNTIF($B$2:B2,B2)=1)', 'format': format1})
        # worksheet1.set_column('P:P', None, None, {'hidden': True,'level':True,})
        worksheet1.set_column('P:P', None, None, {'hidden': True,'level':True,'collapsed':True})
        worksheet1.set_column('Q:Q', None, None, {'hidden': True,'level':True,'collapsed':True})
        worksheet2.set_column('P:P', None, None, {'hidden': True})
        worksheet2.set_column('Q:Q', None, None, {'hidden': True})
        worksheet3.set_column('P:P', None, None, {'hidden': True})
        worksheet3.set_column('Q:Q', None, None, {'hidden': True})

    except Exception as e:
        logging.exception("error")


if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/Riverview Collections Report Feb 2021.xlsx', engine='xlsxwriter', )
    xls = pd.ExcelFile('/home/ajay/Downloads/Jessica Sims Sample Report_Riverview Collections Report FEB 2021 (1).xlsx')
    df_facs1 = pd.read_excel(xls, 'Details')
    Riverview(df_facs1, writer)
    writer.save()
