from Utility.comm_epic_recon_reconcilation import *
from Utility.save_file import *
from Utility.read_file import *
import logging, datetime
import xlrd
from openpyxl.workbook import Workbook
import xlsxwriter
import os
import configparser
configuartion_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path)
local_output_directory = config['Log_Location']['path']
class Comm_epic_recon_reconcilation:
    print("starting data ::::::::::: ",datetime.datetime.now())
    # creation of log file
    logging.basicConfig(filename=local_output_directory+'Comm_epic_recon_reconcilation.log',filemode='a', level=logging.DEBUG,
                       format='%(asctime)s %(levelname)s %(name)s %(message)s')
    #Read required input
    obj = read()
    reconcilation_read = obj.collect_and_preprocess_comm_epic_recon_data()
    reconcilation =comm_epic_recon_reconcilation_report()
    reconcilation.Comm_epic_recon(reconcilation_read)
    save_file = save_statement_to_output_folder()
    save_file.save_file_to_s3()
    print("ending data ::::::::::: ", datetime.datetime.now())

