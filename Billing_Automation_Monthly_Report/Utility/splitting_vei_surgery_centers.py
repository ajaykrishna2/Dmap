from Utility.save_output_to_folder import *
import logging

def splitting_vei_surgery_centers(community_client_statement):
    try:
        # creating CommunityEndoscopy tab
        CommunityEndoscopy = community_client_statement.loc[
                ((community_client_statement['Epic Type'] == "VEI") | (community_client_statement['Epic Type'] == "PHYSICIAN")
                | (community_client_statement['Epic Type'] == "HOSPITAL"))
                & (community_client_statement['System Type'] == "EPIC")
                & (community_client_statement['Client #'].isin(['5019CE'])),
                ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you","Due Agency",
                "Due You", "Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
                 "System Type"]
                ]
        save_statement_to_output_folder.send_statement(CommunityEndoscopy, "5019CE", "VEI_surgery_centers","Community")
    except Exception as e:
        logging.exception("error in splitting data in CommunityEndoscopy")

    try:
        # creating CommunityEastCampus tab
        CommunityEastCampus = community_client_statement.loc[
                ((community_client_statement['Epic Type'] == "VEI") | (community_client_statement['Epic Type'] == "PHYSICIAN")
                | (community_client_statement['Epic Type'] == "HOSPITAL"))
                & (community_client_statement['System Type']== "EPIC")
                & (community_client_statement['Client #'].isin(['5019EC'])),
                ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency"
                , "Due You", "Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
                 "System Type"]
                ]

        save_statement_to_output_folder.send_statement(CommunityEastCampus, "5019EC", "VEI_surgery_centers","Community")
    except Exception as e:
        logging.exception("error in splitting data in CommunityEastCampus")

    try:
        # creating HowardCampus tab
        HowardCampus = community_client_statement.loc[
                ((community_client_statement['Epic Type'] == "VEI") | (community_client_statement['Epic Type'] == "PHYSICIAN")
                | (community_client_statement['Epic Type'] == "HOSPITAL"))
                & (community_client_statement['System Type']== "EPIC")
                & (community_client_statement['Client #'].isin(['5019HC'])),
                ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency"
                , "Due You", "Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
                 "System Type"]
                ]
        save_statement_to_output_folder.send_statement(HowardCampus, "5019HC", "VEI_surgery_centers","Community")
    except Exception as e:
        logging.exception("error in splitting data in HowardCampus")

    try:
        # creating HamiltonSurgeryCenter tab
        HamiltonSurgeryCenter = community_client_statement.loc[
                ((community_client_statement['Epic Type'] == "VEI") | (community_client_statement['Epic Type'] == "PHYSICIAN")
                | (community_client_statement['Epic Type'] == "HOSPITAL"))
                & (community_client_statement['System Type'] == "EPIC")
                & (community_client_statement['Client #'].isin(['5019HS'])),
                ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency"
                , "Due You","Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
                 "System Type"]
                ]

        save_statement_to_output_folder.send_statement(HamiltonSurgeryCenter, "5019HS", "VEI_surgery_centers","Community")
    except Exception as e:
        logging.exception("error in splitting data in HamiltonSurgeryCenter")

    try:
        # creating IndianapolisEndoscopyCenter tab
        IndianapolisEndoscopyCenter = community_client_statement.loc[
                ((community_client_statement['Epic Type'] == "VEI") | (community_client_statement['Epic Type'] == "PHYSICIAN")
                | (community_client_statement['Epic Type'] == "HOSPITAL"))
                & (community_client_statement['System Type']== "EPIC")
                & (community_client_statement['Client #'].isin(['5019IE'])),
                ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency"
                , "Due You", "Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
                 "System Type"]
                ]
        save_statement_to_output_folder.send_statement(IndianapolisEndoscopyCenter, "5019IE", "VEI_surgery_centers","Community")
    except Exception as e:
        logging.exception("error in splitting data in IndianapolisEndoscopyCenter")

    try:
        # creating StonesCrossingImagingServices tab
        StonesCrossingImagingServices = community_client_statement.loc[
                  ((community_client_statement['Epic Type'] == "VEI") | (community_client_statement['Epic Type'] == "PHYSICIAN")
                | (community_client_statement['Epic Type'] == "HOSPITAL"))
                & (community_client_statement['System Type'] == "EPIC")
                & (community_client_statement['Client #'].isin(['5019IS'])),
                ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency"
                , "Due You", "Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
                "System Type"]
                ]
        save_statement_to_output_folder.send_statement(StonesCrossingImagingServices, "5019IS", "VEI_surgery_centers","Community")
    except Exception as e:
        logging.exception("error in splitting data in StonesCrossingImagingServices")

    try:
        # creating NorthCampusSurgeryCenter tab
        NorthCampusSurgeryCenter = community_client_statement.loc[
                ((community_client_statement['Epic Type'] == "VEI") | (community_client_statement['Epic Type'] == "PHYSICIAN")
                | (community_client_statement['Epic Type'] == "HOSPITAL"))
                & (community_client_statement['System Type']== "EPIC")
                & (community_client_statement['Client #'].isin(['5019NC'])),
                ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency"
                , "Due You", "Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
                "System Type"]
                ]
        save_statement_to_output_folder.send_statement(NorthCampusSurgeryCenter, "5019NC", "VEI_surgery_centers","Community")
    except Exception as e:
        logging.exception("error in splitting data in NorthCampusSurgeryCenter")

    try:
        # creating StonesCrossingPhysicalTherapyandRehab tab
        StonesCrossingPhysicalTherapyandRehab = community_client_statement.loc[
             ((community_client_statement['Epic Type'] == "VEI") | (community_client_statement['Epic Type'] == "PHYSICIAN")
                | (community_client_statement['Epic Type'] == "HOSPITAL"))
             & (community_client_statement['System Type']== "EPIC")
             & (community_client_statement['Client #'].isin(['5019PT'])),
             ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
             "Due You","Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
             "System Type"]
             ]
        save_statement_to_output_folder.send_statement(StonesCrossingPhysicalTherapyandRehab, "5019PT", "VEI_surgery_centers","Community")
    except Exception as e:
        logging.exception("error in splitting data in StonesCrossingPhysicalTherapyandRehab")

    try:
        # creating SouthCampusSurgeryCenter tab
        SouthCampusSurgeryCenter = community_client_statement.loc[
            ((community_client_statement['Epic Type'] == "VEI") | (community_client_statement['Epic Type'] == "PHYSICIAN")
                | (community_client_statement['Epic Type'] == "HOSPITAL"))
            & (community_client_statement['System Type']== "EPIC")
            & (community_client_statement['Client #'].isin(['5019SC'])),
            ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
            "Due You", "Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
            "System Type"]
            ]
        save_statement_to_output_folder.send_statement(SouthCampusSurgeryCenter, "5019SC", "VEI_surgery_centers","Community")
    except Exception as e:
        logging.exception("error in splitting data in SouthCampusSurgeryCenter")

    try:
        # creating SCPIndianapolis tab
        SCPIndianapolis = community_client_statement.loc[
           ((community_client_statement['Epic Type'] == "VEI") | (community_client_statement['Epic Type'] == "PHYSICIAN")
                | (community_client_statement['Epic Type'] == "HOSPITAL"))
           & (community_client_statement['System Type']== "EPIC")
           & (community_client_statement['Client #'].isin(['5019SP'])),
           ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
           "Due You", "Client #", "Fee", "First Name", "Last Name", "Ending Bal", "Epic Type", "Acct Location",
            "System Type"]
           ]
        save_statement_to_output_folder.send_statement(SCPIndianapolis, "5019SP", "VEI_surgery_centers","Community")
    except Exception as e:
        logging.exception("error in splitting data in SCPIndianapolis")