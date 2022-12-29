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



styles = [
    dict(selector="th", props=[("font-size", "150%"),
                               ("text-align", "center"),
                               ("color", "#0a0808"),
                               ('background-color', "#8a1212")])
]

def color_filler(series):
    is_greater_than_3=[1 if x > 3 else 0 for x in series]
    return ['background-color: yellow; color:red' if v else 'background-color :black;color: yellow' \
            for v in is_greater_than_3]


def highlight_col(x):
    r = 'background-color: red'
    df1 = pd.DataFrame('', index=x.index, columns=x.columns)
    df1.iloc[:, 8] = r
    return df1



def Riverview(df,writer):
    try:
        def highlight_col(x):
            r = 'background-color: pink'
            e = 'background-color: light grey'
            y= 'color:red'

            df1 = pd.DataFrame('', index=x.index, columns=x.columns)
            df1['NAME'] = e
            df1['CLIENT'] = e
            # df1.iloc[:, 0] = e
            # df1.iloc[:, 1] = e

            df1.iloc[:,7 ] = y
            df1.iloc[:,8] = r
            df1.iloc[:,9] = r
            return df1

        def color_negative_red(val):
            """
            Takes a scalar and returns a string with
            the css property `'color: red'` for negative
            strings, black otherwise.
            """
            color = 'red' if val < 0 else 'black'
            return 'color: %s' % color

        th_props = [
            ('font-size', '11px'),
            ('text-align', 'center'),
            ('font-weight', 'bold'),
            ('color', '#666666'),
            ('background-color', '#8a1212')
        ]
        td_props = [
            ('font-size', '11px')
        ]

        def formatter(x):
            return str(x) if x >= 0 else f'({abs(x)})'

        for col in df.columns[4:4]:
            df[col] = df[col].apply(formatter)
        # df["ADJUSTED"]=(abs(df["ADJUSTED"]))
        # df["ADJUSTED"] = '('+df["ADJUSTED"].astype(str)+')'
        # df.style.applymap(color_negative_red, subset=['ADJUSTED'])
        print(df.style)
        # html = (df.style.set_table_styles(styles)
        #         .set_caption("Hover to highlight."))
        # html = html.set_table_styles({
        #     '': [dict(selector='', props=[('color', 'green')])],
        #     'C': [dict(selector='td', props=[('color', 'red')])],
        # }, overwrite=False)
        # html
        styles = [
            #     hover(),
            dict(selector="th", props=[("font-size", "150%"),
                                       ("text-align", "center"),
                                       ("background-color", "#6d6d6d")])
        ]
        html = df.style.set_table_styles(styles)

        s = html.apply(highlight_col,axis=None)
        # html = (df.style.set_table_styles(styles)
        #         .set_caption("Hover to highlight."))

        # v=df.style.set_properties(**{'color': 'red'}, subset=['ADJUSTED']).apply(color_negative_red,axis=None)
        # r=v.style.set_properties(**{'background-color': 'pink'}, subset=['RECALLED'])
        # df.style.format({"ADJUSTED": "${:20,.0f}"}) \
        #     .highlight_max(color='lightgreen') \
        #     .highlight_min(color='#cd4f39')
        s.to_excel(writer, index=False, sheet_name='MED-12 Collections')
    except Exception as e:
        logging.exception("error")


if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/samp.xlsx', engine='xlsxwriter',
                            options={'strings_to_numbers': True})
    xls = pd.ExcelFile('/home/ajay/Riverview Collections Report Feb 2021.xlsx')
    df_facs1 = pd.read_excel(xls, 'MED-1 Collections')
    Riverview(df_facs1, writer)
    writer.save()
