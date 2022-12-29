from gads_process.g_ads import *
from gads_process.db_connection import *
import logging
import os
import configparser
configuartion_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);
log_directory = config['Log_Dir']['path']
if __name__=="__main__":
    data1 = db().db_creds()
    datan = dict((key, val) for k in data1 for key, val in k.items())
    cid = datan['cid']
    logging.basicConfig(filename=log_directory + "ga_ads.log", filemode='a', level=logging.DEBUG,
                       format='%(asctime)s %(levelname)s %(name)s %(message)s')
    data1 = db().db_creds()
    GADS().get_google_ads_data(cid)
