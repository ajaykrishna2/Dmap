from Utility.st_vincent_dunn import *
from Utility.read_input_file_for_hospital import *
from Utility.save_output_to_folder_dunn import *
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
    logging.basicConfig(filename=local_output_directory+"st-vincent-dunn_data.log",
                        filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')

    
    #splitting St vicent dunn statement
    st_vicent_dunn= read_input_file_for_hospital.collect_and_preprocess_st_vicent_dunn()
    st_vicent_non_facs_dunn.splitting_vincent_dunn_statement(st_vicent_dunn)
    save_dunn_statement_to_output_folder.save_file_to_s3()

    print("ending data ::::::::::: ", datetime.datetime.now())

