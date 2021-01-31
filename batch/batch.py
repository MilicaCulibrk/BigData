
#!/usr/bin/python

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from datetime import datetime
import sys
import re

def quiet_logs(sc):
  logger = sc._jvm.org.apache.log4j
  logger.LogManager.getLogger("org"). setLevel(logger.Level.ERROR)
  logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)

conf = SparkConf().setAppName("USA 2020 Election Tweets").setMaster("local")
sc = SparkContext(conf=conf)
spark = SparkSession(sc)

quiet_logs(spark)

from pyspark.sql.types import *

schemaString = "created_at,tweet_id,tweet,likes,retweet_count,source,user_id,user_name,user_screen_name,user_description,user_join_date,user_followers_count,user_location,lat,long,city,country,continent,state,state_code,collected_at"
fields = [StructField(field_name, StringType(), False) for field_name in schemaString.split(",")]
schema = StructType(fields)

df = spark.read.csv("hdfs://namenode:9000/tweetsDataset/allTweets.csv", header=True, schema=schema)
dfT = spark.read.csv("hdfs://namenode:9000/tweetsDataset/tweetsTrump.csv", header=True, schema=schema)
dfB = spark.read.csv("hdfs://namenode:9000/tweetsDataset/tweetsBiden.csv", header=True, schema=schema)

df = df.withColumn("likes", df["likes"].cast(IntegerType()))
df = df.withColumn("retweet_count", df["retweet_count"].cast(IntegerType()))
df = df.withColumn("user_followers_count", df["user_followers_count"].cast(IntegerType()))
df = df.withColumn("date", df["created_at"].substr(1, 10))
df = df.withColumn("join_date", df["user_join_date"].substr(1, 10))
df = df.withColumn("join_date", df["join_date"].cast(DateType()))

dfT = dfT.withColumn("date", dfT["created_at"].substr(1, 10))
dfB = dfB.withColumn("date", dfB["created_at"].substr(1, 10))


df.printSchema()

df.createOrReplaceTempView("tweet")
dfT.createOrReplaceTempView("tweetT")
dfB.createOrReplaceTempView("tweetB")


# izlistavamo prvih 10 drzava 
query3 = "SELECT country, count(tweet_id) as number_of_tweets \
         FROM tweet \
         WHERE country IS NOT NULL AND country != 'nan' \
         GROUP BY country \
         ORDER BY count(tweet_id) DESC \
         LIMIT 10"
sqlDF3 = spark.sql(query3)
sqlDF3.show(10, False)
sqlDF3.repartition(1).write.csv("hdfs://namenode:9000/queryResults/mostTweetsInACountry", sep=',', header=True)

# izlistavamo prvih 10 saveznih drzava po broju tvitova za Trampa
query2 = "SELECT state, count(tweet_id) as number_of_Trump_tweets \
         FROM tweetT \
         WHERE state IS NOT NULL and country == 'United States'\
         GROUP BY state \
         ORDER BY count(tweet_id) DESC"
sqlDF2 = spark.sql(query2)
sqlDF2.repartition(1).write.csv("hdfs://namenode:9000/queryResults/mostTweetsInAStateT", sep=',')
sqlDF2.createOrReplaceTempView("sqlDF2")

# izlistavamo prvih 10 saveznih drzava po broju tvitova za Bidena
query3 = "SELECT state, count(tweet_id) as number_of_Biden_tweets \
         FROM tweetB \
         WHERE state IS NOT NULL and country == 'United States'\
         GROUP BY state \
         ORDER BY count(tweet_id) DESC"
sqlDF3 = spark.sql(query3)
sqlDF3.repartition(1).write.csv("hdfs://namenode:9000/queryResults/mostTweetsInAStateB", sep=',')
sqlDF3.createOrReplaceTempView("sqlDF3")

