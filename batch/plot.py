
#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyspark.sql.types import *
from os import listdir
import matplotlib.dates as mdates
import re

if __name__ == "__main__":

    def multiply(numberOfTweets):
        numberOfTweets = numberOfTweets * 1000
        return (numberOfTweets)

    # grafikon koji prikazuje broj tvitova po drzavama u svetu
    CSV_Files0 = [file for file in listdir('../results/mostTweetsInACountry/') if file.endswith('.csv')]
    CSV_File0 = CSV_Files0[0]
    data0 = pd.read_csv('../results/mostTweetsInACountry/' + CSV_File0)

    df0 = pd.DataFrame(data0)
    df0.set_index("country", inplace=True)
    df0.head()
    df0.plot(kind='pie', title='Countires with the most tweets', figsize=(10, 5), subplots=True)
    plt.show()

    #grafikon koji prikazuje broj tvitova za Trampa i Bajdena po saveznim drzavama
    CSV_Files1 = [file for file in listdir('../results/mostTweetsInAState/') if file.endswith('.csv')]
    CSV_File1 = CSV_Files1[0]
    data1 = pd.read_csv('../results/mostTweetsInAState/' + CSV_File1)

    df1 = pd.DataFrame(data1)
    df1.set_index("state", inplace=True)
    df1.head()
    df1.plot(kind='bar',title='Number of Trump and Biden tweets in each US state', figsize=(10,5), width = 0.75)
    plt.xlabel('State')
    plt.ylabel('Number of Tweets')
    plt.show()

    #grafikon koji pokazuje top 10 najlajkovanijih korisnika i broj tvitova na kojima su sakupili te lajkove
    CSV_Files2 = [file for file in listdir('../results/mostLikesByUser/') if file.endswith('.csv')]
    CSV_File2 = CSV_Files2[0]
    data2 = pd.read_csv('../results/mostLikesByUser/' + CSV_File2)

    df2 = pd.DataFrame(data2)
    df2.set_index("username", inplace=True)
    df2.loc[:, 'number_of_tweets'] = df2.loc[:, 'number_of_tweets'].apply(lambda x:multiply(x))
    df2.head()
    df2.plot(kind='bar', title='Number of likes and tweets for top 10 liked users', figsize=(10, 5), width=0.75)
    plt.xlabel('User')
    plt.ylabel('Number of Likes and Tweets')
    plt.show()

    # grafikon koji pokazuje top 10 najlajkovanijih korisnika i broj tvitova na kojima su sakupili te lajkove
    CSV_Files3 = [file for file in listdir('../results/mostTweetsInADay/') if file.endswith('.csv')]
    CSV_File3 = CSV_Files3[0]
    data3 = pd.read_csv('../results/mostTweetsInADay/' + CSV_File3)
    df3 = pd.DataFrame(data3)

    df3.set_index("date", inplace=True)
    df3.head()
    df3.plot(kind='bar', title='Number of Trump and Biden tweets per days', figsize=(10, 5), width=0.75)
    plt.xlabel('Date')
    plt.ylabel('Number of Tweets')
    plt.show()









