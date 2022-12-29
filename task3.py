import pandas as pd

# importing module for regex
import re

# reading csv file from url
data = pd.read_csv("/home/ajay/15tmarch.csv")

# String to be searched in start of string
search = "Y"

# count of occurrence of a and creating new column
data["count"] = data["Has certificate"].str.count(search, re.I)

# display
print(data)