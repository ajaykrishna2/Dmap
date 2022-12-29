from Utility.save_output_to_folder import *
import logging

def splitting_reid(community_client_statement):
    try:
        # creating ReidHB tab
        ReidHB = community_client_statement.loc[
              (community_client_statement['Epic Type']== "HOSPITAL")
            & (community_client_statement['Legal Reported']!="YES")
            & (community_client_statement['System Type']== "EPIC")
            & (community_client_statement['Client #'].isin(['6019R','7019R'])),
            ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
            "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
            "System Type"]
            ]

        save_statement_to_output_folder  .send_statement(ReidHB, "M1 HB", "reid","Community")
    except Exception as e:
        logging.exception("error in splitting data in ReidHB")

    try:
        # creating ReidHBLegal tab
        ReidHBLegal = community_client_statement.loc[
              (community_client_statement['Epic Type']== "HOSPITAL")
            & (community_client_statement['Legal Reported']=="YES")
            & (community_client_statement['System Type']== "EPIC")
            & (community_client_statement['Client #'].isin(['6019R','7019R'])),
            ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
            "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
            "System Type"]
            ]
        save_statement_to_output_folder.send_statement(ReidHBLegal, "M1 HB Legal", "reid","Community")
    except Exception as e:
        logging.exception("error in splitting data in ReidHBLegal")

    try:
        # creating ReidPB tab
        ReidPB = community_client_statement.loc[
              (community_client_statement['Epic Type'] == "PHYSICIAN")
            & (community_client_statement['Legal Reported'] != "YES")
            & (community_client_statement['System Type'] == "EPIC")
            & (community_client_statement['Client #'].isin( ['6019R', '7019R'])),
            ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
            "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
            "System Type"]
            ]
        save_statement_to_output_folder.send_statement(ReidPB, "M1 PB", "reid","Community")
    except Exception as e:
        logging.exception("error in splitting data in ReidPB")

    try:
        # creating ReidPBLegal tab
        ReidPBLegal = community_client_statement.loc[
              (community_client_statement['Epic Type']== "PHYSICIAN")
            & (community_client_statement['Legal Reported']=="YES")
            & (community_client_statement['System Type']== "EPIC")
            & (community_client_statement['Client #'].isin(['6019R','7019R'])),
            ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
            "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location", "System Type"]
            ]
        save_statement_to_output_folder.send_statement(ReidPBLegal, "M1 PB Legal", "reid","Community")
    except Exception as e:
        logging.exception("error in splitting data in ReidPBLegal")
