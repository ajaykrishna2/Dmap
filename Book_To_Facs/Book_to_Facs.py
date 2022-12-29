# import necessary module
import pandas as pd
import logging
import xlrd
import xlsxwriter
import boto3, io, os, datetime
import sidetable
import shutil
import glob2
import calendar
import configparser
#Reading key var from config files
configuartion_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);

aws_access_key = config['Aws_Credential']['s3_access_key']
aws_secret_key = config['Aws_Credential']['s3_secret_key']
bucket_region  = config['Aws_Credential']['bucket_region']
bucket_name            = config['Aws_Credential']['bucket_name'];
input_bucket           = config['Aws_Credential']['input_base_path'];
output_bucket          = config['Aws_Credential']['output_base_path']
local_output_directory = config['Output_Location']['book_to_facs_report']
local_log_directory    = config['Log_Location']['path']

def splitting_non_stv(writer, books_to_facs_statement):
    try:
        # Filter DBJ,CRJ Types from the d1_wc_statement file
        books_to_facs_statement.drop(books_to_facs_statement.loc[
                                         (books_to_facs_statement['Pmt Type'].isin(["DBJ", "CRJ"]))
                                     ].index, inplace=True)
        books_to_facs_statement.drop(books_to_facs_statement.loc[
                                         (books_to_facs_statement['Pmt Type'].isin(['RCR', 'TCR']))].index,
                                     inplace=True)
        books_to_facs_statement.drop(books_to_facs_statement.loc[
                                          (books_to_facs_statement['COR Type'].isin(['RCR','TCR']))].index,
                                      inplace=True)
        non_stv = books_to_facs_statement.loc[(books_to_facs_statement['Client#'].isin(
            ['5013', '9013', '501AWP', '501ECA', '53ERP', '53WCP', '53WPP', '1041DA', '1041', '1041BD', '1041PP',
             '128WCP',
             '128AWP', '128E25', '128ECA', '128ERP', '128I55', '128INS', '128R25', '128R55', '128REC', '128SPP',
             '132AWP', '132E25', '132E55', '132ECA', '132ERP', '132I55', '132INS', '132M25', '132MDM', '132R25',
             '132R55', '132REC', '132SPP', '132WCP', '3032', '129AWP', '129E25', '129ECA', '129ERP', '129I55', '129INS',
             '129R25', '129R55', '129REC', '129SPP', '129WCP', '130AWP', '130E25', '130ECA', '130ERP', '130I55',
             '130INS', '130R25', '130R55', '130SPP', '130WCP', '127AWP', '127E25', '127ECA', '127ERP', '127I55',
             '127INS', '127R25', '127R55', '127REC', '127SPP', '127WCP', '1014', '2014', '3014', '9014', '2014F',
             '210ERP',
             '210M25', '210WCP', '210WPP', '239E25', '239I55', '239INS', '239R25', '239R55', '239SPP', '238E25',
             '238I55', '238INS', '238R25', '238R55', '238REC', '238SEC', '238SPP', '239BD', '237E25', '237I55',
             '237INS', '237R25', '237R55', '237REC', '237SEC', '237SPP', '200ERP', '200WCP', '200WPP', '205ERP',
             '205WCP', '220AWP', '220E25', '220ECA', '220ERP', '220I55', '220INS', '220M25', '220R25', '220R55',
             '220SPP', '220WCP', '221ERP', '221WCP', '221AWP', '221ECA', '221I55', '221INS', '221R55', '221SPP', '3003',
             '5003', '9003', '9004', '1.6E+27', '160I55', '160INS', '160MDM', '160PAY', '160R25', '160R55', '160SPP',
             '160TST', '161I55', '161INS', '161MDM', '161PAY', '161R55', '161SPP', '222BD', '222INS', '222PRJ',
             '22BIFU', '22CIFU', '22TIFU', '22VIFU', '22WIFU', '240ERP', '240WCP', '240WPP', '241ERP', '241WCP',
             '241WPP', '264I55', '264R25', '264R55', '150E25', '150I55', '150INS', '150R25', '150R55', '150SPP',
             '151INS', '1010', '3010', '1010PP', '1006', '2006', '3006', '4006', '5006', '1006PP', '135E25', '135I55',
             '135INS',
             '135R25', '135R55', '135SPP', '239WCP', '239WPP', '230IFU', '230RBP', '230WCP', '230WPP', '236WCP',
             '236WPP', '232WCP', '232WPP', '235WCP', '235WPP', '234WCP', '234WPP', '231WCP', '231WPP', '233WCP',
             '233WPP', '1004', '3004', '104AWP', '104ECA', '104ERP', '104M25', '104R25', '104R55', '104W55', '104WCP',
             '201AWP', '201ECA', '201ERP', '201WCP', '202AWP', '202ECA', '202ERP', '202WCP', '131E25', '131I55',
             '131INS', '131M25', '131R25', '131R55', '131SPP', '131REC', '133E25', '134E25', '133I55', '133INS',
             '133R25', '133R55', '133SPP', '134I55', '134INS', '134PAY', '134R25', '134R55', '134SPP', '134REC',
             '140E25', '140DEN', '140FTE', '140I55', '140IFU', '140INS', '140MDC', '140R25', '140R55', '140SPP',
             '14E25F', '14I55F', '14INSF', '14R25F', '14R55F', '14SPPF', '140ATY', '140AT3', '140AT2', '1500', '1501',
             '1.28E+27', '1.32E+27', '1.32E+57', '1.29E+27', '1.3E+27', '2.39E+27', '2.38E+27', '2.37E+27', '2038',
             '1.34E+27', '1.6E+27', "8205PC", "8205PM","8205SP", "8201PC", "8201PM","8201SP", "8203PC", "8203PM","8203SP", "8204PC",
            "8204PM","8204SP" '1013', '3013',
             '5013P', '1034', '3034', '5034', '1034PP',
             '110E25', '110INS', '110SPP', '1015', '1015PP', '110ERP', '110I55', '110M25', '110R25', '110R55', '110VET',
             '110WCP', '110WPP', '128MDM',
             '128E55', '1032', '132MDC', '132IFM', '132IFU', '129MDM', '129E55', '130MDM', '130E55', '127MDM', '127E55',
             '238ERP', '237ERP', '237AWP',
             '1003', '105WCP', '200IFU', '201DEN', '131AWP', '131ECA', '131ERP', '131MDM', '131E55', '131WCP',
             '1.10E+27', '1.29E+57', '1.31E+57', '1.27E+57',
             '238AWP', '237ECA', '238ECA','237WCP','238WCP','229WCP','229ERP']))]

        non_stv = non_stv.astype({"Client#": str})
        non_stv['Total Pay'] = non_stv['PRN'] + non_stv['Int'] + non_stv['Atty'] + non_stv['Misc'] + non_stv['CC'] + \
                               non_stv['PJI']
        non_stv.to_excel(writer, sheet_name='NON_STV', index=False)
        book_to_facs_summary(non_stv, writer, "NON_STV_Summary")
        return non_stv

    except Exception as e:
        logging.exception("Error in spitting non_stv statement")


