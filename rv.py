import xlsxwriter

# Create a new workbook and add a worksheet.
workbook = xlsxwriter.Workbook('/home/ajay/percent.xlsx')
worksheet = workbook.add_worksheet()

# Create a percentage number format.
percent_format = workbook.add_format({'num_format': '0%'})

# Write a number as a percentage.
worksheet.write('A1', .2, percent_format)

workbook.close()