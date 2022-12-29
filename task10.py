from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.types import *
import os
spark = SparkSession.builder \
       .appName('SparkCassandraApp') \
       .config('spark.cassandra.connection.host', '127.0.0.1') \
       .config('spark.cassandra.connection.port', '9042') \
       .config('spark.cassandra.output.consistency.level','ONE') \
       .master('local[2]') \
       .getOrCreate()
df = spark.read.format("org.apache.spark.sql.cassandra").options(table="emp",keyspace="sample").load()
df.show()
# data = SparkSession.read.format("org.apache.spark.sql.cassandra").options(table="emp", keyspace="sample").load()
# data.show()
