from Utility.save_output_to_folder import *
import logging


def st_vicent_invission(vincent_invision_statement):
    try:
        # creating CARMEL tab
        CARMEL = vincent_invision_statement.loc[(vincent_invision_statement['Client #'].isin(
            ['4210', '4216', '4217', '4218', '4219', '4220', '4225', '4230', '42025', '42055', '42CAS', '42L055',
             '42L25', '42LF20', '42LF25', '42LN25', '42LNF', '42LSP', '42E55'])), ["Client's Acct#", "Pmt Date", "Type",
                                                                                   "Pmt Amt", "Pd to Agency",
                                                                                   "PD to you", "Due Agency", "Due You",
                                                                                   "Client #", "First Name",
                                                                                   "Last Name"]]
        save_statement_to_output_folder.send_statement(CARMEL, "CARMEL", "St_vicent_invission","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in CARMEL")

    try:
        # creating CLAY tab

        CLAY = vincent_invision_statement.loc[
            (vincent_invision_statement['Client #'].isin(['2033'])), ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt",
                                                                      "Pd to Agency", "PD to you", "Due Agency",
                                                                      "Due You", "Client #", "First Name", "Last Name"]]
        save_statement_to_output_folder.send_statement(CLAY, "CLAY", "St_vicent_invission","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in CLAY")

    try:
        # creating DUNN tab

        DUNN = vincent_invision_statement.loc[(vincent_invision_statement['Client #'].isin(
            ['201432', '206E25', '206I55', '206INS', '206R25', '206R55', '206SPP'])), ["Client's Acct#", "Pmt Date",
                                                                                       "Type", "Pmt Amt",
                                                                                       "Pd to Agency", "PD to you",
                                                                                       "Due Agency", "Due You",
                                                                                       "Client #", "First Name",
                                                                                       "Last Name"]]
        save_statement_to_output_folder.send_statement(DUNN, "DUNN", "St_vicent_invission","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in DUNN")

    try:
        # creating FRANKFORT tab

        FRANKFORT = vincent_invision_statement.loc[(vincent_invision_statement['Client #'].isin(
            ['1020', '2020', '3020', '1020PP', '2020JU', '2020PC', '2020EO'])), ["Client's Acct#", "Pmt Date", "Type",
                                                                                 "Pmt Amt", "Pd to Agency", "PD to you",
                                                                                 "Due Agency", "Due You", "Client #",
                                                                                 "First Name", "Last Name"]]
        save_statement_to_output_folder.send_statement(FRANKFORT, "FRANKFORT", "St_vicent_invission","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in FRANKFORT")

    try:
        # creating HEARTS tab

        HEART = vincent_invision_statement.loc[(vincent_invision_statement['Client #'].isin(
            ['2117', '2039', '3916', '3917', '3918', '3920', '3925', '3930', '39E55', '2118', '2119'])), [
                                                   "Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency",
                                                   "PD to you", "Due Agency", "Due You", "Client #", "First Name",
                                                   "Last Name"]]
        save_statement_to_output_folder.send_statement(HEART, "HEART", "St_vicent_invission","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in HEART")

    try:
        # creating JENNINGS tab

        JENNINGS = vincent_invision_statement.loc[(vincent_invision_statement['Client #'].isin(
            ['47LN25', '4710', '4717', '4718', '4719', '4720', '4725', '4730', '47LF20', '47SP'])), ["Client's Acct#",
                                                                                                     "Pmt Date", "Type",
                                                                                                     "Pmt Amt",
                                                                                                     "Pd to Agency",
                                                                                                     "PD to you",
                                                                                                     "Due Agency",
                                                                                                     "Due You",
                                                                                                     "Client #",
                                                                                                     "First Name",
                                                                                                     "Last Name"]]
        save_statement_to_output_folder.send_statement(JENNINGS, "JENNINGS", "St_vicent_invission","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in JENNINGS")

    try:
        # creating MERCY tab

        MERCY = vincent_invision_statement.loc[
            (vincent_invision_statement['Client #'].isin(['4517', '4518', '4519', '4520', '4525', '4530', '45FL20'])), [
                "Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you", "Due Agency", "Due You",
                "Client #", "First Name", "Last Name"]]
        save_statement_to_output_folder.send_statement(MERCY, "MERCY", "St_vicent_invission","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in MERCY")

    try:
        # creating RANDOLPH tab

        RANDOLPH = vincent_invision_statement.loc[
            (vincent_invision_statement['Client #'].isin(['2037', '2037MC'])), ["Client's Acct#", "Pmt Date", "Type",
                                                                                "Pmt Amt", "Pd to Agency", "PD to you",
                                                                                "Due Agency", "Due You", "Client #",
                                                                                "First Name", "Last Name"]]
        save_statement_to_output_folder.send_statement(RANDOLPH, "RANDOLPH", "St_vicent_invission","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in RANDOLPH")

    try:
        # creating SALEM tab

        SALEM = vincent_invision_statement.loc[(vincent_invision_statement['Client #'].isin(
            ['2150', '2217', '2218', '2219', 'WCMH', '20517', '20518', '20519', '205I55', '205R25', '205R55'])), [
                                                   "Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency",
                                                   "PD to you", "Due Agency", "Due You", "Client #", "First Name",
                                                   "Last Name"]]
        save_statement_to_output_folder.send_statement(SALEM, "SALEM", "St_vicent_invission","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in SALEM")

    try:
        # creating ST_JOE tab

        ST_JOE = vincent_invision_statement.loc[
            (vincent_invision_statement['Client #'].isin(['6050', '1030', '2030', '3030', '2030MC','59E55'])), [
                "Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you", "Due Agency", "Due You",
                "Client #", "First Name", "Last Name"]]
        save_statement_to_output_folder.send_statement(ST_JOE, "ST JOE", "St_vicent_invission","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in ST_JOE")

    try:
        # creating ANDERSON tab

        ANDERSON = vincent_invision_statement.loc[(vincent_invision_statement['Client #'].isin(
            ['1021', '2021', '3018', '3021', '37E55', '4021', '4023', '4024', '4321', '4421', '4521', '3017',
             '4022'])), ["Client's Acct#", "Pmt Date", "Type", "Pmt Amt", "Pd to Agency", "PD to you", "Due Agency",
                         "Due You", "Client #", "First Name", "Last Name"]]
        save_statement_to_output_folder.send_statement(ANDERSON, "ANDERSON", "St_vicent_invission","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in ANDERSON")

    try:
        # creating WILLIAMSPORT tab

        WILLIAMSPORT = vincent_invision_statement.loc[(vincent_invision_statement['Client #'].isin(
            ['4617', '4618', '4619', '4620', '4625', '4630', '46LF20', '46LF25'])), ["Client's Acct#", "Pmt Date",
                                                                                     "Type", "Pmt Amt", "Pd to Agency",
                                                                                     "PD to you", "Due Agency",
                                                                                     "Due You", "Client #",
                                                                                     "First Name", "Last Name"]]
        save_statement_to_output_folder.send_statement(WILLIAMSPORT, "WILLIAMSPORT", "St_vicent_invission","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in WILLIAMSPORT")

    try:
        # creating INDY tab

        INDY = vincent_invision_statement.loc[(vincent_invision_statement['Client #'].isin(
            ['1016', '1018', '2017', '2022', '3016', '4010', '4016', '4017', '4018', '4020', '4025', '4030', '4118',
             '4119', '4910', '4920', '40025', '40055', '40E55', '3016B', '40L025', '40L055', '40L25', '40LF20',
             '40LF25', '40LN25', '40LNF', '40LSP', '41L25', '41LF25', '41LN25', '41LNF', '41LSP', '49LF20', '49LNF',
             '40LF30', '40W16', '40W17', '40W18', '40W20', '40W25', '40W30', '40WE55'])), ["Client's Acct#", "Pmt Date",
                                                                                           "Type", "Pmt Amt",
                                                                                           "Pd to Agency", "PD to you",
                                                                                           "Due Agency", "Due You",
                                                                                           "Client #", "First Name",
                                                                                           "Last Name"]]
        save_statement_to_output_folder.send_statement(INDY, "INDY", "St_vicent_invission","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in INDPLS")

    try:
        # creating STRESS tab

        STRESS = vincent_invision_statement.loc[(vincent_invision_statement['Client #'].isin(
            ['4110', '4116', '4117', '4120', '4125', '4130', '41E55', '41LF20'])), ["Client's Acct#", "Pmt Date",
                                                                                    "Type", "Pmt Amt", "Pd to Agency",
                                                                                    "PD to you", "Due Agency",
                                                                                    "Due You", "Client #", "First Name",
                                                                                    "Last Name"]]
        save_statement_to_output_folder.send_statement(STRESS, "STRESS", "St_vicent_invission","St_Vincent")
    except Exception as e:
        logging.exception("error in splitting data in STRESS")
