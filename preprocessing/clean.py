import re
import pandas as pd
import csv

def deleteNewLines(text):
    text = text.replace('\n', ' ').replace('\r', '')
    return (text)

def setToUS(text):
    text = text.replace('United States of America', 'United States')
    text = text.replace('Los Angeles', 'United States')
    return (text)

def setCity(text):
    text = text.replace("nan", 'Los Angeles')
    return (text)

data = pd.read_csv('../dataset/deletedEmojisTrump.csv', encoding='utf-8', low_memory=False, skip_blank_lines=True,  index_col=0)

data.loc[:, 'tweet'] = data.loc[:, 'tweet'].astype(str)
data.loc[:, 'tweet'] = data.loc[:, 'tweet'].apply(lambda x:deleteNewLines(x))
data.loc[:, 'user_description'] = data.loc[:, 'user_description'].astype(str)
data.loc[:, 'user_description'] = data.loc[:, 'user_description'].apply(lambda x:deleteNewLines(x))

data.loc[:, 'country'] = data.loc[:, 'country'].astype(str)
data.loc[:, 'country'] = data.loc[:, 'country'].apply(lambda x:setToUS(x))

data.loc[:, 'city'] = data.loc[:, 'city'].astype(str)
data.loc[:, 'city'] = data.loc[:, 'city'].apply(lambda x:setCity(x))

data.to_csv('../dataset/tweetsTrump.csv', encoding="utf-8", index=False, index_label=False)

data2 = pd.read_csv('../dataset/deletedEmojisBiden.csv', encoding='utf-8', skip_blank_lines=True, low_memory=False, index_col=0)

data2.loc[:, 'tweet'] = data2.loc[:, 'tweet'].astype(str)
data2.loc[:, 'tweet'] = data2.loc[:, 'tweet'].apply(lambda x:deleteNewLines(x))
data2.loc[:, 'user_description'] = data2.loc[:, 'user_description'].astype(str)
data2.loc[:, 'user_description'] = data2.loc[:, 'user_description'].apply(lambda x:deleteNewLines(x))

data2.loc[:, 'country'] = data2.loc[:, 'country'].astype(str)
data2.loc[:, 'country'] = data2.loc[:, 'country'].apply(lambda x:setToUS(x))

data2.loc[:, 'city'] = data2.loc[:, 'city'].astype(str)
data2.loc[:, 'city'] = data2.loc[:, 'city'].apply(lambda x:setCity(x))

data2.to_csv('../dataset/tweetsBiden.csv', encoding="utf-8", index=False, index_label=False)