def splitting_non_stv_cc(writer, books_to_facs_statement):
    try:
        non_stv_cc = books_to_facs_statement.loc[(books_to_facs_statement['Client#'].isin(
            ['5013', '9013', '501AWP', '501ECA', '53ERP', '53WCP', '53WPP', '1041DA', '1041', '1041BD', '1041PP',
             '128WCP',
             '128AWP', '128E25', '128ECA', '128ERP', '128I55', '128INS', '128R25', '128R55', '128REC', '128SPP',
             '132AWP', '132E25', '132E55', '132ECA', '132ERP', '132I55', '132INS', '132M25', '132MDM', '132R25',
             '132R55', '132REC', '132SPP', '132WCP', '3032', '129AWP', '129E25', '129ECA', '129ERP', '129I55', '129INS',
             '129R25', '129R55', '129REC', '129SPP', '129WCP', '130AWP', '130E25', '130ECA', '130ERP', '130I55',
             '130INS', '130R25', '130R55', '130SPP', '130WCP', '127AWP', '127E25', '127ECA', '127ERP', '127I55',
             '127INS', '127R25', '127R55', '127REC', '127SPP', '127WCP', '1014', '2014', '3014', '9014', '2014F',
             '210ERP',
             '210M25', '210WCP', '210WPP', '239E25', '239I55', '239INS', '239R25', '239R55', '239SPP', '238E25',
             '238I55', '238INS', '238R25', '238R55', '238REC', '238SEC', '238SPP', '239BD', '237E25', '237I55',
             '237INS', '237R25', '237R55', '237REC', '237SEC', '237SPP', '200ERP', '200WCP', '200WPP', '205ERP',
             '205WCP', '220AWP', '220E25', '220ECA', '220ERP', '220I55', '220INS', '220M25', '220R25', '220R55',
             '220SPP', '220WCP', '221ERP', '221WCP', '221AWP', '221ECA', '221I55', '221INS', '221R55', '221SPP', '3003',
             '5003', '9003', '9004', '1.6E+27', '160I55', '160INS', '160MDM', '160PAY', '160R25', '160R55', '160SPP',
             '160TST', '161I55', '161INS', '161MDM', '161PAY', '161R55', '161SPP', '222BD', '222INS', '222PRJ',
             '22BIFU', '22CIFU', '22TIFU', '22VIFU', '22WIFU', '240ERP', '240WCP', '240WPP', '241ERP', '241WCP',
             '241WPP', '264I55', '264R25', '264R55', '150E25', '150I55', '150INS', '150R25', '150R55', '150SPP',
             '151INS', '1010', '3010', '1010PP', '1006', '2006', '3006', '4006', '5006', '1006PP', '135E25', '135I55',
             '135INS',
             '135R25', '135R55', '135SPP', '239WCP', '239WPP', '230IFU', '230RBP', '230WCP', '230WPP', '236WCP',
             '236WPP', '232WCP', '232WPP', '235WCP', '235WPP', '234WCP', '234WPP', '231WCP', '231WPP', '233WCP',
             '233WPP', '1004', '3004', '104AWP', '104ECA', '104ERP', '104M25', '104R25', '104R55', '104W55', '104WCP',
             '201AWP', '201ECA', '201ERP', '201WCP', '202AWP', '202ECA', '202ERP', '202WCP', '131E25', '131I55',
             '131INS', '131M25', '131R25', '131R55', '131SPP', '131REC', '133E25', '134E25', '133I55', '133INS',
             '133R25', '133R55', '133SPP', '134I55', '134INS', '134PAY', '134R25', '134R55', '134SPP', '134REC',
             '140E25', '140DEN', '140FTE', '140I55', '140IFU', '140INS', '140MDC', '140R25', '140R55', '140SPP',
             '14E25F', '14I55F', '14INSF', '14R25F', '14R55F', '14SPPF', '140ATY', '140AT3', '140AT2', '1500', '1501',
             '1.28E+27', '1.32E+27', '1.32E+57', '1.29E+27', '1.3E+27', '2.39E+27', '2.38E+27', '2.37E+27', '2038',
             '1.34E+27', '1.6E+27'
                , "8205PC", "8205PM", "8201PC", "8201PM", "8203PC", "8203PM", "8204PC", "8204PM","8201SP","8203SP",
             "8204SP","8205SP",'1013', '3013','5013P', '1034', '3034', '5034', '1034PP',
             '110E25', '110INS', '110SPP', '1015', '1015PP', '110ERP', '110I55', '110M25', '110R25', '110R55', '110VET',
             '110WCP', '110WPP', '128MDM',
             '128E55', '1032', '132MDC', '132IFM', '132IFU', '129MDM', '129E55', '130MDM', '130E55', '127MDM', '127E55',
             '238ERP', '237ERP', '237AWP',
             '1003', '105WCP', '200IFU', '201DEN', '131AWP', '131ECA', '131ERP', '131MDM', '131E55', '131WCP',
             '1.10E+27', '1.29E+57', '1.31E+57', '1.27E+57',
             '238AWP', '237ECA', '238ECA','237WCP','238WCP','229WCP','229ERP']))]
        non_stv_cc_final = non_stv_cc.loc[(non_stv_cc['Pmt Type'] == 'CC')
                                          | (non_stv_cc['COR Type'] == 'CC')
                                          & (non_stv_cc['Pmt Type'].isin(['NSF', 'COR']))]

        non_stv_cc_final = non_stv_cc_final.astype({"Client#": str})
        # non_stv_cc_final['Date'] = non_stv_cc_final['Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        non_stv_cc_final['Total Pay'] = non_stv_cc_final['PRN'] + non_stv_cc_final['Int'] + non_stv_cc_final['Atty'] + \
                                        non_stv_cc_final['Misc'] + non_stv_cc_final['CC'] + non_stv_cc_final['PJI']

        non_stv_cc_final.to_excel(writer, sheet_name='NON_STV_CC', index=False)
        book_to_facs_summary(non_stv_cc_final, writer, "NON_STV_CC_Summary")
        return non_stv_cc_final
    except Exception as e:
        logging.exception("Error in splitting non_stv_cc statement")


