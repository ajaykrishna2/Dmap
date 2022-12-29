from Utility.riverview_reconcilation import *
from Utility.save_file import *
from Utility.read_file import *
import logging, datetime
from openpyxl.workbook import Workbook
import os
import configparser

configuartion_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path)
local_output_directory = config['Log_Location']['path']
class Riverview_reconcilation:
    print("starting data ::::::::::: ",datetime.datetime.now())
    # creation of log file
    logging.basicConfig(filename=local_output_directory+'Riverview_reconcilation.log',
                        filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    
    #To create input data in s3
    save_file = save_statement_to_output_folder()
    #Read required input
    obj = read_input_for_reconcilation()
    reconcilation_read = obj.collect_and_preprocess_riverview_data()
    
    #Creating reconcilation report
    reconcilation = riverview_reconcilation_report()
    reconcilation.Riverview(reconcilation_read)
    save_file.save_file_to_s3()
    print("ending data ::::::::::: ", datetime.datetime.now())

