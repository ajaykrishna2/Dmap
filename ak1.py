from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from datetime import datetime

# Create a StreamingContext with batch interval of 3 second
sc = SparkContext("spark://MASTER:7077", "myAppName")
ssc = StreamingContext(sc, 3)

topic = "my-topic"
kafkaStream = KafkaUtils.createStream(ssc, "MASTER_IP:2181", "topic", {topic: 4})

raw = kafkaStream.flatMap(lambda kafkaS: [kafkaS])
time_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
clean = raw.map(lambda xs: xs[1].split(","))

# Match cassandra table fields with dictionary keys
# this reads input of format: x[partition, timestamp]
my_row = clean.map(lambda x: {
      "testid": "test",
      "time1": x[1],
      "time2": time_now,
      "delta": (datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S.%f') -
       datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S.%f')).microseconds,
      })

# save to cassandra
my_row.saveToCassandra("KEYSPACE", "TABLE_NAME")

ssc.start()             # Start the computation
ssc.awaitTermination()