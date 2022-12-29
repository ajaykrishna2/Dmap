from Utility.read_file import *
from Utility.Booktofacs import *
from Utility.save_file import *
import logging, datetime
import os
import configparser
configuartion_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);

local_output_directory = config['Log_Location']['path']

class Booktofacs_Exception:
    print("starting data ::::::::::: ", datetime.datetime.now())
    # creation of log file
    logging.basicConfig(filename=local_output_directory + 'book_to_facs_excepiton.log',
                        filemode='a', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    # Read required input
    obj = read_input_for_exception()
    book_to_facs_read = obj.book_to_facs_read()
    # Saving output to s3
    save_file = save_statement_to_output_folder()
    # Creating exception report
    exception = book_to_facs_exception()
    exception.Amount_validation(book_to_facs_read[0],book_to_facs_read[1],book_to_facs_read[2],book_to_facs_read[3],\
    book_to_facs_read[4],book_to_facs_read[5],save_file)
    exception.Exception_report(book_to_facs_read[0],book_to_facs_read[1],book_to_facs_read[2],book_to_facs_read[3],\
    book_to_facs_read[4],book_to_facs_read[5],save_file)
    save_file.save_file_to_s3()
    print("ending data ::::::::::: ", datetime.datetime.now())
