from Utility.save_output_to_folder import *
import logging

def splitting_howard6019(community_client_statement):
    try:
        # creating Howard6019HHB tab
        Howard6019HHB = community_client_statement.loc[
            (community_client_statement['Epic Type']== "HOSPITAL")
          & (community_client_statement['Legal Reported']!="YES")
          & (community_client_statement['System Type']== "EPIC")
          & (community_client_statement['Client #'].isin(['6019H'])),
          ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
          "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location", "System Type"]]
        save_statement_to_output_folder.send_statement(Howard6019HHB, "HB", "Howard 6019H EPIC MED-1 Statement","Community")
    except Exception as e:
        logging.exception("error in splitting data in HowardCancerCenterHB")

    try:
        # creating Howard6019HPB tab
        Howard6019HPB = community_client_statement.loc[
            (community_client_statement['Epic Type'] == "PHYSICIAN")
          & (community_client_statement['Legal Reported'] != "YES")
          & (community_client_statement['System Type'] == "EPIC")
          & (community_client_statement['Client #'].isin(['6019H'])),
          ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
          "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location", "System Type"]]

        save_statement_to_output_folder.send_statement(Howard6019HPB, "PB", "Howard 6019H EPIC MED-1 Statement","Community")
    except Exception as e:
        logging.exception("error in splitting data in CommunityEastCampus")
