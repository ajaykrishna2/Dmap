from Utility.save_output_to_folder import *
import logging

def splitting_howardCC(community_client_statement):
    try:
        # creating HowardCancerCenterHB tab
        HowardCancerCenterHB = community_client_statement.loc[
              (community_client_statement['Epic Type'] == "HOSPITAL")
            & (community_client_statement['Acct Location'] == "Community Cancer Center Howard")
            & (community_client_statement['System Type'] == "EPIC")
            & (community_client_statement['Client #'].isin(['6019E','6019F'])),
            ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
            "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
            "System Type"]
            ]

        save_statement_to_output_folder.send_statement(HowardCancerCenterHB, "Howard Cancer Center HB", "howard_cancer_center","Community")
    except Exception as e:
        logging.exception("error in splitting data in HowardCancerCenterHB")

    try:
        # creating HowardCancerCenterPB tab
        HowardCancerCenterPB = community_client_statement.loc[
              (community_client_statement['Epic Type'] == "PHYSICIAN")
            & (community_client_statement['Acct Location'] == "Community Cancer Center Howard")
            & (community_client_statement['System Type'] == "EPIC")
            & (community_client_statement['Client #'].isin(['6019E', '6019F'])),
            ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
            "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location", "System Type"]
            ]

        save_statement_to_output_folder.send_statement(HowardCancerCenterPB, "Howard Cancer Center PB", "howard_cancer_center","Community")
    except Exception as e:
        logging.exception("error in splitting data in CommunityEastCampus")
