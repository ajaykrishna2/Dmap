import openpyxl
import pandas as pd
import numpy as np
import openpyxl
import xlsxwriter

np.random.seed(100)
df =  pd.DataFrame(np.random.randn(5, 3), columns=list('ABC'))

# def highlight_col(x):
#     r = 'background-color: red'
#     df1 = pd.DataFrame('', index=x.index, columns=x.columns)
#     df1.iloc[:, 0] = r
#     return df1
# df.style.apply(highlight_col, axis=0)
# df.style.set_properties(**{'background-color': 'red'}, subset=['A'])
print(df)
def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val < 0 else 'black'
    return 'color: %s' % color
df.style.applymap(color_negative_red,axis=0)

path = '/home/ajay/co.xlsx'
with pd.ExcelWriter(path,engine="openpyxl",mode='a') as writer:
    writer.book = openpyxl.load_workbook(path)
    df.to_excel(writer, sheet_name='In Epic not in Facs', index=False)