from Utility.save_output_file import *
import logging
import sidetable

class good_samaritan:
    def __init__(self, gs_client_statement):  
        self.gs_client_statement = gs_client_statement 
        
    def splitting_gs_cbs_statement(self):
        try:
            # creating CBS tab
            cbs = self.gs_client_statement[0].loc[
                (self.gs_client_statement[0]['Client #'].isin(['238E25', '238INS', '238SPP','238ERP','238AWP','237E25',\
                '237INS', '237SPP','237ERP', '237AWP','237WCP','238WCP']))
                & (self.gs_client_statement[0]['System Type'] == "EPIC"),
                ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
                "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type", "System Type"]
                ]
            save_file = save_statement_to_output_folder()
            save_file.send_statement(cbs, "Sheet1", "Good_samaritan_CBS_statement","Good_Samaritan",self.gs_client_statement[1])
        except Exception as e:
            logging.exception( "error in splitting data in CBS" )

    def splitting_gs_med1_statement(self):
        try:
            # creating MED1 tab
            med1 = self.gs_client_statement[0].loc[
                (self.gs_client_statement[0]['Client #'].isin(['238I55', '238R25', '238R55', '238REC', '238SEC',\
                '239BD','238ECA', '237I55','237R25', '237R55', '237REC', '237SEC','237ECA']))
                & (self.gs_client_statement[0]['System Type'] == "EPIC"),
                ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Over Paid", "Pd to Agency", "PD to you", "Due Agency",
                "Due You", "Client #", "First Name", "Last Name", "Ending Bal", "Epic Type", "System Type"]
                ]    
            save_file = save_statement_to_output_folder()
            save_file.send_statement(med1, "Sheet1", "Good_samaritan_MED1_statement","Good_Samaritan",self.gs_client_statement[1])
        except Exception as e:
            logging.exception("error in splitting data in MED1") 

