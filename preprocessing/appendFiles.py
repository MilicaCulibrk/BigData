import re
import pandas as pd
import csv
from csv import writer
from datetime import datetime


def setToUS(text):
    text = text.replace('United States of America', 'United States')
    text = text.replace('Los Angeles', 'United States')
    return (text)

def setCity(text):
    text = text.replace("nan", 'Los Angeles')
    return (text)

data = pd.read_csv('../dataset/allTweets.csv', encoding='utf-8', low_memory=False,  skip_blank_lines=True)

data.loc[:, 'country'] = data.loc[:, 'country'].astype(str)
data.loc[:, 'country'] = data.loc[:, 'country'].apply(lambda x:setToUS(x))

data.loc[:, 'city'] = data.loc[:, 'city'].astype(str)
data.loc[:, 'city'] = data.loc[:, 'city'].apply(lambda x:setCity(x))

data.to_csv('../dataset/allTweets.csv', encoding="utf-8", index=False, index_label=False)
#append_list_as_row('../datasets/allTweets.csv', data)