def splitting_non_stv_eft(writer, books_to_facs_statement):
    try:
        non_stv_eft = books_to_facs_statement.loc[(books_to_facs_statement['Client#'].isin(
            ['5013', '9013', '501AWP', '501ECA', '53ERP', '53WCP', '53WPP', '1041DA', '1041', '1041BD', '1041PP',
             '128WCP',
             '128AWP', '128E25', '128ECA', '128ERP', '128I55', '128INS', '128R25', '128R55', '128REC', '128SPP',
             '132AWP', '132E25', '132E55', '132ECA', '132ERP', '132I55', '132INS', '132M25', '132MDM', '132R25',
             '132R55', '132REC', '132SPP', '132WCP', '3032', '129AWP', '129E25', '129ECA', '129ERP', '129I55', '129INS',
             '129R25', '129R55', '129REC', '129SPP', '129WCP', '130AWP', '130E25', '130ECA', '130ERP', '130I55',
             '130INS', '130R25', '130R55', '130SPP', '130WCP', '127AWP', '127E25', '127ECA', '127ERP', '127I55',
             '127INS', '127R25', '127R55', '127REC', '127SPP', '127WCP', '1014', '2014', '3014', '9014', '2014F',
             '210ERP',
             '210M25', '210WCP', '210WPP', '239E25', '239I55', '239INS', '239R25', '239R55', '239SPP', '238E25',
             '238I55', '238INS', '238R25', '238R55', '238REC', '238SEC', '238SPP', '239BD', '237E25', '237I55',
             '237INS', '237R25', '237R55', '237REC', '237SEC', '237SPP', '200ERP', '200WCP', '200WPP', '205ERP',
             '205WCP', '220AWP', '220E25', '220ECA', '220ERP', '220I55', '220INS', '220M25', '220R25', '220R55',
             '220SPP', '220WCP', '221ERP', '221WCP', '221AWP', '221ECA', '221I55', '221INS', '221R55', '221SPP', '3003',
             '5003', '9003', '9004', '1.6E+27', '160I55', '160INS', '160MDM', '160PAY', '160R25', '160R55', '160SPP',
             '160TST', '161I55', '161INS', '161MDM', '161PAY', '161R55', '161SPP', '222BD', '222INS', '222PRJ',
             '22BIFU', '22CIFU', '22TIFU', '22VIFU', '22WIFU', '240ERP', '240WCP', '240WPP', '241ERP', '241WCP',
             '241WPP', '264I55', '264R25', '264R55', '150E25', '150I55', '150INS', '150R25', '150R55', '150SPP',
             '151INS', '1010', '3010', '1010PP', '1006', '2006', '3006', '4006', '5006', '1006PP', '135E25', '135I55',
             '135INS',
             '135R25', '135R55', '135SPP', '239WCP', '239WPP', '230IFU', '230RBP', '230WCP', '230WPP', '236WCP',
             '236WPP', '232WCP', '232WPP', '235WCP', '235WPP', '234WCP', '234WPP', '231WCP', '231WPP', '233WCP',
             '233WPP', '1004', '3004', '104AWP', '104ECA', '104ERP', '104M25', '104R25', '104R55', '104W55', '104WCP',
             '201AWP', '201ECA', '201ERP', '201WCP', '202AWP', '202ECA', '202ERP', '202WCP', '131E25', '131I55',
             '131INS', '131M25', '131R25', '131R55', '131SPP', '131REC', '133E25', '134E25', '133I55', '133INS',
             '133R25', '133R55', '133SPP', '134I55', '134INS', '134PAY', '134R25', '134R55', '134SPP', '134REC',
             '140E25', '140DEN', '140FTE', '140I55', '140IFU', '140INS', '140MDC', '140R25', '140R55', '140SPP',
             '14E25F', '14I55F', '14INSF', '14R25F', '14R55F', '14SPPF', '140ATY', '140AT3', '140AT2', '1500', '1501',
             '1.28E+27', '1.32E+27', '1.32E+57', '1.29E+27', '1.3E+27', '2.39E+27', '2.38E+27', '2.37E+27', '2038',
             '1.34E+27', '1.6E+27'
                , "8205PC", "8205PM", "8201PC", "8201PM", "8203PC", "8203PM", "8204PC", "8204PM","8201SP","8203SP",
             "8204SP","8205SP", '1013', '3013',
             '5013P', '1034', '3034', '5034', '1034PP',
             '110E25', '110INS', '110SPP', '1015', '1015PP', '110ERP', '110I55', '110M25', '110R25', '110R55', '110VET',
             '110WCP', '110WPP', '128MDM',
             '128E55', '1032', '132MDC', '132IFM', '132IFU', '129MDM', '129E55', '130MDM', '130E55', '127MDM', '127E55',
             '238ERP', '237ERP', '237AWP',
             '1003', '105WCP', '200IFU', '201DEN', '131AWP', '131ECA', '131ERP', '131MDM', '131E55', '131WCP',
             '1.10E+27', '1.29E+57', '1.31E+57', '1.27E+57',
             '238AWP', '237ECA', '238ECA','237WCP','238WCP','229WCP','229ERP']))]
        non_stv_eft_final = non_stv_eft.loc[(non_stv_eft['Pmt Type'] == 'EFT')
                                            | (non_stv_eft['COR Type'] == 'EFT')
                                            & (non_stv_eft['Pmt Type'].isin(['NSF', 'COR']))]
        non_stv_eft_final = non_stv_eft_final.astype({"Client#": str})
        # non_stv_eft_final['Date'] = non_stv_eft_final['Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        non_stv_eft_final['Total Pay'] = non_stv_eft_final['PRN'] + non_stv_eft_final['Int'] + non_stv_eft_final[
            'Atty'] + non_stv_eft_final['Misc'] + non_stv_eft_final['CC'] + non_stv_eft_final['PJI']
        non_stv_eft_final.to_excel(writer, sheet_name='NON_STV_EFT', index=False)
        book_to_facs_summary(non_stv_eft_final, writer, "NON_STV_EFT_Summary")
        return non_stv_eft_final
    except Exception as e:
        logging.exception("Error in splitting non_stv_cc statement")


def splitting_community(writer, books_to_facs_statement):
    try:
        # Filter DBJ,CRJ Types from the d1_wc_statement file
        books_to_facs_statement.drop(books_to_facs_statement.loc[
                                         (books_to_facs_statement['Pmt Type'].isin(["DBJ", "CRJ"]))
                                     ].index, inplace=True)
        community = books_to_facs_statement.loc[(books_to_facs_statement['Client#'].isin(
            ['6019BG', '6019BH', '5019HH', '2019T', '5019D', '2019L', '6019A', '6019B', '6019C', '6019D', '6019E',
             '6019F', '6019G', '6019L', '2019', '2019D', '7019A', '7019D', '5019', '50AERP', '50AM25', '50AWCP',
             '50AWPP',
             '2019B', '5019B', '50BERP', '50BM25', '50BWCP', '50BWPP', '7019B', '2019C', '5019C', '50CERP', '50CM25',
             '50CWCP', '50CWPP', '7019C', '60IFU', '61IFU', '62IFU', '6019R', '7019R', '6019V', '7019G', '1031', '3031',
             '5031', '303AWP', '303ECA', '50GERP', '50GM25', '50GWCP', '50GWPP', '5019V', '50VERP', '50VM25', '50VWCP',
             '50VWPP', '5019CE', '5019SP', '5019EC', '5019HS', '5019HC', '5019IE', '5019NC', '5019SC', '5019IS',
             '5019PT', '6019HP', '106R55', '6019HW', '6019HA', '6019H', '4019H', '4019HW', '40HERP', '40HM25', '40HWCP',
             '40HWPP', '40RERP', '40RM25', '40RWCP', '40RWPP', '1001', '2001', '3001', '5001', '9001', '1001SP',
             '101ERP',
             '101IFU', '101INS', '101SPP', '101I55', '101M25', '101R25', '101R55', '101W55', '101WCP', '102ERP',
             '102M25', '102R25', '102R55', '102W55', '102WCP', '103ERP', '103M25', '103R25', '103R55', '103W55',
             '103WCP', '2019M', '1019OH', '2019OH', '6019K', '6019M', '6019I', '6019J', '1019', '5019MK', '8019A',
             '8019B', '8019C', '8019D', '101E25', '1.01E+27']))]
        community = community.astype({"Client#": str})
        # community['Date'] = community['Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        community['Total Pay'] = community['PRN'] + community['Int'] + community['Atty'] + community['Misc'] + \
                                 community['CC'] + community['PJI']
        community.to_excel(writer, sheet_name='COMMUNITY', index=False)
        book_to_facs_summary(community, writer, "COMMUNITY_Summary")

    except Exception as e:
        logging.exception("Error in spitting community statement")


def splitting_community_cc(writer, books_to_facs_statement):
    try:
        community_cc = books_to_facs_statement.loc[(books_to_facs_statement['Client#'].isin(
            ['6019BG', '6019BH', '5019HH', '2019T', '5019D', '2019L', '6019A', '6019B', '6019C', '6019D', '6019E',
             '6019F', '6019G', '6019L', '2019', '2019D', '7019A', '7019D', '5019', '50AERP', '50AM25', '50AWCP',
             '50AWPP',
             '2019B', '5019B', '50BERP', '50BM25', '50BWCP', '50BWPP', '7019B', '2019C', '5019C', '50CERP', '50CM25',
             '50CWCP', '50CWPP', '7019C', '60IFU', '61IFU', '62IFU', '6019R', '7019R', '6019V', '7019G', '1031', '3031',
             '5031', '303AWP', '303ECA', '50GERP', '50GM25', '50GWCP', '50GWPP', '5019V', '50VERP', '50VM25', '50VWCP',
             '50VWPP', '5019CE', '5019SP', '5019EC', '5019HS', '5019HC', '5019IE', '5019NC', '5019SC', '5019IS',
             '5019PT', '6019HP', '106R55', '6019HW', '6019HA', '6019H', '4019H', '4019HW', '40HERP', '40HM25', '40HWCP',
             '40HWPP', '40RERP', '40RM25', '40RWCP', '40RWPP', '1001', '2001', '3001', '5001', '9001', '1001SP',
             '101ERP',
             '101IFU', '101INS', '101SPP', '101I55', '101M25', '101R25', '101R55', '101W55', '101WCP', '102ERP',
             '102M25', '102R25', '102R55', '102W55', '102WCP', '103ERP', '103M25', '103R25', '103R55', '103W55',
             '103WCP', '2019M', '1019OH', '2019OH', '6019K', '6019M', '6019I', '6019J', '1019', '5019MK', '8019A',
             '8019B', '8019C', '8019D', '101E25', '1.01E+27']))]
        community_cc_final = community_cc.loc[(community_cc['Pmt Type'] == 'CC')
                                              | (community_cc['COR Type'] == 'CC')
                                              & (community_cc['Pmt Type'].isin(['NSF', 'COR']))]
        community_cc_final = community_cc_final.astype({"Client#": str})
        # community_cc_final['Date'] = community_cc_final['Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        community_cc_final['Total Pay'] = community_cc_final['PRN'] + community_cc_final['Int'] + community_cc_final[
            'Atty'] + community_cc_final['Misc'] + community_cc_final['CC'] + community_cc_final['PJI']
        community_cc_final.to_excel(writer, sheet_name='COMMUNITY_CC', index=False)

        book_to_facs_summary(community_cc_final, writer, "COMMUNITY_CC_Summary")

    except Exception as e:
        logging.exception("Error in splitting community_cc statement")


