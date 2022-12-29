# import csv
#
# totals = {}
#
# # Aggregate sales by company, state, and quarter.
# for row in csv.reader(open('/home/ajay/hicsv.csv')):
#     key = (row[2], row[1][:2], row[0])
#     totals[key] = totals.setdefault(key, 0) + (row[4])
#
# # Write aggregated data to file.
# with open('/home/ajay/aggregated.csv', 'w') as out_file:
#   writer = csv.writer(out_file)
#   for key, value in sorted(totals.items()):
#     row = list(key) + [value]
#     writer.writerow(row)
import csv
import pandas as pd
from itertools import combinations

file1 = '/home/ajay/cid.csv'
file2 =  '/home/ajay/cid2.csv'

with open(file1) as fp1:
    root = csv.reader(fp1)
    print(root)
    rows1 = {}
    for i in root:
        rows1[i[2]] = i
        rows1[i[0]] = i
        rows1[i[1]] = i
        rows1[i[4]] = i
        rows1[i[5]] = i
        rows1[i[7]] = i
        rows1[i[8]] = i


    if "id" in rows1:
        del rows1["Collectionid"]

with open(file2) as fp1:
    root = csv.reader(fp1)
    rows2 = {}
    for i in root:
        rows2[i[0]]=i



    if "id" in rows2:
        del rows2["course_id"]
p=rows1
print(p)
for i in p:
    print(i)
# e=list(rows1)


q=rows2
# f=list(rows1)


# print(p)
df=pd.DataFrame(p)
print(df)
df2=pd.DataFrame(q)
r=pd.Series(list(set(df).intersection(set(df2))))
s=pd.Series(list(set(r).union(set(df))))
print(s)
# c=df.merge(df2)
# print(c)
result = set(rows1.keys()).intersection(set(rows2.keys()))
# d1=list(result)
# d2=list(rows1.keys())
# print(list(filter(lambda x:x in d1, d2)))

# res=set(result).union(set(u))
#
# df=pd.DataFrame(res)
# print(df)

# res4 = max(combinations(res, 2), key = lambda sub: rows1[0] + sub[1])
# print(res4)
# for i in result:
#     print(i.join(rows1))
# print(result)
# print(rows1["Published by"])
# for line in result:
#     for line in rows1.keys():
#       print('\t')
#       print(line)

# print(df)
result1=list(result)
result2 = [[x] for x in result1]
csv_columns=['course_id']

with open('/home/ajay/update1.csv', 'w') as outFile:
    writer = csv.writer(outFile)
    writer.writerow(csv_columns)
    writer.writerows(result2)


