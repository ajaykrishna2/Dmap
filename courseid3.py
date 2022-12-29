import csv
import pandas as pd

with open('/home/ajay/cid.csv', 'r') as t1, open('/home/ajay/cid1.csv', 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()


df = pd.read_csv("/home/ajay/cid.csv", usecols=['State', 'Total enrolments By State','Total completion By State'])

with open('/home/ajay/update.csv', 'w') as outFile:
    for line in filetwo:
        if line not in fileone:
            d = df.groupby(['State']).agg({ 'Total enrolments By State': 'sum', 'Total completion By State': 'sum'}
              outFile.write(line)