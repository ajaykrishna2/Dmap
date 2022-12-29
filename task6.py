import pyspark_cassandra
import pyspark_cassandra.streaming

from pyspark_cassandra import CassandraSparkContext

from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid1

import json
# set up our contexts
sc = CassandraSparkContext(conf=conf)
sql = SQLContext(sc)
stream = StreamingContext(sc, 1) # 1 second window

kafka_stream = KafkaUtils.createStream(stream, \
                                       "localhost:2181", \
                                       "raw-event-streaming-consumer",
                                        {"pageviews":1})
parsed = kafka_stream.map(lambda (k, v): json.loads(v))
summed = parsed.map(lambda event: (event['site_id'], 1)).\
                reduceByKey(lambda x,y: x + y).\
                map(lambda x: {"site_id": x[0], "ts": str(uuid1()), "pageviews": x[1]})
summed.saveToCassandra("killranalytics", "real_time_data")
stream.start()
stream.awaitTermination()