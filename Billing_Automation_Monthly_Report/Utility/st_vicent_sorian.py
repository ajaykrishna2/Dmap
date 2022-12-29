from Utility.save_output_to_folder import *
import logging

def st_vicent_sorian(vincent_soarian_statement):
    try:
        # creating CARMEL AMB tab
        CARMEL_AMB = vincent_soarian_statement.loc[(vincent_soarian_statement['Client #'].isin(
            ['6416', '6417', '6418', '6419', '6420', '6425', '6430', '64E55'])), ["Client's Acct#", "Pmt Date", "Type",
                                                                                  "Pmt Amt", "Pd to Agency",
                                                                                  "PD to you", "Due Agency", "Due You",
                                                                                  "Client #", "First Name",
                                                                                  "Last Name"]]
        save_statement_to_output_folder.send_statement(CARMEL_AMB, "CARMEL AMB", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in CARME_AMB")

    try:
        # creating CARMEL tab
        CARMEL = vincent_soarian_statement.loc[
            (vincent_soarian_statement['Client #'].isin(['7016', '7017', '7018', '7020', '7025', '7030', '70E55'])), [
                "Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you", "Due Agency", "Due You",
                "Client #", "First Name", "Last Name"]]
        save_statement_to_output_folder.send_statement(CARMEL, "CARMEL", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in CARMEL")

    try:
        # creating CLAY tab

        CLAY = vincent_soarian_statement.loc[
            (vincent_soarian_statement['Client #'].isin(['4818', '4819', '5017', '5020', '5025', '5030', '50E55'])), [
                "Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you", "Due Agency", "Due You",
                "Client #", "First Name", "Last Name"]]
        save_statement_to_output_folder.send_statement(CLAY, "CLAY", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in CLAY")

    try:
        # creating DUNN tab

        DUNN = vincent_soarian_statement.loc[(vincent_soarian_statement['Client #'].isin(
            ['7216', '7217', '7218', '7219', '7220', '7225', '7230', '72E55'])), ["Client's Acct#", "Pmt Date", "Type",
                                                                                  "Pmt Amt", "Pd to Agency",
                                                                                  "PD to you", "Due Agency", "Due You",
                                                                                  "Client #", "First Name",
                                                                                  "Last Name"]]
        save_statement_to_output_folder.send_statement(DUNN, "DUNN", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in DUNN")

    try:
        # creating FISHERS tab

        FISHERS = vincent_soarian_statement.loc[(vincent_soarian_statement['Client #'].isin(
            ['6216', '6217', '6218', '6219', '6220', '6225', '6230', '62E55'])), ["Client's Acct#", "Pmt Date", "Type",
                                                                                  "Pmt Amt", "Pd to Agency",
                                                                                  "PD to you", "Due Agency", "Due You",
                                                                                  "Client #", "First Name",
                                                                                  "Last Name"]]
        save_statement_to_output_folder.send_statement(FISHERS, "FISHERS", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in FISHERS")

    try:
        # creating FRANKFORT tab

        FRANKFORT = vincent_soarian_statement.loc[(vincent_soarian_statement['Client #'].isin(
            ['5816', '5817', '5818', '5819', '5820', '5825', '5830', '36E55', '58E55'])), ["Client's Acct#", "Pmt Date",
                                                                                           "Type", "Pmt Amt",
                                                                                           "Pd to Agency", "PD to you",
                                                                                           "Due Agency", "Due You",
                                                                                           "Client #", "First Name",
                                                                                           "Last Name"]]
        save_statement_to_output_folder.send_statement(FRANKFORT, "FRANKFORT", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in FRANKFORT")

    try:
        # creating HEARTS tab

        HEARTS = vincent_soarian_statement.loc[
            (vincent_soarian_statement['Client #'].isin(['6316', '6317', '6318', '6320', '6325', '6330', '63E55'])), [
                "Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you", "Due Agency", "Due You",
                "Client #", "First Name", "Last Name"]]
        save_statement_to_output_folder.send_statement(HEARTS, "HEARTS", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in HEARTS")

    try:
        # creating JENNINGS tab

        JENNINGS = vincent_soarian_statement.loc[(vincent_soarian_statement['Client #'].isin(
            ['5716', '5717', '5718', '5719', '5720', '5725', '5730', '57E55', '47LNF', '47LF25', '47NH'])), [
                                                     "Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency",
                                                     "PD to you", "Due Agency", "Due You", "Client #", "First Name",
                                                     "Last Name"]]
        save_statement_to_output_folder.send_statement(JENNINGS, "JENNINGS", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in JENNINGS")

    try:
        # creating MERCY tab

        MERCY = vincent_soarian_statement.loc[(vincent_soarian_statement['Client #'].isin(
            ['5215', '5216', '5217', '5218', '5219', '5220', '5225', '5230', '52E55', '2025', '45FL25', '45SUIT'])), [
                                                  "Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency",
                                                  "PD to you", "Due Agency", "Due You", "Client #", "First Name",
                                                  "Last Name"]]
        save_statement_to_output_folder.send_statement(MERCY, "MERCY", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in MERCY")

    try:
        # creating NAAB RD tab

        NAAB_RD = vincent_soarian_statement.loc[(vincent_soarian_statement['Client #'].isin(
            ['6616', '6617', '6618', '6619', '6620', '6625', '6630', '66E55'])), ["Client's Acct#", "Pmt Date", "Type",
                                                                                  "Pmt Amt", "Pd to Agency",
                                                                                  "PD to you", "Due Agency", "Due You",
                                                                                  "Client #", "First Name",
                                                                                  "Last Name"]]
        save_statement_to_output_folder.send_statement(NAAB_RD, "NAAB RD", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in NAAB RD")

    try:
        # creating RANDOLPH tab

        RANDOLPH = vincent_soarian_statement.loc[(vincent_soarian_statement['Client #'].isin(
            ['5117', '5118', '5119', '5120', '5125', '5130', '51E55', '4918', '4919'])), ["Client's Acct#", "Pmt Date",
                                                                                          "Type", "Pmt Amt",
                                                                                          "Pd to Agency", "PD to you",
                                                                                          "Due Agency", "Due You",
                                                                                          "Client #", "First Name",
                                                                                          "Last Name"]]
        save_statement_to_output_folder.send_statement(RANDOLPH, "RANDOLPH", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in RANDOLPH")

    try:
        # creating SALEM tab

        SALEM = vincent_soarian_statement.loc[(vincent_soarian_statement['Client #'].isin(
            ['6116', '6117', '6118', '6119', '6120', '6125', '6130', '61E55'])), ["Client's Acct#", "Pmt Date", "Type",
                                                                                  "Pmt Amt", "Pd to Agency",
                                                                                  "PD to you", "Due Agency", "Due You",
                                                                                  "Client #", "First Name",
                                                                                  "Last Name"]]
        save_statement_to_output_folder.send_statement(SALEM, "SALEM", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in SALEM")

    try:
        # creating ST_JOE tab

        ST_JOE = vincent_soarian_statement.loc[(vincent_soarian_statement['Client #'].isin(
            ['6017', '6018', '6019', '6020', '6025', '6030', '60E55'])), ["Client's Acct#", "Pmt Date", "Type",
                                                                                   "Pmt Amt", "Pd to Agency",
                                                                                   "PD to you", "Due Agency", "Due You",
                                                                                   "Client #", "First Name",
                                                                                   "Last Name"]]
        save_statement_to_output_folder.send_statement(ST_JOE, "ST JOE", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in ST_JOE")

    try:
        # creating EVANSVILLE tab

        EVANSVILLE = vincent_soarian_statement.loc[(vincent_soarian_statement['Client #'].isin(
            ['3007', '5007', '190CL2', '190CLN', '190INS', '190SPP', '190C55', '190C66', '190I55', '190R25',
             '190R55'])), ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you", "Due Agency",
                           "Due You", "Client #", "First Name", "Last Name"]]
        save_statement_to_output_folder.send_statement(EVANSVILLE, "EVANSVILLE", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in EVANSVILLE")

    try:
        # creating ANDERSON tab

        ANDERSON = vincent_soarian_statement.loc[(vincent_soarian_statement['Client #'].isin(
            ['7116', '7117', '7118', '7119', '7120', '7125', '7130', '71E55'])), ["Client's Acct#", "Pmt Date", "Type",
                                                                                  "Pmt Amt", "Pd to Agency",
                                                                                  "PD to you", "Due Agency", "Due You",
                                                                                  "Client #", "First Name",
                                                                                  "Last Name"]]
        save_statement_to_output_folder.send_statement(ANDERSON, "ANDERSON", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in ANDERSON")

    try:
        # creating WILLIAMSPORT tab

        WILLIAMSPORT = vincent_soarian_statement.loc[(vincent_soarian_statement['Client #'].isin(
            ['5617', '5618', '5619', '5620', '5625', '5630', '56E55', '5116'])), ["Client's Acct#", "Pmt Date", "Type",
                                                                                  "Pmt Amt", "Pd to Agency",
                                                                                  "PD to you", "Due Agency", "Due You",
                                                                                  "Client #", "First Name",
                                                                                  "Last Name"]]
        save_statement_to_output_folder.send_statement(WILLIAMSPORT, "WILLIAMSPORT", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in WILLIAMSPORT")

    try:
        # creating INDPLS tab

        INDPLS = vincent_soarian_statement.loc[
            (vincent_soarian_statement['Client #'].isin(['7316', '7317', '7318', '7320', '7325', '7330', '73E55'])), [
                "Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you", "Due Agency", "Due You",
                "Client #", "First Name", "Last Name"]]
        save_statement_to_output_folder.send_statement(INDPLS, "INDPLS", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in INDPLS")

    try:
        # creating STRESS tab

        STRESS = vincent_soarian_statement.loc[
            (vincent_soarian_statement['Client #'].isin(['7416', '7417', '7418', '7420', '7425', '7430', '74E55'])), [
                "Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you", "Due Agency", "Due You",
                "Client #", "First Name", "Last Name"]]
        save_statement_to_output_folder.send_statement(STRESS, "STRESS", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in STRESS")

    try:
        # creating ENDOSCOPY tab

        ENDOSCOPY = vincent_soarian_statement.loc[
            (vincent_soarian_statement['Client #'].isin(['6516', '6517', '6518', '6519', '6520', '6525', '6530'])), [
                "Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you", "Due Agency", "Due You",
                "Client #", "First Name", "Last Name"]]
        save_statement_to_output_folder.send_statement(ENDOSCOPY, "ENDOSCOPY", "St_vicent_sorian","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in ENDOSCOPY")
