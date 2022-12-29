import logging
import numpy as np
import pandas as pd
import re
from Utility.save_file import*
from pandas import DatetimeIndex

class deaconess_reconcilation_report:
    def Deaconess(self,df,inf):
        try:

            save_file = save_statement_to_output_folder()
            pd.set_option('display.float_format', lambda x: '%.0f' % x)
            date_sr = pd.to_datetime(pd.Series(df['List Date']))
            df['List Date'] = date_sr.dt.strftime('%m-%d-%Y')
            date_sr1 = pd.to_datetime(pd.Series(df['Last Payment Date']))
            df['Last Payment Date'] = date_sr1.dt.strftime('%m-%d-%Y')
            date_sr1 = pd.to_datetime(pd.Series(df['Cancel Date']))
            df1 = df[df.duplicated(['EPIC #'], keep=False)].sort_values('EPIC #')
            ph1 = df1[df1['Issue Detected'] == 'EPIC has this account in Early Out, but the account is in the 3000 phase.'].index
            ph2 = df1[df1['Issue Detected'] == 'EPIC has this account in Med1 Bad Debt, but the account is in the 1000 phase.'].index
            ph3 = df1[df1['Issue Detected'] == 'EPIC has this account in Med1 Bad Debt, but the account is in the 3000 phase.'].index
            ph4 = df1[df1['Issue Detected'] == "EPIC has this account in Med1 Outsource, but the account is in the 1000 phase."].index
            ph5 = df1[df1['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 128ERP client ID."].index
            ph6 = df1[df1['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 128WCP client ID."].index
            ph7 = df1[df1['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 132INS client ID."].index
            df1.drop(ph1, inplace=True)
            df1.drop(ph2,inplace=True)
            df1.drop(ph3,inplace=True)
            df1.drop(ph4,inplace=True)
            df1.drop(ph5,inplace=True)
            df1.drop(ph6,inplace=True)
            df1.drop(ph7,inplace=True)
            df1.drop(df1[df1['Issue Detected'] == 'The balance in FACS and EPIC match'].index, inplace=True)
            dfw = df1[df1.groupby(['EPIC #'])['FACS #'].transform('nunique') > 1]
            df1.drop(dfw.index, inplace=True)
            df.drop(dfw.index, inplace=True)
            dfw = dfw.sort_values(by=['EPIC #', 'FACS #'], ascending=[True, True], na_position='first')
            dfw['Recon file (EPIC) balance'] = dfw['Recon file (EPIC) balance'].replace(to_replace=[np.NAN,0], method='ffill')
            dfw.drop(dfw[(dfw['FACS #'].isna())].index, inplace=True)
            dfw['Match?'] = np.where(dfw['Med-1 Balance'] == dfw['Recon file (EPIC) balance'], 'True', 'False')
            dfw['Issue Detected'] = dfw['Match?'].apply(lambda x: 'Multiples' if x == 'True' else 'Balance Mismatch')
            df2 = df[df.duplicated(['EPIC #'])].sort_values('EPIC #')
            df.drop(df1.index,inplace=True)
            df2.drop(df2[df2['Issue Detected'] == 'The balance in FACS and EPIC match'].index, inplace=True)
            p1 = df2[df2['Issue Detected'] == 'EPIC has this account in Early Out, but the account is in the 3000 phase.'].index
            p2 =  df2[df2['Issue Detected'] == 'EPIC has this account in Med1 Bad Debt, but the account is in the 1000 phase.'].index
            p3 = df2[df2['Issue Detected'] == 'EPIC has this account in Med1 Bad Debt, but the account is in the 3000 phase.'].index
            p4 = df2[df2['Issue Detected'] == "EPIC has this account in Med1 Outsource, but the account is in the 1000 phase."].index
            p5 = df2[df2['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 128ERP client ID."].index
            p6 = df2[df2['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 128WCP client ID."].index
            p7 = df2[df2['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 132INS client ID."].index
            df2.drop(df2[df2['Issue Detected'] == 'The balance in FACS and EPIC match'].index,inplace=True)
            df2.drop(p1,inplace=True)
            df2.drop(p2, inplace=True)
            df2.drop(p3, inplace=True)
            df2.drop(p4, inplace=True)
            df2.drop(p5, inplace=True)
            df2.drop(p6, inplace=True)
            df2.drop(p7, inplace=True)
            indexdf1=df1[((~df1['Med-1 Balance'].isna()) & (~df1['Recon file (EPIC) balance'].isna()))].index
            indexdf2=df2[((~df2['Med-1 Balance'].isna()) & (~df2['Recon file (EPIC) balance'].isna()))].index
            dff1=df1[((df1['Med-1 Balance'].isna()) | (df1['Recon file (EPIC) balance'].isna()))].index
            dff2 = df2[((df2['Med-1 Balance'].isna()) | (df1['Recon file (EPIC) balance'].isna()))].index
            df1.drop(indexdf1,inplace=True)
            df2.drop(indexdf2,inplace=True)
            df3=df1.merge(df2, indicator=True, how='left').loc[lambda x: x['_merge'] != 'both']
            df3.drop('_merge', axis=1, inplace=True)
            df2 = df2.reset_index()
            df3 = df3.reset_index()
            df2["Recon file (EPIC) balance"] = df3["Recon file (EPIC) balance"]
            df2['Match?'] = np.where(df2['Med-1 Balance'] == df2['Recon file (EPIC) balance'], 'True', 'False')
            df2['Issue Detected'] = df2['Match?'].apply(lambda x: 'Balance Match' if x == 'True' else 'Balance Mismatch')
            df2.drop('Match?', axis=1, inplace=True)
            df4 = df[df['Issue Detected'] == "Account is closed in FACS, but open in EPIC."]
            df5= df[df['Issue Detected'] == "Account is in FACS, but not in Deaconess EPIC."]
            df6 = df[df['Issue Detected'] == "Account is in EPIC, but it is either not in FACS, or does not have EPIC flag."]
            df71=df[df['Issue Detected'] == "EPIC has this account in Early Out, but the account is in the 3000 phase."]
            df72 = df[df['Issue Detected'] == "EPIC has this account in Med1 Bad Debt, but the account is in the 1000 phase."]
            df73 = df[df['Issue Detected'] == "EPIC has this account in Med1 Bad Debt, but the account is in the 3000 phase."]
            df74 = df[df['Issue Detected'] == "EPIC has this account in Med1 Outsource, but the account is in the 1000 phase."]
            df75 = df[df['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 128ERP client ID."]
            df76 = df[df['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 128WCP client ID."]
            df77 = df[df['Issue Detected'] == "EPIC indicates that this is an AUTO/COMP/LIABILITY account, but the account is assigned to the 132INS client ID."]
            df7=pd.concat([df71,df72,df73,df74,df75,df76,df77])
            df8 = df[df['Issue Detected'] == "The balance in EPIC is greater than the balance in FACS."]
            df9 = df[df['Issue Detected'] == "The balance in FACS is greater than the balance in EPIC."]
            df11 = df2[df2['Issue Detected'] == "Balance Mismatch"]
            df111 = dfw[dfw['Issue Detected'] == "Balance Mismatch"]
            df12 =pd.concat([df8,df9])
            df13 =pd.concat([df12,df11,df111])
            df10 = df[df['Issue Detected'] == "The balance in FACS and EPIC Match."]
            df14 = df2[df2['Issue Detected'] == "Balance Match"]
            df15=pd.concat([df10,df14])
            dfw.drop(dfw[dfw['Issue Detected'] == "Balance Mismatch"].index, inplace=True)
            df4['Cancel Date'] = date_sr1.dt.strftime('%m-%d-%Y')
            df4['Date'] = pd.datetime.now().date()
            df4['year1'] = pd.DatetimeIndex(df4['Date']).year
            df4['month1'] = pd.DatetimeIndex(df4['Date']).month
            df4['day1'] = pd.DatetimeIndex(df4['Date']).day
            df4['year2'] = pd.DatetimeIndex(df4['Cancel Date']).year
            df4['month2'] = pd.DatetimeIndex(df4['Cancel Date']).month
            df4['day2'] = pd.DatetimeIndex(df4['Cancel Date']).day
            index_name = df4[(df4['year2'] >= df4['year1']) & (df4['month2'] >= df4['month1']) & (df4['day2'] >= df4['day1'])&((df4['Disposition']=='9000')&(df4['Cancel Code']=='4'))].index
            df4.drop(index_name, inplace=True)
            df4.drop('year1', axis=1, inplace=True)
            df4.drop('year2', axis=1, inplace=True)
            df4.drop('month1', axis=1, inplace=True)
            df4.drop('month2', axis=1, inplace=True)
            df4.drop('day1', axis=1, inplace=True)
            df4.drop('day2', axis=1, inplace=True)
            df4.drop('Date', axis=1, inplace=True)
            df4.drop(df4[df4['Cancel Code'].isna()].index,inplace=True)
            inf['Issue Deteched'] = ''
            inf['Phase'] = ''
            inf['Payment Date']=''
            inf['Days in Dispo']=np.NAN
            inf['PMT TO PRN']=np.NAN
            inf.drop(labels=['Unnamed: 15', 'Unnamed: 17', 'Unnamed: 20'], axis="columns", inplace=True)
            date_sr = pd.to_datetime(pd.Series(inf['List DTE']))
            inf['List DTE'] = date_sr.dt.strftime('%d-%m-%Y')
            inf = inf[['Issue Deteched', 'FACS Acct', 'Client REF #', 'Client ID', 'First Name', 'Last Name', 'Disposition','Phase', 'List DTE','Current BAL',  'Recon File BAL','AMT Cancelled','Payment Date', 'Cancel Code','Last Pay DTE', 'Days in Dispo', 'Cancel DTE','PMT TO PRN']]
            inf2 = inf.rename(columns={'Issue Deteched': 'Issue Detected', 'FACS Acct': 'FACS #', 'Client REF #': 'EPIC #',
                         'List DTE': 'List Date', 'AMT Cancelled': 'Amount Cancelled', 'Current BAL': 'Med-1 Balance',
                         'Recon File BAL': 'Recon file (EPIC) balance', 'Cancel DTE': 'Cancel Date','Last Pay DTE': 'Last Payment Date'}, inplace=False)
            inf2['Cancel Code']=pd.to_numeric(inf2['Cancel Code'] ,errors='coerce').astype(float)
            index11=inf2[(inf2['Cancel Code']==71)|(inf2['Cancel Code']==11)].index
            inf2.drop(index11,inplace=True)
            inf3 = pd.merge(df6, inf2, on='EPIC #', how='left')
            indexd=inf3[inf3.duplicated(['EPIC #'])].sort_values('EPIC #')
            inf3.drop(indexd.index,inplace=True)
            inf3=inf3.rename(columns={'Issue Detected_x':'Issue Detected','Recon file (EPIC) balance_x':'Recon file (EPIC) balance','FACS #_y':'FACS #','Client ID_y':'Client ID','First Name_y':'First Name','Last Name_y':'Last Name','Disposition_y':'Disposition','Phase_y':'Phase','List Date_y':'List Date','Med-1 Balance_y':'Med-1 Balance','Amount Cancelled_y':'Amount Cancelled','Payment Date_y':'Payment Date','Cancel Code_y':'Cancel Code','Last Payment Date_y':'Last Payment Date','Days in Dispo_y':'Days in Dispo','Cancel Date_y':'Cancel Date' ,'PMT TO PRN_y':'PMT TO PRN' }, inplace=False)
            inf3=inf3[['Issue Detected','FACS #','EPIC #','Client ID','First Name','Last Name','Disposition','Phase','List Date','Med-1 Balance','Recon file (EPIC) balance','Amount Cancelled','Payment Date','Cancel Code','Last Payment Date','Days in Dispo','Cancel Date','PMT TO PRN']]               
            indexn=inf3[~inf3['FACS #'].isna()].index
            inf3.drop(indexn,inplace=True)
            indexg=df5[(df5['Phase']==10)&((df5['Disposition']=='1TEM')|(df5['Disposition'] =='1MCB')|(df5['Disposition'] =='1700')|(df5['Disposition'] == '3700')|(df5['Disposition']=='2TEM')|(df5['Disposition']=='3TEM')|(df5['Disposition']=='5TEM'))].index
            df5.drop(indexg,inplace=True)
            indexbkr = df5[(df5['Disposition'] == '1BKR')].index
            df5.drop(indexbkr, inplace=True)
            indexmex=df7[df7['Med-1 Balance']<=0].index
            df7.drop(indexmex,inplace=True)
            df13['Date1'] = pd.datetime.now().date()
            df13['year1'] = pd.DatetimeIndex(df13['Date1']).year
            df13['month1'] = pd.DatetimeIndex(df13['Date1']).month
            df13['day1'] = pd.DatetimeIndex(df13['Date1']).day
            df13['year2'] = pd.DatetimeIndex(df13['Payment Date']).year
            df13['month2'] = pd.DatetimeIndex(df13['Payment Date']).month
            df13['day2'] = pd.DatetimeIndex(df13['Payment Date']).day
            index_name13 = df13[(df13['year2'] >= df13['year1']) & (df13['month2'] >= df13['month1']) & (df13['day2'] >= df13['day1'])].index
            df13.drop('year1', axis=1, inplace=True)
            df13.drop('year2', axis=1, inplace=True)
            df13.drop('month1', axis=1, inplace=True)
            df13.drop('month2', axis=1, inplace=True)
            df13.drop('day1', axis=1, inplace=True)
            df13.drop('day2', axis=1, inplace=True)
            df13.drop('Date1', axis=1, inplace=True)
            df13.drop(index_name13, inplace=True)
            index_13 = df13[(df13['Recon file (EPIC) balance'] < 0) | (df13['Recon file (EPIC) balance'].isna())].index
            df13.drop(index_13, inplace=True)
            dfw.drop('Match?', axis=1, inplace=True)
            df15.drop('index', axis=1, inplace=True)
            df13.drop('index', axis=1, inplace=True)
            df13.drop('Match?', axis=1, inplace=True)
            save_file.send_statement(df4, 'Closed in FACS','EPC_RECON','Rec_Deaconess')
            save_file.send_statement(df5, 'FACS not RECON','EPC_RECON','Rec_Deaconess')
            save_file.send_statement(inf3, 'RECON not FACS','EPC_RECON','Rec_Deaconess')
            save_file.send_statement(df7, 'Phase Mismatch','EPC_RECON','Rec_Deaconess')
            save_file.send_statement(df13, 'Balance Mismatch','EPC_RECON','Rec_Deaconess')
            save_file.send_statement(df15, 'Balance Match','EPC_RECON','Rec_Deaconess')
            save_file.send_statement(dfw, 'Multiples','EPC_RECON','Rec_Deaconess')
        
        except Exception as e:
            logging.exception("Error in processing deaconess recon file")

    