def splitting_community_eft(writer, books_to_facs_statement):
    try:
        community_eft = books_to_facs_statement.loc[(books_to_facs_statement['Client#'].isin(
            ['6019BG', '6019BH', '5019HH', '2019T', '5019D', '2019L', '6019A', '6019B', '6019C', '6019D', '6019E',
             '6019F', '6019G', '6019L', '2019', '2019D', '7019A', '7019D', '5019', '50AERP', '50AM25', '50AWCP',
             '50AWPP',
             '2019B', '5019B', '50BERP', '50BM25', '50BWCP', '50BWPP', '7019B', '2019C', '5019C', '50CERP', '50CM25',
             '50CWCP', '50CWPP', '7019C', '60IFU', '61IFU', '62IFU', '6019R', '7019R', '6019V', '7019G', '1031', '3031',
             '5031', '303AWP', '303ECA', '50GERP', '50GM25', '50GWCP', '50GWPP', '5019V', '50VERP', '50VM25', '50VWCP',
             '50VWPP', '5019CE', '5019SP', '5019EC', '5019HS', '5019HC', '5019IE', '5019NC', '5019SC', '5019IS',
             '5019PT', '6019HP', '106R55', '6019HW', '6019HA', '6019H', '4019H', '4019HW', '40HERP', '40HM25', '40HWCP',
             '40HWPP', '40RERP', '40RM25', '40RWCP', '40RWPP', '1001', '2001', '3001', '5001', '9001', '1001SP',
             '101ERP',
             '101IFU', '101INS', '101SPP', '101I55', '101M25', '101R25', '101R55', '101W55', '101WCP', '102ERP',
             '102M25', '102R25', '102R55', '102W55', '102WCP', '103ERP', '103M25', '103R25', '103R55', '103W55',
             '103WCP', '2019M', '1019OH', '2019OH', '6019K', '6019M', '6019I', '6019J', '1019', '5019MK', '8019A',
             '8019B', '8019C', '8019D', '101E25', '1.01E+27']))]
        community_eft_final = community_eft.loc[(community_eft['Pmt Type'] == 'EFT')
                                                | (community_eft['COR Type'] == 'EFT')
                                                & (community_eft['Pmt Type'].isin(['NSF', 'COR']))]

        community_eft_final = community_eft_final.astype({"Client#": str})
        # community_eft_final['Date'] = community_eft_final['Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        community_eft_final['Total Pay'] = community_eft_final['PRN'] + community_eft_final['Int'] + \
                                           community_eft_final['Atty'] + community_eft_final['Misc'] + \
                                           community_eft_final['CC'] + community_eft_final['PJI']
        community_eft_final.to_excel(writer, sheet_name='COMMUNITY_EFT', index=False)
        book_to_facs_summary(community_eft_final, writer, "COMMUNITY_EFT_Summary")


    except Exception as e:
        logging.exception("Error in splitting community_EFT statement")


def splitting_med1(writer, books_to_facs_statement):
    try:
        # Filter DBJ,CRJ Types from the d1_wc_statement file
        books_to_facs_statement.drop(books_to_facs_statement.loc[
                                         (books_to_facs_statement['Pmt Type'].isin(["DBJ", "CRJ"]))
                                     ].index, inplace=True)
        med1 = books_to_facs_statement.loc[
            (books_to_facs_statement['Client#'].isin(['11299A', '11299B', '11299C', '11299D','766101','820902']))]

        med1 = med1.astype({"Client#": str})
        # med1['Date'] = med1['Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        med1['Total Pay'] = med1['PRN'] + med1['Int'] + med1['Atty'] + med1['Misc'] + med1['CC'] + med1['PJI']
        med1.to_excel(writer, sheet_name='MED1', index=False)
        book_to_facs_summary(med1, writer, "MED1_Summary")

    except Exception as e:
        logging.exception("Error in spitting community statement")


def splitting_med1_cc(writer, books_to_facs_statement):
    try:
        med1_cc = books_to_facs_statement.loc[
            (books_to_facs_statement['Client#'].isin(['11299A', '11299B', '11299C', '11299D','766101','820902']))]

        med1_cc_final = med1_cc.loc[(med1_cc['Pmt Type'] == 'CC')
                                    | (med1_cc['COR Type'] == 'CC')
                                    & (med1_cc['Pmt Type'].isin(['NSF', 'COR']))]
        med1_cc_final = med1_cc_final.astype({"Client#": str})
        # med1_cc_final['Date'] = med1_cc_final['Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        med1_cc_final['Total Pay'] = med1_cc_final['PRN'] + med1_cc_final['Int'] + med1_cc_final['Atty'] + \
                                     med1_cc_final['Misc'] + med1_cc_final['CC'] + med1_cc_final['PJI']
        med1_cc_final.to_excel(writer, sheet_name='MED1_CC', index=False)
        book_to_facs_summary(med1_cc_final, writer, "MED1_CC_Summary")

    except Exception as e:
        logging.exception("Error in splitting community_cc statement")


def splitting_med1_eft(writer, books_to_facs_statement):
    try:
        med1_eft = books_to_facs_statement.loc[

            (books_to_facs_statement['Client#'].isin(['11299A', '11299B', '11299C', '11299D','766101','820902']))]

        med1_eft_final = med1_eft.loc[(med1_eft['Pmt Type'] == 'EFT')
                                      | (med1_eft['COR Type'] == 'EFT')
                                      & (med1_eft['Pmt Type'].isin(['NSF', 'COR']))]
        med1_eft_final = med1_eft_final.astype({"Client#": str})
        # med1_eft_final['Date'] = med1_eft_final['Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        med1_eft_final['Total Pay'] = med1_eft_final['PRN'] + med1_eft_final['Int'] + med1_eft_final['Atty'] + \
                                      med1_eft_final['Misc'] + med1_eft_final['CC'] + med1_eft_final['PJI']
        med1_eft_final.to_excel(writer, sheet_name='MED1_EFT', index=False)
        book_to_facs_summary(med1_eft_final, writer, "MED1_EFT_Summary")


    except Exception as e:
        logging.exception("Error in splitting community_EFT statement")


