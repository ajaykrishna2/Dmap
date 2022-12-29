import pandas as pd
import sys
import logging
import xlrd
import os
import openpyxl
from openpyxl.workbook import Workbook
import xlsxwriter
import numpy as np


def wellfund_community(facs, epic, writer):
    # Rows in facs not in epic
    try:
        print(facs)
        # df = facs.merge(epic, how='outer', indicator=True).loc[lambda x: x['_merge'] == 'left_only']
        # df_out = df[['DATE LISTED', 'FIRST NAME', 'LAST NAME', 'DISPOSITION',
        #              'HAR', 'MRN NUM', 'BABY GRAM APPR', 'HIP APPROVED',
        #              'INSURANCE FOUND', 'HPE APPROVED', 'HPE DENIED', 'HHW APPROVED',
        #              'MK APPROVED', 'DATE APP COMP', 'MSP LVL', 'MK EFF DATE',
        #              'RECERTIFICATION', 'MSP APPROVED', 'COBRA', 'ACCOUNT #',
        #              'DATE DISP CHANGE', 'CLIENT', 'PREVIOUS DISPO', 'ACCT CLASS']]
        # df_output = df_out.rename({'HAR': 'ACCT# FROM CLT'}, axis=1)
        #
        # df_output.to_excel(writer, index=False, sheet_name='in_facs_not_in_epic')
    except Exception as e:
        logging.exception("error")

    try:
        # Rows in epic not in facs
        df1 = facs.merge(facs, how='outer', indicator=True).loc[lambda x: x['_merge'] == 'right_only']
        df1_out = df1[['Patient MRN', 'HAR', 'HAR Type',
                       'Patient', 'Base Class', 'BI Add Date',
                       'Billing Indicator Customer', 'BI Description', 'Admit Date',
                       'Discharge Date', 'Sum of Fee', 'Department', 'Location']]

        df1_out.to_excel(writer, index=False, sheet_name='in_epic_not_in_facs')
    except Exception as e:
        logging.exception("error")


if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/COMMAPP2.xlsx', engine='openpyxl')
    xls1 = pd.ExcelFile('/home/ajay/Downloads/Community_Apps_Nov.xlsx', engine='openpyxl')
    df_facs1 = pd.read_excel(xls1, 'COMAPP')
    df_facs=df_facs1[['DATE LISTED', 'FIRST NAME', 'LAST NAME', 'DISPOSITION',
                     'HAR', 'MRN NUM', 'BABY GRAM APPR', 'HIP APPROVED',
                     'INSURANCE FOUND', 'HPE APPROVED', 'HPE DENIED', 'HHW APPROVED',
                     'MK APPROVED', 'DATE APP COMP', 'MSP LVL', 'MK EFF DATE',
                     'RECERTIFICATION', 'MSP APPROVED', 'COBRA', 'ACCOUNT #',
                     'DATE DISP CHANGE', 'CLIENT', 'PREVIOUS DISPO', 'ACCT CLASS']]
    df_facs.to_excel(writer, index=False, sheet_name='COMAPP')
    df_facs_output = df_facs.rename({'ACCT# FROM CLT': 'HAR'}, axis=1)
    xls2 = pd.ExcelFile('/home/ajay/Downloads/WellFundMonthlyActivityDetails.HB.PB.202011.xlsx', engine='openpyxl')

    df_epic1 = pd.read_excel(xls2, 'Details')

    df_epic=df_epic1[['Patient MRN', 'HAR', 'HAR Type',
                      'Patient', 'Base Class', 'BI Add Date',
                      'Billing Indicator Customer', 'BI Description', 'Admit Date',
                      'Discharge Date', 'Sum of Fee', 'Department', 'Location']]


    df_epic.to_excel(writer, index=False, sheet_name="Details")

    wellfund_community(df_facs_output, df_epic, writer)
    writer.save()