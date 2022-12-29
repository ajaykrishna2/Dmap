import numpy as np
import glob
import pandas as pd
import logging
import xlrd
import xlsxwriter
import boto3, io, os, datetime
import shutil
import configparser
import glob2
import calendar
from Utility.save_file import *

class vincent_exception:
    def book_to_facs_preprocess(self,book_to_facs):
        try:
            book_to_facs.drop(book_to_facs.loc[
                                   (book_to_facs['PRN']== 0.0)
                                  ].index, inplace =  True)
            book_to_facs.drop(book_to_facs.loc[book_to_facs['Client#'].isin(['2046','5026','38E55','403R55','5040','2041','3041','4041','5050',\
            '2037CL','1037','2012','200INS','200M25','200SPP','201IFU','201INS','201M25','201SPP','ATH65','2042','2047'])].index, inplace = True)
            book_to_facs['Acct#'] = book_to_facs['Acct#'].str.lstrip('0')
            book_to_facs['year'] = pd.DatetimeIndex(book_to_facs['Date']).year
            book_to_facs['month'] = pd.DatetimeIndex(book_to_facs['Date']).month
            book_to_facs['day'] = pd.DatetimeIndex(book_to_facs['Date']).day
            book_to_facs['flag_book_to_FACS'] = book_to_facs["Acct#"].map(str)+book_to_facs["year"].map(str)+book_to_facs['month'].map(str)+\
            book_to_facs["day"].map(str)+book_to_facs['PRN'].map(str)
            book_to_facs['flag_id'] = book_to_facs["Acct#"].map(str)+book_to_facs["year"].map(str)+book_to_facs['month'].map(str)+\
            book_to_facs["day"].map(str)+book_to_facs['Pmt Type'].map(str)
            book_to_facs_sum = book_to_facs[['Client#','PRN']].groupby(['Client#']).sum()
            book_to_facs_PRN_sum = book_to_facs_sum.reset_index()
            return [book_to_facs_PRN_sum,book_to_facs]
        except Exception as e:
            print("Error in preprocessing book to facs data")


    def billing_statement_preprocess(self,st_vincent_hospital):
        try:  
            st_vincent_hospital.drop(st_vincent_hospital.loc[
                                #  (st_vincent_hospital['Pmt Amt']==0.0)
                                 (st_vincent_hospital['Due Agency'] == 0.0)
                                 & (st_vincent_hospital['Pd to Agency'] == 0.0)
                                 & (st_vincent_hospital['PD to you'] == 0.0)
                                 & (st_vincent_hospital['Due You']==0.0)
                                 ].index, inplace=True)
            st_vincent_hospital['Pmt Amt'] = round(st_vincent_hospital['Pmt Amt'],2)
            st_vincent_hospital['year'] = pd.DatetimeIndex(st_vincent_hospital['Pmt Date']).year
            st_vincent_hospital['month'] = pd.DatetimeIndex(st_vincent_hospital['Pmt Date']).month
            st_vincent_hospital['day'] = pd.DatetimeIndex(st_vincent_hospital['Pmt Date']).day 
            st_vincent_hospital['Statement_Total'] = st_vincent_hospital['Pd to Agency']+st_vincent_hospital['PD to you']
            st_vincent_hospital['flag_bill']= st_vincent_hospital["Client's Acct#"].map(str)+st_vincent_hospital["year"].map(str)+\
            st_vincent_hospital['month'].map(str)+st_vincent_hospital["day"].map(str)+st_vincent_hospital['Statement_Total'].map(str)
            st_vincent_hospital['flag_id']= st_vincent_hospital["Client's Acct#"].map(str)+st_vincent_hospital["year"].map(str)+\
            st_vincent_hospital['month'].map(str)+st_vincent_hospital["day"].map(str)+st_vincent_hospital['Type'].map(str)
            dataframe = st_vincent_hospital[["Client #","Client's Acct#","Pmt Amt","Pd to Agency","PD to you","Due Agency","Due You"]]
            df1 = dataframe[["Client #","Pmt Amt","PD to you",'Pd to Agency',"Due Agency","Due You"]].groupby(["Client #"]).sum()
            df1['Total'] = df1['Pd to Agency']+df1['PD to you']
            return [df1.reset_index(),st_vincent_hospital]
        except Exception as e:
            print("Error in st vincent statement  preprocess")

    def Amount_Validation(self,st_vincent_hospital,book_to_facs):
        try:
            book_to_facs= self.book_to_facs_preprocess(book_to_facs)
            book_to_facs_clientid =  book_to_facs[0]
            vincent = self.billing_statement_preprocess(st_vincent_hospital)
            vincent_clientid = vincent[0]
            #Merge 2 dataframes based on client id
            client_id_level = pd.merge(book_to_facs_clientid,vincent_clientid[['Client #','Pd to Agency', 'PD to you', 'Total']],\
            left_on="Client#",right_on="Client #",how='outer')
            #Dataframe where both client ids are matched
            client_id_level12 = client_id_level[(client_id_level['Client#'].isin(client_id_level["Client #"]))\
            &(client_id_level['Client #'].isin(client_id_level["Client#"]))]
            client_id_level12['Total'] = round(client_id_level12['Total'],2)
            client_id_level12['PRN'] = round(client_id_level12['PRN'],2)
            comparison_column = np.where(client_id_level12["PRN"] == client_id_level12["Total"], True, False)
            client_id_level12['Total-Validation']=comparison_column
            client_id_level12=client_id_level12[['Client #','Pd to Agency', 'PD to you', 'Total','PRN','Total-Validation']]
            obj1 = save_statement_to_output_folder()
            obj1.send_statement(client_id_level12,"Amount Validation","Exec_St_Vincent","output/St_Vincent")
        except Exception as e:
            print("Error in creating amount validation tab")

    def Exception_report(self,st_vincent_hospital,book_to_facs):
        try:
            obj1 = save_statement_to_output_folder()
            book_to_facs= self.book_to_facs_preprocess(book_to_facs)
            book_to_facs_original = book_to_facs[1]
            vincent = self.billing_statement_preprocess(st_vincent_hospital)
            vincent_original = vincent[1]
            dff1 = pd.merge(vincent_original,book_to_facs_original[['Client#',"Acct#",'flag_id','flag_book_to_FACS','PRN','Int','Atty',\
            'Misc','CC','PJI','Total Pay','O/P Amt']],on="flag_id",how='outer')
            #Mismatch records from amount validation tab based on PRN and Total 
            exception = dff1[~dff1['flag_book_to_FACS'].isin(dff1['flag_bill'].values)]
            exception11 = exception[(exception['Client#'].isin(exception["Client #"]))&(exception['Client #'].isin(exception["Client#"]))]
            exception11 = exception11[["Client #","Client's Acct#",'Pd to Agency','PD to you',"Due Agency","Due You","Statement_Total","PRN",\
            'Int','Atty','Misc','CC','PJI','Total Pay','O/P Amt']]
            obj1.send_statement(exception11,"Balance_Mismatch","Exec_St_Vincent","output/St_Vincent")
            
            #Records present in book to facs but not in statement
            statement_exception = dff1[~dff1["Acct#"].isin(dff1["Client's Acct#"])]
            statement_exception = statement_exception[statement_exception['Client #'].isna()]
            statement_exception = statement_exception[["Client#","Acct#","PRN",'Int','Atty','Misc','CC','PJI','Total Pay','O/P Amt']]
            
            obj1.send_statement(statement_exception,"Statement_Missing_Records","Exec_St_Vincent","output/St_Vincent")
            #Records present in statement but not in book to facs
            book_to_facs_exception = dff1[~dff1["Client's Acct#"].isin(dff1["Acct#"])]
            book_to_facs_exception = book_to_facs_exception[book_to_facs_exception['Client#'].isna()]
            book_to_facs_exception = book_to_facs_exception[["Client #","Client's Acct#",'Pd to Agency','PD to you',"Due Agency","Due You","Statement_Total"]]
            obj1.send_statement(book_to_facs_exception,"BookToFacs_Missing_Records","Exec_St_Vincent","output/St_Vincent")
        
            #Duplicate records in booktofacs and statement
            statement_dup = pd.concat(g for _, g in vincent_original.groupby(["Client's Acct#", "Pmt Date", "Type", 'Pmt Amt', 'Pd to Agency', 'PD to you',\
            'Due Agency', 'Due You', "Client #"]) if len(g) > 1)
            statement_dup = statement_dup[["Client's Acct#", "Pmt Date", "Type", 'Pmt Amt', 'Pd to Agency', 'PD to you','Due Agency', 'Due You', "Client #",\
            "First Name","Last Name"]]
            obj1.send_statement(statement_dup,"Statement Miscellaneous","Exec_St_Vincent","output/St_Vincent")

            booktofacs_dup = pd.concat(g for _, g in book_to_facs_original.groupby(["FACS#", "Client#", "Acct#", 'Date', 'Total', 'Pmt Type', 'PRN', 'Int',\
            'Atty', 'Misc', 'CC', 'PJI', 'Total Pay', 'O/P Amt']) if len(g) > 1)
            booktofacs_dup=booktofacs_dup[["FACS#", "Client#", "Acct#", 'Date', 'Total', 'Pmt Type', 'PRN', 'Int', 'Atty', 'Misc', 'CC', 'PJI', 'Total Pay',\
            'O/P Amt',"Ref#","First Name","Last Name"]]
            obj1.send_statement(statement_dup,"Book To Facs Miscellaneous","Exec_St_Vincent","output/St_Vincent")
        
        except Exception as e:
            print("Error in creating exception report for st vincent hospital")
