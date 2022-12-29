from Utility.save_output_to_folder import *
import logging

def splitting_howard_med1_non_epic(community_client_statement):
    try:
        # creating HowardMED1NonEPIC tab
        HowardMED1NonEPIC = community_client_statement.loc[
            (community_client_statement['Epic Type'] == "PHYSICIAN")
          & (community_client_statement['System Type'].isnull())
          & (community_client_statement['Client #'].isin(['6019H', '6019HA', '1001', '9001', '101I55',
          '101R25', '101R55','3001','2001','5001','101W55'])), ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency",
          "PD to you", "Due Agency", "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type",
          "Acct Location", "System Type"]]

        save_statement_to_output_folder.send_statement(HowardMED1NonEPIC, "HowardMED1NonEPIC", "howard_med1_non_epic","Community")
    except Exception as e:
        logging.exception("error in splitting data in HowardMED1NonEPIC")
