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
            f'{keyword} {loc} since:{start} until:{end}',maxEmptyPages=1000)
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
ausie = f'lang:en geocode:-25.165173,134.386371,2000km'
indo = f'lang:id'
# Singapore= lang:en near:"Singapore" within:50km




# df = getTweets('motor listrik',start,end,10000,indo)
# print(df.tail(10))
# # print(df.head())
# # print(df.columns)
# df.to_csv(f'EVIndo2-{tahun}{bulan}.csv')
# pemda = 'jateng'
# df = getTweets(f'(pemda jateng) OR (pemda jawa tengah)','2019-01-01','2023-04-30',30000,indo)
# print(df.tail(10))
# df.to_csv(f'{pemda}1923.csv')

# keys = ["pemda lampung","pemda sumsel","pemda jabar"]
# tahun = 2023
# bulan = '03'
# start = f'{tahun}-{bulan}-01'
# end = f'{tahun}-{bulan}-31'

# def runScraper(keys,start,end,n,loc):
#     for key in keys:
#         df = getTweets(key,start,end,n,loc)
#         updateDb(df)
#         time.sleep(0.5)
#     print("scraping tweets is done")

# runScraper(keys,'2023-01-01','2023-04-30',10000,indo)
ausie = f'lang:en geocode:-25.165173,134.386371,2000km'
indo = f'lang:id'
key_indo = f'(motor listrik) OR (mobil listrik) OR (kendaraan listrik)'
key_aus = f'(electric car) OR (electric vehicle)'
tahun = 2022
bulan = '11'
start = f'{tahun}-{bulan}-01'
end = f'{tahun}-{bulan}-30'

df = getTweets(key_indo, start,end,10000,indo)
df.to_csv(f'EVIndo-{tahun}{bulan}.csv')