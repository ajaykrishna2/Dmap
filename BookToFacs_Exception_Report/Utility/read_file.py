import pandas as pd
import configparser
import logging, boto3, io,datetime
import calendar
import os
class read_input_for_exception:
    configuartion_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/config/config.ini"
    config = configparser.ConfigParser()
    config.read(configuartion_path)
    aws_access_key = config['Aws_Credential']['s3_access_key']
    aws_secret_key = config['Aws_Credential']['s3_secret_key']
    bucket_region  = config['Aws_Credential']['bucket_region']
    bucket_name    = config['Aws_Credential']['bucket_name']
    input_bucket   = config['Aws_Credential']['input_base_path']
    output_bucket  = config['Aws_Credential']['output_base_path']
    if((datetime.datetime.now().month)!=1):
            year  = datetime.datetime.now().year
            month = (datetime.datetime.now().month) -1
            month_name = calendar.month_name[month]

    else:
            year = datetime.datetime.now().year -1
            month = (datetime.datetime.now().month) -1 
            month_name = calendar.month_name[month]

    def book_to_facs_read(self):
      try:
          client = boto3.client('s3',aws_access_key_id=read_input_for_exception.aws_access_key, aws_secret_access_key=read_input_for_exception.aws_secret_key,
          region_name=read_input_for_exception.bucket_region)
          obj = client.get_object(Bucket=read_input_for_exception.bucket_name,Key="Exception_Report_Input/Book_to_Facs/"+\
          str(read_input_for_exception.year)+"/"+read_input_for_exception.month_name+"/"+"book_to_facs.xlsx")
          data = obj['Body'].read()
          payrpt = pd.read_excel(io.BytesIO(data),sheet_name="payrpt")
          NON_STV = pd.read_excel(io.BytesIO(data),sheet_name="NON_STV")
          COMMUNITY = pd.read_excel(io.BytesIO(data),sheet_name="COMMUNITY")
          MED1 = pd.read_excel(io.BytesIO(data),sheet_name="MED1")
          STV = pd.read_excel(io.BytesIO(data),sheet_name="STV")
          RCR = pd.read_excel(io.BytesIO(data),sheet_name="RCR")
          return [payrpt,NON_STV,STV,COMMUNITY,MED1,RCR]

      except Exception as e:
          print("Error in reading input for book_to_facs exception",e)
