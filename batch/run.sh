  
#!/bin/bash

rm -R -- ../results/*

winpty docker exec -it namenode bash -c "hdfs dfsadmin -safemode leave"
winpty docker exec -it namenode bash -c "hdfs dfs -rm -r -f /queryResults*"

winpty docker exec -it namenode bash -c "hdfs dfs -mkdir /queryResults"

docker cp . spark-master:/home
winpty docker exec -it spark-master bash -c "chmod +x /home/batch.sh && /home/batch.sh"

docker cp saveResults.sh namenode:/home/results
winpty docker exec -it namenode bash -c "chmod +x /home/results/saveResults.sh &&  /home/results/saveResults.sh"







