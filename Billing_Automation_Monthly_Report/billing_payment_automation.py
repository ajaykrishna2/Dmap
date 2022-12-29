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
from Utility.deaconess_dsp import *
from Utility.deaconess_gibson import *
from Utility.deaconess_health_heart import *
from Utility.deaconess_health_sys import *
from Utility.deaconess_heart_hospital import *
from Utility.deaconess_henderson import *
from Utility.deaconess_union_county import *
from Utility.union_county_hospital import *
from Utility.womens_hospital import *
from Utility.st_vicent_invission import *
from Utility.st_vicent_sorian import *
from Utility.st_vicent_non_facs import *
from Utility.park_view import *
from Utility.read_input_file_for_hospital import *
from Utility.save_output_to_folder import *
from Utility.good_samaritan_family import *
import logging, datetime
import xlrd
from openpyxl.workbook import Workbook
import xlsxwriter

configuartion_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);

local_output_directory = config['Log_Location']['path']


class billing_payment_automation:

    print("starting data ::::::::::: ", datetime.datetime.now())
    # creation of log file
    logging.basicConfig(filename=local_output_directory+'monthly_statements.log',
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

    # spliiting deaconess data
    deaconess_complete_data = read_input_file_for_hospital.collect_and_preprocess_deaconess_data()
    deaconess_dsp(deaconess_complete_data)
    deaconess_gibson(deaconess_complete_data)
    deaconess_health_heart(deaconess_complete_data)
    deaconess_health_sys(deaconess_complete_data)
    splitting_heart_hospital(deaconess_complete_data)
    deaconess_henderson(deaconess_complete_data)
    deaconess_union_county(deaconess_complete_data)
    union_county_hospital(deaconess_complete_data)

    # splitting womens data
    women_data = read_input_file_for_hospital.collect_and_preprocess_women_data()
    womens_hospital(women_data)

    # splitting st vicent data
    st_vicent_data = read_input_file_for_hospital.collect_and_preprocess_st_vicent()
    st_vicent_invission(st_vicent_data)
    st_vicent_sorian(st_vicent_data)

    st_vicent_non_facs_data = read_input_file_for_hospital.collect_and_preprocess_st_vicent_non_facs()
    st_vicent_non_facs.splitting_d1_accident_statement(st_vicent_non_facs_data)
    st_vicent_non_facs.splitting_d1_wc_statement(st_vicent_non_facs_data)
    st_vicent_non_facs.splitting_pbs_statement(st_vicent_non_facs_data)
    st_vicent_non_facs.St_Vincent_PBS_Athena(st_vicent_non_facs_data)

    # splitting St vicent dunn statement
    st_vicent_dunn= read_input_file_for_hospital.collect_and_preprocess_st_vicent_dunn()
    st_vicent_non_facs.splitting_vincent_dunn_statement(st_vicent_dunn)

    # splitting park view statement
    park_view_statement = read_input_file_for_hospital.collect_and_preprocess_parkview_data()
    park_view(park_view_statement)
    
    # Splitting Good samaritan family health statement
    good_samaritan_family_statement = read_input_file_for_hospital()
    good_samaritan_preprocess = good_samaritan_family_statement.collect_and_preprocess_good_samaritan_family_input()
    good_samaritan_statement = good_samaritan(good_samaritan_preprocess)
    good_samaritan_statement.splitting_gs_cbs_statement()
    good_samaritan_statement.splitting_gs_med1_statement()

    save_statement_to_output_folder.save_file_to_s3()

    print("ending data ::::::::::: ", datetime.datetime.now())
