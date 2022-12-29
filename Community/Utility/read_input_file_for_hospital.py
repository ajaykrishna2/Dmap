import pandas as pd
import logging, boto3, io,datetime
import calendar
import os
import configparser


configuartion_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/config/config.ini"
print(configuartion_path)
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
    def collect_and_preprocess_input(cls):
        # Read Excel file as argument
        # community_client_statement is PAYMENTS_AGY-PAYN data
        # logic for collection of data need to work, right now considering file as argument and fetching data
        try:
            cli = boto3.client("s3")

            data = cli.get_object(Bucket=bucket_name, Key=input_bucket+"/Community/"+str(cls.year)+"/"+\
            read_input_file_for_hospital.month_name+"/"+"PAYMENTS_AGY-PAYN.TXT")
            data = data['Body'].read()
            community_client_statement = pd.read_table(io.BytesIO(data),sep="|",encoding="ISO-8859-1")
            # Filter $7 from the community_client_statement file
            community_client_statement.drop(community_client_statement.loc[
                                                (community_client_statement['Due Agency'] == 7.0)
                                                & (community_client_statement['Over Paid'] == 0.0)
                                                & (community_client_statement['Pd to Agency'] == 0.0)
                                                & (community_client_statement['PD to you'] == 0.0)
                                                & (community_client_statement['Type'].isin(["CC", "EFT"]))
                                                ].index, inplace=True)

            # drop records for type CRJ and DBJ from the community_client_statement file
            community_client_statement.drop(community_client_statement.loc[
                                                (community_client_statement['Type'].isin(['CRJ', 'DBJ']))
                                            ].index, inplace=True)
            community_client_statement['Pmt Amt'] = community_client_statement['Over Paid']+community_client_statement['Pd to Agency']+\
            community_client_statement['PD to you']
            #community_client_statement.loc[community_client_statement['Pmt Type'] == "COR", "O/P Amt"] = -community_client_statement['O/P Amt']
            # Converting date format in the community_client_statement file
            #community_client_statement['Pmt Date'] = community_client_statement['Pmt Date'].apply(lambda x:
            #                                                                                      x.strftime('%m/%d/%Y'))

            logging.info("read community_client_statement file successfully")
            return community_client_statement

        except Exception as e:
            logging.exception("error in reading file")

    @classmethod
    def collect_preprocess_cal_fees_input(cls):
        # Read Excel file as argument
        # community_client_statement is PAYMENTS_AGY-PAYN data
        # logic for collection of data need to work, right now considering file as argument and fetching data

        try:
            cli = boto3.client("s3")

            data = cli.get_object(Bucket=bucket_name, Key=input_bucket+"/Community/"+str(cls.year)+"/"+\
            read_input_file_for_hospital.month_name+"/"+"PAYMENTS_AGY-PAYN.TXT")
            data = data['Body'].read()
            community_client_statement1 = pd.read_table(io.BytesIO(data),sep="|", index_col=False,encoding="ISO-8859-1")
            # Filter $7 from the community_client_statement file
            community_client_statement1.drop(community_client_statement1.loc[
                                                 (community_client_statement1['Due Agency'] == 7.0)
                                                 & (community_client_statement1['Over Paid'] == 0.0)
                                                 & (community_client_statement1['Pd to Agency'] == 0.0)
                                                 & (community_client_statement1['PD to you'] == 0.0)
                                                 & (community_client_statement1['Type'].isin(["CC", "EFT"]))
                                                 ].index, inplace=True)

            # drop records for type CRJ and DBJ from the community_client_statement file
            community_client_statement1.drop(community_client_statement1.loc[
                                                 (community_client_statement1['Type'].isin(['CRJ', 'DBJ']))
                                             ].index, inplace=True)
            # adding column Fee
            community_client_statement1["Fee"] = ((community_client_statement1["Due Agency"] /
                                                   community_client_statement1["Pmt Amt"]).mul(100).fillna(0).round(0).
                                                  astype(str) + "%")
            community_client_statement1['Pmt Amt'] = community_client_statement1['Over Paid']+community_client_statement1['Pd to Agency']+\
            community_client_statement1['PD to you']
            #community_client_statement1.loc[community_client_statement1['Pmt Type'] == "COR", "O/P Amt"] = -community_client_statement1['O/P Amt']

            # Converting date format in the community_client_statement file
            # community_client_statement1['Pmt Date'] = community_client_statement1['Pmt Date'].apply(lambda x:
            #                                                                                         x.strftime('%m/%d/%Y'))

            logging.info("read community_client_statement file successfully")
            return community_client_statement1
        except Exception as e:
            logging.exception("error in reading file")

