import pandas as pd
import tweetnlp
model_sentiment_indo = tweetnlp.load_model('sentiment', model_name="w11wo/indonesian-roberta-base-sentiment-classifier")
model_emosi_indo = tweetnlp.load_model('emotion',model_name= "StevenLimcorn/indonesian-roberta-base-emotion-classifier")

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

def predict_sentiment(text):
    prediction = model_sentiment_indo.sentiment(text)
    return prediction['label']

def predict_emotion(text):
    prediction = model_emosi_indo.emotion(text)
    return prediction['label']

# def runNlp(df):
#     df['text'] = df['rawContent'].apply(pre_process)
#     # df['sentiment'] = df['Text'].apply(predict_sentiment)
#     # df['emotion'] = df['Text'].apply(predict_emotion)
#     return df

# # text = 'saya marah sekali'
# # prediction = model_emosi_indo.emotion(text)
# # print(prediction['label'])
# df = pd.read_csv('twitter_pemda.csv')
# df = runNlp(df)
# # print(df.tail())
# emotions = []
# for text in df['rawContent']:
#     emotions.append(predict_emotion(text))

# emotions[:10]
# df.to_csv('twitdata.csv', index=False)
