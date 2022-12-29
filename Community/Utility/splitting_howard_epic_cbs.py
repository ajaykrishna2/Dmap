from Utility.save_output_to_folder import *
import logging

def splitting_howard_epic_cbs(community_client_statement):
    try:
        # creating HowardCBS tab
        HowardCBS = community_client_statement.loc[
                          (community_client_statement['Epic Type'].isin(["HOSPITAL","UNDEFINED"]))
                        & (community_client_statement['System Type'] == "EPIC")
                        & (community_client_statement['Client #'].isin(['40HERP', '40HWCP', '40HM25', '40RERP',
                        '40RM25', '40RWCP','40HWPP','4019H','4019HW','40RWPP'])),
                        ["Client's Acct#",  "Pmt Date", "Type", "Pmt Amt",  "Over Paid",    "Pd to Agency", "PD to you",
                        "Due Agency", "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type",
                        "Acct Location", "System Type"]
                        ]
        save_statement_to_output_folder.send_statement(HowardCBS, "HowardCBS", "howard_CBS","Community")
    except Exception as e:
        logging.exception("error in splitting data in HowardCBS")
