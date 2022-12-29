import logging

import openpyxl
import pandas as pd

def book_to_facs1(df,writer):
    try:

        rslt_df = df[(df['Client Name'] == 'Deaconess Gibson Hospital')|(df['Client Name'] == 'Deaconess Health System')|(df['Client Name'] == 'Deaconess Henderson Hospital')|(df['Client Name'] == 'Deaconess Specialty Physicians')|(df['Client Name'] == 'Deaconess Union County Hospital')|(df['Client Name'] == 'THE HEART HOSPITAL')]
        rslt_df.to_excel(writer, index=False, sheet_name='book_to_facs')

    except Exception as e:
        logging.exception("error")



if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/Deaconess_book_facs.xlsx', engine='xlsxwriter')
    book_to_facs1 = pd.read_excel('/home/ajay/Downloads/book_to_facs.xlsx', sheet_name='NON_STV')
    book_to_facs1(book_to_facs1, writer)
    writer.save()



