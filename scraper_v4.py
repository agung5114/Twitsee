import snscrape.modules.twitter as sntwitter
import pandas as pd
import itertools
import time
import datetime
from datetime import timedelta

# start = datetime.date(2022, 12, 1)
# # end = datetime.date(2022, 12, 25)
# end = datetime.date.today()
# start = end - timedelta(days = 31)

# end = end.strftime('%Y-%m-%d')
# start = start.strftime('%Y-%m-%d')

from classifier import pre_process,predict_emotion,predict_sentiment
# def scrapeTweet(keyword, start,end,n):
#     df = getTweets(str(keyword).lower(),start,end,n)
#     df = getSentiment(df)
#     df = getEmotion(df)
#     return df
from classifier_dev import pre_process, predict_emotion,predict_sentiment

def getUser(df,Col):
    col = df[Col].values

def getTweets(keyword,start,end,n,loc):
    keyword = keyword
    df = pd.DataFrame(itertools.islice(
            sntwitter.TwitterSearchScraper(
            f'{keyword} {loc} since:{start} until:{end}',maxEmptyPages=100)
            .get_items(),n)
            )[['id','date', 'rawContent', 'user','mentionedUsers',
            'replyCount', 'retweetCount', 'likeCount','quoteCount','viewCount','place','hashtags']]
            # 'lang','coordinates', 'place', 'hashtags','url']]
    df['username'] = df['user'].str['username']
    df['followers'] = df['user'].str['followersCount']
    df['mentioned'] = [[d.get('username') for d in x] if x is not None else [] for x in df['mentionedUsers']]
    df['text'] = df['rawContent'].apply(pre_process)
    df['emotion'] = df['text'].apply(predict_emotion)
    df['sentiment'] = df['text'].apply(predict_sentiment)
    keywords=[]
    for i in df['id']:
        keywords.append(keyword)
    df['keyword'] = keywords
    # df['city'] = df['place'].str['city']
    # df['mentioned'] = df['mentionedUsers'].apply( lambda x: [d['username'] for d in x])
    return df[['id','keyword','date','username','rawContent','sentiment','emotion','viewCount','replyCount', 'retweetCount', 'likeCount', 'quoteCount','followers','mentioned','hashtags']]
#     # return df.explode('mentioned')


#columnlist: ['url', 'date', 'rawContent', 'renderedContent', 'id', 'user',
    #    'replyCount', 'retweetCount', 'likeCount', 'quoteCount',
    #    'conversationId', 'lang', 'source', 'sourceUrl', 'sourceLabel', 'links',
    #    'media', 'retweetedTweet', 'quotedTweet', 'inReplyToTweetId',
    #    'inReplyToUser', 'mentionedUsers', 'coordinates', 'place', 'hashtags',
    #    'cashtags', 'card',  'vibe']

sing= f'lang:en near:"Jakarta" within:50km'

ausie = f'lang:en geocode:-25.165173,134.386371,2000km'
# ausie = f'lang:en geocode:-25.165173,134.386371,2000km'
usa = f'country_code:us'
indo = f'lang:id'
key_indo = f'(motor listrik) OR (mobil listrik) OR (kendaraan listrik)'
key_aus = f'(electric car) OR (electric vehicle)'
import datetime, calendar
# from calendar import monthrange
# monthrange(2014, 2)

keyword = key_aus
loc = usa
year = 2023
month = 4
numb = 10
num_days = calendar.monthrange(year, month)[1]
# num_days = 2
dates = list(range(1, num_days+1))
current_time = datetime.datetime.now()
today = current_time.day

df = None
for i in dates:
    if datetime.datetime(year, month, i) > current_time:
        df1 = None
    # elif month>11:
    #     df1 = getTweets(keyword,f'{year}-{month}-{i}',f'{year+1}-1-1',numb,loc)
    # elif i == dates[-1]:
    #     df1 = getTweets(keyword,f'{year}-{month}-{i}',f'{year}-{month+1}-1',numb,loc)
    elif i < dates[-1]:
        df1 = getTweets(keyword,f'{year}-{month}-{i}',f'{year}-{month}-{i+1}',numb,loc)
    else:
        df1 = None
    df = pd.concat([df,df1])

# df = getTweets(keyword,f'{year}-{month}-1',f'{year}-{month+1}-1',numb,loc)
# # df = pd.concat([df,df1])
# df.to_csv(f'EVUS-{year}{month}.csv')
print(df.tail())

