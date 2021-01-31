  
#!/bin/bash

docker cp dataset/ namenode:/home

winpty docker exec -it namenode bash -c "hdfs dfs -rm -r -f /tweetsDataset*"

winpty docker exec -it namenode bash -c "hdfs dfs -mkdir /tweetsDataset"

winpty docker exec -it namenode bash -c "hdfs dfs -put /home/dataset/allTweets.csv /tweetsDataset/"

winpty docker exec -it namenode bash -c "hdfs dfs -put /home/dataset/tweetsTrump.csv /tweetsDataset/"

winpty docker exec -it namenode bash -c "hdfs dfs -put home/dataset/tweetsBiden.csv /tweetsDataset/"




