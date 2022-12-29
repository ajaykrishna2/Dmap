import pandas as pd
import os
import boto3
import datetime
import calendar
import configparser

configuartion_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);
aws_access_key = config['Aws_Credential']['s3_access_key']
aws_secret_key = config['Aws_Credential']['s3_secret_key']
bucket_region  = config['Aws_Credential']['bucket_region']
bucket_name            = config['Aws_Credential']['bucket_name'];
input_bucket           = config['Aws_Credential']['input_base_path'];
output_bucket          = config['Aws_Credential']['output_base_path'];
local_output_directory = config['Output_Location']['exception_report'];
local_input_directory  = config['Output_Location']['exception_input'];
directory_path         =  config['Output_Location']['path'];


class save_statement_to_output_folder:
    def save_file_to_s3(self):
        if ((datetime.datetime.now().month) != 1):
                year = datetime.datetime.now().year
                month = (datetime.datetime.now().month) - 1
                month_name = calendar.month_name[month]

        else:
                year = datetime.datetime.now().year - 1
                month = (datetime.datetime.now().month) - 1
                month_name = calendar.month_name[month]
        session = boto3.Session(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key,
        region_name=bucket_region)
        s3 = session.resource('s3')
        my_bucket = s3.Bucket(bucket_name)
        i = local_output_directory+ "Good_Samaritan_Family"
        output_filename = i.split('/')[::-1][0]
        directory_contents = os.listdir(i)
        for j in directory_contents:
            path_s3 = "Exception_Report_Output"+ "/" + "Exec_Good_Samaritan_Family_Health" + "/" + str(year) + "/" + month_name + "/" + j
            print(path_s3)
            my_bucket.upload_file(i+"/"+j, path_s3)
        for j in directory_contents:
           os.remove(os.path.join(local_output_directory+output_filename+"/"+j))
        os.remove(local_input_directory+"Good_Samaritan_Family/good_sam_family_repo.xlsx")
    def send_statement(self,statement_file, sheet_name, file_name, folder_name):
        s3 = boto3.client("s3")
        file_name = file_name + ".xlsx"
        if not os.path.exists(os.path.join(directory_path+folder_name, file_name)):
            writer = pd.ExcelWriter(os.path.join(directory_path+folder_name, file_name),
                                    engine='openpyxl')
            statement_file.to_excel(writer, sheet_name=sheet_name, index=False)
            writer.save()
        else:
            writer = pd.ExcelWriter(os.path.join(directory_path+folder_name, file_name), engine='openpyxl'
                                    , mode='a')
            statement_file.to_excel(writer, sheet_name=sheet_name, index=False)
            writer.save()

