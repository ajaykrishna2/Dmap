from kafka import KafkaProducer
from kafka import KafkaConsumer
import json

producer = KafkaProducer(bootstrap_servers= 'localhost:9092' )
producer.send('some',b'some')
consumer = KafkaConsumer('some',  bootstrap_servers=['localhost:9092'],auto_offset_reset='earliest',group_id='none')
for msg in consumer:
    print(msg.value)








