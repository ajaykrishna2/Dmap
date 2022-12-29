from Utility.save_output_to_folder import *
import logging

def womens_hospital(womens_client_statement):
    try:
        # creating EPIC tab
        EPIC = womens_client_statement.loc[
                           (womens_client_statement['System Type'] == "EPIC")
                           & (womens_client_statement['Client #'].isin([ '133E25', '133I55', '133INS', '133R25', '133R55'
                           , '133SPP', '134E25', '134I55', '134INS', '134PAY', '134R25', '134R55', '134SPP', '134REC'])),
                           ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you"
                           , "Due Agency","Due You", "Client #", "First Name", "Last Name", "Ending Bal", "System Type"]
                           ]

        save_statement_to_output_folder.send_statement(EPIC, "EPIC", "womens_hospital","Womens_Hospital")
    except Exception as e:
        logging.exception("error in splitting data in EPIC")
    try:
        # creating NON-EPIC tab
        NON_EPIC = womens_client_statement.loc[
                           (womens_client_statement['System Type'].isnull())
                           & (womens_client_statement['Client #'].isin(['133E25', '133I55', '133INS', '133R25', '133R55'
                           , '133SPP', '134E25', '134I55', '134INS', '134PAY', '134R25', '134R55', '134SPP', '134REC'])),
                           ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you"
                           , "Due Agency","Due You", "Client #", "First Name", "Last Name", "Ending Bal", "System Type"]
                           ]

        save_statement_to_output_folder.send_statement(NON_EPIC, "NON EPIC","womens_hospital","Womens_Hospital")
    except Exception as e:
        logging.exception("error in splitting data in NON-EPIC")
