# BigData
Student project for batch and real-time processing of tweets with hashtags #DonaldTrump and #JoeBiden posted in the period from  15.10.2020. to 08.11.2020.

# Downloading and Preprocessing data
Download data [here](https://www.kaggle.com/manchunhui/us-election-2020-tweets). In folder preprocessing there are python scripts for deleting emojis, empty rows 
and merging the two files form the link. Processed files should than be coppied to folder ./datasets, and megred file to both ./datasets and ./stream/consumer. 

# Environment setup
 - $ cd docker
 - $ docker-compose up --build
 
# Adding Data to HDFS
  $ sh uploadFiles.sh
  
# Batch Processing
  - $ cd batch
  - $ sh run.sh
  
# Plot Batch Results
  - $ cd batch
  - run plot.py
  
# Stream Processing
  - $ cd ./stream/consumer
  - $ sh run.sh