def splitting_stv(writer, books_to_facs_statement):
    try:
        # Filter DBJ,CRJ Types from the d1_wc_statement file
        books_to_facs_statement.drop(books_to_facs_statement.loc[
                                         (books_to_facs_statement['Pmt Type'].isin(["DBJ", "CRJ"]))
                                     ].index, inplace=True)
        stv = books_to_facs_statement.loc[(books_to_facs_statement['Client#'].isin([
            '6416', '6419', '6417', '6418', '6420', '6425', '6430', '64E55', '65E55', '2046', '6516', '6517', '6518',
            '6519', '6520', '6525', '6530',
            '6616', '6617', '6618', '6619', '6620', '6625', '6630', '66E55', '201432', '206E25', '206I55', '206INS',
            '206R25', '206R55',
            '206SPP', '5026', '38E55', '6050', '1030', '2030', '3030', '2030MC', '3007', '5007', '190CL2', '190CLN',
            '190INS', '190SPP',
            '190C55', '190C66', '190I55', '190R25', '190R55', '7016', '7017', '7018', '7020', '7025', '7030', '70E55',
            '4818', '4819',
            '5017', '5020', '5025', '5030', '50E55', '2033', '72E55', '7216', '7217', '7218', '7219', '7220', '7225',
            '7230', '49E55', '1040-3',
            '1040-4', '2040-3', '2040-4', '5040-3', '5040-4', '5040-6', '5050-3', '5050-4', '5050-6', '2040', '1021',
            '2021',
            '3018', '3021', '37E55', '4023', '4024', '4021', '4321', '4421', '4521', '3017', '4022', '71E55', '7116',
            '7117', '7118', '7119', '7120',
            '7125', '7130', '42E55', '4216', '4217', '4220', '4225', '4230', '4210', '4218', '4219', '42025', '42055',
            '42CAS', '42L025',
            '42L055', '42L25', '42LF20', '42LF25', '42LN25', '42LNF', '42LSP', '1020', '2020', '3020', '1020PP',
            '2020JU',
            '2020PC', '2020EO', '6216', '6217', '6218', '6219', '6220', '6225', '6230', '62E55', '5816', '5817', '5818',
            '5819', '5820', '5825',
            '5830', '36E55', '58E55', '2117', '2039', '3916', '3917', '3918', '3920', '3925', '3930', '39E55', '2118',
            '2119', '6316', '6317',
            '6318', '6320', '6325', '6330', '63E55', '47LNF', '57E55', '5716', '5717', '5718', '5719', '5720', '5725',
            '5730', '47LF25',
            '47NH', '47LN25', '4710', '4717', '4718', '4719', '4720', '4725', '4730', '47LF20', '47SP', '5215', '5220',
            '5225', '5230', '5216',
            '5217', '5218', '5219', '52E55', '2025', '45FL25', '45SUIT', '4517', '4518', '4519', '4520', '4525', '4530',
            '45FL20', '403R55',
            '5040', '2041', '3041', '4041', '5050', '4918', '4919', '5117', '5120', '5125', '5130', '5118', '5119',
            '51E55', '2037', '2037MC',
            '2037CL', '1037', '2150', '2217', '2218', '2219', 'WCMH', '20517', '20518', '20519', '205I55', '205R25',
            '205R55', '6116',
            '6117', '6118', '6119', '6120', '6125', '6130', '61E55', '59E55', '6017', '6018', '6019', '6020', '6025',
            '6030', '60E55', '2012',
            '2022', '1016', '1018', '2017', '3016', '4010', '4016', '4017', '4018', '4020', '4025', '4030', '4118',
            '4119', '4910', '4920', '40025',
            '40055', '40E55', '3016B', '40L025', '40L055', '40L25', '40LF20', '40LF25', '40LN25', '40LNF', '40LSP',
            '41L25', '41LF25', '41LN25', '41LNF', '41LSP', '49LF20', '49LNF', '40LF30', '40W16', '40W17', '40W18',
            '40W20', '40W25', '40W30', '40WE55', '7316', '7317', '7318', '73E55', '7320', '7325', '7330', '4110',
            '4116', '4117', '4120',
            '4125', '4130', '41E55', '41LF20', '7416', '7417', '7418', '7420', '7425', '7430', '74E55', '4617', '4618',
            '4619', '4620', '4625',
            '4630', '46LF20', '46LF25', '5116', '5617', '5618', '5619', '5620', '5625', '5630', '56E55', '200INS',
            '200M25', '200SPP',
            '201IFU', '201INS', '201M25', '201SPP', '190ERP', '36D1', '36ERP', '37D1', '37ERP', '38D1', '38ERP', '39D1',
            '39ERP', '40D1', '40ERP', '41D1', '41ERP', '42D1', '42ERP', '49D1', '49ERP', '50D1', '50ERP', '51D1',
            '51ERP', '52D1', '52ERP', '56D1', '56ERP', '57D1', '57ERP', '58D1', '58ERP', '59ERP', '60ERP', '61ERP',
            '62ERP', '63ERP', '64ERP', '65ERP', '66D1', '66ERP', '70ERP', '71ERP', '72ERP', '73D1', '73ERP', '74D1',
            '74ERP', '75ERP', '76ERP', '40WD1', '40WERP', '39PP', '39WC', '1016PP', '1033', '1033PP', '1046PP',
            '1046WC',
            '190WC', '190WCP', '191WCP', '37PP', '37WC', '37WCP', '41PP', '41WC', '4216PP', '4216WC', '45WC', '47WC',
            '5033PP', '5033WC', '5137PP', '5137WC', '5237PP', '5237WC', '52PP', '52WC', '5646PP', '5646WC', '5737PP',
            '5737WC', '57PP', '57WC', '5837PP', '5837WC', '6037PP', '6037WC', '6137PP', '6137WC', '6237PP', '6237WC',
            '6337PP', '6337WC', '6437PP', '6437WC', '64PP', '64WC', '6537PP', '6537WC', '6637PP', '6637WC', '66PP',
            '66WC', '7037PP', '7037WC', '70PP', '70WC', '71PP', '71WC', '72PP', '72WC', '73PP', '73WC', '74PP', '74WC',
            'ATH01', 'ATH101', 'ATH102', 'ATH103', 'ATH104', 'ATH164', 'ATH21', 'ATH22', 'ATH23', 'ATH24', 'ATH25',
            'ATH26', 'ATH41', 'ATH61', 'ATH62', 'ATH63', 'ATH64', 'ATH65', '2042', '2047', '75E55', '76E55', '5.90E+56',
            '3.70E+56', '59ERP', '40E55', '4.00E+56', 'G'
        ]))]
        stv = stv.astype({"Client#": str})
        # stv['Date'] = stv['Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        stv['Total Pay'] = stv['PRN'] + stv['Int'] + stv['Atty'] + stv['Misc'] + stv['CC'] + stv['PJI']
        stv.to_excel(writer, sheet_name='STV', index=False)
        book_to_facs_summary(stv, writer, "STV_Summary")

    except Exception as e:
        logging.exception("Error in spitting community statement")


