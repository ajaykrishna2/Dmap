import numpy as np
import openpyxl
import pandas as pd
xls = pd.ExcelFile('/home/ajay/Downloads/Riverview.xlsx',engine='openpyxl')
facs = pd.read_excel(xls, 'Details')
df = facs[(facs.CLIENT == '201ECA') & (
            (facs.Year == 2016) | (facs.Year == 2017) | (facs.Year == 2018) | (facs.Year == 2019) | (
                facs.Year == 2020) | (facs.Year == 2021))]

df2 = facs[(facs.CLIENT == '202ECA') & (
            (facs.Year == 2016) | (facs.Year == 2017) | (facs.Year == 2018) | (facs.Year == 2019) | (
                facs.Year == 2020) | (facs.Year == 2021))]

df1 = df.append(df2)
print(df1)
df1['Unadjusted %'] = ((df1['COLLECTED'] / df1['LISTED']) * 100)
df1['adjusted %'] = (
            ((df1['COLLECTED']) / (df1['LISTED'] + df1['ADJUSTED'] - df1['RECALLED'] - df1['VOL_CANCELLED'])) * 100)
df1['Inventory Remaining'] = (
            (df1['LISTED']) - (df1['COLLECTED']) + (df1['ADJUSTED']) + (df1['RECALLED']) + (df1['VOL_CANCELLED']))
df3 = df1[['CLIENT', 'NAME', 'Year', 'Month', 'NUM_ACCTS_LISTED', 'LISTED', 'NUM_ACCTS_ADJ_LIST', 'ADJUSTED',
           'NUM_ACCTS_RECALLED', 'RECALLED', 'NUM_ACCTS_CANCELED', 'VOL_CANCELLED', 'COLLECTED', 'FEES',
           'NET COLLECTIONS', 'Correspond_Clnt', 'CLASS', 'MTHLY COLLECTIONS', 'AVG AGE AT LIST', 'Unadjusted %',
           'adjusted %', 'Inventory Remaining']]
df3.columns=['CLIENT','NAME','Year','Month','# of Accts Listed','Amt Listed','NUM_ACCTS_ADJ_LIST','Adjustments','NUM_ACCTS_RECALLED','Returned','NUM_ACCTS_CANCELED','RECALLED','Recovered','FEES','NET COLLECTIONS','Correspond_Clnt','CLASS','MTHLY COLLECTIONS','AVG AGE AT LIST','Unadjusted %','adjusted %','Inventory Remaining']
out = df3.pivot_table(
    index=['NAME','CLIENT','Year','Month'],
    values=['# of Accts Listed','Amt Listed','Recovered','Adjustments','RECALLED','Returned','FEES','AVG AGE AT LIST','Unadjusted %','adjusted %','Inventory Remaining'] )


# out.loc['Total']=out[['# of Accts Listed','Amt Listed','Recovered','Adjustments','RECALLED','Returned','FEES','AVG AGE AT LIST','Unadjusted %','adjusted %','Inventory Remaining']].sum()
# out.loc['Total']=out.loc['Total'].fillna('')
# container = []
# for label,_df  in out.groupby(['CLIENT','Year']):
#     _df.loc[f'{label[0]} {label[1]} {label[2]} {label[3]} {label[4]} {label[5]} {label[6]} {label[7]} {label[8]} {label[9]} {label[10]}Subtotal']=_df[['# of Accts Listed','Amt Listed','Recovered','Adjustments','RECALLED','Returned','FEES','AVG AGE AT LIST','Unadjusted %','adjusted %','Inventory Remaining']].sum()
#     container.append(_df)
#
# df_summary=pd.concat(container)
# df_summary.loc['Total']=out[['# of Accts Listed','Amt Listed','Recovered','Adjustments','RECALLED','Returned','FEES','AVG AGE AT LIST','Unadjusted %','adjusted %','Inventory Remaining']].sum()
# tab_tots = out.groupby(level='NAME').sum()
# tab_tots.index = [tab_tots.index, ['Total'] * len(tab_tots)]
# print(tab_tots)
# pd.concat(
#     [out, tab_tots]
# ).sort_index().append(
#     out.sum().rename(('Grand', 'Total'))
# )
tablesum1 = out.groupby(level=['NAME']).sum()
print(tablesum1)
table1 = tablesum1.pivot_table(
    index=['NAME'],
    values=['# of Accts Listed','Amt Listed','Recovered','Adjustments','RECALLED','Returned','FEES','AVG AGE AT LIST','Unadjusted %','adjusted %','Inventory Remaining'] )
tablesum2 = out.groupby(level=['CLIENT','Year']).sum()
table2 = tablesum2.pivot_table(
    index=['CLIENT','Year'],
    values=['# of Accts Listed','Amt Listed','Recovered','Adjustments','RECALLED','Returned','FEES','AVG AGE AT LIST','Unadjusted %','adjusted %','Inventory Remaining'] )

# tablesum3 = out.groupby(level=['Year']).sum()
# table3 = tablesum3.pivot_table(
#     index=['Year'],
#     values=['# of Accts Listed','Amt Listed','Recovered','Adjustments','RECALLED','Returned','FEES','AVG AGE AT LIST','Unadjusted %','adjusted %','Inventory Remaining'] )


# print(tablesum3)
# tablesum4=pd.concat(table2,table3).sort_index(level=0)
# tablesum=pd.concat(table1,tablesum4)
# print(tablesum)


dff = pd.concat([out, table1,table2])
dff.pivot_table(
    index=['NAME','CLIENT', 'Year','Month'],
    values=['# of Accts Listed', 'Amt Listed', 'Recovered', 'Adjustments', 'RECALLED', 'Returned', 'FEES','AVG AGE AT LIST', 'Unadjusted %', 'adjusted %', 'Inventory Remaining'])
path = '/home/ajay/C.xlsx'
with pd.ExcelWriter(path,engine="openpyxl",mode='a') as writer:
    writer.book = openpyxl.load_workbook(path)
    dff.to_excel(writer,index=True, sheet_name='MED-1')