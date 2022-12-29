import pandas as pd
from openpyxl import workbook

# Create a test df
# df=pd.read_excel("/home/ajay/test.xlsx")
# df=df.ffill()
def hide_rows_columns(self):
     workbook = self.Workbook(self.dataDir + '/home/ajay/test.xls')
     worksheet = workbook.getWorksheets().get(0)
     cells = worksheet.getCells()
     # cells.hideRow(2)
     cells.hideColumn(1)
     workbook.save(self.dataDir + "/home/ajay/HideRowsAndColumns.xls")
     print("Hide Rows And Columns Successfully.")

hide_rows_columns