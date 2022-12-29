import configparser
import pandas as pd
import os
import boto3
import datetime
from datetime import timedelta
import shutil
import glob2
import calendar

configuartion_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);
aws_access_key = config['Aws_Credential']['s3_access_key']
aws_secret_key = config['Aws_Credential']['s3_secret_key']
bucket_region  = config['Aws_Credential']['bucket_region']
bucket_name            = config['Aws_Credential']['bucket_name'];
input_bucket           = config['Aws_Credential']['input_base_path'];
output_bucket          = config['Aws_Credential']['output_base_path']
local_output_directory = config['Output_Location']['good_samaritan']
local_log_directory    = config['Log_Location']['path']


class save_statement_to_output_folder:
    
    def save_file_to_s3(self,date_range,path):
    
        year = path.split("/")[::-1][3]
        month_name= path.split("/")[::-1][2]
        session = boto3.Session(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key,
        region_name=bucket_region)
        s3 = session.resource('s3')
        my_bucket = s3.Bucket(bucket_name)
        i = local_output_directory + "Good_Samaritan"
        output_filename = i.split('/')[::-1][0]+"_" +date_range
        os.chdir(local_output_directory)
        shutil.make_archive(output_filename, 'zip', i);
        zipped_file = local_output_directory + output_filename +".zip"
        xls_list = glob2.glob(i + "/*.xlsx");
        xls_list.append(zipped_file)
        path_s3 ='BA_output_folder/Good_Samaritan/'+ str(year)+"/"+month_name+"/" +zipped_file.split("/")[::-1][0]
        my_bucket.upload_file(zipped_file, path_s3)
        for j in xls_list:
            if (".zip" not in j):
                y = j.split("/")[::-1][0];
                z = y.replace(".xlsx", "")
                excle_s3 = "Exception_Report_Input" + "/" + "Exec_Good_Samaritan" + "/" + str(year) + "/" +\
                month_name + "/" + y
                my_bucket.upload_file(j, excle_s3)
        for file_name in xls_list:
            os.remove(file_name)

    def send_statement(self, statement_file, sheet_name, file_name, folder_name,date_range):

        # saving input file to output location
        s3 = boto3.client("s3")
        file_name = file_name + "_" + date_range +".xlsx"
        if not os.path.exists(os.path.join(local_output_directory + folder_name, file_name)):
            writer = pd.ExcelWriter(os.path.join(local_output_directory + folder_name, file_name),
                                    engine='openpyxl')
            statement_file.to_excel(writer, sheet_name=sheet_name, index=False)
            writer.save()
        else:
            writer = pd.ExcelWriter(os.path.join(local_output_directory + folder_name, file_name), engine='openpyxl'
                                    , mode='a')
            statement_file.to_excel(writer, sheet_name=sheet_name)
            writer.save()

