from Utility.save_output_to_folder import *
import logging

class st_vicent_non_facs:
    def splitting_d1_accident_statement(vincent_statement):
        try:
            # creating Accident tab
            accident = vincent_statement.loc[(vincent_statement['Client #'].isin(
                ['190ERP', '36D1', '36ERP', '37D1', '37ERP', '38D1', '38ERP', '39D1', '39ERP', '40D1', '40ERP', '41D1',
                 '41ERP', '42D1', '42ERP', '49D1', '49ERP', '50D1', '50ERP', '51D1', '51ERP', '52D1', '52ERP', '56D1',
                 '56ERP', '57D1', '57ERP', '58D1', '58ERP', '59ERP', '60ERP', '61ERP', '62ERP', '63ERP', '64ERP', '65ERP',
                 '66D1', '66ERP', '70ERP', '71ERP', '72ERP', '73D1', '73ERP', '74D1', '74ERP', '75ERP', '76ERP', '40WD1',
                 '40WERP'])), ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you", "Due Agency",
                               "Due You", "Client #", "First Name", "Last Name"]]
            save_statement_to_output_folder.send_statement(accident, "d1_acciednt", "day1_accident_statement","St_Vincent")
        except Exception as e:
            logging.exception("error in splitting data in Accident")


    def splitting_d1_wc_statement(vincent_statement):
        try:
            # creating wc tab
            d1_wc_statement = vincent_statement.loc[(vincent_statement['Client #'].isin(
                ['39PP', '39WC', '1016PP', '1033', '1033PP', '1046PP', '1046WC', '190WC', '190WCP', '191WCP', '37PP',
                 '37WC', '37WCP', '41PP', '41WC', '4216PP', '4216WC', '45WC', '47WC', '5033PP', '5033WC', '5137PP',
                 '5137WC', '5237PP', '5237WC', '52PP', '52WC', '5646PP', '5646WC', '5737PP', '5737WC', '57PP', '57WC',
                 '5837PP', '5837WC', '6037PP', '6037WC', '6137PP', '6137WC', '6237PP', '6237WC', '6337PP', '6337WC',
                 '6437PP', '6437WC', '64PP', '64WC', '6537PP', '6537WC', '6637PP', '6637WC', '66PP', '66WC', '7037PP',
                 '7037WC', '70PP', '70WC', '71PP', '71WC', '72PP', '72WC', '73PP', '73WC', '74PP', '74WC'])) | (
                                                        vincent_statement['Client #'].isin(
                                                            ['39PP', '39WC', '1016PP', 1033, '1033PP', '1046PP', '1046WC',
                                                             '190WC', '190WCP', '191WCP', '37PP', '37WC', '37WCP', '41PP',
                                                             '41WC', '4216PP', '4216WC', '45WC', '47WC', '5033PP', '5033WC',
                                                             '5137PP', '5137WC', '5237PP', '5237WC', '52PP', '52WC',
                                                             '5646PP', '5646WC', '5737PP', '5737WC', '57PP', '57WC',
                                                             '5837PP', '5837WC', '6037PP', '6037WC', '6137PP', '6137WC',
                                                             '6237PP', '6237WC', '6337PP', '6337WC', '6437PP', '6437WC',
                                                             '64PP', '64WC', '6537PP', '6537WC', '6637PP', '6637WC', '66PP',
                                                             '66WC', '7037PP', '7037WC', '70PP', '70WC', '71PP', '71WC',
                                                             '72PP', '72WC', '73PP', '73WC', '74PP', '74WC'])), [
                                                        "Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency",
                                                        "PD to you", "Due Agency", "Due You", "Client #", "First Name",
                                                        "Last Name"]]
            save_statement_to_output_folder.send_statement(d1_wc_statement, "d1_wc_statement", "day1_WC_statement","St_Vincent")
        except Exception as e:
            logging.exception("error in splitting data in d1_wc_statement")


    def splitting_pbs_statement(vincent_statement):
        try:
            # creating pbs tab
            pbs_statement = vincent_statement.loc[(vincent_statement['Client #'].isin(
                ['49E55', '1040-3', '1040-4', '2040-3', '2040-4', '5040-3', '5040-4', '5040-6', '5050-3', '5050-4',
                 '5050-6', '2040'])) | (vincent_statement['Client #'].isin(
                ['49E55', '1040-3', '1040-4', '2040-3', '2040-4', '5040-3', '5040-4', '5040-6', '5050-3', '5050-4',
                 '5050-6', 2040])), ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you",
                                     "Due Agency", "Due You", "Client #", "First Name", "Last Name"]]
            save_statement_to_output_folder.send_statement(pbs_statement, "PBS_data", "PBS_statement","St_Vincent")
        except Exception as e:
            logging.exception("error in splitting data in pbs_statement")


    def St_Vincent_PBS_Athena(vincent_statement):
        try:
             # creating PBS_Athena tab
             PBS_Athena = vincent_statement.loc[(vincent_statement['Client #'].isin(
             ['ATH01', 'ATH101', 'ATH102', 'ATH103', 'ATH104', 'ATH164', 'ATH21', 'ATH22', 'ATH23', 'ATH24', 'ATH25',\
             'ATH26', 'ATH41', 'ATH61', 'ATH62', 'ATH63', 'ATH64'])), ["Client's Acct#", "Pmt Date", "Type",
                                                                                   "Pmt Amt", "Pd to Agency",
                                                                                   "PD to you", "Due Agency", "Due You",
                                                                                   "Client #", "First Name",
                                                                                   "Last Name"]]
             save_statement_to_output_folder.send_statement(PBS_Athena, "PBS_Athena","PBS_Athena_Statement","St_Vincent")
        except Exception as e:
             logging.exception("Error in splitting data in PBS_Athena")
