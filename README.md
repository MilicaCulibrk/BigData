# BigData
Student project for batch and real-time processing of tweets with hashtags #DonaldTrump and #JoeBiden posted in the period from  15.10.2020. to 08.11.2020.

# Downloading and Preprocessing data
Download data [from here](https://www.kaggle.com/manchunhui/us-election-2020-tweets) and create ./dataset folder for placing the downloaded files. In folder preprocessing there are python scripts for deleting emojis, empty rows and merging the two files form the link and they should be run in the following order:
 - deleteEmojis.py
 - clean.py
 - appendFiles.py
 
Merged file should also be coppied to both ./stream/consumer folder. 

# Environment setup
 - $ cd docker
 - $ docker-compose up --build
 
# Adding Data to HDFS
  $ sh uploadFiles.sh
  
# Batch Processing
Goals of batch processing are to show:
  - top 10 countries with most tweets in general
  - top 10 states in the US with the most tweet for Trump in comparison with tweets for Biden
  - top 10 dates by number of posted tweets for Trump in comparison to Biden
  - top 10 users by number of likes recieved in ther tweets 
  - top 10 users by number of tweets who joined twitter after september 2020 (suspicious users)
  - top 10 tweets by number of likes posted by users with over one million twitter followers
  
  Run batch:
  - $ cd batch
  - $ sh run.sh
  
# Plot Batch Results
  - $ cd batch
  - run plot.py
  
# Stream Processing
Goals of stream processing are:
  - to show users with more than 3 tweets posted for Trump or Biden during the 3 minute time period
  - to show cities where more than 150 tweets have been posted during the 3 minute time period
  
  Run stream:
  - $ cd ./stream/consumer
  - $ sh run.sh
