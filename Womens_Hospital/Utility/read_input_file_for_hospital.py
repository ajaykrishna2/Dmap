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
            month = (datetime.datetime.now().month) - 1
            month_name = calendar.month_name[month]
    @classmethod
    def collect_and_preprocess_women_data(cls):
        try:
            cli = boto3.client("s3")
            data = cli.get_object(Bucket=bucket_name, Key=input_bucket+"/Womens_Hospital/"+str(cls.year)+"/"+\
            read_input_file_for_hospital.month_name+"/"+"PAYMENTS_AGY-PAYN.TXT")
            data = data['Body'].read()
            #data = "/home/ubuntu/PAYMENTS_AGY-PAYN.TXT"
            womens_client_statement = pd.read_table(io.BytesIO(data),sep="|",index_col=False, encoding="ISO-8859-1")
            # Filter DBJ,CRJ Types from the womens_client_statement file
            womens_client_statement.drop(womens_client_statement.loc[
                                             (womens_client_statement['Type'].isin(["DBJ", "CRJ"]))
                                         ].index, inplace=True)
            # Filter $7 from the womens_client_statement file
            womens_client_statement.drop(womens_client_statement.loc[
                                             (womens_client_statement['Due Agency'] == 7.0)
                                             & (womens_client_statement['Pd to Agency'] == 0.0)
                                             & (womens_client_statement['PD to you'] == 0.0)
                                             & (womens_client_statement['Type'].isin(["CC", "EFT"]))
                                             ].index, inplace=True)
            # Filter the records where all payments are zero from the womens_client_statement file
            womens_client_statement.drop(womens_client_statement.loc[
                                             (womens_client_statement['Pmt Amt'] == 0.0)
                                             & (womens_client_statement['Due Agency'] == 0.0)
                                             & (womens_client_statement['Due You'] == 0.0)
                                             & (womens_client_statement['Pd to Agency'] == 0.0)
                                             & (womens_client_statement['PD to you'] == 0.0)
                                             ].index, inplace=True)
            #womens_client_statement.loc[womens_client_statement['Pmt Type'] == "COR", "O/P Amt"] = -womens_client_statement['O/P Amt']
            logging.info("read womens_client_statement file successfully")
            return womens_client_statement

        except Exception as e:
            logging.exception("error in reading file")


