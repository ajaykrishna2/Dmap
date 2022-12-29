from Utility.save_output_to_folder import *
import logging


def splitting_howard_west_campus_epic(community_client_statement):
    try:
        # creating HowardWestCampusEPIC tab
        HowardWestCampusEPIC = community_client_statement.loc[
            (community_client_statement['Epic Type'] == "HH")
          & (community_client_statement['System Type'] == "EPIC")
          & (community_client_statement['Client #'].isin(['6019HW'])),
          ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
          "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location", "System Type"]]

        save_statement_to_output_folder.send_statement(HowardWestCampusEPIC, "HowardWestCampusEPIC", "howard_west_campus_epic","Community")
    except Exception as e:
        logging.exception("error in splitting data in HowardWestCampusEPIC")
