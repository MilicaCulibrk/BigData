import re
import pandas as pd
import csv

def demoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U00010000-\U0010ffff"
                               "]+", flags=re.UNICODE)
    return (emoji_pattern.sub(r'', text))

data = pd.read_csv('../dataset/hashtagTrump.csv', encoding='utf-8', low_memory=False, skip_blank_lines=True)

data.loc[:, 'tweet'] = data.loc[:, 'tweet'].astype(str)
data.loc[:, 'tweet'] = data.loc[:, 'tweet'].apply(lambda x:demoji(x))
data.loc[:, 'user_name'] = data.loc[:, 'user_name'].astype(str)
data.loc[:, 'user_name'] = data.loc[:, 'user_name'].apply(lambda x:demoji(x))
data.loc[:, 'user_screen_name'] = data.loc[:, 'user_screen_name'].astype(str)
data.loc[:, 'user_screen_name'] = data.loc[:, 'user_screen_name'].apply(lambda x:demoji(x))
data.loc[:, 'user_description'] = data.loc[:, 'user_description'].astype(str)
data.loc[:, 'user_description'] = data.loc[:, 'user_description'].apply(lambda x:demoji(x))
data.loc[:, 'user_location'] = data.loc[:, 'user_location'].astype(str)
data.loc[:, 'user_location'] = data.loc[:, 'user_location'].apply(lambda x:demoji(x))

data.to_csv('../dataset/deletedEmojisTrump.csv', encoding="utf-8")

data2 = pd.read_csv('../dataset/hashtagBiden.csv', encoding='utf-8', skip_blank_lines=True, engine='python' )

data2.loc[:, 'tweet'] = data2.loc[:, 'tweet'].astype(str)
data2.loc[:, 'tweet'] = data2.loc[:, 'tweet'].apply(lambda x:demoji(x))
data2.loc[:, 'user_name'] = data2.loc[:, 'user_name'].astype(str)
data2.loc[:, 'user_name'] = data2.loc[:, 'user_name'].apply(lambda x:demoji(x))
data2.loc[:, 'user_screen_name'] = data2.loc[:, 'user_screen_name'].astype(str)
data2.loc[:, 'user_screen_name'] = data2.loc[:, 'user_screen_name'].apply(lambda x:demoji(x))
data2.loc[:, 'user_description'] = data2.loc[:, 'user_description'].astype(str)
data2.loc[:, 'user_description'] = data2.loc[:, 'user_description'].apply(lambda x:demoji(x))
data2.loc[:, 'user_location'] = data2.loc[:, 'user_location'].astype(str)
data2.loc[:, 'user_location'] = data2.loc[:, 'user_location'].apply(lambda x:demoji(x))

data2.to_csv('../dataset/deletedEmojisBiden.csv', encoding="utf-8")




