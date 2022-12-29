from Utility.splitting_community_health_network import *
from Utility.splitting_howard6019 import *
from Utility.splitting_howard_epic_cbs import *
from Utility.splitting_howard_med1_non_epic import *
from Utility.splitting_howard_west_campus_epic import *
from Utility.splitting_howardCC import *
from Utility.splitting_howard_cbs_non_epic import *
from Utility.splitting_reid import *
from Utility.splitting_6019_non_epic import *
from Utility.splitting_westview import *
from Utility.splitting_vei import *
from Utility.splitting_vei_surgery_cbs import *
from Utility.splitting_vei_surgery_centers import *
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


class community_payment_automation:
    print("starting data ::::::::::: ",datetime.datetime.now())
    # creation of log file
    logging.basicConfig(filename=local_output_directory+"community_data.log",
                        filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    # read file from folder and filter necessary condition
    community_client_statement = read_input_file_for_hospital.collect_and_preprocess_input()
    #  splitting community data
    splitting_community_health_network_statement(community_client_statement)
    splitting_howard6019(community_client_statement)
    splitting_howard_epic_cbs(community_client_statement)
    splitting_howard_med1_non_epic(community_client_statement)
    splitting_howard_west_campus_epic(community_client_statement)
    splitting_howardCC(community_client_statement)
    splitting_howard_cbs_non_epic(community_client_statement)
    splitting_reid(community_client_statement)
    splitting_westview(community_client_statement)
    splitting_6019_non_epic(community_client_statement)


    community_client_statement1 = read_input_file_for_hospital.collect_preprocess_cal_fees_input()
    splitting_vei(community_client_statement1)
    splitting_vei_surgery_cbs(community_client_statement1)
    splitting_vei_surgery_centers(community_client_statement1)

    save_statement_to_output_folder.save_file_to_s3()

    print("ending data ::::::::::: ", datetime.datetime.now())

