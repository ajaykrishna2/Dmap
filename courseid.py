import csv

with open('/home/ajay/cid.csv', 'r') as t1, open('/home/ajay/cid2.csv', 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()


with open('/home/ajay/update.csv', 'w') as outFile:
    for line in filetwo:
        if line  in fileone:
            print(line)
            outFile.write(line)
