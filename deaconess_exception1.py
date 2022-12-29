import numpy as np
import pandas as pd
from Utility.save_file import *
class deaconess_exception_report:
    def book_to_facs_preprocess(self,book_to_facs):
        try:
            book_to_facs.drop(book_to_facs[(book_to_facs['PRN'] == 0.0)].index, inplace=True)

            book_to_facs['year'] = pd.DatetimeIndex(book_to_facs['Date']).year
            book_to_facs['month'] = pd.DatetimeIndex(book_to_facs['Date']).month
            book_to_facs['day'] = pd.DatetimeIndex(book_to_facs['Date']).day
            book_to_facs['flag_book_to_FACS'] = book_to_facs["Acct#"].map(str) + book_to_facs["year"].map(str) + \
                                                book_to_facs['month'].map(str) + book_to_facs["day"].map(str) + \
                                                book_to_facs['PRN'].map(str)
            book_to_facs['flag_id'] = book_to_facs["Acct#"].map(str) + book_to_facs["year"].map(str) + book_to_facs['month'].map(str)\
                    + book_to_facs["day"].map(str) + book_to_facs['Pmt Type'].map(str)
            book_to_facs_sum = book_to_facs[['Client#', 'PRN']].groupby(['Client#']).sum()
            book_to_facs_PRN_sum = book_to_facs_sum.reset_index()
            return [book_to_facs_PRN_sum, book_to_facs]
        except Exception as e:
            print("Error in preprocessing book to facs data")

    def billing_statement_preprocess(self,deaconess_hospital):
        try:
            deaconess_hospital.drop(deaconess_hospital[(deaconess_hospital['Due Agency'] == 0.0)&(deaconess_hospital['Pd to Agency'] == 0.0)& (deaconess_hospital['Pd to You'] == 0.0)&(deaconess_hospital['Due You'] == 0.0)].index, inplace=True)
            deaconess_hospital['Pmt Amt Applied'] = round(deaconess_hospital['Pmt Amt Applied'], 2)
            deaconess_hospital['year'] = pd.DatetimeIndex(deaconess_hospital['Pmt Date']).year
            deaconess_hospital['month'] = pd.DatetimeIndex(deaconess_hospital['Pmt Date']).month
            deaconess_hospital['day'] = pd.DatetimeIndex(deaconess_hospital['Pmt Date']).day
            deaconess_hospital['Pd to Agency'] = pd.to_numeric(deaconess_hospital['Pd to Agency'], errors='coerce')
            deaconess_hospital['Pd to You'] = pd.to_numeric(deaconess_hospital['Pd to You'], errors='coerce')
            deaconess_hospital['Statement_Total'] = deaconess_hospital['Pd to Agency'] + deaconess_hospital['Pd to You']
            deaconess_hospital['flag_bill'] = deaconess_hospital["Clients Acct #"].map(str) + deaconess_hospital["year"].map(str)\
             + deaconess_hospital["month"].map(str) + deaconess_hospital["day"].map(str) + deaconess_hospital['Statement_Total'].map(str)
            deaconess_hospital['flag_id'] = deaconess_hospital["Clients Acct #"].map(str)\
                    + deaconess_hospital["year"].map(str) + deaconess_hospital["month"].map(str)\
                    + deaconess_hospital["day"].map(str) + deaconess_hospital['Pmt Type'].map(str)
            dataframe = deaconess_hospital[["Client #", "Clients Acct #", "Pmt Amt Applied", "Pd to Agency", "Pd to You",\
                    "Due Agency", "Due You"]]
            df = dataframe[['Client #', "Pmt Amt Applied", "Pd to Agency", "Pd to You", "Due Agency", "Due You"]].groupby(['Client #']).sum()
            df['Total'] = df['Pd to Agency'] + df['Pd to You']
        except Exception as e:
            print("Error in preprocessing deaconess hospital data")


    def Amount_Validation(self,deaconess_hospital,book_to_facs):
        try:
            book_to_facs = self.book_to_facs_preprocess(book_to_facs)
            book_to_facs_clientid = book_to_facs[0]

            deacones = self.billing_statement_preprocess(deaconess_hospital)
            deaconess_clientid = deacones[0]

            # Merge 2 dataframes based on client id
            client_id_level = pd.merge(book_to_facs_clientid,deaconess_clientid[['Client #', 'Pd to Agency', 'Pd to You', 'Total']]\
                    ,left_on="Client#", right_on="Client #", how='outer')
            # Dataframe where both client ids are matched
            client_id_level12 = client_id_level[(client_id_level['Client#'].isin(client_id_level["Client #"]))& (client_id_level['Client #'].isin(client_id_level["Client#"]))]
            client_id_level12['Total'] = round(client_id_level12['Total'], 2)
            client_id_level12['PRN'] = round(client_id_level12['PRN'], 2)
            comparison_column = np.where(client_id_level12["PRN"] == client_id_level12["Total"], True, False)
            client_id_level12['Total-Validation'] = comparison_column
            save_file = save_statement_to_output_folder()
            save_file.send_statement(client_id_level12,'Amount Validation','Deaconess','Deaconess')
        except Exception as e:
            print("Error in creating Amount validation tab")


    def Exception_report(self,deaconess_hospital,book_to_facs):
        try:
            book_to_facs1 = self.book_to_facs_preprocess(book_to_facs)
            book_to_facs_original = book_to_facs1[1]
            deaconess1 = self.billing_statement_preprocess(deaconess_hospital)
            deaconess_original = deaconess1[1]
            dff1 = pd.merge(deaconess_original, book_to_facs_original[['Client#', "Acct#", 'flag_id', 'flag_book_to_FACS', 'PRN', 'Int','Atty', 'Misc', 'CC', 'PJI','Total Pay', 'O/P Amt']], on="flag_id", how='outer')
            # Mismatch records from amount validation tab based on PRN and Total
            exception = dff1[~dff1['flag_book_to_FACS'].isin(dff1['flag_bill'].values)]
            exception11 = exception[(exception['Client#'].isin(exception["Client #"])) & (exception['Client #'].isin(exception["Client#"]))]
            exception11 = exception11[["Client #", "Clients Acct #", 'Pd to Agency', 'Pd to You', "Due Agency", "Due You","Statement_Total", "PRN", 'Int', 'Atty', 'Misc', 'CC', 'PJI', 'Total Pay', 'O/P Amt']]
            #exception11.to_excel(writer, sheet_name="Exception", index=False)
            save_file.send_statement(exception11,'Exception','Deaconess','Deaconess')
            # Records present in book to facs but not in statement
            statement_exception = dff1[~dff1["Acct#"].isin(dff1["Clients Acct #"])]
            statement_exception = statement_exception[statement_exception['Client #'].isna()]

            statement_exception = statement_exception[["Client#", "Acct#", "PRN", 'Int', 'Atty', 'Misc', 'CC', 'PJI', 'Total Pay', 'O/P Amt']]

            #statement_exception.to_excel(writer, sheet_name="Statement_Missing_Records", index=False)
            save_file.send_statement(statement_exception,'Statement_Missing_Records','Deaconess','Deaconess')
            # Records present in statement but not in book to facs
            book_to_facs_exception = dff1[~dff1["Clients Acct #"].isin(dff1["Acct#"])]
            book_to_facs_exception = book_to_facs_exception[book_to_facs_exception['Client#'].isna()]
            book_to_facs_exception = book_to_facs_exception[["Client #", "Clients Acct #", 'Pd to Agency', 'Pd to You', "Due Agency", "Due You", "Statement_Total"]]
            #book_to_facs_exception.to_excel(writer, sheet_name="BookToFacs_Missing_Records", index=False)
            save_file.send_statement(book_to_facs_exception,'BookToFacs_Missing_Records','Deaconess','Deaconess')
            # Duplicate records in booktofacs and statement
            statement_dup = pd.concat(g for _, g in deaconess_original.groupby(["Clients Acct #", "Pmt Date", "Pmt Type",'Pmt Amt Applied', 'Pd to Agency', 'Pd to You', 'Due Agency', 'Due You',"Client #"]) if len(g) > 1)
            statement_dup = statement_dup[["Clients Acct #", "Pmt Date", "Pmt Type", 'Pmt Amt Applied', 'Pd to Agency','Pd to You', 'Due Agency', 'Due You',"Client #", "First Name", "Last Name"]]
            #statement_dup.to_excel(writer, sheet_name="Statement Miscellaneous", index=False)
            save_file.send_statement(statement_dup,'Statement Miscellaneous','Deaconess','Deaconess')
            booktofacs_dup = pd.concat(g for _, g in book_to_facs_original.groupby(["FACS#", "Client#", "Acct#", 'Date', 'Total','Pmt Type', 'PRN', 'Int', 'Atty', 'Misc', 'CC', 'PJI','O/P Amt', "First Name", "Last Name"]) if len(g) > 1)
            booktofacs_dup = booktofacs_dup[["FACS#", "Client#", "Acct#", 'Date', 'Total', 'Pmt Type', 'PRN', 'Int', 'Atty','Misc', 'CC', 'PJI','O/P Amt', "Ref#", "First Name", "Last Name"]]
            #booktofacs_dup.to_excel(writer, sheet_name="Book to FACS Miscellaneous", index=False)
            save_file.send_statement(booktofacs_dup,'Book to FACS Miscellaneous','Deaconess','Deaconess')
        except Exception as e:
            print("Error in creating exception report for deaconess hospital")
