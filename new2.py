# import json
# import csv
# import pandas as pd
#
# df = pd.read_json('/home/ajay/today.json',lines=True,typ='series')
#
# def flatten_json(y):
#     out = {}
#
#     def flatten(x, name=''):
#
#         # If the Nested key-value
#         # pair is of dict type
#         if type(x) is dict:
#
#             for a in x:
#                 flatten(x[a], name + a + '_')
#
#                 # If the Nested key-value
#         # pair is of list type
#         elif type(x) is list:
#
#             i = 0
#
#             for a in x:
#                 flatten(a, name + str(i) + '_')
#                 i += 1
#         else:
#             out[name[:-1]] = x
#
#     flatten(y)
#     return out
#
# data1=flatten_json(df)
# print(type(data1))
# df2 = pd.DataFrame.from_dict(data1)
# df2=pd.read_json(data1)
#
# export_csv = df2.to_csv (r'/home/ajay/sample1.csv', index = None, header=True)
import pandas as pd
from pandas.io.json import json_normalize
df = pd.read_json('/home/ajay/today.json',lines=True)