import logging

import numpy as np
import pandas as pd
import glob
from pandas import DatetimeIndex


# from Utility.save_file import *
# from Utility.read_file import *
class deaconess_exception_report:
    def preprocess(self):
        all_data = pd.DataFrame()
        path = '/home/ajay/Downloads/Deaconess/*.xlsx'
        for f in glob.glob(path):
            df = pd.read_excel(f, sheet_name=None, dtype={"Client #": str})
            dff = pd.concat(df.values())
            all_data = all_data.append(dff, ignore_index=True)
        return all_data

    def book_to_facs_preprocess(self, book_to_facs):
        try:

            book_to_facs=book_to_facs[(book_to_facs['Client Name'] == 'Deaconess Gibson Hospital')
                                      & (book_to_facs['Client Name'] == 'Deaconess Health System') & (book_to_facs['Client Name'] == 'Deaconess Henderson Hospital') & (book_to_facs['Client Name'] == 'Deaconess Specialty Physicians') & (book_to_facs['Client Name'] == 'Deaconess Union County Hospital') & (book_to_facs['Client Name'] == 'THE HEART HOSPITAL')]
            book_to_facs.drop(book_to_facs[(book_to_facs['PRN'] == 0.0)].index, inplace=True)
            print(book_to_facs)
            book_to_facs['year'] = pd.DatetimeIndex(book_to_facs['Date']).year
            book_to_facs['month'] = pd.DatetimeIndex(book_to_facs['Date']).month
            book_to_facs['day'] = pd.DatetimeIndex(book_to_facs['Date']).day
            book_to_facs['flag_book_to_FACS'] = book_to_facs["Acct#"].map(str) + book_to_facs["year"].map(str) + \
                                                book_to_facs['month'].map(str) + book_to_facs["day"].map(str) + \
                                                book_to_facs['PRN'].map(str)
            book_to_facs['flag_id'] = book_to_facs["Acct#"].map(str) + book_to_facs["year"].map(str) + book_to_facs[
                'month'].map(str) + book_to_facs["day"].map(str) + book_to_facs['Pmt Type'].map(str)
            book_to_facs_sum = book_to_facs[['Client#', 'PRN']].groupby(['Client#']).sum()
            book_to_facs_PRN_sum = book_to_facs_sum.reset_index()
            return [book_to_facs_PRN_sum, book_to_facs]


        except Exception as e:
            print("Error in preprocessing book to facs data")

    def billing_statement_preprocess(self, deaconess):
        try:
            print(deaconess)
            deaconess.drop(deaconess[(deaconess['Due Agency'] == 0.0)& (deaconess['Pd to Agency'] == 0.0)& (deaconess['Pd to You'] == 0.0)& (deaconess['Due You'] == 0.0)].index, inplace=True)
            deaconess['Pmt Amt Applied'] = round(deaconess['Pmt Amt Applied'], 2)
            deaconess['year'] = pd.DatetimeIndex(deaconess['Pmt Date']).year
            deaconess['month'] = pd.DatetimeIndex(deaconess['Pmt Date']).month
            deaconess['day'] = pd.DatetimeIndex(deaconess['Pmt Date']).day
            deaconess['Pd to Agency'] = pd.to_numeric(deaconess['Pd to Agency'], errors='coerce')
            deaconess['Pd to You'] = pd.to_numeric(deaconess['Pd to You'], errors='coerce')
            deaconess['Statement_Total'] = deaconess['Pd to Agency'] + deaconess['Pd to You']
            deaconess['flag_bill'] = deaconess["Clients Acct #"].map(str) + deaconess["year"].map(str) + deaconess["month"].map(str) + deaconess["day"].map(str) + deaconess['Statement_Total'].map(str)
            deaconess['flag_id'] = deaconess["Clients Acct #"].map(str) + deaconess["year"].map(str) + deaconess["month"].map(str) + deaconess["day"].map(str) + deaconess['Pmt Type'].map(str)
            dataframe = deaconess[["Client #", "Clients Acct #", "Pmt Amt Applied", "Pd to Agency", "Pd to You", "Due Agency", "Due You"]]
            df = dataframe[['Client #', "Pmt Amt Applied", "Pd to Agency", "Pd to You", "Due Agency", "Due You"]].groupby(['Client #']).sum()
            df['Total'] = df['Pd to Agency'] + df['Pd to You']
            return [df.reset_index(), deaconess]
        except Exception as e:
            print("Error in preprocessing dataframe")

    def Amount_Validation(self, deaconess, book_to_facs, writer):
        try:
            book_to_facs.drop(book_to_facs[(book_to_facs['PRN'] == 0.0)].index, inplace=True)
            deaconess.drop(deaconess[(deaconess['Due Agency'] == 0.0) & (deaconess['Pd to Agency'] == 0.0) & (deaconess['Pd to You'] == 0.0) & (deaconess['Due You'] == 0.0)].index, inplace=True)
            b1 = book_to_facs[(book_to_facs['Client Name'] == 'Deaconess Gibson Hospital')]
            b2 = book_to_facs[(book_to_facs['Client Name'] == 'Deaconess Health System')]
            b3 = book_to_facs[(book_to_facs['Client Name'] == 'Deaconess Henderson Hospital')]
            b4 = book_to_facs[(book_to_facs['Client Name'] == 'Deaconess Specialty Physicians')]
            b5 = book_to_facs[(book_to_facs['Client Name'] == 'Deaconess Union County Hospital')]
            b6 = book_to_facs[(book_to_facs['Client Name'] == 'THE HEART HOSPITAL')]
            book_to_facs = pd.concat([b1, b2, b3, b4, b5, b6])
            book_to_facs = self.book_to_facs_preprocess(book_to_facs)
            book_to_facs_clientid = book_to_facs[0]

            deacones = self.billing_statement_preprocess(deaconess)
            deaconess_clientid = deacones[0]

            # Merge 2 dataframes based on client id
            client_id_level = pd.merge(book_to_facs_clientid,deaconess_clientid[['Client #', 'Pd to Agency', 'Pd to You', 'Total']],left_on="Client#", right_on="Client #", how='outer')
            # Dataframe where both client ids are matched
            client_id_level12 = client_id_level[(client_id_level['Client#'].isin(client_id_level["Client #"])) & (client_id_level['Client #'].isin(client_id_level["Client#"]))]
            client_id_level12['Total'] = round(client_id_level12['Total'], 2)
            client_id_level12['PRN'] = round(client_id_level12['PRN'], 2)
            comparison_column = np.where(client_id_level12["PRN"] == client_id_level12["Total"], True, False)
            client_id_level12['Total-Validation'] = comparison_column
            client_id_level12 = client_id_level12[['Client #', 'Pd to Agency', 'Pd to You', 'Total', 'PRN', 'Total-Validation']]
            client_id_level12.to_excel(writer,sheet_name='Amount Validation',index=False)

        except Exception as e:
            print("Error in creating amount validation tab")

    def Exception_report(self,deaconess, book_to_facs, writer):
        try:
            book_to_facs.drop(book_to_facs[(book_to_facs['PRN'] == 0.0)].index, inplace=True)
            deaconess.drop(deaconess[(deaconess['Due Agency'] == 0.0) & (deaconess['Pd to Agency'] == 0.0) & (deaconess['Pd to You'] == 0.0) & (deaconess['Due You'] == 0.0)].index, inplace=True)
            b1 = book_to_facs[(book_to_facs['Client Name'] == 'Deaconess Gibson Hospital')]
            b2 = book_to_facs[(book_to_facs['Client Name'] == 'Deaconess Health System')]
            b3 = book_to_facs[(book_to_facs['Client Name'] == 'Deaconess Henderson Hospital')]
            b4 = book_to_facs[(book_to_facs['Client Name'] == 'Deaconess Specialty Physicians')]
            b5 = book_to_facs[(book_to_facs['Client Name'] == 'Deaconess Union County Hospital')]
            b6 = book_to_facs[(book_to_facs['Client Name'] == 'THE HEART HOSPITAL')]
            book_to_facs = pd.concat([b1, b2, b3, b4, b5, b6])
            # book_to_facs[(book_to_facs['Client Name'] == 'Deaconess Gibson Hospital')]
                         # | (book_to_facs['Client Name'] == 'Deaconess Health System') | (book_to_facs['Client Name'] == 'Deaconess Henderson Hospital') | (book_to_facs['Client Name'] == 'Deaconess Specialty Physicians') | (book_to_facs['Client Name'] == 'Deaconess Union County Hospital') | (book_to_facs['Client Name'] == 'THE HEART HOSPITAL')]
            book_to_facs1 = self.book_to_facs_preprocess(book_to_facs)
            book_to_facs_original = book_to_facs1[1]
            deaconess1 = self.billing_statement_preprocess(deaconess)
            deaconess_original = deaconess1[1]
            dff1 = pd.merge(deaconess_original, book_to_facs_original[['Client#', "Acct#", 'flag_id', 'flag_book_to_FACS', 'PRN', 'Int', 'Atty', 'Misc', 'CC', 'PJI','Total Pay', 'O/P Amt']], on="flag_id", how='outer')
            # Mismatch records from amount validation tab based on PRN and Total
            exception = dff1[~dff1['flag_book_to_FACS'].isin(dff1['flag_bill'].values)]
            exception11 = exception[(exception['Client#'].isin(exception["Client #"])) & (exception['Client #'].isin(exception["Client#"]))]
            exception11 = exception11[["Client #", "Clients Acct #", 'Pd to Agency', 'Pd to You', "Due Agency", "Due You", "Statement_Total", "PRN", 'Int', 'Atty', 'Misc', 'CC', 'PJI', 'Total Pay', 'O/P Amt']]
            exception11.to_excel(writer, sheet_name="Exception", index=False)
            # save_file.send_statement(exception11,'Exception','','')
            # Records present in book to facs but not in statement
            statement_exception = dff1[~dff1["Acct#"].isin(dff1["Clients Acct #"])]
            statement_exception = statement_exception[statement_exception['Client #'].isna()]

            statement_exception = statement_exception[["Client#", "Acct#", "PRN", 'Int', 'Atty', 'Misc', 'CC', 'PJI', 'Total Pay', 'O/P Amt']]

            statement_exception.to_excel(writer, sheet_name="Statement_Missing_Records", index=False)
            # save_file.send_statement(statement_exception,'Statement_Missing_Records','','')
            # Records present in statement but not in book to facs
            book_to_facs_exception = dff1[~dff1["Clients Acct #"].isin(dff1["Acct#"])]
            book_to_facs_exception = book_to_facs_exception[book_to_facs_exception['Client#'].isna()]
            book_to_facs_exception = book_to_facs_exception[["Client #", "Clients Acct #", 'Pd to Agency', 'Pd to You', "Due Agency", "Due You", "Statement_Total"]]
            book_to_facs_exception.to_excel(writer, sheet_name="BookToFacs_Missing_Records", index=False)
            # save_file.send_statement(book_to_facs_exception,'BookToFacs_Missing_Records','','')
            # Duplicate records in booktofacs and statement
            statement_dup = pd.concat(g for _, g in deaconess_original.groupby(["Clients Acct #", "Pmt Date", "Pmt Type", 'Pmt Amt Applied', 'Pd to Agency', 'Pd to You', 'Due Agency', 'Due You',"Client #"]) if len(g) > 1)
            statement_dup = statement_dup[["Clients Acct #", "Pmt Date", "Pmt Type", 'Pmt Amt Applied', 'Pd to Agency', 'Pd to You', 'Due Agency', 'Due You',"Client #", "First Name", "Last Name"]]
            statement_dup.to_excel(writer, sheet_name="Statement Miscellaneous", index=False)
            # save_file.send_statement(statement_dup,'Statement Miscellaneous','','')
            booktofacs_dup = pd.concat(g for _, g in book_to_facs_original.groupby(["FACS#", "Client#", "Acct#", 'Date', 'Total', 'Pmt Type', 'PRN', 'Int', 'Atty', 'Misc', 'CC', 'PJI','O/P Amt', "First Name", "Last Name"]) if len(g) > 1)
            booktofacs_dup = booktofacs_dup[["FACS#", "Client#", "Acct#", 'Date', 'Total', 'Pmt Type', 'PRN', 'Int', 'Atty', 'Misc', 'CC', 'PJI','O/P Amt', "Ref#", "First Name", "Last Name"]]
            booktofacs_dup.to_excel(writer, sheet_name="Book to FACS Miscellaneous", index=False)
            # save_file.send_statement(booktofacs_dup,'Book to FACS Miscellaneous','','')
        except Exception as e:
            print("Error in creating exception report for women's hospital")



if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/Deconess_exception_report2.xlsx', engine='xlsxwriter')
    obj = deaconess_exception_report()
    deacones=obj.preprocess()
    deacones.to_excel("deaconess_repo.xlsx", index=False)
    deaconess = pd.read_excel("deaconess_repo.xlsx")
    book_to_facs = pd.read_excel('/home/ajay/Downloads/Book_to_Facs/book_to_facs.xlsx', sheet_name='NON_STV')
    exception = deaconess_exception_report()
    exception.Amount_Validation(deaconess, book_to_facs, writer)
    exception.Exception_report(deaconess, book_to_facs, writer)
    writer.save()