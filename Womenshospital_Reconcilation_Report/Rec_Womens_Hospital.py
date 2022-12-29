from Utility.womenshospital_reconcilation import *
from Utility.save_file import *
from Utility.read_file import *
import logging, datetime
import xlrd
from openpyxl.workbook import Workbook
import xlsxwriter
import os
import configparser
configuartion_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path)
local_output_directory = config['Log_Location']['path']
class Womenshospital_reconcilation:
    print("starting data ::::::::::: ",datetime.datetime.now())
    # creation of log file
    logging.basicConfig(filename=local_output_directory+'Womenshospital_reconcilation.log',filemode='a', level=logging.DEBUG,
                       format='%(asctime)s %(levelname)s %(name)s %(message)s')
    #Read required input
    obj = read()
    reconcilation_read = obj.collect_and_preprocess_womenshospital_data()
    info_out_read=obj.info_out_read()
    reconcilation =womenshospital_reconcilation_report()
    reconcilation.Womenshospital(reconcilation_read,info_out_read)
    save_file = save_statement_to_output_folder()
    save_file.save_file_to_s3()
    print("ending data ::::::::::: ", datetime.datetime.now())

