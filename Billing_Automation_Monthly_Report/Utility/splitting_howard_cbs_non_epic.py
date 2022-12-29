from Utility.save_output_to_folder import *
import logging

def splitting_howard_cbs_non_epic(community_client_statement):
    try:
        # creating HowardCBSNonEPIC tab
        HowardCBSNonEPIC = community_client_statement.loc[
            (community_client_statement['Epic Type'] == "PHYSICIAN")
          & (community_client_statement['System Type'].isnull())
          & (community_client_statement['Client #'].isin(['101ERP', '101M25', '101E25', '101SPP', '101WCP', '101INS', '101IFU', '1001SP', '101W55']))
          , ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency",
          "PD to you", "Due Agency", "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type",
          "Acct Location", "System Type"]]

        save_statement_to_output_folder.send_statement(HowardCBSNonEPIC, "HowardCBSNonEPIC", "howard_cbs_non_epic","Community")
    except Exception as e:
        logging.exception("error in splitting data in HowardCBSNonEPIC")

