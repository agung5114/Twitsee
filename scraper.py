import snscrape.modules.twitter as sntwitter
import pandas as pd
import itertools

from classifier import pre_process, predict_emotion,predict_sentiment

# def getUser(df,Col):
#     col = df[Col].values

def getTweets(keyword,start,end,n):
    keyword = keyword
    df = pd.DataFrame(itertools.islice(
            sntwitter.TwitterSearchScraper(
            f'{keyword} lang:id since:{start} until:{end}',maxEmptyPages=1000)
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
    return df[['date','username','rawContent','emotion','sentiment','viewCount','replyCount', 'retweetCount', 'likeCount', 'quoteCount','followers','mentioned','hashtags']]
#     # return df.explode('mentioned')'sentiment','emotion',



#columnlist: ['url', 'date', 'rawContent', 'renderedContent', 'id', 'user',
    #    'replyCount', 'retweetCount', 'likeCount', 'quoteCount',
    #    'conversationId', 'lang', 'source', 'sourceUrl', 'sourceLabel', 'links',
    #    'media', 'retweetedTweet', 'quotedTweet', 'inReplyToTweetId',
    #    'inReplyToUser', 'mentionedUsers', 'coordinates', 'place', 'hashtags',
    #    'cashtags', 'card',  'vibe']
ausie = f'lang:en geocode:-25.165173,134.386371,2000km'
indo = f'lang:id'
# keys = f'(motor listrik) OR (mobil listrik) OR (kendaraan listrik)'
keys = f'(electric car) OR (electric vehicle)'
tahun = 2023
bulan = '05'
start = f'{tahun}-{bulan}-01'
end = f'{tahun}-{bulan}-12'

df = getTweets(keys, start,end,10000,ausie)
df.to_csv(f'EVAus-{tahun}{bulan}.csv')
