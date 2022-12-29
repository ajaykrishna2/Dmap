# count number of files in folder
import os, os.path

# simple version for working with CWD
print(len([name for name in os.listdir('.') if os.path.isfile(name)]))

# path joining version for other paths
DIR = '/home/ajay/PycharmProjects/pythonProject/venv/lib64/python3.8/site-packages/_distutils_hack'
print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))