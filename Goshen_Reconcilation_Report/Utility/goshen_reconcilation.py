import logging
import numpy as np
import pandas as pd
from Utility.save_file import*
from pandas import DatetimeIndex
from datetime import date
class goshen_reconcilation_report:
    def Goshen(self,df):
        try:
            save_file = save_statement_to_output_folder()
            date_sr = pd.to_datetime(pd.Series(df['List Date']))
            df['List Date'] = date_sr.dt.strftime('%m-%d-%Y')
            df1 = df[df.duplicated(['Goshen #'], keep=False)].sort_values('Goshen #')
            df2 = df[df.duplicated(['Goshen #'])].sort_values('Goshen #')
            rdf = df1.merge(df2, indicator=True, how='left')
            rdf1 = rdf[rdf['_merge'] == 'left_only']
            rdf1.drop('_merge', axis=1, inplace=True)
            df4 = df.merge(df1, indicator=True, how='left')
            df4.drop('_merge', axis=1, inplace=True)
            df4['Goshen #'] = df4['Goshen #'].apply(str)
            df10 = df4[df4['Issue Detected'] == "Account is in Goshen File, but it is not in FACS."]
            df3 = df4[df4['Goshen #'].str.contains("-", regex=True)]
            index_names = df4[df4['Goshen #'].str.contains("-", regex=True)].index
            df4.drop(index_names, inplace=True)
            df4['Year'] = DatetimeIndex(df4['List Date']).year
            index_name = df4[df4['Year'] < 2018].index
            df4.drop(index_name, inplace=True)
            df4.drop('Year', axis=1, inplace=True)
            df3= df3[
                ["Issue Detected", "FACS #", "Goshen #", "Client ID", "First Name", "Last Name", "Disposition", "Phase",
                 "List Date", "FACS Balance", "Recon file (Goshen) Balance", "Amount Cancelled", "Cancel Date",
                 "Cancel Code", "Cancel Code Desc", "Last Payment Date", "Goshen Status"]]
            df4 = df4[
                ["Issue Detected", "FACS #", "Goshen #", "Client ID", "First Name", "Last Name", "Disposition", "Phase",
                 "List Date", "FACS Balance", "Recon file (Goshen) Balance", "Amount Cancelled", "Cancel Date",
                 "Cancel Code", "Cancel Code Desc", "Last Payment Date", "Goshen Status"]]       
            df['Date'] = pd.datetime.now().date()
            inf6_dt = pd.to_datetime(pd.Series(df['Date']))
            df['Date'] = inf6_dt.dt.strftime('%m-%d-%Y')
            df['year1'] = pd.DatetimeIndex(df['Date']).year
            df['month1'] = pd.DatetimeIndex(df['Date']).month
            df['day1'] = pd.DatetimeIndex(df['Date']).day
            df['year2'] = pd.DatetimeIndex(df['List Date']).year
            df['month2'] = pd.DatetimeIndex(df['List Date']).month
            df['day2'] = pd.DatetimeIndex(df['List Date']).day
            df['day1']=df['day1'].sub(1)
            index_name = df4[
                (df['year2'] >= df['year1']) & (df['month2'] >= df['month1']) & (df['day2'] > df['day1'])].index
            df.drop(index_name, inplace=True)
            df.drop('year1', axis=1, inplace=True)
            df.drop('year2', axis=1, inplace=True)
            df.drop('month1', axis=1, inplace=True)
            df.drop('month2', axis=1, inplace=True)
            df.drop('day1', axis=1, inplace=True)
            df.drop('day2', axis=1, inplace=True)
            df.drop('Date', axis=1, inplace=True)
            index_name1 = df4[(df4['FACS Balance'] == 0)&(df4['Recon file (Goshen) Balance'] == 0)].index
            df4.drop(index_name1, inplace=True)
            df5 = df4[df4['Issue Detected'] == "Account is closed in FACS, but open at Goshen."]
            df7 = df4[df4['Issue Detected'] == "Account is in FACS, but not in Goshen File."]
            df81 = df4[(df4['Issue Detected'] == "The balance in FACS is greater than the balance at Goshen.")]
            df82 = df4[(df4['Issue Detected'] == "The balance at Goshen is greater than the balance in FACS.")]
            df8 = pd.concat([df81, df82])
            df9 = df4[(df4['Issue Detected'] == "Balance Match")]
            fdf = df7[(df7['Disposition'] == '9000') | (df7['Disposition'] == '9999')]
            fdf["Issue Detected"].replace({"Account is in FACS, but not in Goshen File.": "Account is closed in FACS, but open at Goshen."},inplace=True)
            index_names0 = df7[(df7['Disposition'] == '9000') | (df7['Disposition'] == '9999')].index
            df7.drop(index_names0, inplace=True)
            df6 = pd.concat([df5, rdf1, fdf])
            index_names1 = df6[df6['Cancel Code'] == 11].index
            df6.drop(index_names1, inplace=True)
            df6.loc[((df6['Disposition'] != '9000') & (df6['Disposition'] != '9999')), 'Cancel Code'] = ''
            df6.loc[((df6['Disposition'] != '9000') & (df6['Disposition'] != '9999')), 'Cancel Code Desc'] = ''
            index_names2 = df7[df7['Cancel Code'] == 11].index
            df7.drop(index_names2, inplace=True)
            df7.loc[((df7['Disposition'] != '9000') & (df7['Disposition'] != '9999')), 'Cancel Code'] = ''
            df7.loc[((df7['Disposition'] != '9000') & (df7['Disposition'] != '9999')), 'Cancel Code Desc'] = ''
            index_names3 = df3[df3['Cancel Code'] == 11].index
            df3.drop(index_names3, inplace=True)
            index_names4 = df8[df8['Cancel Code'] == 11].index
            df8.drop(index_names4, inplace=True)
            df10 = df8[(df8['Disposition'] == '9000')|(df8['Disposition'] == '9999')]
            df10["Issue Detected"].replace({ "Balance Mismatch":"Acct is in Harrison file but closed in FACS"},
                                           inplace=True)
            df8.drop(df8[(df8['Disposition'] == '9000')|(df8['Disposition'] == '9999')].index, inplace=True)
            df6 = pd.concat([df6, df10])
            df8.loc[((df8['Disposition'] != '9000') &(df8['Disposition'] != '9999')), 'Cancel Code'] = ''
            df8.loc[((df8['Disposition'] != '9000') & (df8['Disposition'] != '9999')), 'Cancel Code Desc'] = ''
            index_names5 = df9[df9['Cancel Code'] == 11].index
            df9.drop(index_names5, inplace=True)
            df11=df9[(df9['Disposition'] == '9000')|(df9['Disposition'] == '9999')]
            df11["Issue Detected"].replace({"Balance Match":"Acct is in Harrison file but closed in FACS"},
                                          inplace=True)
            df9.drop(df9[(df9['Disposition'] == '9000')|(df9['Disposition'] == '9999')].index,inplace=True)
            df6=pd.concat([df6,df11])
            df9.loc[((df9['Disposition'] != '9000') & (df9['Disposition'] != '9999')), 'Cancel Code'] = ''
            df9.loc[((df9['Disposition'] != '9000') & (df9['Disposition'] != '9999')), 'Cancel Code Desc'] = ''
            df6.loc[((df6['Disposition'] != '9000') & (df6['Disposition'] != '9999')), 'Cancel Code'] = ''
            df6.loc[((df6['Disposition'] != '9000') & (df6['Disposition'] != '9999')), 'Cancel Code Desc'] = ''
            save_file.send_statement(df6, 'Closed in FACS','Rec_Goshen_Hospital','Goshen')
            save_file.send_statement(df7, 'FACS not RECON','Rec_Goshen_Hospital','Goshen')
            save_file.send_statement(df10, 'RECON not FACS', 'Rec_Goshen_Hospital', 'Goshen')
            save_file.send_statement(df3, 'Recurring Accounts','Rec_Goshen_Hospital','Goshen')
            save_file.send_statement(df8, 'Balance Mismatch','Rec_Goshen_Hospital','Goshen')
            save_file.send_statement(df9, 'Balance Match','Rec_Goshen_Hospital','Goshen')
        
        except Exception as e:
            logging.exception("Error in processing goshen recon file")

    
