import pandas as pd
import sys
import os
import operator as op
import numpy as np
import openpyxl
def Exception_report(data, book_to_facs, writer):
    try:

if __name__ == "__main__":
    writer = pd.ExcelWriter('/home/ajay/deconess_hospital_exception_report.xlsx', engine='xlsxwriter')

    data = pd.read_excel('/home/ajay/Deaconess2.xlsx', sheet_name='data')
    book_to_facs = pd.read_excel('/home/ajay/Downloads/book_to_facs.xlsx', sheet_name='NON_STV')
    Exception_report(data, book_to_facs, writer)


    writer.save()