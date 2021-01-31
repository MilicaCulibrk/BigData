#!/usr/bin/python3

import os
import time
from kafka import KafkaProducer
import kafka.errors
import json
import csv
from datetime import datetime

KAFKA_BROKER = os.environ["KAFKA_BROKER"]
TOPIC = "tweets"


while True:
    try:
        producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER.split(","), value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        print("Connected to Kafka!")
        break
    except kafka.errors.NoBrokersAvailable as e:
        print(e)
        time.sleep(3)

f = csv.reader(open("tweetsTrump.csv"), delimiter=",")
headers = next(f, None)
print("Loaded data")

dataList = list(f)
print("Initiating tweets")

for i, line in enumerate(dataList):
    producer.send(TOPIC, key=bytes(line[0], 'utf-8'), value=line)

    current_date_time = datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S")

    if len(dataList) > i+1:
      next_event = dataList[i+1]
      next_date_time = datetime.strptime(next_event[0], "%Y-%m-%d %H:%M:%S")
    
      difference = next_date_time - current_date_time
      print('Sleeping ' + str(difference.seconds/5) + ' seconds...')
      time.sleep(difference.seconds/5)
