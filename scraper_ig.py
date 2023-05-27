import snscrape.modules.instagram as sninstagram
import pandas as pd
import itertools

from classifier import pre_process, predict_emotion,predict_sentiment

# def getUser(df,Col):
#     col = df[Col].values

def getIgpost(keyword,n):
    keyword = keyword
    df = pd.DataFrame(itertools.islice(
            sninstagram.InstagramHashtagScraper(
            f'{keyword}')
            .get_items(),n)
            )
            # 'lang','coordinates', 'place', 'hashtags','url']]
    return df


df = getIgpost('mobillistrik',10)
print(df.head())
