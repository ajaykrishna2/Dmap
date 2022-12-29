from Utility.save_output_to_folder import *
import logging

def splitting_6019_non_epic(community_client_statement):
    try:
        # creating Howard6019HWNONEPIC tab
        Howard6019HWNONEPIC = community_client_statement.loc[
            (community_client_statement['Epic Type'] == "PHYSICIAN")
          & (community_client_statement['System Type'] != "EPIC")
          & (community_client_statement['Client #'].isin(['6019HW','103W55','103R55'])),
          ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
          "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location", "System Type"]]

        save_statement_to_output_folder.send_statement(Howard6019HWNONEPIC, "Sheet1", "Howard 6019HW NON EPIC MED-1 Statement","Community")
    except Exception as e:
        logging.exception("error in splitting data in HowardMED1NonEPIC")
