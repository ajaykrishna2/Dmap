from Utility.good_samaritan import *
from Utility.read_input_file import *
from Utility.save_output_file import *
import logging,datetime
import xlrd
from openpyxl.workbook import Workbook
import xlsxwriter
import configparser

configuartion_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);

local_output_directory = config['Log_Location']['path']

class weekly_billing_automation:
    print("starting data ::::::::::: ",datetime.datetime.now())
    # creation of log file
    logging.basicConfig(filename=local_output_directory+"good_samaritan.log",
                        filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    # read file from folder and filter necessary condition
    read_file = read_input_file_for_hospital()
    good_samaritan_preprocess = read_file.collect_and_preprocess_input()
    #  splitting good summaritan data
    good_samaritan_statement = good_samaritan(good_samaritan_preprocess)
    good_samaritan_statement.splitting_gs_cbs_statement()
    good_samaritan_statement.splitting_gs_med1_statement()
    save_file = save_statement_to_output_folder()
    save_file.save_file_to_s3(good_samaritan_preprocess[1],good_samaritan_preprocess[2])

    print("ending data ::::::::::: ", datetime.datetime.now())


