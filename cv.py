import pandas as pd
excel = '/home/ajay/Downloads/PARKVIEW_EPIC_RECON_061521_29533.TXT'

df = pd.read_csv(excel, sep='\t')

column_indexes = list(df.columns)

df.reset_index(inplace=True)


# df.drop(columns=df.columns[-1], inplace=True)


column_indexes = dict(zip(list(df.columns), column_indexes))
df1=df.rename(columns={'Cancel Description':''})


df1.rename(columns=column_indexes, inplace=True)
df1['regex'] = df1['Client ID'].str.contains('IFU', regex=True)


df2=df1[df1['regex']==True]
df3=df1

df2.to_excel('/home/ajay/output.xlsx', 'Sheet1', index=False)
# df3.to_excel('/home/ajay/output.xlsx', 'Sheet2', index=False)