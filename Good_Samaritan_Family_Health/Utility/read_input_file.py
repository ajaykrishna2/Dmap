import pandas as pd
import logging, boto3, io, os
import datetime
import calendar
import configparser
configuartion_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);
aws_access_key = config['Aws_Credential']['s3_access_key'];
aws_secret_key = config['Aws_Credential']['s3_secret_key'];
bucket_region  = config['Aws_Credential']['bucket_region'];
bucket_name = config['Aws_Credential']['bucket_name'];
input_bucket = config['Aws_Credential']['input_base_path'];
output_bucket = config['Aws_Credential']['output_base_path'];

class read_input_file_for_hospital:
    
    def collect_and_preprocess_input(self):
        try:
            if((datetime.datetime.now().month)!=1):
                year  = datetime.datetime.now().year
                month = (datetime.datetime.now().month) -1
                month_name = calendar.month_name[month]

            else:
                year = datetime.datetime.now().year -1
                month = (datetime.datetime.now().month) - 1
                month_name = calendar.month_name[month]
            cli = boto3.client("s3")
            data = cli.get_object(Bucket=bucket_name,Key=input_bucket+"/Good_Samaritan_Family/" + str(year) +\
            "/" + month_name + "/" + "PAYMENTS_AGY-PAYN.TXT")
            data = data['Body'].read()
            gs_client_statement= pd.read_table(io.BytesIO(data),sep="|", dtype={"Client's Acct#": str} )
            gs_client_statement["Client's Acct#"] = gs_client_statement["Client's Acct#"].str.lstrip('0')
            # Filter $7 from the good_sammaritan_statement
            gs_client_statement.drop( gs_client_statement.loc[
                                      (gs_client_statement['Due Agency'] == 7.0)
                                      & (gs_client_statement['Pd to Agency'] == 0.0)
                                      & (gs_client_statement['PD to you'] == 0.0)
                                      & (gs_client_statement['Type'].isin( ["CC", "EFT"] ))
                                      ].index, inplace=True )
            # Filter the records where all payments are zero from the good_samaritan_statement 
            gs_client_statement.drop(gs_client_statement.loc[
                                   (gs_client_statement['Pmt Amt'] == 0.0)
                                 & (gs_client_statement['Due Agency'] == 0.0)
                                 & (gs_client_statement['Due You'] == 0.0)
                                 & (gs_client_statement['Pd to Agency'] == 0.0)
                                 & (gs_client_statement['PD to you'] == 0.0)
                                 ].index, inplace = True)
            # drop records for type CRJ and DBJ from the gs_client_statement file
            gs_client_statement.drop( gs_client_statement.loc[
                                      (gs_client_statement['Type'].isin( ['CRJ', 'DBJ'] ))
                                  ].index, inplace=True )
            logging.info( "read gs_client_statement file successfully")
            return gs_client_statement
        except Exception as e:
            logging.exception("error in reading file")

   
