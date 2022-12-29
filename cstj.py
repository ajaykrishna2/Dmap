import pandas as pd

df = pd.read_json('/home/ajay/Downloads/collection-summary-report-20210427.json',lines=True)
export_csv = df.to_csv (r'/home/ajay/sample1.csv', index = None, header=True)