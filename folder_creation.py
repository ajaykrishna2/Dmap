import os
import configparser

configuartion_path = os.path.dirname(os.path.abspath(__file__))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);

monthly_report   = config['Output_Location']['monthly_report']
book_to_facs     = config['Output_Location']['book_to_facs_report']
weekly_report    = config['Output_Location']['good_samaritan']
exception_path  = config['Output_Location']['path']
exception_report = config['Output_Location']['exception_report']
exception_input  = config['Output_Location']['exception_input']


monthly_report_list = ['Community','Deaconess','Good_Samaritan','Park_View','St_Vincent','St_Vincent_Dunn','Womens_Hospital','stv_repo'];
book_to_facs_var   = 'Book_to_Facs';
weekly_report_var  = 'Good_Samaritan';


def create_base_directory(path):

    if not os.path.exists(path):
        os.makedirs(path);


def create_directory(param):

    if(param in ('monthly_report')):
        for i in monthly_report_list:
         if not os.path.exists(monthly_report+i):
             os.mkdir(monthly_report+i);
         else:
             pass;
    elif(param in ('exception_report')):
        for i in monthly_report_list:
            if not os.path.exists(exception_report + i):
                os.mkdir(exception_report+ i);
            else:
                pass;
    elif (param in ('exception_input')):
        for i in monthly_report_list:
            if not os.path.exists(exception_input + i):
                os.mkdir(exception_input + i);
            else:
                pass;

    elif(param=='book_to_facs'):
        if not os.path.exists(book_to_facs + book_to_facs_var):
            os.mkdir(book_to_facs + book_to_facs_var);
        else:
            pass;

    elif (param == 'weekly_report'):

        if not os.path.exists(weekly_report + weekly_report_var):
            os.mkdir(weekly_report + weekly_report_var);
        else:
            pass;

base_directory = [monthly_report,book_to_facs,weekly_report,exception_path,exception_report,exception_input];
param_list     = ['monthly_report','exception_report','exception_input','book_to_facs','weekly_report']
for i in base_directory:
  create_base_directory(i);
for j in param_list:
 create_directory(j);

