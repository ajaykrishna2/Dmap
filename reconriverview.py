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
def Riverview(df,writer):
    try:
        pd.set_option('display.float_format', lambda x: '%.0f' % x)
        date_sr = pd.to_datetime(pd.Series(df['List Date']))
        df['List Date'] = date_sr.dt.strftime('%d-%m-%Y')
        date_sr1 = pd.to_datetime(pd.Series(df['Last Payment Date']))
        df['Last Payment Date'] = date_sr1.dt.strftime('%d-%m-%Y')
        date_sr1 = pd.to_datetime(pd.Series(df['Cancel Date']))
        df['Cancel Date'] = date_sr1.dt.strftime('%d-%m-%Y')
        df["Last Payment Date.1"]=df["Cancel Description"]
        df.drop(labels=["Cancel Description"], axis="columns", inplace=True)
        df= df.rename(columns = {'Last Payment Date.1':'Cancel Description'},inplace=False)
        print(df.style.format({"List Date": lambda t: t.strftime("%d-%m-%Y")}))
        print(df.to_string())
        df1 = df[df.duplicated(['EPIC #'],keep=False)].sort_values('EPIC #')
        df2 = df[df.duplicated(['EPIC #'])].sort_values('EPIC #')
        df3 =df1.merge(df2,indicator = True, how='left').loc[lambda x : x['_merge']!='both']
        df4= df.merge(df1,indicator = True, how='left').loc[lambda x : x['_merge']!='both']
        df2["Recon file (EPIC) balance"]=df2["Recon file (EPIC) balance"]
        df4.drop('_merge',axis=1,inplace=True)
        print(df4.to_string())
        print(len(df4))
        df2 = df2.reset_index(drop = True)
        df3 = df3.reset_index(drop=True)
        print(df2.to_string())
        df2["Recon file (EPIC) balance"]=df3["Recon file (EPIC) balance"]
        df2['Match?'] = np.where(df2['Med-1 Balance'] == df2['Recon file (EPIC) balance'], 'True','False')
        # create new column in df1 to check if prices match
        df2['Issue Detected'] = df2['Match?'].apply(lambda x: 'Balance Match' if x == 'True' else 'Balance Mismatch')
        df2.drop('Match?', axis=1, inplace=True)
        print(df4.to_string())
        df2['EPIC #']=df2['EPIC #'].apply(str)
        df4['EPIC #'] = df4['EPIC #'].apply(str)
        df5=df4[df4['Issue Detected']=="Account is closed in FACS, but open in RV File."]
        df6=df4[df4['Issue Detected']=="Account is in FACS, but not in River View File."]
        df7=df4[df4['Issue Detected']=="Account is in RV File, but it is not in FACS."]
        df8=df4[(df4['Issue Detected']=="The balance in FACS is greater than the balance in RV File.")]
        df9=df4[(df4['Issue Detected']=="The balance in RV File is greater than the balance in FACS.")]
        df10 = pd.concat([df8, df9])
        df11=df2[df2['Issue Detected']=="Balance Mismatch"]
        df12 = pd.concat([df10, df11])
        df13=df4[df4['Issue Detected'] == "The balances in FACS and RV File are same."]
        df14 = df2[df2['Issue Detected'] == "Balance Match"]
        df15 = pd.concat([df13, df14])
        df5.to_excel(writer, index=False, sheet_name='Closed in FACS')
        df6.to_excel(writer, index=False, sheet_name='FACS not RECON')
        df7.to_excel(writer, index=False, sheet_name='RECON not FACS')
        df12.to_excel(writer, index=False, sheet_name='Balance Mismatch')
        df15.to_excel(writer, index=False, sheet_name='Balance Match')
        workbook = writer.book
        worksheet1 = writer.sheets['Closed in FACS']
        worksheet2 = writer.sheets['FACS not RECON']
        worksheet3 = writer.sheets['RECON not FACS']
        worksheet4 = writer.sheets['Balance Mismatch']
        worksheet5 = writer.sheets['Balance Match']


        # Add some cell formats.
        format1 = workbook.add_format({'num_format': '#################################0'})
        worksheet1.set_column('C:C', 18, format1)
        worksheet2.set_column('C:C', 18, format1)
        worksheet3.set_column('C:C', 18, format1)
        worksheet4.set_column('C:C', 18, format1)
        worksheet5.set_column('C:C', 18, format1)
        print(df13.to_string())
        print(len(df13))




        # df2.loc["Recon file (EPIC) balance"]=df[df["Recon file (EPIC) balance"]>0]["Recon file (EPIC) balance"].copy()
        # df2["Recon file (EPIC) balance"]=df3["Recon file (EPIC) balance"].copy()
        # # df2["Recon file (EPIC) balance"]=df2["Recon file (EPIC) balance"].fillna(df3["Recon file (EPIC) balance"])
        # df2.loc[df2["Recon file (EPIC) balance"].isnull(), "Recon file (EPIC) balance"] = df3["Recon file (EPIC) balance"]
    except Exception as e:
        logging.exception("error")




if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/RVH_Inven_RECON_062921_34626.xlsx', engine='xlsxwriter',options={'strings_to_numbers':True} )
    df_facs1 = pd.read_csv("/home/ajay/Downloads/RVH_Inven_RECON_062921_34626.TXT",delimiter="\t")
    Riverview(df_facs1,writer)
    writer.save()