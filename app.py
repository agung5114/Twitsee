
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
belanja_color = {"53. Belanja Modal": "#e96678", "51. Belanja Pegawai": "#ced4d0", "52. Belanja Barang Jasa": "#70bda0",'54. Belanja Lainnya':"#e96678"}
sentiment_color = {"negative": "#e96678", "neutral": "#ced4d0", "positive": "#70bda0"}
emotions_emoji = {"anger":"😡","disgust":"🤮", "fear":"😱", "happy":"🤗", "joy":"🤩", "love":"😍", "neutral":"😐", "sad":"😔", "sadness":"😥", "shame":"😳", "surprise":"😮"}
emotions_color = {"😡anger":"#e96678","🤮disgust":"#e96678", "😱fear":"#e96678", "🤗happy":"#70bda0", "🤩joy":"#70bda0","😍love":"#70bda0", "😐neutral":"#ced4d0", "😔sad":"#e96678", "😥sadness":"#e96678", "😳shame":"#e96678", "😮surprise":"#70bda0"}
            
from PIL import Image
# def main():
##TOP PAGE
st.title("Media Analytics & Warning Systems of Money Politics")
st.subheader("Toward Clean & Accountable Local Government")
st.markdown('<style>h1{color:dark-grey;font-size:62px}</style>',unsafe_allow_html=True)
st.sidebar.image(Image.open('MAWSMP.png'))
menu = ['Monitoring Nasional','Analisis Risiko Pemerintah Daerah','Tren & Histori Sentimen Publik', 'Sentimen Publik Terkini','Analisis LHKPN']
choice = st.sidebar.selectbox("Pilih Menu",menu)

if choice == 'Sentimen Publik Terkini':
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
        df['emoji'] = [emotions_emoji[x]+x for x in df['emotion']]
        df['tanggal'] = pd.to_datetime(df['date']).dt.date
        df['count'] = 1
        st.subheader("Tren Sentiment Publik")
        linefig = px.bar(df, x='tanggal', y='viewCount', color='sentiment', color_discrete_map=sentiment_color)
        st.plotly_chart(linefig,use_container_width=True)
        col1,col2 = st.columns((1,1))
        with col1:
            st.subheader("Sebaran Sentiment Publik")
            piefig = px.pie(df, names='sentiment', values='count', color='sentiment', hole=.6, color_discrete_map=sentiment_color)
            st.plotly_chart(piefig,use_container_width=True)
        with col2:
            st.subheader("Sebaran Emosi Publik")
            barfig = px.pie(df, names='emoji', values='likeCount', color='emoji',hole=.6)
            st.plotly_chart(barfig,use_container_width=True)
        st.dataframe(df)
    else:
        st.write("masukkan kata pencarian")
elif choice == 'Tren & Histori Sentimen Publik':
    st.subheader("Analisis Data historis Twitter")
    df = pd.read_csv('twitdata.csv')
    custom_search = st.expander(label='Histori Persepsi Publik Melalui Media Twitter')
    with custom_search:
        listpemda = df['city'].unique().tolist()
        ctr = st.selectbox("Pilih Pemda",listpemda)
        if st.button("Jalankan"):
            df = df[df['city'].isin([ctr])]
            df['emoji'] = [emotions_emoji[x]+x for x in df['emotion']]
            df['bulan'] = pd.to_datetime(df['date']).dt.month
            df['tanggal'] = pd.to_datetime(df['date']).dt.date
            df['count'] = [1 for x in df['emotion']]
            st.subheader("Tren Sentiment Publik")
            linefig = px.bar(df, x='tanggal', y='count', color='sentiment', color_discrete_map=sentiment_color)
            st.plotly_chart(linefig,use_container_width=True)
            # st.line_chart(df)
            c1,c2 = st.columns((1,1))
            with c1:
                st.subheader("Sebaran Sentiment Publik")
                piefig = px.pie(df, names='sentiment', values='count', color='sentiment', hole=.6, color_discrete_map=sentiment_color)
                st.plotly_chart(piefig,use_container_width=True)
            with c2:
                st.subheader("Sebaran Emosi Publik")
                barfig = px.pie(df, names='emoji', values='likeCount', color='emoji',hole=.6)
                st.plotly_chart(barfig,use_container_width=True)
                # barfig = px.bar(df, x='emoji', y='likeCount', color='emoji', color_discrete_map=emotions_color)
                # st.plotly_chart(barfig,use_container_width=True)
            dff = df[['date','username','rawContent','emoji','sentiment','likeCount', 'retweetCount', 'mentioned']]
            st.dataframe(dff)
