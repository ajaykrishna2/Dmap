from Utility.save_output_to_folder import *
import logging

def splitting_vei_surgery_cbs(community_client_statement):
    try:
        # creating EASTCAMPUSSURGERYCENTER tab
        EASTCAMPUSSURGERYCENTER = community_client_statement.loc[
            (community_client_statement['Epic Type'].isin(["UNDEFINED", "VEI"]))
          & (community_client_statement['System Type'] == "EPIC")
          & (community_client_statement['Acct Location'] == "EAST CAMPUS SURGERY CENTER LLC-ISC EAST")
          & (community_client_statement['Client #'].isin(['5019V', '50VERP', '50VM25', '50VWCP', '50VWPP'])),
          ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
          "Due You", "Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
          "System Type"]
          ]

        save_statement_to_output_folder.send_statement(EASTCAMPUSSURGERYCENTER, "5019EC", "VEI_surgery_cbs","Community")
    except Exception as e:
        logging.exception("error in splitting data in CommunityEndoscopy")

    try:
        # creating HAMILTONSURGERYCENTER tab
        HAMILTONSURGERYCENTER = community_client_statement.loc[
            (community_client_statement['Epic Type'].isin(["UNDEFINED", "VEI"]))
          & (community_client_statement['System Type'] == "EPIC")
          & (community_client_statement['Acct Location'] == "HAMILTON SURGERY CENTER LLC-ISC NOBLESVILLE")
          & (community_client_statement['Client #'].isin(['5019V', '50VERP', '50VM25', '50VWCP', '50VWPP'])),
          ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
          "Due You", "Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
          "System Type"]
          ]

        save_statement_to_output_folder.send_statement(HAMILTONSURGERYCENTER, "5019HS", "VEI_surgery_cbs","Community")
    except Exception as e:
        logging.exception("error in splitting data in CommunityEastCampus")

    try:
        # creating NORTHCAMPUSSURGERYCENTER tab
        NORTHCAMPUSSURGERYCENTER = community_client_statement.loc[
            (community_client_statement['Epic Type'].isin(["UNDEFINED", "VEI"]))
          & (community_client_statement['System Type'] == "EPIC")
          & (community_client_statement['Acct Location'] == "NORTH CAMPUS SURGERY CENTER LLC-ISC NORTH")
          & (community_client_statement['Client #'].isin(['5019V', '50VERP', '50VM25', '50VWCP', '50VWPP'])),
          ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
          "Due You", "Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
          "System Type"]
          ]

        save_statement_to_output_folder.send_statement(NORTHCAMPUSSURGERYCENTER, "5019NC", "VEI_surgery_cbs","Community")
    except Exception as e:
        logging.exception("error in splitting data in CommunityEastCampus")

    try:
        # creating SOUTHCAMPUSSURGERYCENTER tab
        SOUTHCAMPUSSURGERYCENTER = community_client_statement.loc[
            (community_client_statement['Epic Type'].isin(["UNDEFINED", "VEI"]))
          & (community_client_statement['System Type'] == "EPIC")
          & (community_client_statement['Acct Location'] == "SOUTH CAMPUS SURGERY CENTER LLC-ISC SOUTH")
          & (community_client_statement['Client #'].isin(['5019V', '50VERP', '50VM25', '50VWCP', '50VWPP'])),
          ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
          "Due You", "Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
          "System Type"]
          ]

        save_statement_to_output_folder.send_statement(SOUTHCAMPUSSURGERYCENTER, "5019SC", "VEI_surgery_cbs","Community")
    except Exception as e:
        logging.exception("error in splitting data in CommunityEastCampus")

    try:
        # creating STONESCROSSING tab
        STONESCROSSING = community_client_statement.loc[
            (community_client_statement['Epic Type'].isin(["UNDEFINED", "VEI"]))
            & (community_client_statement['System Type'] == "EPIC")
            & (community_client_statement['Acct Location'].isin(["STONES CROSSING IMAGING SERVICES",
                                                                 "STONES CROSSING PHYSICAL THERAPY AND REHAB",
                                                                 "STONES CROSSING FAMILY MEDICINE AND PEDIATRICS"]))
            & (community_client_statement['Client #'].isin(['5019V', '50VERP', '50VM25', '50VWCP', '50VWPP'])),
            ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
             "Due You", "Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
             "System Type"]
        ]

        save_statement_to_output_folder.send_statement(STONESCROSSING, "5019IS", "VEI_surgery_cbs","Community")
    except Exception as e:
        logging.exception("error in splitting data in CommunityEastCampus")

    try:
        # creating CBSImaging  tab
        CBSImaging = community_client_statement.loc[
            (community_client_statement['Epic Type'].isin(["UNDEFINED", "VEI"]))
            & (community_client_statement['System Type'] == "EPIC")
            & (community_client_statement['Acct Location'].isin(["Community Imaging Associates Saxony",
                                                                 "Community Imaging Associates Washington Square Pavilion",
                                                                 "Community Imaging Associates Breast Diag Ctr Carmel",
                                                                 "HOWARD CAMPUS SURGERY CENTER LLC-ISC KOKOMO"]))
            & (community_client_statement['Client #'].isin(['5019V', '50VERP', '50VM25', '50VWCP', '50VWPP'])),
            ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
             "Due You", "Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
             "System Type"]
        ]

        save_statement_to_output_folder.send_statement(CBSImaging, "CBS Imaging", "VEI_surgery_cbs","Community")
    except Exception as e:
        logging.exception("error in splitting data in CommunityEastCampus")