def splitting_stv_cc(writer, books_to_facs_statement):
    try:
        stv_cc = books_to_facs_statement.loc[(books_to_facs_statement['Client#'].isin([
            '6416', '6419', '6417', '6418', '6420', '6425', '6430', '64E55', '65E55', '2046', '6516', '6517', '6518',
            '6519', '6520', '6525', '6530',
            '6616', '6617', '6618', '6619', '6620', '6625', '6630', '66E55', '201432', '206E25', '206I55', '206INS',
            '206R25', '206R55',
            '206SPP', '5026', '38E55', '6050', '1030', '2030', '3030', '2030MC', '3007', '5007', '190CL2', '190CLN',
            '190INS', '190SPP',
            '190C55', '190C66', '190I55', '190R25', '190R55', '7016', '7017', '7018', '7020', '7025', '7030', '70E55',
            '4818', '4819',
            '5017', '5020', '5025', '5030', '50E55', '2033', '72E55', '7216', '7217', '7218', '7219', '7220', '7225',
            '7230', '49E55', '1040-3',
            '1040-4', '2040-3', '2040-4', '5040-3', '5040-4', '5040-6', '5050-3', '5050-4', '5050-6', '2040', '1021',
            '2021',
            '3018', '3021', '37E55', '4023', '4024', '4021', '4321', '4421', '4521', '3017', '4022', '71E55', '7116',
            '7117', '7118', '7119', '7120',
            '7125', '7130', '42E55', '4216', '4217', '4220', '4225', '4230', '4210', '4218', '4219', '42025', '42055',
            '42CAS', '42L025',
            '42L055', '42L25', '42LF20', '42LF25', '42LN25', '42LNF', '42LSP', '1020', '2020', '3020', '1020PP',
            '2020JU',
            '2020PC', '2020EO', '6216', '6217', '6218', '6219', '6220', '6225', '6230', '62E55', '5816', '5817', '5818',
            '5819', '5820', '5825',
            '5830', '36E55', '58E55', '2117', '2039', '3916', '3917', '3918', '3920', '3925', '3930', '39E55', '2118',
            '2119', '6316', '6317',
            '6318', '6320', '6325', '6330', '63E55', '47LNF', '57E55', '5716', '5717', '5718', '5719', '5720', '5725',
            '5730', '47LF25',
            '47NH', '47LN25', '4710', '4717', '4718', '4719', '4720', '4725', '4730', '47LF20', '47SP', '5215', '5220',
            '5225', '5230', '5216',
            '5217', '5218', '5219', '52E55', '2025', '45FL25', '45SUIT', '4517', '4518', '4519', '4520', '4525', '4530',
            '45FL20', '403R55',
            '5040', '2041', '3041', '4041', '5050', '4918', '4919', '5117', '5120', '5125', '5130', '5118', '5119',
            '51E55', '2037', '2037MC',
            '2037CL', '1037', '2150', '2217', '2218', '2219', 'WCMH', '20517', '20518', '20519', '205I55', '205R25',
            '205R55', '6116',
            '6117', '6118', '6119', '6120', '6125', '6130', '61E55', '59E55', '6017', '6018', '6019', '6020', '6025',
            '6030', '60E55', '2012',
            '2022', '1016', '1018', '2017', '3016', '4010', '4016', '4017', '4018', '4020', '4025', '4030', '4118',
            '4119', '4910', '4920', '40025',
            '40055', '40E55', '3016B', '40L025', '40L055', '40L25', '40LF20', '40LF25', '40LN25', '40LNF', '40LSP',
            '41L25', '41LF25', '41LN25', '41LNF', '41LSP', '49LF20', '49LNF', '40LF30', '40W16', '40W17', '40W18',
            '40W20', '40W25', '40W30', '40WE55', '7316', '7317', '7318', '73E55', '7320', '7325', '7330', '4110',
            '4116', '4117', '4120',
            '4125', '4130', '41E55', '41LF20', '7416', '7417', '7418', '7420', '7425', '7430', '74E55', '4617', '4618',
            '4619', '4620', '4625',
            '4630', '46LF20', '46LF25', '5116', '5617', '5618', '5619', '5620', '5625', '5630', '56E55', '200INS',
            '200M25', '200SPP',
            '201IFU', '201INS', '201M25', '201SPP', '190ERP', '36D1', '36ERP', '37D1', '37ERP', '38D1', '38ERP', '39D1',
            '39ERP', '40D1', '40ERP', '41D1', '41ERP', '42D1', '42ERP', '49D1', '49ERP', '50D1', '50ERP', '51D1',
            '51ERP', '52D1', '52ERP', '56D1', '56ERP', '57D1', '57ERP', '58D1', '58ERP', '59ERP', '60ERP', '61ERP',
            '62ERP', '63ERP', '64ERP', '65ERP', '66D1', '66ERP', '70ERP', '71ERP', '72ERP', '73D1', '73ERP', '74D1',
            '74ERP', '75ERP', '76ERP', '40WD1', '40WERP', '39PP', '39WC', '1016PP', '1033', '1033PP', '1046PP',
            '1046WC',
            '190WC', '190WCP', '191WCP', '37PP', '37WC', '37WCP', '41PP', '41WC', '4216PP', '4216WC', '45WC', '47WC',
            '5033PP', '5033WC', '5137PP', '5137WC', '5237PP', '5237WC', '52PP', '52WC', '5646PP', '5646WC', '5737PP',
            '5737WC', '57PP', '57WC', '5837PP', '5837WC', '6037PP', '6037WC', '6137PP', '6137WC', '6237PP', '6237WC',
            '6337PP', '6337WC', '6437PP', '6437WC', '64PP', '64WC', '6537PP', '6537WC', '6637PP', '6637WC', '66PP',
            '66WC', '7037PP', '7037WC', '70PP', '70WC', '71PP', '71WC', '72PP', '72WC', '73PP', '73WC', '74PP', '74WC',
            'ATH01', 'ATH101', 'ATH102', 'ATH103', 'ATH104', 'ATH164', 'ATH21', 'ATH22', 'ATH23', 'ATH24', 'ATH25',
            'ATH26', 'ATH41', 'ATH61', 'ATH62', 'ATH63', 'ATH64', 'ATH65', '2042', '2047', '75E55', '76E55', '5.90E+56',
            '3.70E+56', '59ERP', '40E55', '4.00E+56', 'G'
        ]))]

        stv_cc_final = stv_cc.loc[(stv_cc['Pmt Type'] == 'CC')
                                  | (stv_cc['COR Type'] == 'CC')
                                  & (stv_cc['Pmt Type'].isin(['NSF', 'COR']))]
        stv_cc_final = stv_cc_final.astype({"Client#": str})
        # stv_cc_final['Date'] = stv_cc_final['Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        stv_cc_final['Total Pay'] = stv_cc_final['PRN'] + stv_cc_final['Int'] + stv_cc_final['Atty'] + stv_cc_final[
            'Misc'] + stv_cc_final['CC'] + stv_cc_final['PJI']
        stv_cc_final.to_excel(writer, sheet_name='STV_CC', index=False)
        book_to_facs_summary(stv_cc_final, writer, "STV_CC_Summary")

    except Exception as e:
        logging.exception("Error in spitting community statement")


