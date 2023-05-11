
import streamlit as st
st.set_page_config(page_title="MAWS", page_icon=None, layout="wide", initial_sidebar_state="auto",menu_items=None)
# import sys
# from streamlit.web import cli as stcli
# from streamlit import runtime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime
from datetime import timedelta
from scraper import getTweets

end = datetime.date.today()
start = end - timedelta(days = 31)

end = end.strftime('%Y-%m-%d')
start = start.strftime('%Y-%m-%d')
sentiment_color = {"negative": "#e96678", "neutral": "#ced4d0", "positive": "#70bda0"}
emotions_emoji = {"anger":"😡","disgust":"🤮", "fear":"😱", "happy":"🤗", "joy":"🤩", "love":"😍", "neutral":"😐", "sad":"😔", "sadness":"😥", "shame":"😳", "surprise":"😮"}
emotions_color = {"anger":"#e96678","disgust":"#e96678", "fear":"#e96678", "happy":"#70bda0", "joy":"#70bda0","love":"#70bda0", "neutral":"#ced4d0", "sad":"#e96678", "sadness":"#e96678", "shame":"#e96678", "surprise":"#70bda0"}
            

# def main():
menu = ['Analisis Pemerintah Daerah','Monitoring Nasional', 'Analisis Sentimen']
choice = st.sidebar.selectbox("Pilih Menu",menu)

if choice == 'Analisis Sentimen':
    submitted = st.empty()
    with st.sidebar.form(key='text'):
        search_text = st.text_input("Pencarian Tweet terbaru")
        submitted = st.form_submit_button('Submit')
    st.subheader("Sentimen dan Emosi Publik Terkini")
    # c1,c2 = st.columns((1,4))
    # with c1:
    # with c2:
    #     st.empty()
    if submitted:
        raw_text = search_text
        df = getTweets(raw_text,start,end,100)
        col1,col2 = st.columns((1,1))
        with col1:
            piefig = px.pie(df, names='sentiment', values='retweetCount', color='sentiment', hole=.4, color_discrete_map=sentiment_color)
            st.plotly_chart(piefig)
        with col2:
            df['emoji'] = [emotions_emoji[x] for x in df['emotion']]
            barfig = px.bar(df, x='emoji', y='likeCount', color='emotion', color_discrete_map=emotions_color)
            st.plotly_chart(barfig)
        st.dataframe(df)
    else:
        st.write("masukkan kata pencarian")
elif choice == 'Analisis Pemerintah Daerah':
    st.subheader("Analisis Data historis")
    df = pd.read_csv('twitdata.csv')
    c1,c2 = st.columns((1,1))
    with c1:
        piefig = px.pie(df, names='sentiment', values='retweetCount', color='sentiment', hole=.4, color_discrete_map=sentiment_color)
        st.plotly_chart(piefig)
    with c2:
        df['emoji'] = [emotions_emoji[x] for x in df['emotion']]
        barfig = px.bar(df, x='emoji', y='likeCount', color='emotion', color_discrete_map=emotions_color)
        st.plotly_chart(barfig)
    st.dataframe(df)
elif choice == 'Monitoring Nasional':
    st.subheader("Sentiment-Emotion Prediction")

# if __name__=='__main__':
#     # if st._is_running_with_streamlit:
#     if runtime.exists():
#         main()   
#     else:
#         sys.argv = ["streamlit", "run", sys.argv[0]]
#         sys.exit(stcli.main())
