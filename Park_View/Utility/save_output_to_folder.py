import configparser
import pandas as pd
import shutil
import glob2
import calendar
import os,datetime
import boto3

configuartion_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);

bucket_name            = config['Aws_Credential']['bucket_name'];
input_bucket           = config['Aws_Credential']['input_base_path'];
output_bucket          = config['Aws_Credential']['output_base_path'];
local_output_directory = config['Output_Location']['monthly_report']


class save_statement_to_output_folder:

    @classmethod
    def save_file_to_s3(cls):
        if((datetime.datetime.now().month)!=1):
            year  = datetime.datetime.now().year
            month = (datetime.datetime.now().month) -1
            month_name = calendar.month_name[month]

        else:
            year = datetime.datetime.now().year -1
            month = (datetime.datetime.now().month) - 1
            month_name = calendar.month_name[month]

        s3 = boto3.resource("s3")
        my_bucket = s3.Bucket(bucket_name)
        i = local_output_directory+ "Park_View"
        print(i)
        output_filename = i.split('/')[::-1][0]
        os.chdir(local_output_directory)
        shutil.make_archive(output_filename, 'zip', i);
        zipped_file = local_output_directory + output_filename + ".zip"
        xls_list = glob2.glob(i + "/*.xlsx");
        xls_list.append(zipped_file);
        y = zipped_file.split("/")[::-1][0]
        z = y.replace(".zip", "")
        path_s3 = output_bucket+ "/" + z + "/" + str(year) + "/" + month_name + "/" + zipped_file.split("/")[::-1][0]
        my_bucket.upload_file(zipped_file, path_s3)
        for file_name in xls_list:
            os.remove(file_name)


    @classmethod
    def send_statement(cls,statement_file, sheet_name, file_name, folder_name):

        # saving input file to output location
        # need to work on this, saving in current directory
        file_name = file_name + ".xlsx"
        if not os.path.exists(os.path.join(local_output_directory+folder_name, file_name)):
            writer = pd.ExcelWriter(os.path.join(local_output_directory+folder_name, file_name),engine='openpyxl')
            statement_file.to_excel(writer, sheet_name=sheet_name, index=False)
            writer.save()
        else:
            writer = pd.ExcelWriter(os.path.join(local_output_directory+folder_name, file_name), engine='openpyxl', mode='a')
            statement_file.to_excel(writer, sheet_name=sheet_name, index=False)
            writer.save()