def splitting_stv_eft(writer, books_to_facs_statement):
    try:
        stv_eft = books_to_facs_statement.loc[(books_to_facs_statement['Client#'].isin([
            '6416', '6419', '6417', '6418', '6420', '6425', '6430', '64E55', '65E55', '2046', '6516', '6517', '6518',
            '6519', '6520', '6525', '6530',
            '6616', '6617', '6618', '6619', '6620', '6625', '6630', '66E55', '201432', '206E25', '206I55', '206INS',
            '206R25', '206R55',
            '206SPP', '5026', '38E55', '6050', '1030', '2030', '3030', '2030MC', '3007', '5007', '190CL2', '190CLN',
            '190INS', '190SPP',
            '190C55', '190C66', '190I55', '190R25', '190R55', '7016', '7017', '7018', '7020', '7025', '7030', '70E55',
            '4818', '4819',
            '5017', '5020', '5025', '5030', '50E55', '2033', '72E55', '7216', '7217', '7218', '7219', '7220', '7225',
            '7230', '49E55', '1040-3',
            '1040-4', '2040-3', '2040-4', '5040-3', '5040-4', '5040-6', '5050-3', '5050-4', '5050-6', '2040', '1021',
            '2021',
            '3018', '3021', '37E55', '4023', '4024', '4021', '4321', '4421', '4521', '3017', '4022', '71E55', '7116',
            '7117', '7118', '7119', '7120',
            '7125', '7130', '42E55', '4216', '4217', '4220', '4225', '4230', '4210', '4218', '4219', '42025', '42055',
            '42CAS', '42L025',
            '42L055', '42L25', '42LF20', '42LF25', '42LN25', '42LNF', '42LSP', '1020', '2020', '3020', '1020PP',
            '2020JU',
            '2020PC', '2020EO', '6216', '6217', '6218', '6219', '6220', '6225', '6230', '62E55', '5816', '5817', '5818',
            '5819', '5820', '5825',
            '5830', '36E55', '58E55', '2117', '2039', '3916', '3917', '3918', '3920', '3925', '3930', '39E55', '2118',
            '2119', '6316', '6317',
            '6318', '6320', '6325', '6330', '63E55', '47LNF', '57E55', '5716', '5717', '5718', '5719', '5720', '5725',
            '5730', '47LF25',
            '47NH', '47LN25', '4710', '4717', '4718', '4719', '4720', '4725', '4730', '47LF20', '47SP', '5215', '5220',
            '5225', '5230', '5216',
            '5217', '5218', '5219', '52E55', '2025', '45FL25', '45SUIT', '4517', '4518', '4519', '4520', '4525', '4530',
            '45FL20', '403R55',
            '5040', '2041', '3041', '4041', '5050', '4918', '4919', '5117', '5120', '5125', '5130', '5118', '5119',
            '51E55', '2037', '2037MC',
            '2037CL', '1037', '2150', '2217', '2218', '2219', 'WCMH', '20517', '20518', '20519', '205I55', '205R25',
            '205R55', '6116',
            '6117', '6118', '6119', '6120', '6125', '6130', '61E55', '59E55', '6017', '6018', '6019', '6020', '6025',
            '6030', '60E55', '2012',
            '2022', '1016', '1018', '2017', '3016', '4010', '4016', '4017', '4018', '4020', '4025', '4030', '4118',
            '4119', '4910', '4920', '40025',
            '40055', '40E55', '3016B', '40L025', '40L055', '40L25', '40LF20', '40LF25', '40LN25', '40LNF', '40LSP',
            '41L25', '41LF25', '41LN25', '41LNF', '41LSP', '49LF20', '49LNF', '40LF30', '40W16', '40W17', '40W18',
            '40W20', '40W25', '40W30', '40WE55', '7316', '7317', '7318', '73E55', '7320', '7325', '7330', '4110',
            '4116', '4117', '4120',
            '4125', '4130', '41E55', '41LF20', '7416', '7417', '7418', '7420', '7425', '7430', '74E55', '4617', '4618',
            '4619', '4620', '4625',
            '4630', '46LF20', '46LF25', '5116', '5617', '5618', '5619', '5620', '5625', '5630', '56E55', '200INS',
            '200M25', '200SPP',
            '201IFU', '201INS', '201M25', '201SPP', '190ERP', '36D1', '36ERP', '37D1', '37ERP', '38D1', '38ERP', '39D1',
            '39ERP', '40D1', '40ERP', '41D1', '41ERP', '42D1', '42ERP', '49D1', '49ERP', '50D1', '50ERP', '51D1',
            '51ERP', '52D1', '52ERP', '56D1', '56ERP', '57D1', '57ERP', '58D1', '58ERP', '59ERP', '60ERP', '61ERP',
            '62ERP', '63ERP', '64ERP', '65ERP', '66D1', '66ERP', '70ERP', '71ERP', '72ERP', '73D1', '73ERP', '74D1',
            '74ERP', '75ERP', '76ERP', '40WD1', '40WERP', '39PP', '39WC', '1016PP', '1033', '1033PP', '1046PP',
            '1046WC',
            '190WC', '190WCP', '191WCP', '37PP', '37WC', '37WCP', '41PP', '41WC', '4216PP', '4216WC', '45WC', '47WC',
            '5033PP', '5033WC', '5137PP', '5137WC', '5237PP', '5237WC', '52PP', '52WC', '5646PP', '5646WC', '5737PP',
            '5737WC', '57PP', '57WC', '5837PP', '5837WC', '6037PP', '6037WC', '6137PP', '6137WC', '6237PP', '6237WC',
            '6337PP', '6337WC', '6437PP', '6437WC', '64PP', '64WC', '6537PP', '6537WC', '6637PP', '6637WC', '66PP',
            '66WC', '7037PP', '7037WC', '70PP', '70WC', '71PP', '71WC', '72PP', '72WC', '73PP', '73WC', '74PP', '74WC',
            'ATH01', 'ATH101', 'ATH102', 'ATH103', 'ATH104', 'ATH164', 'ATH21', 'ATH22', 'ATH23', 'ATH24', 'ATH25',
            'ATH26', 'ATH41', 'ATH61', 'ATH62', 'ATH63', 'ATH64', 'ATH65', '2042', '2047', '75E55', '76E55', '5.90E+56',
            '3.70E+56', '59ERP', '40E55', '4.00E+56', 'G'
        ]))]
        stv_eft_final = stv_eft.loc[(stv_eft['Pmt Type'] == 'EFT')
                                    | (stv_eft['COR Type'] == 'EFT')
                                    & (stv_eft['Pmt Type'].isin(['NSF', 'COR']))]
        stv_eft_final = stv_eft_final.astype({"Client#": str})
        # stv_eft_final['Date'] = stv_eft_final['Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
        stv_eft_final['Total Pay'] = stv_eft_final['PRN'] + stv_eft_final['Int'] + stv_eft_final['Atty'] + \
                                     stv_eft_final['Misc'] + stv_eft_final['CC'] + stv_eft_final['PJI']
        stv_eft_final.to_excel(writer, sheet_name='STV_EFT', index=False)
        book_to_facs_summary(stv_eft_final, writer, "STV_EFT_Summary")


    except Exception as e:
        logging.exception("Error in spitting community statement")


