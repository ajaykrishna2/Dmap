import os

myfile1 = "dele.txt"
if os.path.isfile(myfile1):
    os.remove(myfile1)
else:
    print("Error: %s file not found" % myfile1)
