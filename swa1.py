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
        df.to_excel(writer, index=True, sheet_name='MED-1 Collections')
        df.to_excel(writer, index=True, sheet_name='CBS Early Out')
        df.to_excel(writer, index=True, sheet_name='CBS Work Comp_Accident')


    except Exception as e:
        logging.exception("error")


if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/Riverview Collections Report Feb 2021.xlsx', engine='xlsxwriter',
                            options={'strings_to_numbers': True})
    xls = pd.ExcelFile('/home/ajay/Downloads/Jessica Sims Sample Report_Riverview Collections Report FEB 2021 (1).xlsx')
    df_facs1 = pd.read_excel(xls, 'Details')
    Riverview(df_facs1, writer)
    workbook = writer.book
    worksheet1 = writer.sheets['MED-1 Collections']
    worksheet2 = writer.sheets['CBS Early Out']
    worksheet3 = writer.sheets['CBS Work Comp_Accident']
    # Add a header format.
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'align':'side',
        'fg_color': '#D7E4BC',
        'border': 1})

    # Write the column headers with the defined format.
    for col_num, value in enumerate(df_facs1.columns.values):
        worksheet1.write(0, col_num + 1, value, header_format)
        worksheet2.write(0, col_num + 1, value, header_format)
        worksheet3.write(0, col_num + 1, value, header_format)


    writer.save()