def splitting_RCR_TCR(books_to_facs_statement):
    try:
        RCR_TCR = books_to_facs_statement.loc[
            (books_to_facs_statement['Client#'].isin(['5013', '9013', '501AWP', '501ECA', '53ERP',
                                                      '53WCP', '53WPP', '1041DA', '1041', '1041BD', '1041PP', '128WCP',
                                                      '128AWP', '128E25', '128ECA', '128ERP', '128I55', '128INS',
                                                      '128R25', '128R55', '128REC', '128SPP',
                                                      '132AWP', '132E25', '132E55', '132ECA', '132ERP', '132I55',
                                                      '132INS', '132M25', '132MDM', '132R25',
                                                      '132R55', '132REC', '132SPP', '132WCP', '3032', '129AWP',
                                                      '129E25', '129ECA', '129ERP', '129I55', '129INS',
                                                      '129R25', '129R55', '129REC', '129SPP', '129WCP', '130AWP',
                                                      '130E25', '130ECA', '130ERP', '130I55',
                                                      '130INS', '130R25', '130R55', '130SPP', '130WCP', '127AWP',
                                                      '127E25', '127ECA', '127ERP', '127I55',
                                                      '127INS', '127R25', '127R55', '127REC', '127SPP', '127WCP',
                                                      '1014', '2014', '3014', '9014', '2014F', '210ERP',
                                                      '210M25', '210WCP', '210WPP', '239E25', '239I55', '239INS',
                                                      '239R25', '239R55', '239SPP', '238E25',
                                                      '238I55', '238INS', '238R25', '238R55', '238REC', '238SEC',
                                                      '238SPP', '239BD', '237E25', '237I55',
                                                      '237INS', '237R25', '237R55', '237REC', '237SEC', '237SPP',
                                                      '200ERP', '200WCP', '200WPP', '205ERP',
                                                      '205WCP', '220AWP', '220E25', '220ECA', '220ERP', '220I55',
                                                      '220INS', '220M25', '220R25', '220R55',
                                                      '220SPP', '220WCP', '221ERP', '221WCP', '221AWP', '221ECA',
                                                      '221I55', '221INS', '221R55', '221SPP', '3003',
                                                      '5003', '9003', '9004', '1.6E+27', '160I55', '160INS', '160MDM',
                                                      '160PAY', '160R25', '160R55', '160SPP',
                                                      '160TST', '161I55', '161INS', '161MDM', '161PAY', '161R55',
                                                      '161SPP', '222BD', '222INS', '222PRJ',
                                                      '22BIFU', '22CIFU', '22TIFU', '22VIFU', '22WIFU', '240ERP',
                                                      '240WCP', '240WPP', '241ERP', '241WCP',
                                                      '241WPP', '264I55', '264R25', '264R55', '150E25', '150I55',
                                                      '150INS', '150R25', '150R55', '150SPP',
                                                      '151INS', '1010', '3010', '1010PP', '1006', '2006', '3006',
                                                      '4006', '5006', '1006PP', '135E25', '135I55', '135INS',
                                                      '135R25', '135R55', '135SPP', '239WCP', '239WPP', '230IFU',
                                                      '230RBP', '230WCP', '230WPP', '236WCP',
                                                      '236WPP', '232WCP', '232WPP', '235WCP', '235WPP', '234WCP',
                                                      '234WPP', '231WCP', '231WPP', '233WCP',
                                                      '233WPP', '1004', '3004', '104AWP', '104ECA', '104ERP', '104M25',
                                                      '104R25', '104R55', '104W55', '104WCP',
                                                      '201AWP', '201ECA', '201ERP', '201WCP', '202AWP', '202ECA',
                                                      '202ERP', '202WCP', '131E25', '131I55',
                                                      '131INS', '131M25', '131R25', '131R55', '131SPP', '131REC',
                                                      '133E25', '134E25', '133I55', '133INS',
                                                      '133R25', '133R55', '133SPP', '134I55', '134INS', '134PAY',
                                                      '134R25', '134R55', '134SPP', '134REC',
                                                      '140E25', '140DEN', '140FTE', '140I55', '140IFU', '140INS',
                                                      '140MDC', '140R25', '140R55', '140SPP',
                                                      '14E25F', '14I55F', '14INSF', '14R25F', '14R55F', '14SPPF',
                                                      '140ATY', '140AT3', '140AT2', '1500', '1501',
                                                      '1.28E+27', '1.32E+27', '1.32E+57', '1.29E+27', '1.3E+27',
                                                      '2.39E+27', '2.38E+27', '2.37E+27', '2038', '1.34E+27', '1.6E+27'
                                                         , "8205PC", "8205PM", "8201PC", "8201PM", "8203PC", "8203PM",
                                                      "8204PC", "8204PM", '1013', '3013', '5013P', '1034', '3034',
                                                      '5034', '1034PP',"8201SP","8203SP","8204SP","8205SP"
                                                         , '110E25', '110INS', '110SPP', '1015', '1015PP', '110ERP',
                                                      '110I55', '110M25', '110R25', '110R55', '110VET', '110WCP',
                                                      '110WPP', '128MDM'
                                                         , '128E55', '1032', '132MDC', '132IFM', '132IFU', '129MDM',
                                                      '129E55', '130MDM', '130E55', '127MDM', '127E55', '238ERP',
                                                      '237ERP', '237AWP'
                                                         , '1003', '105WCP', '200IFU', '201DEN', '131AWP', '131ECA',
                                                      '131ERP', '131MDM', '131E55', '131WCP', '1.10E+27', '1.29E+57',

                                                      '1.31E+57', '1.27E+57','237WCP','238WCP','229WCP','229ERP','766101','820902']))]

        RCR_TCR_final = RCR_TCR.loc[(RCR_TCR['Pmt Type'].isin(['RCR', 'TCR']))]

        RCR_TCR_final = RCR_TCR_final.astype({"Client#": str})
        # RCR_TCR_final['Date'] = RCR_TCR_final['Date'].apply( lambda x: x.strftime( '%m/%d/%Y' ))
        RCR_TCR_final['Total Pay'] = RCR_TCR_final['PRN'] + RCR_TCR_final['Int'] + RCR_TCR_final['Atty'] + \
                                     RCR_TCR_final['Misc'] + RCR_TCR_final['CC'] + RCR_TCR_final['PJI']

        return RCR_TCR_final
    except Exception as e:
        logging.exception("Error in splitting non_stv_cc statement")


def book_to_facs_summary(books, writer, sheet):
    try:
        df = books[
            ['Client Name', 'Client#', 'PRN', 'Int', 'Atty', 'Misc', 'CC', 'PJI', 'Total Pay', 'O/P Amt']].groupby(
            ['Client Name', 'Client#']).sum().stb.subtotal()
        df['PRN'] = df['PRN'].map('{:,.2f}'.format)
        df['Int'] = df['Int'].map('{:,.2f}'.format)
        df['Atty'] = df['Atty'].map('{:,.2f}'.format)
        df['Misc'] = df['Misc'].map('{:,.2f}'.format)
        df['CC'] = df['CC'].map('{:,.2f}'.format)
        df['PJI'] = df['PJI'].map('{:,.2f}'.format)
        df['Total Pay'] = df['Total Pay'].map('{:,.2f}'.format)
        df['O/P Amt'] = df['O/P Amt'].map('{:,.2f}'.format)
        df.to_excel(writer, sheet_name=sheet)

    except Exception as e:
        logging.exception("error")


def save_file_to_s3(year, month_name):
    session = boto3.Session(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key,
    region_name=bucket_region)
    s3 = session.resource('s3')
    my_bucket = s3.Bucket(bucket_name)
    i = local_output_directory + "Book_to_Facs"
    output_filename = i.split('/')[::-1][0]
    os.chdir(local_output_directory)
    shutil.make_archive(output_filename, 'zip', i);
    zipped_file = local_output_directory + output_filename + ".zip"
    xls_list = glob2.glob(i + "/*.xlsx");
    xls_list.append(zipped_file);
    y = zipped_file.split("/")[::-1][0]
    z = y.replace(".zip", "")
    path_s3 = output_bucket + "/" + z + "/" + str(year) + "/" + month_name + "/" + zipped_file.split("/")[::-1][0]
    my_bucket.upload_file(zipped_file, path_s3)
    for j in xls_list:
        if (".zip" not in j):
            y = j.split("/")[::-1][0];
            z = y.replace(".xlsx", "")
            excle_s3 = "Exception_Report_Input" + "/" + "Book_to_Facs" + "/" + str(year) + "/" + month_name + "/" + y
            my_bucket.upload_file(j, excle_s3)
    for file_name in xls_list:
        os.remove(file_name)


if __name__ == "__main__":
    print("starting data ::::::::::: ", datetime.datetime.now())
    # creation of log file
    logging.basicConfig(filename=local_log_directory+"book_to_facs.log", filemode='a', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    cli = boto3.client("s3")
    if ((datetime.datetime.now().month) != 1):
        year = datetime.datetime.now().year
        month = (datetime.datetime.now().month) - 1
        month_name = calendar.month_name[month]

    else:
        year = datetime.datetime.now().year - 1
        month = (datetime.datetime.now().month) - 1
        month_name = calendar.month_name[month]

    data = cli.get_object(Bucket=bucket_name,Key=input_bucket+"/Book_to_Facs/" + str(year) + "/" + month_name + "/" + "payrpt.csv")
    data = data['Body'].read()
    books_to_facs_data = pd.read_csv(io.BytesIO(data), sep="|", error_bad_lines=False, index_col=False,
                                     dtype={"Client#": str})
    books_to_facs_data.loc[books_to_facs_data['Pmt Type'] == "COR", 'O/P Amt'] = -abs(books_to_facs_data['O/P Amt'])
    books_to_facs_data['Date'] = pd.to_datetime(books_to_facs_data['Date'], errors='coerce').dt.strftime('%m-%d-%Y')
    writer = pd.ExcelWriter(local_output_directory+'Book_to_Facs/book_to_facs.xlsx', engine='xlsxwriter')
    books_to_facs_data.to_excel(writer, sheet_name='payrpt', index=False)
    rcr_tcr = splitting_RCR_TCR(books_to_facs_data)
    splitting_non_stv(writer, books_to_facs_data)
    splitting_non_stv_cc(writer, books_to_facs_data)
    splitting_non_stv_eft(writer, books_to_facs_data)
    splitting_community(writer, books_to_facs_data)
    splitting_community_cc(writer, books_to_facs_data)
    splitting_community_eft(writer, books_to_facs_data)
    splitting_med1(writer, books_to_facs_data)
    splitting_med1_cc(writer, books_to_facs_data)
    splitting_med1_eft(writer, books_to_facs_data)
    splitting_stv(writer, books_to_facs_data)
    splitting_stv_cc(writer, books_to_facs_data)
    splitting_stv_eft(writer, books_to_facs_data)
    rcr_tcr.to_excel(writer, sheet_name='RCR', index=False)
    writer.save()
    save_file_to_s3(year, month_name)
    print("ending data ::::::::::: ", datetime.datetime.now())
