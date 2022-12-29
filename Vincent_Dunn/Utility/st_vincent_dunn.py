from Utility.save_output_to_folder_dunn import *
import logging

class st_vicent_non_facs_dunn:
   @classmethod
   def splitting_vincent_dunn_statement(cls,vincent_statement):
        try:
            # creating dunn tab
            dunn_statement = vincent_statement.loc[
                (vincent_statement['Client #'].isin([2014])) | (vincent_statement['Client #'].isin(['2014'])), [
                    "Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you", "Due Agency", "Due You",
                    "Client #", "First Name", "Last Name"]]
            save_dunn_statement_to_output_folder.send_statement(dunn_statement, "DUNN_data", "DUNN_statement","St_Vincent_Dunn")
        except Exception as e:
            logging.exception("error in splitting data in dunn_statement")

