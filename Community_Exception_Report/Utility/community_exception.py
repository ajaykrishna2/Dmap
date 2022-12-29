import numpy as np
import pandas as pd
from Utility.save_file import *


class community_exception_report:
    def book_to_facs_preprocess(self, book_to_facs):
        try:
            book_to_facs.drop(book_to_facs.loc[
                                  (book_to_facs['PRN'] == 0.0)
                              ].index, inplace=True)
            book_to_facs.drop(book_to_facs.loc[book_to_facs['Client#'].isin(
                ['6019BG', '6019BH', '5019HH', '2019T', '2019L', '60IFU', '61IFU', \
                 '62IFU', '1031', '3031', '5031', '303AWP', '303ECA', '6019HP', '106R55', '2019M', '1019OH',
                 '2019OH'])].index, inplace=True)
            book_to_facs['year'] = pd.DatetimeIndex(book_to_facs['Date']).year
            book_to_facs['month'] = pd.DatetimeIndex(book_to_facs['Date']).month
            book_to_facs['day'] = pd.DatetimeIndex(book_to_facs['Date']).day
            book_to_facs['booktofacs_date'] = book_to_facs["Acct#"].map(str) + book_to_facs["year"].map(str) + \
                                              book_to_facs['month'].map(str) + book_to_facs["day"].map(str)
            book_to_facs['flag_book_to_FACS'] = book_to_facs["Acct#"].map(str) + book_to_facs["year"].map(str) + \
                                                book_to_facs['month'].map(str) + \
                                                book_to_facs["day"].map(str) + book_to_facs['PRN'].map(str)
            book_to_facs['flag_id'] = book_to_facs["Acct#"].map(str) + book_to_facs["year"].map(str) + book_to_facs[
                'month'].map(str) + \
                                      book_to_facs["day"].map(str) + book_to_facs['Pmt Type'].map(str)
            book_to_facs_sum = book_to_facs[['Client#', 'PRN', 'O/P Amt']].groupby(['Client#']).sum()
            book_to_facs_PRN_sum = book_to_facs_sum.reset_index()
            return [book_to_facs_PRN_sum, book_to_facs]
        except Exception as e:
            print("Error in preprocessing book to facs data")

    def billing_statement_preprocess(self, community_hospital):
        try:
            community_hospital.drop(community_hospital.loc[
                                        (community_hospital['Pmt Amt'] == 0.0)
                                        & (community_hospital['Due Agency'] == 0.0)
                                        & (community_hospital['Over Paid'] == 0.0)
                                        & (community_hospital['Pd to Agency'] == 0.0)
                                        & (community_hospital['PD to you'] == 0.0)
                                        & (community_hospital['Due You'] == 0.0)
                                        ].index, inplace=True)
            community_hospital['year'] = pd.DatetimeIndex(community_hospital['Pmt Date']).year
            community_hospital['month'] = pd.DatetimeIndex(community_hospital['Pmt Date']).month
            community_hospital['day'] = pd.DatetimeIndex(community_hospital['Pmt Date']).day
            community_hospital['Sum'] = community_hospital['Pd to Agency'] + community_hospital['PD to you'] + \
                                        community_hospital["Over Paid"]
            community_hospital['bill_date'] = community_hospital["Client's Acct#"].map(str) + community_hospital[
                "year"].map(str) + \
                                              community_hospital['month'].map(str) + community_hospital["day"].map(str)
            community_hospital['flag_bill'] = community_hospital["Client's Acct#"].map(str) + community_hospital[
                "year"].map(str) + \
                                              community_hospital['month'].map(str) + community_hospital["day"].map(
                str) + community_hospital['Sum'].map(str)
            community_hospital['flag_id'] = community_hospital["Client's Acct#"].map(str) + community_hospital[
                "year"].map(str) + \
                                            community_hospital['month'].map(str) + community_hospital["day"].map(str) + \
                                            community_hospital['Type'].map(str)
            dataframe = community_hospital[
                ["Client #", "Client's Acct#", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
                 "Due You"]]
            dff1 = dataframe[
                ["Client #", "Pmt Amt", 'Pd to Agency', "PD to you", "Due Agency", "Due You", "Over Paid"]].groupby(
                ["Client #"]).sum()
            dff1['Total'] = dff1['Pd to Agency'] + dff1['PD to you'] + dff1["Over Paid"]
            return [dff1.reset_index(), community_hospital]
        except Exception as e:
            print("Error in preprocessing community hospital data")

    def Exception_report(self, community_hospital, book_to_facs):
        try:
            book_to_facs = self.book_to_facs_preprocess(book_to_facs)
            book_to_facs_original = book_to_facs[1]
            community = self.billing_statement_preprocess(community_hospital)
            community_original = community[1]
            dff1 = pd.merge(community_original, book_to_facs_original[
                ['Client#', "Acct#", 'flag_id', 'flag_book_to_FACS', 'booktofacs_date', 'PRN', \
                 'Int', 'Atty', 'Misc', 'CC', 'PJI', 'Total Pay', 'O/P Amt']], on="flag_id", how='outer')
            dff1['PRN+O/P Amt'] = dff1["PRN"] + dff1['O/P Amt']
            dff1['PRN+O/P Amt'] = round(dff1['PRN+O/P Amt'], 2)
            dff1['Sum'] = round(dff1['Sum'], 2)
            comparison = np.where(dff1["Sum"] == dff1["PRN+O/P Amt"], True, False)
            dff1['Pmt Amt-Validation'] = comparison
            # Balance Mismatch
            exception = dff1[~dff1['flag_book_to_FACS'].isin(dff1['flag_bill'].values)]
            exception11 = exception[
                (exception['Client#'].isin(exception["Client #"])) & (exception['Client #'].isin(exception["Client#"]))]
            exception11 = exception11[
                ["Client #", "Client's Acct#", 'Pmt Amt', 'Pd to Agency', 'PD to you', "Due Agency", "Due You",
                 'Over Paid', \
                 "PRN", 'Int', 'Atty', 'Misc', 'CC', 'PJI', 'Total Pay', 'O/P Amt', 'PRN+O/P Amt',
                 'Pmt Amt-Validation']]
            # Statement_Missing_Records
            statement_exception = dff1[~dff1["booktofacs_date"].isin(dff1["bill_date"])]
            statement_exception = statement_exception[statement_exception['Client #'].isna()]
            statement_exception = statement_exception[
                ["Client#", "Acct#", "PRN", 'Int', 'Atty', 'Misc', 'CC', 'PJI', 'Total Pay', 'O/P Amt']]
            # BookToFacs_Missing_Records
            book_to_facs_exception = dff1[~dff1["bill_date"].isin(dff1["booktofacs_date"])]
            book_to_facs_exception = book_to_facs_exception[book_to_facs_exception['Client#'].isna()]
            book_to_facs_exception = book_to_facs_exception[
                ["Client #", "Client's Acct#", 'Pmt Amt', 'Pd to Agency', 'PD to you', "Due Agency", \
                 "Due You", 'Over Paid']]
            # Duplicate records
            statement_dup = pd.concat(g for _, g in community_original.groupby(
                ["Client's Acct#", "Pmt Date", "Type", 'Pmt Amt', 'Pd to Agency', \
                 'PD to you', 'Due Agency', 'Due You', 'Over Paid', "Client #"]) if len(g) > 1)
            statement_dup = statement_dup[
                ["Client's Acct#", "Pmt Date", "Type", 'Pmt Amt', 'Pd to Agency', 'PD to you', 'Due Agency', 'Due You', \
                 'Over Paid', "Client #", "First Name", "Last Name"]]
            booktofacs_dup = pd.concat(g for _, g in book_to_facs_original.groupby(
                ["FACS#", "Client#", "Acct#", 'Date', 'Total', 'Pmt Type', 'PRN', \
                 'Int', 'Atty', 'Misc', 'CC', 'PJI', 'Total Pay', 'O/P Amt']) if len(g) > 1)
            booktofacs_dup = booktofacs_dup[
                ["FACS#", "Client#", "Acct#", 'Date', 'Total', 'Pmt Type', 'PRN', 'Int', 'Atty', 'Misc', 'CC', 'PJI', \
                 'Total Pay', 'O/P Amt', "Ref#", "First Name", "Last Name"]]
            return [exception11, statement_exception, book_to_facs_exception, statement_dup, booktofacs_dup]
        except Exception as e:
            print("Error in creating exception report for community hospital")

    def Amount_Validation(self, community_hospital, book_to_facs):
        try:
            save_file = save_statement_to_output_folder()
            book_to_facs1 = self.book_to_facs_preprocess(book_to_facs)
            book_to_facs_clientid = book_to_facs1[0]
            community = self.billing_statement_preprocess(community_hospital)
            community_clientid = community[0]
            client_id_level = pd.merge(book_to_facs_clientid, community_clientid[
                ['Client #', 'Pd to Agency', 'PD to you', 'Over Paid', 'Total']], \
                                       left_on="Client#", right_on="Client #", how='outer')
            client_id_level12 = client_id_level[(client_id_level['Client#'].isin(client_id_level["Client #"])) & \
                                                (client_id_level['Client #'].isin(client_id_level["Client#"]))]
            client_id_level12['Difference'] = client_id_level12['Total'] - client_id_level12['PRN']
            client_id_level12['Difference'] = round(client_id_level12['Difference'], 2)
            client_id_level12['Over Paid'] = round(client_id_level12['Over Paid'], 2)
            comparison_column = np.where(client_id_level12["Difference"] == client_id_level12["Over Paid"], True, False)
            client_id_level12['Over Paid-Validation'] = comparison_column
            client_id_level13 = client_id_level12[
                ["Client#", "Pd to Agency", "PD to you", "Over Paid", "Total", "PRN", "O/P Amt", "Difference",
                 "Over Paid-Validation"]]
            comments = client_id_level13[~client_id_level13['Difference'].isin(client_id_level13['Over Paid'].values)]
            # call the exception report function
            exception_repo = self.Exception_report(community_hospital, book_to_facs)
            exception = exception_repo[0]
            op1 = comments[comments['Client#'].isin(exception['Client #'])]
            statement_exception = exception_repo[1]
            op2 = comments[comments['Client#'].isin(statement_exception['Client#'])]
            book_to_facs_exce = exception_repo[2]
            op3 = comments[comments['Client#'].isin(book_to_facs_exce['Client #'])]
            statement_dup = exception_repo[3]
            booktofacs_dup = exception_repo[4]

            for index, row1 in client_id_level13.iterrows():
                for index, row2 in op1.iterrows():
                    if (row1['Client#'] == row2['Client#']):
                        client_id_level13.loc[client_id_level13['Client#'] == row1[
                            'Client#'], "Over Paid-Validation"] = "Check Balance Mismatch"

            for index, row1 in client_id_level13.iterrows():
                for index, row2 in op2.iterrows():
                    if (row1['Client#'] == row2['Client#']):
                        client_id_level13.loc[client_id_level13['Client#'] == row1[
                            'Client#'], "Over Paid-Validation"] = "Check Statement_Missing_Records"

            for index, row1 in client_id_level13.iterrows():
                for index, row2 in op3.iterrows():
                    if (row1['Client#'] == row2['Client#']):
                        client_id_level13.loc[client_id_level13['Client#'] == row1[
                            'Client#'], "Over Paid-Validation"] = "Check BookToFacs_Missing_Records"

            for index, row1 in client_id_level13.iterrows():
                for index, row2 in op1.iterrows():
                    for index, row3 in op2.iterrows():
                        if (row1['Client#'] == row2['Client#']) & (row1['Client#'] == row3['Client#']):
                            client_id_level13.loc[client_id_level13['Client#'] == row1['Client#'], \
                                                  "Over Paid-Validation"] = "Check Balance Mismatch and Statement_Missing_Records"
                    for index, row4 in op3.iterrows():
                        if (row1['Client#'] == row2['Client#']) & (row1['Client#'] == row4['Client#']):
                            client_id_level13.loc[client_id_level13['Client#'] == row1['Client#'], \
                                                  "Over Paid-Validation"] = "Check Balance Mismatch and BookToFacs_Missing_Records"

            save_file.send_statement(client_id_level13, 'Amount Validation','Exec_Community','output/Community')
            save_file.send_statement(exception, 'Balance Mismatch', 'Exec_Community','output/Community')
            save_file.send_statement(statement_exception, "Statement_Missing_Records", 'Exec_Community','output/Community')
            save_file.send_statement(book_to_facs_exce, "BookToFacs_Missing_Records", 'Exec_Community','output/Community')
            save_file.send_statement(statement_dup, "Statement Miscellaneous", 'Exec_Community','output/Community')
            save_file.send_statement(booktofacs_dup, "Book To Facs Miscellaneous", 'Exec_Community','output/Community')

        except Exception as e:
            print("Error in creating Amount validation tab")
