import pandas as pd
import logging, boto3, io,datetime
import calendar
import os
import configparser


configuartion_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);

bucket_name            = config['Aws_Credential']['bucket_name'];
input_bucket           = config['Aws_Credential']['input_base_path'];
output_bucket          = config['Aws_Credential']['output_base_path'];
local_output_directory = config['Output_Location']['monthly_report']

class read_input_file_for_hospital:
    if((datetime.datetime.now().month)!=1):
            year  = datetime.datetime.now().year
            month = (datetime.datetime.now().month) -1
            month_name = calendar.month_name[month]

    else:
            year = datetime.datetime.now().year -1
            month = (datetime.datetime.now().month) -1
            month_name = calendar.month_name[month]
    
    @classmethod
    def collect_and_preprocess_deaconess_data(cls):
        # Read Excel file as argument
        # community_client_statement is PAYMENTS_AGY-PAYN data
        # logic for collection of data need to work, right now considering file as argument and fetching data

        try:
            cli = boto3.client("s3")

            data = cli.get_object(Bucket=bucket_name, Key=input_bucket+"/Deaconess/"+str(cls.year)+"/"+\
            cls.month_name+"/"+"CBS_ACL.TXT")
            data = data['Body'].read()
            deaconess_data = pd.read_table(io.BytesIO(data),sep="\t",index_col=False,encoding="ISO-8859-1")
            # Filter $7 from the MD1_OS tab
            deaconess_data.drop(deaconess_data.loc[
                                    (deaconess_data['Due Agency'] == 7.0)
                                    & (deaconess_data['Pd to Agency'] == 0.0)
                                    & (deaconess_data['Pd to You'] == 0.0)
                                    & (deaconess_data['Pmt Type'].isin(["CC", "EFT"]))
                                    ].index, inplace=True)

            # drop records for type CRJ and DBJ from the dsp_client_statement file
            deaconess_data.drop(deaconess_data.loc[
                                    (deaconess_data['Pmt Type'].isin(['CRJ', 'DBJ']))
                                ].index, inplace=True)
            #deaconess_data.loc[deaconess_data['Pmt Type'] == "COR", "O/P Amt"] = -deaconess_data['O/P Amt']
            logging.info("read dsp_client_statement file successfully")
            return deaconess_data

        except Exception as e:
            logging.exception("error in reading file")

    
