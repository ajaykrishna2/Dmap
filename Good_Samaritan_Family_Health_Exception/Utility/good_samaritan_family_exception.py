import numpy as np
import pandas as pd
from Utility.save_file import *
class good_sam_family_exception:

    def book_to_facs_preprocess(self,book_to_facs):
        try:
            book_to_facs.drop(book_to_facs.loc[
                                  (book_to_facs['PRN']== 0.0)
                                 &(book_to_facs['O/P Amt']==0.0)
                                 ].index, inplace = True)
            book_to_facs = book_to_facs.loc[book_to_facs['Client Name'].isin(['Good Samaritan Family Health Center'])]
            book_to_facs['Acct#'] = book_to_facs['Acct#'].str.lstrip('0')
            book_to_facs['year'] = pd.DatetimeIndex(book_to_facs['Date']).year
            book_to_facs['month'] = pd.DatetimeIndex(book_to_facs['Date']).month
            book_to_facs['day'] = pd.DatetimeIndex(book_to_facs['Date']).day 
            book_to_facs['flag_book_to_FACS'] = book_to_facs["Acct#"].map(str)+book_to_facs["year"].map(str)+\
            book_to_facs['month'].map(str)+book_to_facs["day"].map(str)+book_to_facs['PRN'].map(str)
            book_to_facs['flag_id'] = book_to_facs["Acct#"].map(str)+book_to_facs["year"].map(str)+book_to_facs['month'].map(str)+\
            book_to_facs["day"].map(str)+book_to_facs['Pmt Type'].map(str)
            book_to_facs_sum = book_to_facs[['Client#','PRN']].groupby(['Client#']).sum()
            book_to_facs_PRN_sum = book_to_facs_sum.reset_index()
            return [book_to_facs_PRN_sum,book_to_facs]
        except Exception as e:
            print("Error in preprocessing book to facs data")
    def billing_statement_preprocess(self,good_samaritan):
        try:  
            good_samaritan.drop(good_samaritan.loc[
                                 (good_samaritan['Pmt Amt']==0.0)
                                 & (good_samaritan['Due Agency'] == 0.0)
                                 & (good_samaritan['Pd to Agency'] == 0.0)
                                 & (good_samaritan['PD to you'] == 0.0)
                                 & (good_samaritan['Due You']==0.0)
                                 ].index, inplace=True)
            good_samaritan['year'] = pd.DatetimeIndex(good_samaritan['Pmt Date']).year
            good_samaritan['month'] = pd.DatetimeIndex(good_samaritan['Pmt Date']).month
            good_samaritan['day'] = pd.DatetimeIndex(good_samaritan['Pmt Date']).day 
            good_samaritan['Statement_Total'] = good_samaritan['Pd to Agency']+good_samaritan['PD to you']
            good_samaritan['flag_bill']= good_samaritan["Client's Acct#"].map(str)+good_samaritan["year"].map(str)+good_samaritan['month'].map(str)+\
            good_samaritan["day"].map(str)+good_samaritan['Statement_Total'].map(str)
            good_samaritan['flag_id']= good_samaritan["Client's Acct#"].map(str)+good_samaritan["year"].map(str)+good_samaritan['month'].map(str)+\
            good_samaritan["day"].map(str)+good_samaritan['Type'].map(str)
            dataframe = good_samaritan[["Client #","Client's Acct#","Pmt Amt","Pd to Agency","PD to you","Due Agency","Due You"]]
            df1 = dataframe[["Client #","Pmt Amt","PD to you",'Pd to Agency',"Due Agency","Due You"]].groupby(["Client #"]).sum()
            df1['Total'] = df1['Pd to Agency']+df1['PD to you']
            return [df1.reset_index(),good_samaritan]
        except Exception as e:
            print("Error in preprocessing billing_statement_preprocess")

    def Amount_Validation(self,good_samaritan,book_to_facs):
        try:
            book_to_facs= self.book_to_facs_preprocess(book_to_facs)
            book_to_facs_clientid =  book_to_facs[0]
            good_sam = self.billing_statement_preprocess(good_samaritan)
            good_sam_clientid = good_sam[0]
            #Merge 2 dataframes based on client id 
            client_id_level = pd.merge(book_to_facs_clientid,good_sam_clientid[['Client #','Pd to Agency', 'PD to you', 'Total']],left_on="Client#",\
            right_on="Client #",how='outer')
            #Dataframe where both client ids are matched
            client_id_level12 = client_id_level[(client_id_level['Client#'].isin(client_id_level["Client #"]))&\
            (client_id_level['Client #'].isin(client_id_level["Client#"]))]
            client_id_level12['Total'] = round(client_id_level12['Total'],2)
            client_id_level12['PRN'] = round(client_id_level12['PRN'],2)
            comparison_column = np.where(client_id_level12["PRN"] == client_id_level12["Total"], True, False)
            client_id_level12['Total-Validation']=comparison_column
            client_id_level12=client_id_level12[['Client #','Pd to Agency', 'PD to you','Total','PRN','Total-Validation']]
            save_file = save_statement_to_output_folder()
            save_file.send_statement(client_id_level12,'Amount Validation','Exec_Good_Samaritan_Family_Health','output/Good_Samaritan_Family')
        
        except Exception as e:
            print("Error in creating amount validation tab")

    def Exception_report(self,good_samaritan,book_to_facs):
            try:
                save_file = save_statement_to_output_folder()
                book_to_facs= self.book_to_facs_preprocess(book_to_facs)
                book_to_facs_original = book_to_facs[1]
                good_sam = self.billing_statement_preprocess(good_samaritan)
                good_sam_original = good_sam[1]
                dff1 = pd.merge(good_sam_original,book_to_facs_original[['Client#',"Acct#",'flag_id','flag_book_to_FACS','PRN','Int','Atty','Misc','CC',\
                'PJI','Total Pay','O/P Amt']],on="flag_id",how='outer')
                #Mismatch records from amount validation tab based on PRN and Total 
                exception = dff1[~dff1['flag_book_to_FACS'].isin(dff1['flag_bill'].values)]
                exception11 = exception[(exception['Client#'].isin(exception["Client #"]))&(exception['Client #'].isin(exception["Client#"]))]
                exception11 = exception11[["Client #","Client's Acct#",'Pd to Agency','PD to you',"Due Agency","Due You","Statement_Total","PRN",'Int',\
                'Atty','Misc','CC','PJI','Total Pay','O/P Amt']]
                print(exception11)
                save_file.send_statement(exception11,'Balance Mismatch','Exec_Good_Samaritan_Family_Health','output/Good_Samaritan_Family')
                #Records present in book to facs but not in statement
                statement_exception = dff1[~dff1["Acct#"].isin(dff1["Client's Acct#"])]
                statement_exception = statement_exception[statement_exception['Client #'].isna()]
                statement_exception = statement_exception[["Client#","Acct#","PRN",'Int','Atty','Misc','CC','PJI','Total Pay','O/P Amt']]
                save_file.send_statement(statement_exception,'Statement_Missing_Records','Exec_Good_Samaritan_Family_Health','output/Good_Samaritan_Family')
                #Records present in statement but not in book to facs
                book_to_facs_exception = dff1[~dff1["Client's Acct#"].isin(dff1["Acct#"])]
                book_to_facs_exception = book_to_facs_exception[book_to_facs_exception['Client#'].isna()]
                book_to_facs_exception = book_to_facs_exception[["Client #","Client's Acct#",'Pd to Agency','PD to you',"Due Agency","Due You","Statement_Total"]]
                save_file.send_statement(book_to_facs_exception,'BookToFacs_Missing_Records','Exec_Good_Samaritan_Family_Health','output/Good_Samaritan_Family')
                #Duplicate records in booktofacs and statement
                statement_dup = pd.concat(g for _, g in good_sam_original.groupby(["Client's Acct#", "Pmt Date", "Type", 'Pmt Amt', 'Pd to Agency',\
                'PD to you','Due Agency', 'Due You', "Client #"]) if len(g) > 1)
                statement_dup = statement_dup[["Client's Acct#", "Pmt Date", "Type", 'Pmt Amt', 'Pd to Agency', 'PD to you','Due Agency', 'Due You',\
                "Client #","First Name","Last Name"]]
                print(statement_dup)
                save_file.send_statement(statement_dup,'Statement Miscellaneous','Exec_Good_Samaritan_Family_Health','output/Good_Samaritan_Family')
                booktofacs_dup = pd.concat(g for _, g in book_to_facs_original.groupby(["FACS#", "Client#", "Acct#", 'Date', 'Total', 'Pmt Type', 'PRN',\
                'Int', 'Atty', 'Misc', 'CC', 'PJI', 'O/P Amt',"First Name","Last Name"]) if len(g) > 1)
                booktofacs_dup=booktofacs_dup[["FACS#", "Client#", "Acct#", 'Date', 'Total', 'Pmt Type', 'PRN', 'Int', 'Atty', 'Misc', 'CC', 'PJI',\
                'O/P Amt',"Ref#","First Name","Last Name"]]
                save_file.send_statement(booktofacs_dup,'Book To Facs Miscellaneous','Exec_Good_Samaritan_Family_Health','output/Good_Samaritan_Family')
            except Exception as e:
                print("Error in creating exception report for good samaritan family heath",e)


