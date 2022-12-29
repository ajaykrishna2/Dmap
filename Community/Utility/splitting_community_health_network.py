from Utility.save_output_to_folder import *
import logging

def splitting_community_health_network_statement(community_client_statement):
    # creating M1HB tab
    try:
        M1HB = community_client_statement.loc[
              (community_client_statement['Epic Type'] == "HOSPITAL")
            & (community_client_statement['Legal Reported'].isnull())
            & (community_client_statement['STAR CONVERT Acct'].isnull())
            & (community_client_statement['Acct Location'] != "Community Cancer Center Howard")
            & (community_client_statement['System Type'] == "EPIC")
            & (community_client_statement['Client #'].isin(['6019A', '6019B', '6019C', '6019D', '6019E', '6019F', '6019G', '6019L'
            , '2019', '2019D', '7019A', '7019D', '2019B', '7019B', '2019C', '7019C','7019G'])),
            ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt"
            , "Over Paid", "Pd to Agency", "PD to you", "Due Agency", "Due You", "Client #", "First Name", "Last Name"
            , "Ending Bal", "Epic Type", "Acct Location", "System Type"]
        ]
        save_statement_to_output_folder.send_statement(M1HB, "M1_HB","community_health_network","Community")
    except Exception as e:
        logging.exception("error in splitting data in M1HB")

    # creating M1PB tab
    try:
        M1PB = community_client_statement.loc[
              (community_client_statement['Epic Type'] == "PHYSICIAN")
            & (community_client_statement['Legal Reported'].isnull())
            & (community_client_statement['STAR CONVERT Acct'].isnull())
            & (community_client_statement['Acct Location'] != "Community Cancer Center Howard")
            & (community_client_statement['System Type'] == "EPIC")
            & (community_client_statement['Client #'].isin(['6019A', '6019B', '6019C', '6019D', '6019E', '6019F', '6019G', '6019L'
            , '2019', '2019D', '7019A', '7019D', '2019B', '7019B', '2019C', '7019C','7019G'])), 
            ["Client's Acct#","Pmt Date", "Type"
            , "Pmt Amt","Over Paid", "Pd to Agency","PD to you", "Due Agency","Due You", "Client #", "First Name"
            , "Last Name", "Ending Bal","Epic Type", "Acct Location", "System Type"]
        ]
        save_statement_to_output_folder.send_statement(M1PB, "M1_PB", "community_health_network","Community")
    except Exception as e:
        logging.exception("error in splitting data in M1PB")

    # creating CBSHB tab
    try:
        CBSHB = community_client_statement.loc[
              (community_client_statement['Epic Type'] == "HOSPITAL")
            & (community_client_statement['Legal Reported'].isnull())
            & (community_client_statement['STAR CONVERT Acct'].isnull())
            & (community_client_statement['System Type'] == "EPIC")
            & (community_client_statement['Client #'].isin(['5019', '5019B', '5019C', '50AERP', '50AM25', '50AWCP', '50AWPP'
            , '50BERP', '50BM25', '50BWCP', '50BWPP', '50CERP', '50CM25', '50CWCP', '50WCPP', '50GERP', '50GM25', '50GWCP'
            , '50GWPP', '8019A', '8019B', '8019C', '8019D', '5019MK', '1019'])), ["Client's Acct#"
            , "Pmt Date", "Type","Pmt Amt", "Over Paid", "Pd to Agency","PD to you", "Due Agency", "Due You","Client #"
            , "First Name", "Last Name","Ending Bal","Epic Type", "Acct Location", "System Type"]
        ]

        save_statement_to_output_folder.send_statement(CBSHB, "CBS_HB", "community_health_network","Community")
    except Exception as e:
        logging.exception("error in splitting data in CBSHB")

        # creating M1LegalHB tab
    try:
        M1LegalHB = community_client_statement.loc[
              (community_client_statement['Epic Type'] == "HOSPITAL")
            & (community_client_statement['Legal Reported'] == "YES")
            & (community_client_statement['System Type'] == "EPIC")
            & (community_client_statement['Acct Location'] != "Community Cancer Center Howard")
            & (community_client_statement['Client #'].isin(['6019A', '6019B', '6019C', '6019D', '6019E', '6019F', '6019G', '6019L'
            , '2019', '2019D', '7019A', '7019D', '2019B', '7019B', '2019C', '7019C','6019H','7019G','5019', '5019B', '5019C', '50AERP'
            , '50AM25', '50AWCP', '50AWPP', '50BERP', '50BM25', '50BWCP', '50BWPP', '50CERP', '50CM25', '50CWCP', '50WCPP', '50GERP'
            , '50GM25', '50GWCP', '50GWPP', '8019A', '8019B', '8019C', '8019D', '5019MK', '1019'])),
            ["Client's Acct#","Pmt Date", "Type", "Pmt Amt","Over Paid", "Pd to Agency"
            ,"PD to you", "Due Agency","Due You", "Client #", "First Name","Last Name", "Ending Bal","Epic Type"
            , "Acct Location","System Type"]
        ]
        save_statement_to_output_folder.send_statement(M1LegalHB, "M1_Legal_HB", "community_health_network","Community")
    except Exception as e:
        logging.exception("error in splitting data in M1LegalHB")

    # creating M1LegalPB tab
    try:
        M1LegalPB = community_client_statement.loc[
              (community_client_statement['Epic Type'] == "PHYSICIAN")
            & (community_client_statement['Legal Reported'] == "YES")
            & (community_client_statement['System Type'] == "EPIC")
            & (community_client_statement['Acct Location'] != "Community Cancer Center Howard")
            & (community_client_statement['Client #'].isin(['6019A', '6019B', '6019C', '6019D', '6019E', '6019F', '6019G', '6019L'
            , '2019', '2019D', '7019A', '7019D', '2019B', '7019B', '2019C', '7019C','6019H','7019G'])), 
            ["Client's Acct#", "Pmt Date", "Type","Pmt Amt", "Over Paid", "Pd to Agency", "PD to you"
            , "Due Agency", "Due You", "Client #", "First Name", "Last Name", "Ending Bal","Epic Type", "Acct Location",
            "System Type"]
        ]
        save_statement_to_output_folder.send_statement(M1LegalPB, "M1_Legal_PB", "community_health_network","Community")
    except Exception as e:
        logging.exception("error in splitting data in M1LegalPB")

    # creating StarConverted tab
    try:
        StarConverted = community_client_statement.loc[
              (community_client_statement['Epic Type'] == "HOSPITAL")
            & (community_client_statement['Legal Reported'].isnull())
            & (community_client_statement['Client #'].isin(['6019A','6019B','6019C','6019D','6019E','6019L','5019','5019B',
             '5019C','2019','2019B','2019C','2019D','7019A','7019B','7019C','7019D']))
            & (community_client_statement['STAR CONVERT Acct'].notnull()), ["Client's Acct#", "Pmt Date","Type"
            , "Pmt Amt", "Over Paid","Pd to Agency", "PD to you", "Due Agency","Due You", "Client #","First Name"
            , "Last Name", "Ending Bal","Epic Type", "Acct Location", "System Type"]
        ]
        save_statement_to_output_folder.send_statement(StarConverted, "Star_Converted", "community_health_network","Community")
    except Exception as e:
        logging.exception("error in splitting data in StarConverted")

    # creating HBOC tab
    try:
        M1HBOC = community_client_statement.loc[
             ((community_client_statement['Epic Type'] == "HBOC") & (community_client_statement['Client #'].isin(
             ['6019A', '6019B', '6019C', '6019D', '6019E', '6019F', '6019L', '2019', '2019D', '7019A', '7019D', '2019B', '7019B', '2019C', '7019C'])))
             , ["Client's Acct#", "Pmt Date", "Type","Pmt Amt"
             , "Over Paid", "Pd to Agency", "PD to you","Due Agency", "Due You", "Client #","First Name", "Last Name"
             , "Ending Bal", "Epic Type","Acct Location", "System Type"]
        ]
        save_statement_to_output_folder.send_statement(M1HBOC, "M1_HBOC", "community_health_network","Community")
    except Exception as e:
        logging.exception("error in splitting data in HBOC")

        # creating CBSHBOC tab
    try:
        CBSHBOC = community_client_statement.loc[
              (community_client_statement['Epic Type'] == "HBOC")
            & (community_client_statement['Client #'].isin(['5019', '5019B', '5019C', '5019D'])),["Client's Acct#"
            , "Pmt Date", "Type","Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency", "Due You"
            , "Client #","First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location", "System Type"]
        ]
        save_statement_to_output_folder.send_statement(CBSHBOC, "CBS_HBOC", "community_health_network","Community")
    except Exception as e:
        logging.exception("error in splitting data in CBSHBOC")
