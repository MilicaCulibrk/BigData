  
#!/bin/bash

docker cp . spark-master:/spark/stream
winpty docker exec -it spark-master bash -c "spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 spark/stream/main.py zoo1:2181 tweets"





