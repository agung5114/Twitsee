import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
import itertools
#Import library tweepy yang dibutuhkan
# import tweepy
import sys
# import jsonpickle
import time
import datetime
from datetime import timedelta
#Memasukan consumer key dan secret untuk akses API Twitter
# consumer_key = '1Dj3ZsGnZLNsQAHvAm59wvznf'
# consumer_secret = 'vaR7iBmeOucGnYhiVcmA7oXBKDNLfzazTPUaCsV6ZeXpSEy0ld'

# auth = tweepy.AppAuthHandler(consumer_key,consumer_secret)
# api = tweepy.API(auth)

# start = datetime.date(2022, 12, 1)
# end = datetime.date(2022, 12, 25)
# end = datetime.date.today()
# start = end - timedelta(days = 365)

# end = end.strftime('%Y-%m-%d')
# start = start.strftime('%Y-%m-%d')



import re
def pre_process(text):
    # Remove links
    text = re.sub('http://\S+|https://\S+', '', text)
    text = re.sub('http[s]?://\S+', '', text)
    text = re.sub(r"http\S+", "", text)
    # Convert HTML references
    text = re.sub('&amp', 'and', text)
    text = re.sub('&lt', '<', text)
    text = re.sub('&gt', '>', text)
    # text = re.sub('\xao', ' ', text)
    # Remove new line characters
    text = re.sub('[\r\n]+', ' ', text)
    # Remove mentions
    text = re.sub(r'@\w+', '', text)
    # Remove hashtags
    text = re.sub(r'#\w+', '', text)
    # Remove multiple space characters
    text = re.sub('\s+',' ', text)
    # Convert to lowercase
    text = text.lower()
    return text

from tweet_classifier import getSentiment, getEmotion
def scrapeTweet(keyword, start,end,n):
    df = getTweets(str(keyword).lower(),start,end,n)
    df = getSentiment(df)
    df = getEmotion(df)
    return df


def getUser(df,Col):
    col = df[Col].values

def getTweets(keyword,start,end,n,loc):
    keyword = keyword
    df = pd.DataFrame(itertools.islice(
            sntwitter.TwitterSearchScraper(
            f'{keyword} {loc} since:{start} until:{end}')
            .get_items(),n)
            )[['id','date', 'rawContent', 'user','mentionedUsers',
            'replyCount', 'retweetCount', 'likeCount','quoteCount','viewCount','place','hashtags']]
            # 'lang','coordinates', 'place', 'hashtags','url']]
    df['username'] = df['user'].str['username']
    df['mentioned'] = [[d.get('username') for d in x] if x is not None else [] for x in df['mentionedUsers']]
    df['city'] = df['place'].str['city']
    # df['mentioned'] = df['mentionedUsers'].apply( lambda x: [d['username'] for d in x])
    return df[['id','date','username','rawContent','replyCount', 'retweetCount', 'likeCount', 'quoteCount','mentioned','city']]
#     # return df.explode('mentioned')
# import time
# def getTweets(keyword,start,end,n,loc):
#     tweetsList = []
#     # Using TwitterSearchScraper to scrape data and append tweets to list
#     for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{keyword} {loc} since:{start} until:{end}')
#             .get_items()):
#         if i>(n-1):
#             break
#         tweetsList.append([tweet.id,tweet.date, tweet.user,tweet.rawContent,
#                         tweet.replyCount,tweet.retweetCount,tweet.likeCount,tweet.quoteCount,tweet.mentionedUsers,tweet.place])
#         time.sleep(0.02)
#     df = pd.DataFrame(tweetsList, columns=['id','date','username','rawContent','replyCount', 'retweetCount', 'likeCount', 'quoteCount','mentioned','city'])
#     df['username'] = df['username'].str['username']
#     df['city'] = df['city'].str['city']
#     df['mentioned'] = [[d.get('username') for d in x] if x is not None else [] for x in df['mentioned']]
#     return df.sort_values(by='retweetCount',ascending=False)


#columnlist: ['url', 'date', 'rawContent', 'renderedContent', 'id', 'user',
    #    'replyCount', 'retweetCount', 'likeCount', 'quoteCount',
    #    'conversationId', 'lang', 'source', 'sourceUrl', 'sourceLabel', 'links',
    #    'media', 'retweetedTweet', 'quotedTweet', 'inReplyToTweetId',
    #    'inReplyToUser', 'mentionedUsers', 'coordinates', 'place', 'hashtags',
    #    'cashtags', 'card',  'vibe']
ausie = f'lang:en geocode:-25.165173,134.386371,2000km'
indo = f'lang:id'
# Singapore= lang:en near:"Singapore" within:50km

tahun = 2023
bulan = '03'
start = f'{tahun}-{bulan}-01'
end = f'{tahun}-{bulan}-31'

# df = getTweets('motor listrik',start,end,10000,indo)
# print(df.tail(10))
# # print(df.head())
# # print(df.columns)
# df.to_csv(f'EVIndo2-{tahun}{bulan}.csv')
pemda = 'jateng'
df = getTweets(f'(pemda jateng) OR (pemda jawa tengah)','2019-01-01','2023-04-30',30000,indo)
print(df.tail(10))
df.to_csv(f'{pemda}1923.csv')