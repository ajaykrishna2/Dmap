from Utility.save_output_to_folder import *
import logging

def splitting_vei(community_client_statement):
    try:
        # creating VEIImagingCenter tab
        VEIImagingCenter_statement = community_client_statement.loc[
                              (community_client_statement['Epic Type'] == "VEI")
                            & (community_client_statement['System Type'] == "EPIC")
                            & (community_client_statement['Client #'].isin(['6019V'])),
                            ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you"
                            , "Due Agency", "Due You", "Client #", "Fee", "First Name", "Last Name", "Ending Bal",
                            "Epic Type", "Acct Location", "System Type"]
                            ]
        save_statement_to_output_folder.send_statement(VEIImagingCenter_statement, "VEIImagingCenter",
                                        "VEI_imaging_center","Community")
    except Exception as e:
        logging.exception("error in splitting data in VEIImagingCenter")
