import configparser
import pandas as pd
import shutil
import glob2
import calendar
import os,datetime
import boto3

configuartion_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path)
aws_access_key = config['Aws_Credential']['s3_access_key']
aws_secret_key = config['Aws_Credential']['s3_secret_key']
bucket_region  = config['Aws_Credential']['bucket_region']
bucket_name    = config['Aws_Credential']['bucket_name']
input_bucket   = config['Aws_Credential']['input_base_path']
output_bucket  = config['Aws_Credential']['output_base_path']
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
        session = boto3.Session(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key,
        region_name=bucket_region)
        s3 = session.resource('s3')
        my_bucket = s3.Bucket(bucket_name)
        directory_contents = []
        static_list = ['Community','Deaconess','Park_View','St_Vincent','St_Vincent_Dunn','Womens_Hospital','Good_Samaritan_Family']
        directory_contents_list = glob2.glob(local_output_directory+"*");
        for folder_name in directory_contents_list:
            for fname in static_list:
                f_lower = folder_name.lower()
                n_lower = fname.lower()
                if(n_lower in f_lower):
                    directory_contents.append(folder_name);
        for i in directory_contents:
            base_dir= local_output_directory
            output_filename = i.split('/')[::-1][0]
            os.chdir(base_dir)
            shutil.make_archive(output_filename, 'zip',i)
        zipped_files = glob2.glob(local_output_directory+"*.zip")
        for file_name in zipped_files:
                y = file_name.split("/")[::-1][0]
                z  = y.replace(".zip","")
                path = "BA_output_folder/"+z+"/"+str(year)+"/"+month_name+"/"+file_name.split("/")[::-1][0]
                my_bucket.upload_file(file_name, path)

        file_names = glob2.glob(local_output_directory+'*.zip')
        xls_list=glob2.glob(local_output_directory+'*/*.xlsx')
        file_names.extend(xls_list)
        for j in xls_list:
            if((".zip" not in j) and (j.split("/")[::-1][1]not in ["St_Vincent_Dunn","Park_View"]) ):
               y =j.split("/")[::-1][0];
               folder_name = j.split("/")[::-1][1];
               z = y.replace(".xlsx","")
               if("Good_Samaritan_Family" not in folder_name):
                  excle_s3 = "Exception_Report_Input" + "/" + "Exec_"+folder_name+ "/" + str(year) + "/" + month_name + "/" +y
                  my_bucket.upload_file(j,excle_s3)
               else:
                  excle_s3 = "Exception_Report_Input" + "/" + "Exec_"+folder_name+"_Health"+ "/" + str(year) + "/" +\
                  month_name + "/" +y
                  my_bucket.upload_file(j,excle_s3)
        for file_name in file_names:
                os.remove(file_name)


    @classmethod
    def send_statement(cls,statement_file, sheet_name, file_name, folder_name):

        # saving input file to output location
        # need to work on this, saving in current directory
        file_name = file_name + ".xlsx"
        if not os.path.exists(os.path.join(local_output_directory+folder_name, file_name)):
            writer = pd.ExcelWriter(os.path.join(local_output_directory+folder_name, file_name),
                                    engine='openpyxl')
            statement_file.to_excel(writer, sheet_name=sheet_name, index=False)
            writer.save()
        else:
            writer = pd.ExcelWriter(os.path.join(local_output_directory+folder_name, file_name), engine='openpyxl'
                                    , mode='a')
            statement_file.to_excel(writer, sheet_name=sheet_name, index=False)
            writer.save()


