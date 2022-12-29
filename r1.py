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
        # for Med1 collections

        med1_df = df.loc[
            (df['CLIENT'].isin(['201ECA', '202ECA'])), Column1]
        med1_df.round(1)
        med1_df.columns = Column2
        med1_df["Inventory Remaining"] = med1_df["Inventory Remaining"]
        med1_pivot = pd.pivot_table(med1_df, index=index1)
        med1_pivot.reset_index(inplace=True)
        data=med1_pivot[Column3].groupby(["NAME", "CLIENT"], as_index = False)
        d11 = data.sum().stb.subtotal()
        d11["Unadjusted %"]=((d11["Recovered"]/d11["Amt Listed"])*100)
        d11["adjusted %"] = ((d11["Recovered"] / (d11["Amt Listed"]+d11["Adjustments"]-d11["RECALLED"]-d11["Returned"])) * 100)
        da1 =d11["Unadjusted %"]
        da2=d11["adjusted %"]
        da3 = pd.concat([da1, da2],axis=1)
        d1=pd.merge(d11,da3)
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
        data2=Sheet1[Column5].groupby(["NAME", "CLIENT", "Year"], as_index=False)
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
        df2 = dff[dff.columns.difference(sub2)]
        df2.columns = Column6
        Sheet2 = pd.concat([Sheet1, df2])
        Sheet2['Month'] = Sheet2['Month'].astype(cat_month)
        Sheet2.set_index(index1, inplace=True)
        Sheet2 = Sheet2.sort_values(index1)
        column_order1 = Column7
        Sheet2 = Sheet2[Column7].apply(lambda x: round(x, 2))
        Sheet2["AVG AGE AT LIST"] = Sheet2["AVG AGE AT LIST"].apply(lambda x: round(x, 0))
        Sheet2["adjusted %"] = Sheet2["adjusted %"].apply(lambda x: round(x, decimals))
        Sheet2["Unadjusted %"] = Sheet2["Unadjusted %"].apply(lambda x: round(x, decimals))
        Sheet2["adjusted %"] = Sheet2["adjusted %"].fillna(0)
        Sheet2["Unadjusted %"] = Sheet2["Unadjusted %"].apply(str) + "%"
        Sheet2["adjusted %"] = Sheet2["adjusted %"].apply(str) + "%"
        Sheet2["Amt Listed"]=Sheet2.apply(lambda x: "{:,.0f}".format(x["Amt Listed"]), axis=1)
        Sheet2["Recovered"] = Sheet2.apply(lambda x: "{:,.0f}".format(x["Recovered"]), axis=1)
        Sheet2["Adjustments"] = Sheet2.apply(lambda x: "{:,.0f}".format(x["Adjustments"]), axis=1)
        Sheet2["RECALLED"] = Sheet2.apply(lambda x: "{:,.0f}".format(x["RECALLED"]), axis=1)
        Sheet2["Returned"] = Sheet2.apply(lambda x: "{:,.0f}".format(x["Returned"]), axis=1)
        Sheet2["Inventory Remaining"] = Sheet2.apply(lambda x: "{:,.0f}".format(x["Inventory Remaining"]), axis=1)
        Sheet2["FEES"] = Sheet2.apply(lambda x: "{:,.0f}".format(x["FEES"]), axis=1)
        table3 = Sheet2.reindex(column_order1, axis=1)
        table3.reset_index(inplace=True)
        table3['Month'] = np.where(table3['Month'].isna(), "Total_" + table3['Year'].astype('str'), table3['Month']);
        table3['Month'] = np.where((table3['Year'].isna()), "Total_" + table3['CLIENT'], table3['Month'])
        table3['Month'] = table3['Month'].astype(str).str.split('.', expand=True)[0]
        shape = list(table3.shape)
        table3.at[shape[0] - 1, "Month"] = "Grand Total"
        table3.set_index(index1, inplace=True)
        table3.to_excel(writer, index=True, sheet_name='MED-12 Collections')

    except Exception as e:
        logging.exception("error")




if __name__ == "__main__":
    pd.options.display.float_format = '{:,.2f}'.format
    writer = pd.ExcelWriter('/home/ajay/PGDs_Riverview12.xlsx', engine='openpyxl')
    xls = pd.ExcelFile('/home/ajay/Downloads/Riverview.xlsx', engine='openpyxl')
    df_facs1 = pd.read_excel(xls, 'Details')
    Riverview(df_facs1,writer)
    writer.save()
