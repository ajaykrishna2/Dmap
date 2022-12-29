from Utility.good_samaritan_exception import *
from Utility.save_file import *
from Utility.read_file import *
import logging, datetime
import os
import configparser
configuartion_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);

local_output_directory = config['Log_Location']['path']
local_directory = config['Output_Location']['exception_input'];

class st_vincent_exception:
    print("starting data ::::::::::: ",datetime.datetime.now())
    # creation of log file
    logging.basicConfig(filename=local_output_directory+'good_sam_exception.log',
                        filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    

    save_file = save_statement_to_output_folder()
    #Read required input
    obj = read_input_for_exception()
    good_sam_read = obj.good_sam_read()
    save_file.send_statement(good_sam_read,"data","good_sam_repo","input/Good_Samaritan")
    good_sam_hospital = pd.read_excel(local_directory+"Good_Samaritan/good_sam_repo.xlsx")
    book_to_facs = obj.book_to_facs_read()
    #Creating exception report
    exception = good_sam_exception()
    exception.Amount_Validation(good_sam_hospital,book_to_facs)
    exception.Exception_report(good_sam_hospital,book_to_facs)
    save_file.save_file_to_s3()
    print("ending data ::::::::::: ", datetime.datetime.now())

