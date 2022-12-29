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
import locale
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import HTML
import matplotlib.colors as col



def Riverview(writer):
    try:
        df = df.reset_index()

        def color(x):
            c1 = 'background-color: yellow'
            c2 = 'background-color: orange'
            c3 = 'background-color: green'
            c4 = 'background-color: blue'
            c = ''
            # compare columns
            mask1 = x['NAME'] == 'RIVERVIEW HEALTH'
            mask2 = x['CLIENT'].isin(['201ECA','202ECA'])
            mask3 = x['Month'].isin(['Total_201ECA','Total_202ECA'])
            # both = mask1 | mask2
            # DataFrame with same index and columns names as original filled empty strings
            df1 = pd.DataFrame(c, index=x.index, columns=x.columns)
            # modify values of df1 column by boolean mask
            df1.loc[~, 'price'] = c1
            df1.loc[~both, 'GrandTot'] = c2
            df1.loc[mask1, :] = c3
            df1.loc[mask2, :] = c4
            return df1

        df.style.apply(color, axis=None)
        df2.to_excel(writer, index=True, sheet_name='MED-12 Collections')
    except Exception as e:
        logging.exception("error")


if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/samp.xlsx', engine='xlsxwriter',
                            options={'strings_to_numbers': True})
    # xls = pd.ExcelFile('/home/ajay/Riverview Collections Report Feb 2021.xlsx')
    # df_facs1 = pd.read_excel(xls, 'MED-1 Collections')
    Riverview(writer)
    writer.save()
