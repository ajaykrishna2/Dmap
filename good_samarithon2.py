import pandas as pd
import logging
import numpy as np
class Good_sam:
    def Good_sam(self,df, writer):
        try:
            dfw = df[df.groupby(['EPIC #'])['FACS #'].transform('nunique') > 1]
            df.drop(dfw.index, inplace=True)
            pd.set_option('display.float_format', lambda x: '%.0f' % x)
            date_sr = pd.to_datetime(pd.Series(df['List Date']))
            df['List Date'] = date_sr.dt.strftime('%m-%d-%Y')
            date_sr1 = pd.to_datetime(pd.Series(df['Last Payment Date']))
            df['Last Payment Date'] = date_sr1.dt.strftime('%m-%d-%Y')

            df['Date'] = pd.datetime.now().date()
            df['year1'] = pd.DatetimeIndex(df['Date']).year
            df['month1'] = pd.DatetimeIndex(df['Date']).month
            df['day1'] = pd.DatetimeIndex(df['Date']).day
            df['year2'] = pd.DatetimeIndex(df['List Date']).year
            df['month2'] = pd.DatetimeIndex(df['List Date']).month
            df['day2'] = pd.DatetimeIndex(df['List Date']).day
            index_name = df[(df['year2'] >= df['year1']) & (df['month2'] >= df['month1']) & (df['day2'] > df['day1'])].index
            df.drop(index_name, inplace=True)
            df.drop('year1', axis=1, inplace=True)
            df.drop('year2', axis=1, inplace=True)
            df.drop('month1', axis=1, inplace=True)
            df.drop('month2', axis=1, inplace=True)
            df.drop('day1', axis=1, inplace=True)
            df.drop('day2', axis=1, inplace=True)
            df.drop('Date', axis=1, inplace=True)
            df['Cancel Code'] = pd.to_numeric(df['Cancel Code'], errors='coerce')
            print(len(df))
            dfc=df[(df['Cancel Code']==12)|(df['Cancel Code']==3)|(df['Cancel Code'] == 11)]
            df.drop(dfc.index,inplace=True)
            print(len(df))
            dfl=df[df['Phase'] == 50]
            df.drop(dfl.index,inplace=True)
            print(len(df))
            df6 = df[df['Issue Detected'] == "The balance in EPIC is greater than the balance in FACS."]
            df7 = df[df['Issue Detected'] == "The balance in FACS is greater than the balance in EPIC."]
            df10 = df[df['Issue Detected'] == "The balance in FACS Match with balance in EPIC."]
            df.drop(df6.index, inplace=True)
            df.drop(df7.index, inplace=True)
            df.drop(df10.index, inplace=True)
            df2 = df[df.duplicated(['EPIC #'], keep=False)].sort_values('EPIC #')
            print(df2)

            # df2.drop(dfw.index,inplace=True)
            df13=df2[df2['Issue Detected'] == "EPIC has this account in Early Out, but the account is in the 3000 phase."]
            df2.drop(df13.index, inplace=True)
            df.drop(df13.index, inplace=True)

            print(len(df))

            dfd = df[df.duplicated(['EPIC #'])].sort_values('EPIC #')
            print(len(df2))
            print(len(dfd))
            df.drop(df2.index, inplace=True)
            dfm= df2.merge(dfd, indicator=True, how='left').loc[lambda x: x['_merge'] != 'both']
            dfm.drop('_merge', axis=1, inplace=True)

            df = df.merge(dfd, indicator=True, how='left').loc[lambda x: x['_merge'] != 'both']
            df.drop('_merge', axis=1, inplace=True)
            dfd = dfd.reset_index(drop=True)
            dfm = dfm.reset_index(drop=True)
            print(len(dfd))
            dfm.drop(dfm[dfm['Issue Detected'] =='The balance in FACS and EPIC Match.'].index,inplace=True)
            dfm.drop(dfm[dfm['Issue Detected'] == 'The balance in EPIC is greater than the balance in FACS.'].index, inplace=True)
            dfm.drop(dfm[dfm['Issue Detected'] == 'The balance in FACS is greater than the balance in EPIC.'].index, inplace=True)
            dfd=dfd.sort_values('EPIC #')
            dfm=dfm.sort_values('EPIC #')
            print(dfm.to_string())
            dfd["Recon file (EPIC) balance"] = dfm["Recon file (EPIC) balance"]
            print(dfd.to_string())
            dfd['Match?'] = np.where(dfd['Med-1 Balance'] == dfd['Recon file (EPIC) balance'], 'True', 'False')
            dfd['Issue Detected'] = dfd['Match?'].apply(lambda x: 'Balance Match' if x == 'True' else 'Balance Mismatch')
            dfd.drop('Match?', axis=1, inplace=True)


            df31 =df[df['Issue Detected'] == "Account is closed in EPIC, but open in FACS."]
            df32 = df[df['Issue Detected'] == "Account is closed in FACS, but open in Epic."]
            df3=pd.concat([df31,df32])
            df4 = df[df['Issue Detected'] == "Account is in EPIC File, but it is not in FACS."]
            print(df4)
            df5=df[df['Issue Detected'] == "Account is in FACS, but not in EPIC COM File. (Check Bank Funded)"]

            df8=dfd[dfd['Issue Detected'] == "Balance Mismatch"]
            print(df8)
            df9=pd.concat([df6,df7,df8])

            df11=dfd[dfd['Issue Detected'] == "Balance Match"]
            df12=pd.concat([df10,df11])

            df3.to_excel(writer, index=False, sheet_name='Closed in FACS')
            df4.to_excel(writer, index=False, sheet_name='FACS not RECON')
            df5.to_excel(writer, index=False, sheet_name='RECON not FACS')
            df9.to_excel(writer, index=False, sheet_name='Balance Mismatch')
            df12.to_excel(writer, index=False, sheet_name='Balance Match')
            dfw.to_excel(writer, index=False, sheet_name='Multiples')
            dfl.to_excel(writer, index=False, sheet_name='legal account')
            df13.to_excel(writer, index=False, sheet_name='Phase Mismatch')



        except Exception as e:
            logging.exception("error")


if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/EPI_RECON_080321_49871.xlsx', engine='xlsxwriter',options={'strings_to_numbers':True} )
    df_gsh= pd.read_csv("/home/ajay/Downloads/OneDrive_1_23-11-2021/EPI_RECON_080321_49871.TXT",delimiter="\t")
    reconcilation=Good_sam()
    reconcilation.Good_sam(df_gsh,writer)
    writer.save()