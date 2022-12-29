from Utility.save_output_file import *
import logging
import sidetable

class good_samaritan:
    def __init__(self, gs_client_statement):  
        self.gs_client_statement = gs_client_statement 

    def splitting_gs_cbs_statement(self):
        try:
            # creating CBS tab
            cbs = self.gs_client_statement.loc[
                (self.gs_client_statement['Client #'].isin(['239E25', '239INS', '239SPP','229WCP','229ERP']))
                & (self.gs_client_statement['System Type'] == "EPIC"),
                ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you", "Due Agency",
                "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type", "System Type"]
                ]
            save_file = save_statement_to_output_folder()
            save_file.send_statement(cbs, "Sheet1", "GOOD_SAMARITAN_FAMILY_HEALTH_CBS_STATEMENT","Good_Samaritan_Family")
        except Exception as e:
            logging.exception( "error in splitting data in CBS" )

    def splitting_gs_med1_statement(self):
        try:
            # creating MED1 tab
            med1 = self.gs_client_statement.loc[
                (self.gs_client_statement['Client #'].isin(['239I55', '239R25', '239R55']))
                & (self.gs_client_statement['System Type'] == "EPIC"),
                ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you", "Due Agency",
                "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type", "System Type"]
                ]    
            save_file = save_statement_to_output_folder()
            save_file.send_statement(med1, "Sheet1", "GOOD_SAMARITAN_FAMILY_HEALTH_MED-1_STATEMENT","Good_Samaritan_Family")
        except Exception as e:
            logging.exception("error in splitting data in MED1") 