# poredimo prvih 10 saveznih drzava po broju tvitova za Trampa i Bajdena
query4 = "SELECT sqlDF2.state, number_of_Trump_tweets, number_of_Biden_tweets\
         FROM sqlDF2 \
         INNER JOIN sqlDF3 \
         ON sqlDF2.state = sqlDF3.state\
         ORDER BY number_of_Trump_tweets DESC"
sqlDF4 = spark.sql(query4)
sqlDF4.show(10, False)
sqlDF4.repartition(1).write.csv("hdfs://namenode:9000/queryResults/mostTweetsInAState", sep=',', header=True)

# izlistavamo prvih 10 dana po broju tvitova za Trampa
query5 = "SELECT date, count(tweet_id) as number_of_Trump_tweets \
         FROM tweetT \
         GROUP BY date \
         ORDER BY count(tweet_id) DESC"
sqlDF5 = spark.sql(query5)
sqlDF5.repartition(1).write.csv("hdfs://namenode:9000/queryResults/mostTweetsInADayForTrump", sep=',')
sqlDF5.createOrReplaceTempView("sqlDF5")

# izlistavamo prvih 10 dana po broju tvitova za Bajdena
query6 = "SELECT date, count(tweet_id) as number_of_Biden_tweets \
         FROM tweetB \
         GROUP BY date \
         ORDER BY count(tweet_id) DESC"
sqlDF6 = spark.sql(query6)
sqlDF6.repartition(1).write.csv("hdfs://namenode:9000/queryResults/mostTweetsInADayForBiden", sep=',')
sqlDF6.createOrReplaceTempView("sqlDF6")

# poredimo prvih 10 dana po broju tvitova za Trampa i Bajdena
query7 = "SELECT sqlDF5.date, number_of_Trump_tweets, number_of_Biden_tweets\
         FROM sqlDF5 \
         INNER JOIN sqlDF6 \
         ON sqlDF5.date = sqlDF6.date\
         ORDER BY number_of_Trump_tweets DESC\
         LIMIT 10"
sqlDF7 = spark.sql(query7)
sqlDF7.show(10, False)
sqlDF7.repartition(1).write.csv("hdfs://namenode:9000/queryResults/mostTweetsInADay", sep=',', header=True)

# izlistavamo sumnjive korisnike (ako su se skoro prikljucili a imaju veliki broj tvitova)
query2 = "SELECT join_date, user_screen_name as username, count(tweet_id) as number_of_tweets \
         FROM tweet \
         WHERE join_date IS NOT NULL AND join_date >= '2020-09-01'\
         GROUP BY join_date, user_screen_name \
         ORDER BY count(tweet_id) DESC \
         LIMIT 10"
sqlDF2 = spark.sql(query2)
sqlDF2.show(10, False)
sqlDF2.repartition(1).write.csv("hdfs://namenode:9000/queryResults/suspiciousUsers", sep=',')

# izlistavamo prvih 10 korisnika po broju lajkova i broj tvitova u kojima ih je sakupio
query2 = "SELECT  user_screen_name as username, sum(likes) as number_of_likes, count(tweet_id) as number_of_tweets\
         FROM tweet \
         WHERE user_screen_name IS NOT NULL \
         GROUP BY user_screen_name \
         ORDER BY sum(likes) DESC \
         LIMIT 10"
sqlDF2 = spark.sql(query2)
sqlDF2.show(10, False)
sqlDF2.repartition(1).write.csv("hdfs://namenode:9000/queryResults/mostLikesByUser", sep=',', header=True)

# izlistavamo tvitove korisnika sa vise od 1.000.000 pratilaca
query2 = "SELECT tweet as tweet, likes as number_of_likes, user_screen_name as username \
         FROM tweet \
         WHERE user_followers_count > 1000000 \
         ORDER BY likes DESC \
         LIMIT 10"
sqlDF2 = spark.sql(query2)
sqlDF2.show(10, False)
sqlDF2.repartition(1).write.csv("hdfs://namenode:9000/queryResults/tweetsByCelebrities", sep=',')







