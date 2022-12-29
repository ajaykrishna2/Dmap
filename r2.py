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
        print(df['Inventory Remaining'])
        index1=["NAME", "CLIENT", "Year", "Month"]
        Column1=["NAME", "CLIENT", "Year", "Month", "NUM_ACCTS_LISTED", "LISTED","COLLECTED", "ADJUSTED", "RECALLED", "VOL_CANCELLED", "FEES","AVG AGE AT LIST", "Inventory Remaining", "Unadjusted %", "adjusted %"]
        Column2=["NAME", "CLIENT", "Year", "Month", "# of Accts Listed", "Amt Listed", "Recovered","Adjustments", "RECALLED", "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining","Unadjusted %", "adjusted %"]
        Column3=["NAME", "CLIENT", "Month", "# of Accts Listed", "Amt Listed", "Recovered", "Adjustments", "RECALLED","Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining"]
        Column4=["# of Accts Listed", "AVG AGE AT LIST", "Adjustments", "Amt Listed", "CLIENT", "FEES", "Inventory Remaining", "NAME", "RECALLED", "Recovered", "Returned", "Unadjusted %", "adjusted %"]
        Column5=["NAME", "CLIENT", "Year", "Month", "# of Accts Listed", "Amt Listed", "Recovered", "Adjustments", "RECALLED", "Returned", "FEES", "AVG AGE AT LIST", "Inventory Remaining"]
        sub = ["AVG AGE AT LIST_x",  "# of Accts Listed_y", "Amt Listed_y","Recovered_y", "Adjustments_y","RECALLED_y", "Returned_y", "FEES_y", "Inventory Remaining_y"]
        sub2 =  ["AVG AGE AT LIST_x",  "NAME_y", "# of Accts Listed_y", "Amt Listed_y", "Recovered_y", "Adjustments_y", "RECALLED_y", "Returned_y", "FEES_y", "Inventory Remaining_y"]
        Column6=["# of Accts Listed", "AVG AGE AT LIST", "Adjustments", "Amt Listed", "CLIENT", "FEES","Inventory Remaining", "NAME", "RECALLED", "Recovered", "Returned", "Unadjusted %", "Year", "adjusted %"]
        Column7=["# of Accts Listed", "Amt Listed", "Recovered", "Unadjusted %", "Adjustments", "RECALLED","Returned", "adjusted %", "Inventory Remaining", "FEES", "AVG AGE AT LIST"]
        column_order = ["# of Accts Listed", "Amt Listed", "Recovered", "Unadjusted %", "Adjustments", "RECALLED",
                        "Returned", "adjusted %", "Inventory Remaining", "FEES", "AVG AGE AT LIST" ]
        cat_month = CategoricalDtype(
            ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC'], ordered=True)
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
        Sheet4 = pd.concat([Sheet3, df4])
        Sheet4['Month'] = Sheet4['Month'].astype(cat_month)
        Sheet4.set_index(index1, inplace=True)
        Sheet4 = Sheet4.sort_values(index1)
        column_order1 = Column7
        Sheet4 = Sheet4[Column7].apply(lambda x: round(x, 2))
        Sheet4["AVG AGE AT LIST"] = Sheet4["AVG AGE AT LIST"].apply(lambda x: round(x, 0))
        Sheet4["adjusted %"] = Sheet4["adjusted %"].apply(lambda x: round(x, decimals))
        Sheet4["Unadjusted %"] = Sheet4["Unadjusted %"].apply(lambda x: round(x, decimals))
        Sheet4["adjusted %"] = Sheet4["adjusted %"].fillna(0)
        Sheet4["Unadjusted %"] = Sheet4["Unadjusted %"].apply(str) + "%"
        Sheet4["adjusted %"] = Sheet4["adjusted %"].apply(str) + "%"
        Sheet4["Amt Listed"] = Sheet4.apply(lambda x: "{:,.0f}".format(x["Amt Listed"]), axis=1)
        Sheet4["Recovered"] = Sheet4.apply(lambda x: "{:,.0f}".format(x["Recovered"]), axis=1)
        Sheet4["Adjustments"] = Sheet4.apply(lambda x: "{:,.0f}".format(x["Adjustments"]), axis=1)
        Sheet4["RECALLED"] = Sheet4.apply(lambda x: "{:,.0f}".format(x["RECALLED"]), axis=1)
        Sheet4["Returned"] = Sheet4.apply(lambda x: "{:,.0f}".format(x["Returned"]), axis=1)
        Sheet4["Inventory Remaining"] = Sheet4.apply(lambda x: "{:,.0f}".format(x["Inventory Remaining"]), axis=1)
        Sheet4["FEES"] = Sheet4.apply(lambda x: "{:,.0f}".format(x["FEES"]), axis=1)
        table4 = Sheet4.reindex(column_order1, axis=1)
        table4.reset_index(inplace=True)
        table4['Month'] = np.where(table4['Month'].isna(), "Total_" + table4['Year'].astype('str'), table4['Month']);
        table4['Month'] = np.where((table4['Year'].isna()), "Total_" + table4['CLIENT'], table4['Month'])
        table4['Month'] = table4['Month'].astype(str).str.split('.', expand=True)[0]
        shape = list(table4.shape)
        table4.at[shape[0] - 1, "Month"] = "Grand Total"
        table4.set_index(index1, inplace=True)

        table4.to_excel(writer, index=True, sheet_name='CBS Early Out')

    except Exception as e:
        logging.exception("error")




if __name__ == "__main__":
    pd.options.display.float_format = '{:,.2f}'.format
    writer = pd.ExcelWriter('/home/ajay/PGDs_Riverview12.xlsx', engine='openpyxl')
    xls = pd.ExcelFile('/home/ajay/Downloads/Riverview.xlsx', engine='openpyxl')
    df_facs1 = pd.read_excel(xls, 'Details')
    Riverview(df_facs1,writer)
    writer.save()
