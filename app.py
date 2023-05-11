import tweetnlp
model_sentiment_indo = tweetnlp.load_model('sentiment', model_name="w11wo/indonesian-roberta-base-sentiment-classifier")

# sentence = "Wali Kota Bandung diindikasikan curang saat pemilu"
# print(model_sentiment_indo.sentiment(sentence, return_probability=True))

import streamlit as st
import sys
from streamlit.web import cli as stcli
from streamlit import runtime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
st.set_page_config(page_title="Twitsee", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

def main():
    st.subheader("Sentiment-Emotion Prediction")

    with st.form(key='textarea'):
        search_text = st.text_area("Type Here")
        submit_text = st.form_submit_button(label='Submit')

    if submit_text:
        raw_text = search_text
        prediction = model_sentiment_indo.sentiment(raw_text, return_probability=True)
        st.success("Sentiment")
        st.write(raw_text)
        st.success("Prediction")
        st.write(prediction)
        df = pd.read_csv("data2023.csv")
        sentiment_color = {"negative": "#e96678", "neutral": "#ced4d0", "positive": "#70bda0"}
        col1,col2 = st.columns((1,1))
        with col1:
            piefig = px.pie(df, names='Sentiment', values='Retweeted', color='Sentiment', hole=.4, color_discrete_map=sentiment_color)
            st.plotly_chart(piefig)
        with col2:
            barfig = px.bar(df, x='Sentiment', y='Likes', color='Sentiment', color_discrete_map=sentiment_color)
            st.plotly_chart(barfig)

        st.dataframe(df)


if __name__=='__main__':
    # if st._is_running_with_streamlit:
    if runtime.exists():
        main()   
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
