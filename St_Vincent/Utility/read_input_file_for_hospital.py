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
    def collect_and_preprocess_st_vicent(cls):
        try:
            cli = boto3.client("s3")

            data = cli.get_object(Bucket=bucket_name, Key=input_bucket+"/St_Vincent/"+str(cls.year)+"/"+\
            cls.month_name+"/"+"PAYMENTRPT.TXT")
            data = data['Body'].read()
            vincent_invision_statement = pd.read_table(io.BytesIO(data),sep=",",index_col=False,encoding="ISO-8859-1")
            # Filter DBJ,CRJ Types from the womens_client_statement file
            vincent_invision_statement.drop(vincent_invision_statement.loc[
                                                (vincent_invision_statement['Type'].isin(["DBJ", "CRJ"]))
                                            ].index, inplace=True)

            # Filter $7 from the vincent_invision_statement file
            vincent_invision_statement.drop(vincent_invision_statement.loc[
                                                (vincent_invision_statement['Due Agency'] == 7.0)
                                                & (vincent_invision_statement['Pd to Agency'] == 0.0)
                                                & (vincent_invision_statement['PD to you'] == 0.0)
                                                & (vincent_invision_statement['Type'].isin(["CC", "EFT"]))
                                                ].index, inplace=True)
            # Filter the records where all payments are zero from the womens_client_statement file
            vincent_invision_statement.drop(vincent_invision_statement.loc[
                                                (vincent_invision_statement['Pmt Amt'] == 0.0)
                                                & (vincent_invision_statement['Due Agency'] == 0.0)
                                                & (vincent_invision_statement['Due You'] == 0.0)
                                                & (vincent_invision_statement['Pd to Agency'] == 0.0)
                                                & (vincent_invision_statement['PD to you'] == 0.0)
                                                ].index, inplace=True)
            vincent_invision_statement['Pmt Amt'] = vincent_invision_statement['Pd to Agency'] + \
                                                    vincent_invision_statement['PD to you']
            vincent_invision_statement['Due Agency'] = vincent_invision_statement['Pmt Amt'] * 15 / 100
            vincent_invision_statement['Due You'] = vincent_invision_statement['Pmt Amt'] - vincent_invision_statement[
                'Due Agency']
            #vincent_invision_statement.loc[vincent_invision_statement['Pmt Type'] == "COR", "O/P Amt"] = -vincent_invision_statement['O/P Amt']
            vincent_invision_statement = vincent_invision_statement.astype(
                {'Pmt Amt': 'float64', "Due Agency": 'float64', "Due You": 'float64', "Pd to Agency": 'float64',
                 "PD to you": 'float64'})
            logging.info("read vincent_invision_statement file successfully")
            return vincent_invision_statement

        except Exception as e:
            logging.exception("error in reading file")

    @classmethod
    def collect_and_preprocess_st_vicent_non_facs(cls):
        try:
            cli = boto3.client("s3")

            data = cli.get_object(Bucket=bucket_name, Key= input_bucket+"/St_Vincent/"+str(cls.year)+"/"+\
            cls.month_name+"/"+"PAYMENTRPT.TXT")
            data = data['Body'].read()
            vincent_statement = pd.read_table(io.BytesIO(data),sep=",",index_col=False,encoding="ISO-8859-1")
            vincent_statement.drop(vincent_statement.loc[
                                       (vincent_statement['Type'].isin(["DBJ", "CRJ"]))
                                   ].index, inplace=True)

            # Filter $7 from the vincent_statement file
            vincent_statement.drop(vincent_statement.loc[
                                       (vincent_statement['Due Agency'] == 7.0)
                                       & (vincent_statement['Pd to Agency'] == 0.0)
                                       & (vincent_statement['PD to you'] == 0.0)
                                       & (vincent_statement['Type'].isin(["CC", "EFT"]))
                                       ].index, inplace=True)
            # Filter the records where all payments are zero from the womens_client_statement file
            vincent_statement.drop(vincent_statement.loc[
                                       (vincent_statement['Pmt Amt'] == 0.0)
                                       & (vincent_statement['Due Agency'] == 0.0)
                                       & (vincent_statement['Due You'] == 0.0)
                                       & (vincent_statement['Pd to Agency'] == 0.0)
                                       & (vincent_statement['PD to you'] == 0.0)
                                       ].index, inplace=True)
            #vincent_statement.loc[vincent_statement['Pmt Type'] == "COR", "O/P Amt"] = -vincent_statement['O/P Amt']
            vincent_statement = vincent_statement.astype(
                {'Pmt Amt': 'float64', "Due Agency": 'float64', "Due You": 'float64', "Pd to Agency": 'float64',
                 "PD to you": 'float64'})
            logging.info("read vincent_statement file successfully")
            return vincent_statement

        except Exception as e:
            logging.exception("error in reading file")


