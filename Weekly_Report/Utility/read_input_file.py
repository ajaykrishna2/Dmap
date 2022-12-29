import configparser
import os
import pandas as pd
import logging, boto3, io
import datetime
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
goodsam_date_period = config['Aws_Credential']['goodsam_date_period']
local_output_directory = config['Output_Location']['good_samaritan']

class read_input_file_for_hospital:
    
    def collect_and_preprocess_input(self):
        # good_sammaritan_statement is PAYMENTS_AGY-PAYN data
        try:            
            session = boto3.Session(aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key,region_name=bucket_region);
            s3 = session.resource('s3')
            my_bucket = s3.Bucket(bucket_name)
            list_of_files = []
            for file in my_bucket.objects.filter(Prefix='BA_input_folder/Good_Samaritan/'):
                list_of_files.append(file)
            filtered_list = [obj.key for obj in sorted(list_of_files, key=lambda x: x.last_modified,
                reverse=True)][0:1]
            for i in filtered_list:
                    j = goodsam_date_period
                    client = boto3.client('s3', aws_access_key_id=aws_access_key,
                                          aws_secret_access_key=aws_secret_key,
                                          region_name=bucket_region)
                    # Reading Goodsam Weekly dates file
                    date_range = client.get_object(Bucket=bucket_name, Key=j)
                    ranges = date_range['Body'].read()
                    goodsam_dates = pd.read_excel(io.BytesIO(ranges))
                    week_num = i.split("/")[::-1][1]
                    month = i.split("/")[::-1][2]
                    for k in goodsam_dates.index:
                        if str(goodsam_dates['Month'][k]) == month and str(goodsam_dates['Week Number'][k]) == week_num:
                           weekly_dates = goodsam_dates['Statement Time Period'][k]
                    #Reading input file PAYMENTS_AGY-PAYN
                    obj = client.get_object(Bucket=bucket_name, Key=i)
                    data = obj['Body'].read()
                    gs_client_statement= pd.read_table(io.BytesIO(data),sep="|", dtype={"Client #": str} )
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
                                 & (gs_client_statement['Over Paid'] == 0.0)
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
                    return [gs_client_statement,weekly_dates,i]
        except Exception as e:
            logging.exception("error in reading file")

