import pandas as pd
import logging, boto3, io,datetime
import calendar
import os
import configparser

configuartion_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);

bucket_name    = config['Aws_Credential']['bucket_name'];
input_bucket   = config['Aws_Credential']['input_base_path'];
output_bucket  = config['Aws_Credential']['output_base_path'];


class read_input_file_for_hospital:
    if((datetime.datetime.now().month)!=1):
            year  = datetime.datetime.now().year
            month = (datetime.datetime.now().month) -1
            month_name = calendar.month_name[month]

    else:
            year = datetime.datetime.now().year -1
            month = (datetime.datetime.now().month) - 1
            month_name = calendar.month_name[month]
    def collect_and_preprocess_input():
        # Read Excel file as argument
        # community_client_statement is PAYMENTS_AGY-PAYN data
        # logic for collection of data need to work, right now considering file as argument and fetching data
        try:
            cli = boto3.client("s3")
            data = cli.get_object(Bucket=bucket_name, Key=input_bucket+"/Community/"+str(read_input_file_for_hospital.year)+"/"+\
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

    def collect_preprocess_cal_fees_input():
        # Read Excel file as argument
        # community_client_statement is PAYMENTS_AGY-PAYN data
        # logic for collection of data need to work, right now considering file as argument and fetching data

        try:
            cli = boto3.client("s3")

            data = cli.get_object(Bucket= bucket_name, Key=input_bucket+"/Community/"+str(read_input_file_for_hospital.year)+"/"+\
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

    def collect_and_preprocess_deaconess_data():
        # Read Excel file as argument
        # community_client_statement is PAYMENTS_AGY-PAYN data
        # logic for collection of data need to work, right now considering file as argument and fetching data

        try:
            cli = boto3.client("s3")

            data = cli.get_object(Bucket=bucket_name, Key= input_bucket+"/Deaconess/"+str(read_input_file_for_hospital.year)+"/"+\
            read_input_file_for_hospital.month_name+"/"+"CBS_ACL.TXT")
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

    def collect_and_preprocess_women_data():
        try:
            cli = boto3.client("s3")

            data = cli.get_object(Bucket=bucket_name, Key=input_bucket+"/Womens_Hospital/"+str(read_input_file_for_hospital.year)+"/"+\
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


    def collect_and_preprocess_st_vicent():
        try:
            cli = boto3.client("s3")

            data = cli.get_object(Bucket=bucket_name, Key=input_bucket+"/St_Vincent/"+str(read_input_file_for_hospital.year)+"/"+\
            read_input_file_for_hospital.month_name+"/"+"PAYMENTRPT.TXT")
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


    def collect_and_preprocess_st_vicent_non_facs():
        try:
            cli = boto3.client("s3")

            data = cli.get_object(Bucket=bucket_name, Key=input_bucket+"/St_Vincent/"+str(read_input_file_for_hospital.year)+"/"+read_input_file_for_hospital.month_name+"/"+"PAYMENTRPT.TXT")
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

    def collect_and_preprocess_st_vicent_dunn():
        try:
            cli = boto3.client("s3")

            data = cli.get_object(Bucket=bucket_name, Key=input_bucket+"/St_Vincent_Dunn/"+str(read_input_file_for_hospital.year)+"/"+\
            read_input_file_for_hospital.month_name+"/"+"PAYMENTRPT.TXT")
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
    def collect_and_preprocess_parkview_data():
        try:
            cli = boto3.client("s3")
            data = cli.get_object(Bucket=bucket_name, Key=input_bucket+"/Park_View/"+str(read_input_file_for_hospital.year)+"/"+\
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

    def collect_and_preprocess_good_samaritan_family_input(self):
        try:
            cli = boto3.client("s3")
            data = cli.get_object(Bucket=bucket_name,Key=input_bucket+"/Good_Samaritan_Family/" +\
            str(read_input_file_for_hospital.year) +"/" + read_input_file_for_hospital.month_name + "/" + "PAYMENTS_AGY-PAYN.TXT")
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
