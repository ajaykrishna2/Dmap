import json
import csv
with open('/home/ajay/sample.json') as f:
  data = json.load(f)
def flatten_json(y):
    out = {}

    def flatten(x, name=''):

        # If the Nested key-value
        # pair is of dict type
        if type(x) is dict:

            for a in x:
                flatten(x[a], name + a + '_')

                # If the Nested key-value
        # pair is of list type
        elif type(x) is list:

            i = 0

            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


# Driver code
data=flatten_json(data)
csv_file=open('/home/ajay/csv_format1.csv','w')
write=csv.writer(csv_file)
write.writerow(data.keys())
write.writerow(data.values())
csv_file.close()
