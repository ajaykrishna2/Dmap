from Utility.st_vincent_exception_report import *
from Utility.save_file import *
from Utility.read_file import *
import logging, datetime
import xlrd
from openpyxl.workbook import Workbook
import xlsxwriter
configuartion_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);

local_output_directory = config['Log_Location']['path']
local_directory = config['Output_Location']['exception_input'];

class st_vincent_exception:
    print("starting data ::::::::::: ",datetime.datetime.now())
    # creation of log file
    logging.basicConfig(filename=local_output_directory+'stvincent_exception.log',
                        filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    
    #To create input data in s3
    save_file = save_statement_to_output_folder()
    #Read required input
    obj = read_input_for_exception()
    st_vincent_read = obj.st_vincent_read()
    save_file.send_statement(st_vincent_read,"data","st_vincent_repo","input/St_Vincent")
    st_vincent_hospital = pd.read_excel(local_directory+"St_Vincent/st_vincent_repo.xlsx")
    book_to_facs = obj.book_to_facs_read()
    #Creating exception report
    exception = vincent_exception()
    exception.Amount_Validation(st_vincent_hospital,book_to_facs)
    exception.Exception_report(st_vincent_hospital,book_to_facs)
    save_file.save_file_to_s3()
    print("ending data ::::::::::: ", datetime.datetime.now())

