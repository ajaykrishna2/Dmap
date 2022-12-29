
import pandas as pd

file = '/home/ajay/Downloads/CourseFile.csv'

df = pd.read_csv(file)


print(df.head(100))