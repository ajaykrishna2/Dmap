from pyspark import SparkContext
from pyspark.sql import SQLContext
sc = SparkContext("local", "emp")
sqlContext = SQLContext(sc)
def load_and_get_table_df(keys_space_name, table_name):
    table_df = sqlContext.read\
        .format("org.apache.spark.sql.cassandra")\
        .options(table=table_name, keyspace=keys_space_name)\
        .load()
    return table_df
emp = load_and_get_table_df("sample", "emp")
emp.show()

