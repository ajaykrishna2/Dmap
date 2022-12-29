from Utility.save_output_to_folder import *
import logging

def splitting_westview(community_client_statement):
    try:
        # creating HOSPITAL tab
        HOSPITAL = community_client_statement.loc[
            (community_client_statement['Epic Type'].isin( ["HOSPITAL", "PHYSICIAN"] ))
            & (community_client_statement['System Type'] != "EPIC")
            & (community_client_statement['Client #'].isin(['6019I', '6019J'])),
            ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
            "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location", "System Type"]
            ]
        save_statement_to_output_folder.send_statement( HOSPITAL, "HOSPITAL", "westview","Community")
    except Exception as e:
        logging.exception( "error in splitting data in HOSPITAL" )

    try:
        # creating HOSPITAL tab
        PHYSICIAN = community_client_statement.loc[
            (community_client_statement['Epic Type'].isin( ["HOSPITAL", "PHYSICIAN", "UNDEFINED"] ))
            & (community_client_statement['System Type'] != "EPIC")
            & (community_client_statement['Client #'].isin( ['6019K', '6019M'] )),
            ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you"
            , "Due Agency", "Due You", "Client #", "First Name", "Last Name", "Ending Bal",
            "Epic Type", "Acct Location", "System Type"]
        ]
        save_statement_to_output_folder.send_statement( PHYSICIAN, "PHYSICIAN", "westview","Community")
    except Exception as e:
        logging.exception( "error in splitting data in PHYSICIAN" )
