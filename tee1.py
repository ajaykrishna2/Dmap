import pandas as pd
df=pd.read_excel("/home/ajay/Riverview Collections Report Feb 2021.xlsx")
# print(test)
df = df.sort_values(by=['NAME','CLIENT','Year'])
df.set_index(['NAME', 'CLIENT','Year'], inplace=True)
df=df.ffill()
df.to_excel('/home/ajay/re.xlsx')