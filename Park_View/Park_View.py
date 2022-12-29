from Utility.park_view import *
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


class parkview_billing_payment_automation:
    print("starting data ::::::::::: ",datetime.datetime.now())
    # creation of log file
    logging.basicConfig(filename=local_output_directory+"parkview_data.log",filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    #splitting park view statement
    park_view_statement=read_input_file_for_hospital.collect_and_preprocess_parkview_data()
    park_view(park_view_statement)

    save_statement_to_output_folder.save_file_to_s3()

    print("ending data ::::::::::: ", datetime.datetime.now())