elif choice == 'Analisis Risiko Pemerintah Daerah':
    ipm = pd.read_csv('ipm.csv')
    kasus = pd.read_csv('penindakan.csv')
    blj = pd.read_csv('belanja.csv')
    blj = blj[blj['tahun']>2009]
    custom_search = st.expander(label='Analisis Risiko Berdasarkan Belanja, Histori Penindakan KPK dan Index Pembangunan Manusia')
    with custom_search:
        ipm = pd.read_csv('ipm.csv')
        listpemda = ipm['Pemda'].tolist()
        ctr = st.selectbox("Pilih Pemda",listpemda)
        if st.button("Jalankan"):
            c1,c2 = st.columns((2,1))
            with c1:
                st.subheader("Tren Belanja Daerah")
                blj = blj[blj['namapemda'].isin([ctr])]
                linefig1 = px.bar(blj, x='tahun', y='nilai', color='Level2a',barmode='group')
                linefig1.update_xaxes(categoryorder='array', categoryarray= ['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022'])
                st.plotly_chart(linefig1,use_container_width=True)
                blj = blj[['tahun','level3a','nilai','Gubernur','WakilGubernur','Level2a','level3',]]
                
            with c2:
                st.subheader("Proporsi Belanja Daerah")
                sunfig = px.sunburst(blj, path=['Level2a','level3','level3a'], 
                            values='nilai')
                st.plotly_chart(sunfig,use_container_width=True)
                
            # with c3:
            #     st.subheader("Pertumbuhan IPM Daerah")
            #     ipm = ipm[ipm['Pemda'].isin([ctr])]
            #     linefig3 = px.line(ipm, x='tahun', y='nilai')
            #     linefig3.update_xaxes(type='category')
            #     st.plotly_chart(linefig3,use_container_width=True)
            k1,k2 = st.columns((1,1))
            with k1:
                st.subheader("Detail Belanja Daerah")
                st.dataframe(blj)
            with k2:
                # blj = blj[blj['tahun']==2022]
                st.subheader("Penindakan KPK")
                kasus = kasus[kasus['PROVINSI'].isin([ctr])]
                linefig2 = px.line(kasus, x='Tahun', y='Jumlah Penindakan')
                linefig2.update_xaxes(type='category')
                st.plotly_chart(linefig2,use_container_width=True)


elif choice == 'Monitoring Nasional':
    st.subheader('Peta Risiko Korupsi Pemerintah Daerah')
    import streamlit.components.v1 as components
    components.html('''
        <div class='tableauPlaceholder' id='viz1683812683355' style='position: relative'><noscript><a href='#'><img alt='Tingkat Kerawanan dan Upaya Pencegahan Korupsi ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;In&#47;IndeksSPI&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='IndeksSPI&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;In&#47;IndeksSPI&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1683812683355');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='977px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
        ''',height=900,
            width=1440)
    
elif choice == 'Analisis LHKPN':
    # st.subheader('PErkembangan Daerah')
    import streamlit.components.v1 as components
    components.html('''
        <div class='tableauPlaceholder' id='viz1683819509018' style='position: relative'><noscript><a href='#'><img alt='Perkembangan Total Harta di LHKPN ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;LH&#47;LHKPN&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='LHKPN&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;LH&#47;LHKPN&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1683819509018');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='800px';vizElement.style.height='627px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='800px';vizElement.style.height='627px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
        ''',height=900,
            width=1440)
# if __name__=='__main__':
#     # if st._is_running_with_streamlit:
#     if runtime.exists():
#         main()   
#     else:
#         sys.argv = ["streamlit", "run", sys.argv[0]]
#         sys.exit(stcli.main())
