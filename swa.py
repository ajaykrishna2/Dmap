import pandas as pd

# Create a Pandas dataframe from some data.
# data = [10, 20, 30, 40, 50, 60]
# df = pd.DataFrame({'Heading': data,
#                    'Longer heading that should be wrapped' : data})
xls = pd.ExcelFile('/home/ajay/Downloads/Jessica Sims Sample Report_Riverview Collections Report FEB 2021 (1).xlsx')
df = pd.read_excel(xls, 'Details')

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter("/home/ajay/pandas_header_format.xlsx", engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object. Note that we turn off
# the default header and skip one row to allow us to insert a user defined
# header.
df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False)

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Sheet1']

# Add a header format.
header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#D7E4BC',
    'border': 1})

# Write the column headers with the defined format.
for col_num, value in enumerate(df.columns.values):
    worksheet.write(0, col_num + 1, value, header_format)

# Close the Pandas Excel writer and output the Excel file.
writer.save()