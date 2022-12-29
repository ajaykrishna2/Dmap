from Utility.st_vicent_invission import *
from Utility.st_vicent_sorian import *
from Utility.st_vicent_non_facs import *
from Utility.read_input_file_for_hospital import *
from Utility.save_output_to_folder import *
import logging, datetime
import xlrd
from openpyxl.workbook import Workbook
import xlsxwriter
import os
import  configparser

configuartion_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);

local_output_directory = config['Log_Location']['path']


class billing_payment_automation:
    print("starting data ::::::::::: ",datetime.datetime.now())
    # creation of log file
    logging.basicConfig(filename=local_output_directory+"st-vincent_data.log",
                        filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')

    #splitting st vicent data
    st_vicent_data = read_input_file_for_hospital.collect_and_preprocess_st_vicent()
    print(st_vicent_data)
    st_vincent_invision.invision(st_vicent_data)
    st_vincent_soarian.soarian(st_vicent_data)
    #splitting non facs statements
    st_vicent_non_facs_data = read_input_file_for_hospital.collect_and_preprocess_st_vicent_non_facs()
    st_vicent_non_facs.splitting_d1_accident_statement(st_vicent_non_facs_data)
    st_vicent_non_facs.splitting_d1_wc_statement(st_vicent_non_facs_data)
    st_vicent_non_facs.splitting_pbs_statement(st_vicent_non_facs_data)
    st_vicent_non_facs.St_Vincent_PBS_Athena(st_vicent_non_facs_data)
    save_statement_to_output_folder.save_file_to_s3()

    print("ending data ::::::::::: ", datetime.datetime.now())

