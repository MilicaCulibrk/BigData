r"""
 Run the example
    `$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 $SPARK_HOME/primeri/kafka_wordcount.py zoo:2181 subreddit-politics`
    `$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 $SPARK_HOME/primeri/kafka_wordcount.py zoo:2181 subreddit-politics subredit-funny`
"""
from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import os
import math
import json

HDFS_NAMENODE = os.environ["CORE_CONF_fs_defaultFS"]


def quiet_logs(sc):
  logger = sc._jvm.org.apache.log4j
  logger.LogManager.getRootLogger().setLevel(logger.Level.ERROR)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: kafka_wordcount.py <zk> <topic>", file=sys.stderr)
        sys.exit(-1)

    sc = SparkContext(appName="SparkStreamingKafkaTweets")
    quiet_logs(sc)

    ssc = StreamingContext(sc, 180)
    ssc.checkpoint("stateful_checkpoint_direcory")

    zooKeeper, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zooKeeper, "spark-streaming-consumer", {topic: 1})

    
    parsed = kvs.map(lambda v: json.loads(v[1]))
    #count_this_batch = kvs.count().map(lambda x:('Tweets this batch: %s' % x))
    users = parsed.map(lambda tweet: tweet[7])
    cities = parsed.map(lambda tweet: tweet[15])

    user_count_values_this_batch = users.countByValue()\
                                .transform(lambda rdd:rdd\
                                .sortBy(lambda x:-x[1]))\
                                .filter(lambda x: x[1] > 3)\
                                .map(lambda x:"User '%s' is suspicious. He/She tweeted about Trump %s times in the last 3 minutes!" % (x[0],x[1]))

    cities_count_values_this_batch = cities.countByValue()\
                                .transform(lambda rdd:rdd\
                                .sortBy(lambda x:-x[1]))\
                                .filter(lambda x: x[1] > 170)\
                                .filter(lambda x: x[0] != '')\
                                .map(lambda x:"Something is happening in %s. There has been '%s' tweets from there in the last 3 minutes!" % (x[0],x[1]))

                              

   
    user_count_values_this_batch.pprint()
    cities_count_values_this_batch.pprint()


    ssc.start()
    ssc.awaitTermination()