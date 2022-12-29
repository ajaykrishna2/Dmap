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
    def collect_and_preprocess_parkview_data(cls):
        try:
            cli = boto3.client("s3")
            data = cli.get_object(Bucket=bucket_name, Key=input_bucket+"/Park_View/"+str(cls.year)+"/"+\
            read_input_file_for_hospital.month_name+"/"+"PAYMENTS_AGY-PAYN.TXT")
            data = data['Body'].read()
            parkview_client_statement= pd.read_table(io.BytesIO(data),sep="|")
            # Filter $7
            parkview_client_statement.drop( parkview_client_statement.loc[
                                      (parkview_client_statement['Due Agency'] == 7.0)
                                      & (parkview_client_statement['Pd to Agency'] == 0.0)
                                      & (parkview_client_statement['PD to you'] == 0.0)
                                      & (parkview_client_statement['Type'].isin( ["CC", "EFT"] ))
                                      ].index, inplace=True )

            # drop records for type CRJ and DBJ from the parkview_client_statement file
            parkview_client_statement.drop( parkview_client_statement.loc[
                                      (parkview_client_statement['Type'].isin(['CRJ', 'DBJ']))
                                  ].index, inplace=True )
            parkview_client_statement = parkview_client_statement[["Client's Acct#",'Pmt Date','Type','Pmt Amt','Over Paid','Pd to Agency',
            'PD to you','Due Agency','Due You','Client #','First Name','Last Name','Acct Location']]
            logging.info( "read parkview_client_statement file successfully" )
            return parkview_client_statement

        except Exception as e:
            logging.exception( "error in reading file" )

