from Utility.deaconess_dsp import *
from Utility.deaconess_gibson import *
from Utility.deaconess_health_heart import *
from Utility.deaconess_health_sys import *
from Utility.deaconess_heart_hospital import *
from Utility.deaconess_henderson import *
from Utility.union_county_hospital import *
from Utility.deaconess_union_county import *
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


class deaconess_payment_automation:
    print("starting data ::::::::::: ",datetime.datetime.now())
    # creation of log file
    logging.basicConfig(filename=local_output_directory+"deaconess_data.log",
                        filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    # read file from folder and filter necessary condition
    #spliiting deaconess data
    deaconess_complete_data = read_input_file_for_hospital.collect_and_preprocess_deaconess_data()
    deaconess_dsp(deaconess_complete_data)
    deaconess_gibson(deaconess_complete_data)
    deaconess_health_heart(deaconess_complete_data)
    deaconess_health_sys(deaconess_complete_data)
    splitting_heart_hospital(deaconess_complete_data)
    deaconess_henderson(deaconess_complete_data)
    union_county_hospital(deaconess_complete_data)
    deaconess_union_county(deaconess_complete_data)
    save_statement_to_output_folder.save_file_to_s3()

    print("ending data ::::::::::: ", datetime.datetime.now())

    
