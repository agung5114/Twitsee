
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
from generateWordcloud import create_wordcloud

# from similar import getProgram, apbd
from classifier import pre_process

end = datetime.date.today()
start = end - timedelta(days = 31)

end = end.strftime('%Y-%m-%d')
start = start.strftime('%Y-%m-%d')
belanja_color = {"53. Belanja Modal": "#e96678", "51. Belanja Pegawai": "#ced4d0", "52. Belanja Barang Jasa": "#70bda0",'54. Belanja Lainnya':"#e96678"}
sentiment_color = {"negative": "#e96678", "neutral": "#ced4d0", "positive": "#70bda0"}
group_color = {"opposers": "#e96678", "supporters": "#70bda0"}
emotions_emoji = {"anger":"😡","disgust":"🤮", "fear":"😱", "happy":"🤗", "joy":"🤩", "love":"😍", "neutral":"😐", "sad":"😔", "sadness":"😥", "shame":"😳", "surprise":"😮"}
emotions_color = {"opposers": "#e96678", "supporters": "#70bda0","😡anger":"#de425b","🤮disgust":"#df676e", "😱fear":"#e88b8d", "😔sad":"#eeadad", "😥sadness":"#f1cfce", "😐neutral":"#f1f1f1","😳shame":"#d0ddc9", "😮surprise":"#afc9a2","🤗happy":"#8eb67c", "🤩joy":"#6ca257","😍love":"#488f31"}

@st.cache_data
def getApbd():
    dfa = pd.read_excel('Program APBD.xlsx')
    return dfa

@st.cache_data
def getModal():
    dfm = pd.read_excel('BelanjaModal.xlsx')
    return dfm

from PIL import Image
st.image(Image.open('maws-banner.png'))
st.markdown('<style>h1{color:dark-grey;font-size:62px}</style>',unsafe_allow_html=True)
st.sidebar.image(Image.open('maws-menu.png'))
# menu = ['Peta','Monitoring Nasional','Analisis Risiko Pemerintah Daerah','Tren & Histori Sentimen Publik', 'Sentimen Publik Terkini','Analisis LHKPN','Smart Monitoring Program Daerah']
menu = ['Monitoring Potensi Risiko','Luminosity Analysis','Analisis Data Keuangan','Monitoring Program Daerah','Analisis Sentimen & Emosi Publik']
choice = st.sidebar.selectbox("Pilih Menu",menu)

if choice == 'Monitoring Potensi Risiko':
    st.subheader('Peta Risiko Korupsi Pemerintah Daerah')
    dfcase = pd.read_csv('kasusAll.csv',sep=";")
    c1,c2 = st.columns((1,1))
    import streamlit.components.v1 as components
    with c1:
        components.html('''
            <div class='tableauPlaceholder' id='viz1683812683355' style='position: relative'><noscript><a href='#'><img alt='Tingkat Kerawanan dan Upaya Pencegahan Korupsi ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;In&#47;IndeksSPI&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='IndeksSPI&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;In&#47;IndeksSPI&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1683812683355');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='977px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
            ''',height=627,
                width=800)
    with c2:
        components.html('''
            <div class='tableauPlaceholder' id='viz1683819509018' style='position: relative'><noscript><a href='#'><img alt='Perkembangan Total Harta di LHKPN ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;LH&#47;LHKPN&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='LHKPN&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;LH&#47;LHKPN&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1683819509018');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='800px';vizElement.style.height='627px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='800px';vizElement.style.height='627px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
            ''',height=627,
                width=800)
    k1,k2 = st.columns((1,1))
    with k1:
        st.subheader('Penindakan KPK terkait Pemerintah Daerah')
        dfplot = dfcase.groupby(by=['tahun'],as_index=False).agg({'kepala daerah':'sum','dprd':'sum','dinas':'sum'})
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dfplot['tahun'],
            y=dfplot['kepala daerah'],
            name='kepala daerah',
            marker_color='indianred',
            textposition="inside",
            text=dfplot['kepala daerah'],
        ))
        fig.add_trace(go.Bar(
            x=dfplot['tahun'],
            y=dfplot['dprd'],
            name='dprd',
            marker_color='lightsalmon',
            textposition="inside",
            text=dfplot['dprd'],
        ))
        fig.add_trace(go.Bar(
            x=dfplot['tahun'],
            y=dfplot['dinas'],
            name='dinas',
            marker_color='darkred',
            textposition="inside",
            text=dfplot['dinas'],
        ))
        fig.update_layout(title_text='Perkembangan kasus per tahun')
        st.plotly_chart(fig,use_container_width=True)
    with k2:
        st.plotly_chart(create_wordcloud(dfcase,'text'))

    dftable = dfcase[['kasus','bulan','tahun','pemda']]
    st.dataframe(dftable,use_container_width=True)

elif choice == 'Analisis Sentimen & Emosi Publik':
    # history = st.expander(label="Analisis Data historis Twitter")
    # with history:
    @st.cache_data
    def getData():
        df = pd.read_csv('twitpemda.csv')
        df['emosi'] = [emotions_emoji[x]+x for x in df['emotion']]
        df['group'] = ['opposers' if x in ['anger','fear','sadness','sad'] else 'supporters' for x in df['emotion']]
        # df['bulan'] = pd.to_datetime(df['date']).dt.month
        # df['tanggal'] = pd.to_datetime(df['date']).dt.date
        # df['count'] = [1 for x in df['emotion']]
        # df['engagement'] = df['count']+df['retweetCount']+df['likeCount']
        df = df[['tanggal','tahun','username','rawContent','sentiment','emosi','group','count','engagement','city']]
        return df
    genre = st.sidebar.radio("Pilih Analisis",('Data Historis', 'Realtime'))
    if genre == 'Data Historis':
        st.subheader('Histori Persepsi Publik Melalui Media Twitter')
        df = getData()
        listpemda = df['city'].unique().tolist()
        listtahun = df['tahun'].unique().tolist()
        sb1,sb2 = st.columns((1,1))
        with sb1:
            ctr = st.selectbox("Pilih Pemda",['All']+listpemda)
        with sb2:
            thn = st.selectbox("Pilih Tahun",listtahun, key=2023)
        
        # if st.button("Jalankan"):
        if ctr == 'All':
            st.subheader("Tren Sentiment Publik")
            df = df[df['tahun']==thn]
            dfplot = df.groupby(by=['tanggal','sentiment'],as_index=False).agg({'engagement':'sum'})
            linefig = px.bar(df, x='tanggal', y='engagement', color='sentiment', color_discrete_map=sentiment_color)
            st.plotly_chart(linefig,use_container_width=True)
            st.dataframe(df,use_container_width=True)
        else:
            dfpemda = df[df['city'].isin([ctr])]
            dfpwmda= dfpemda[dfpemda['tahun']==thn]
            # st.line_chart(df)
            c1,c2 = st.columns((1,1))
            with c1:
                st.subheader("Sebaran Sentiment Publik")
                piefig = px.pie(dfpemda, names='sentiment', values='count', color='sentiment', hole=.6, color_discrete_map=sentiment_color)
                st.plotly_chart(piefig,use_container_width=True)
            with c2:
                st.subheader("Sebaran Emosi Publik")
                # barfig = px.pie(dfpemda, names='emosi', values='engagement', color='emosi',hole=.6,color_discrete_map=emotions_color)
                figsun = px.sunburst(df, path=['group','emosi'],values='engagement')
                figsun.update_traces(textinfo='label+value+percent entry')
                figsun.update_traces(marker_colors=[emotions_color[cat] for cat in figsun.data[-1].labels])
                st.plotly_chart(figsun,use_container_width=True)
                # barfig = px.bar(df, x='emoji', y='likeCount', color='emoji', color_discrete_map=emotions_color)
                # st.plotly_chart(barfig,use_container_width=True)
            dff = dfpemda
            st.dataframe(dff,use_container_width=True)
    else:
        st.write("Sentimen dan Emosi Publik Terkini")
    # custom_search = st.expander(label='Histori Persepsi Publik Melalui Media Twitter')
    # with custom_search:
        # realtime = st.expander(label="Sentimen dan Emosi Publik Terkini")
        # with realtime:
        submitted = st.empty()
        with st.form(key='text'):
            search_text = st.text_input("Pencarian Tweet terbaru")
            submitted = st.form_submit_button('Submit')
        # st.subheader("Sentimen dan Emosi Publik Terkini")
        # c1,c2 = st.columns((1,4))
        # with c1:
        # with c2:
        #     st.empty()
        if submitted:
            raw_text = search_text
            df = getTweets(raw_text,start,end,50)
            df['emosi'] = [emotions_emoji[x]+x for x in df['emotion']]
            df['tanggal'] = pd.to_datetime(df['date']).dt.date
            df['count'] = 1
            df['engagement'] = df['count']+df['retweetCount']
            df['group'] = ['opposers' if x in ['anger','fear','sadness','sad'] else 'supporters' for x in df['emotion']]
            df = df[['tanggal','username','rawContent','sentiment','emosi','group','count','engagement']]
            st.subheader("Tren Sentiment Publik")
            dfbar = df.groupby(['tanggal','sentiment'],as_index=False).agg({'count':'sum'})
            linefig = px.bar(dfbar, x='tanggal', y='count', color='sentiment', color_discrete_map=sentiment_color)
            st.plotly_chart(linefig,use_container_width=True)
            col1,col2 = st.columns((1,1))
            with col1:
                st.subheader("Sebaran Sentiment Publik")
                piefig = px.pie(df, names='sentiment', values='count', color='sentiment', hole=.6, color_discrete_map=sentiment_color)
                st.plotly_chart(piefig,use_container_width=True)
            with col2:
                st.subheader("Sebaran Emosi Publik")
                # barfig = px.pie(df, names='emosi', values='likeCount', color='emosi',hole=.6,color_discrete_map=emotions_color)
                # st.plotly_chart(barfig,use_container_width=True)
                figsun = px.sunburst(df, path=['group','emosi'],values='engagement')
                figsun.update_traces(textinfo='label+value+percent entry')
                figsun.update_traces(marker_colors=[emotions_color[cat] for cat in figsun.data[-1].labels])
                st.plotly_chart(figsun,use_container_width=True)
            st.dataframe(df,use_container_width=True)
        else:
            st.write("masukkan kata pencarian")
elif choice == 'Analisis Data Keuangan':
    st.subheader("Analisis Risiko Berdasarkan Belanja dan Histori Penindakan KPK")
    # ipm = pd.read_csv('ipm.csv')
    kasus = pd.read_csv('penindakan.csv')
    blj = pd.read_csv('belanja.csv')
    risk = pd.read_csv('growth.csv')
    blj = blj[blj['tahun']>2009]
    custom_search = st.expander(label='Analisis Risiko Pemerintah Daerah')
    with custom_search:
        # ipm = pd.read_csv('ipm.csv')
        listpemda = blj['namapemda'].unique().tolist()
        ctr = st.selectbox("Pilih Pemda",listpemda)
        if st.button("Jalankan"):
            risk = risk[risk['Pemda'].isin([ctr])]
            bansos = risk['bansos'].values[0]
            modal = risk['modal'].values[0]
            bankeu = risk['bankeu'].values[0]
            risiko = risk['Risiko'].values[0]
            st.write(f'Tingkat Pertumbuhan Belanja Bantuan Sosial:{bansos}')
            st.write(f'Tingkat Pertumbuhan Belanja Modal: {modal}')
            st.write(f'Tingkat Pertumbuhan Belanja Bantuan Keuangan: {bankeu}')
            st.subheader(f'Tingkat Risiko: {risiko}')
            c1,c2 = st.columns((2,1))
            with c1:
                st.subheader("Tren Belanja Daerah")
                blj = blj[blj['namapemda'].isin([ctr])]
                linefig1 = px.bar(blj, x='tahun', y='nilai', color='level3a',barmode='group')
                linefig1.update_xaxes(categoryorder='array', categoryarray= ['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022'])
                st.plotly_chart(linefig1,use_container_width=True)
                blj = blj[['tahun','level3a','nilai','Gubernur','WakilGubernur','Level2a','level3',]]
                
            with c2:
                st.subheader("Proporsi Belanja Daerah")
                sunfig = px.sunburst(blj, path=['Level2a','level3a'], 
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
    
elif choice == 'Monitoring Program Daerah':
    st.subheader("Program Belanja Daerah Berdasarkan Kata Kunci")
    apbd = getApbd
    custom_search = st.expander(label='Pencarian Program')
    with custom_search:
        keyw = st.text_input("Masukkan Kata Kunci")
        out = keyw.lower().split()
        if st.button("Jalankan"):
            st.write(f'Program Terkait dengan {keyw}:')
            # out = getProgram(keyw)
            # st.subheader(out)
            # df = apbd[apbd['Program'] == out]
            apbd['text'] = apbd['Program'].apply(pre_process)
            apbd['key'] = apbd['text'].str.contains('|'.join(out)).astype('int')
            df = apbd[apbd['key'] == 1]
            c1,c2 = st.columns((2,3))
            with c1:
                listpro = df['Program'].unique()
#                 st.dataframe(df.groupby('Program').agg({'Nilaianggaran':'sum'}))
                st.table(df.groupby('Program').agg({'Nilaianggaran':'sum'}))
#                 st.table(listpro)
                st.write("Total anggaran " + ": Rp" + str(round(df['Nilaianggaran'].sum()/1e9,2)) + " Miliar")
                st.write("Porsi anggaran " + " terhadap total belanja: " + str(round(df['Nilaianggaran'].sum()/apbd['Nilaianggaran'].sum()*100,2)) + "%")
            with c2:
                fig = px.bar(df, x="Provinsi", y="Nilaianggaran", color="Akun Analisis", barmode = 'stack')
                st.plotly_chart(fig,use_container_width=True)
            st.dataframe(df.groupby(['Program','Akun Analisis','Provinsi'],as_index=False).agg({'Nilaianggaran':'sum'}),use_container_width=True)


elif choice == 'Luminosity Analysis':
    dfModal = getModal()
    st.subheader('Luminosity Maps')
    import streamlit.components.v1 as components
    # from html2image import Html2Image
    def calc_brightness(image):
            greyscale_image = image.convert('L')
            histogram = greyscale_image.histogram()
            pixels = sum(histogram)
            brightness = scale = len(histogram)
            for index in range(0, scale):
                ratio = histogram[index] / pixels
                brightness += ratio * (-scale + index)
            return 1 if brightness == 255 else brightness / scale

    st.subheader('Perkembangan Index Luminosity Pemda')
    # dflok = pd.read_csv('latlon.csv')
    # dflok = pd.read_csv('latlon.csv')
    # st.dataframe(dflok)
    # pemdas = dflok['city'].unique().tolist()
    dflok = pd.read_csv('latlong_all.csv')
    pemdas = dflok['pemda'].tolist()
    latlon = st.selectbox(label='Pilih Pemda',options=pemdas, key='All')
    pemdalok = dflok[dflok['pemda']==latlon]
    # tombol = st.button('Jalankan')
    # if tombol:
    lat = pemdalok['lat'].tolist()[0]
    lon = pemdalok['lon'].tolist()[0]
    zoom = pemdalok['zoom'].tolist()[0]
    st.write(f'Latitude:{lat} , Longitude:{lon}')
    # lat='-6.1750'
    # lon='106.8275'
    lum = pemdalok['2018'].tolist()[0]
    lum2 = pemdalok['2022'].tolist()[0]
    # st.subheader(f'Tingkat perubahan:{(lum2-lum):.4f}')
    gap = lum2-lum
    growth = gap/lum
    # st.subheader(f'Persentase perubahan:{growth:.2%}')
    if latlon == 'All':
        htmlindo= '''
            <style>
                .iframe-container { overflow: hidden;margin-top: -50px;}
            </style>
            <iframe
                id="2021indo"
                class="iframe-container"
                src=https://www.lightpollutionmap.info/#zoom=4.59&lat=-2.9756&lon=115.2515&state=eyJiYXNlbWFwIjoiTGF5ZXJCaW5nSHlicmlkIiwib3ZlcmxheSI6InZpaXJzXzIwMjEiLCJvdmVybGF5Y29sb3IiOmZhbHNlLCJvdmVybGF5b3BhY2l0eSI6NjUsImZlYXR1cmVzIjpbIlNRQyJdLCJmZWF0dXJlc29wYWNpdHkiOjg1fQ==
                frameborder="20"
                width="1600"
                height="720"
            ></iframe>
            <script src="https://cdn.jsdelivr.net/npm/iframe-resizer@4.3.4/js/iframeResizer.min.js"></script>
            <script>
            iFrameResize({}, "#2021indo")
            </script>
            '''
        components.html(htmlindo,height=730,width=1620)
        fig0 = go.Figure()
        fig0.add_trace(go.Indicator(
                        mode = "number+delta",
                        # value = status*100,
                        value = int(lum*100000)/100000,
                        title = {"text": "Index Luminosity 2018:"},
                        delta = {'reference': int(lum*100000)/100000, 'relative': False},
                        domain = {'row': 0, 'column': 0},
                        ))
        fig0.add_trace(go.Indicator(
                        mode = "number+delta",
                        # value = status*100,
                        value = int(lum2*100000)/100000,
                        title = {"text": "Index Luminosity 2022:"},
                        delta = {'reference': int(lum*100000)/100000, 'relative': False},
                        domain = {'row': 0, 'column': 1},
                        ))
        fig0.add_trace(go.Indicator(
                        mode = "delta",
                        # value = status*100,
                        value = int((1+growth)*100000)/1000,
                        title = {"text": "Tingkat Perubahan (%):"},
                        delta = {'reference': int(100), 'relative': False},
                        domain = {'row': 0, 'column': 2},
                        ))
        fig0.update_layout(grid = {'rows': 1, 'columns': 3, 'pattern': "independent"})
        st.plotly_chart(fig0,use_container_width=True)
    else:
        c1,c2 = st.columns((1,1))
        with c1:
            st.subheader("Tahun 2018")
            # position: relative;
            link1 = f"https://www.lightpollutionmap.info/#zoom={zoom}&lat={lat}&lon={lon}&state=eyJiYXNlbWFwIjoiTGF5ZXJCaW5nUm9hZCIsIm92ZXJsYXkiOiJ2aWlyc18yMDE4Iiwib3ZlcmxheWNvbG9yIjp0cnVlLCJvdmVybGF5b3BhY2l0eSI6NjAsImZlYXR1cmVzb3BhY2l0eSI6ODV9"
            # link1 = f"https://www.lightpollutionmap.info/#zoom=10&lat={lat}&lon={lon}&state=eyJiYXNlbWFwIjoiTGF5ZXJCaW5nSHlicmlkIiwib3ZlcmxheSI6InZpaXJzXzIwMTgiLCJvdmVybGF5Y29sb3IiOnRydWUsIm92ZXJsYXlvcGFjaXR5Ijo2OSwiZmVhdHVyZXMiOlsiU1FNIiwiU1FNTCJdLCJmZWF0dXJlc29wYWNpdHkiOjg1fQ=="
            html1= '''
                <style>
                    .iframe-container { overflow: hidden;margin-top: -50px;}
                </style>
                <iframe
                    id="2018map"
                    class="iframe-container"
                    src='''+link1+'''
                    frameborder="20"
                    width="860"
                    height="720"
                ></iframe>
                <script src="https://cdn.jsdelivr.net/npm/iframe-resizer@4.3.4/js/iframeResizer.min.js"></script>
                <script>
                iFrameResize({}, "#2018map")
                </script>
                '''
            comp1 = components.html(html1,height=720,
                    width=880)
            fig1 = go.Figure()
            fig1.add_trace(go.Indicator(
                        mode = "number+delta",
                        # value = status*100,
                        value = int(lum*100000)/100000,
                        title = {"text": "Index Luminosity 2018:"},
                        delta = {'reference': int(lum*100000)/100000, 'relative': False},
                        domain = {'row': 0, 'column': 0},
                        ))
            
            st.plotly_chart(fig1)
        with c2:
            st.subheader("Tahun 2022")
            link2 = f"https://www.lightpollutionmap.info/#zoom={zoom}&lat={lat}&lon={lon}&state=eyJiYXNlbWFwIjoiTGF5ZXJCaW5nUm9hZCIsIm92ZXJsYXkiOiJ2aWlyc18yMDIyIiwib3ZlcmxheWNvbG9yIjp0cnVlLCJvdmVybGF5b3BhY2l0eSI6NjAsImZlYXR1cmVzb3BhY2l0eSI6ODV9"
            # link2 = f"https://www.lightpollutionmap.info/#zoom=10&lat={lat}&lon={lon}&state=eyJiYXNlbWFwIjoiTGF5ZXJCaW5nSHlicmlkIiwib3ZlcmxheSI6InZpaXJzXzIwMjIiLCJvdmVybGF5Y29sb3IiOnRydWUsIm92ZXJsYXlvcGFjaXR5Ijo2OSwiZmVhdHVyZXMiOlsiU1FNIiwiU1FNTCJdLCJmZWF0dXJlc29wYWNpdHkiOjg1fQ=="
            html2 ='''
                <style>
                    .iframe-container {
                        overflow: hidden;
                        margin-top: -50px;
                    }
                </style>
                <iframe
                    id="2022map"
                    class="iframe-container"
                    src='''+link2+'''
                    frameborder="20"
                    width="860"
                    height="720"
                ></iframe>
                <script src="https://cdn.jsdelivr.net/npm/iframe-resizer@4.3.4/js/iframeResizer.min.js"></script>
                <script>
                iFrameResize({}, "#2022map")
                </script>
                '''
            comp2 = components.html(html2,height=720,
                    width=880)

            fig2 = go.Figure()
            fig2.add_trace(go.Indicator(
                        mode = "number+delta",
                        # value = status*100,
                        value = int(lum2*100000)/100000,
                        title = {"text": "Index Luminosity 2022:"},
                        delta = {'reference': int(lum*100000)/100000, 'relative': False},
                        domain = {'row': 0, 'column': 0},
                        ))
            fig2.add_trace(go.Indicator(
                            mode = "delta",
                            # value = status*100,
                            value = int((1+growth)*100000)/1000,
                            title = {"text": "Tingkat Perubahan (%):"},
                            delta = {'reference': int(100), 'relative': False},
                            domain = {'row': 0, 'column': 1},
                            ))
            fig2.update_layout(grid = {'rows': 1, 'columns': 2, 'pattern': "independent"})
            st.plotly_chart(fig2,use_container_width=True)
#     dfApbd = dfApbd['

    dfModal = dfModal[dfModal['namapemda']==latlon]
    st.dataframe(dfModal,use_container_width=True)
    
    lumcal2 = st.expander(label='Perhitungan Index Luminosity')
    with lumcal2:
        k1,k2 = st.columns((1,1))
        with k1:
            img3 = st.file_uploader(label='Upload map image 1',type=['png', 'jpg'])
            if img3 is not None:
                st.image(Image.open(img3))
                lum3 = calc_brightness(Image.open(img3))
                st.subheader(f'Index Luminosity 1: {lum3:.3f}')
            else:
                st.write("No image uploaded")
        with k2:
            img4 = st.file_uploader(label='Upload map image 2',type=['png', 'jpg'])
            if img4 is not None:
                st.image(Image.open(img4))
                lum4 = calc_brightness(Image.open(img4))
                st.subheader(f'Index Luminosity 2: {lum4:.4f}')
            else:
                st.write("No image uploaded")
        if img3 is not None and img4 is not None:
            # st.subheader(f'Tingkat perubahan:{(lum4-lum3):.4f}')
            growth4 = (lum4-lum3)/lum3
            # st.subheader(f'Persentase perubahan:{growth:.2%}')
            fig4 = go.Figure()
            fig4.add_trace(go.Indicator(
                        mode = "number+delta",
                        # value = status*100,
                        value = int(lum3*100000)/100000,
                        title = {"text": "Index 1:"},
                        delta = {'reference': int(lum3*100000)/100000, 'relative': False},
                        domain = {'row': 0, 'column': 0},
                        ))
            fig4.add_trace(go.Indicator(
                            mode = "number+delta",
                            # value = status*100,
                            value = int(lum4*100000)/100000,
                            title = {"text": "Index 2:"},
                            delta = {'reference': int(lum3*100000)/100000, 'relative': False},
                            domain = {'row': 0, 'column': 1},
                            ))
            fig4.add_trace(go.Indicator(
                            mode = "delta",
                            # value = status*100,
                            value = int((1+growth4)*100000)/1000,
                            title = {"text": "Tingkat Perbedaan (%):"},
                            delta = {'reference': int(100), 'relative': False},
                            domain = {'row': 0, 'column': 2},
                            ))
            fig4.update_layout(grid = {'rows': 1, 'columns': 3, 'pattern': "independent"})
            st.plotly_chart(fig4,use_container_width=True)
        else:
            st.empty()
    
    

    # lumcal = st.expander(label='Perhitungan Index Luminousity')
    # with lumcal:
    #     k1,k2 = st.columns((1,1))
    #     with k1:
    #         img = st.file_uploader(label='Upload map image 1',type=['png', 'jpg'])
    #         if img is not None:
    #             st.image(Image.open(img))
    #             lum = calc_brightness(Image.open(img))
    #             st.subheader(f'Luminousity index: {lum:.3f}')
    #         else:
    #             st.write("No image uploaded")
    #     with k2:
    #         img2 = st.file_uploader(label='Upload map image 2',type=['png', 'jpg'])
    #         if img2 is not None:
    #             st.image(Image.open(img2))
    #             lum2 = calc_brightness(Image.open(img2))
    #             st.subheader(f'Luminousity index: {lum2:.3f}')
    #         else:
    #             st.write("No image uploaded")
    #     if img is not None and img2 is not None:
    #         st.subheader(f'Tingkat perubahan:{(lum2-lum):.3f}')
    #         st.subheader(f'Persentase perubahan:{((lum2-lum)/lum):.3%}')
# if __name__=='__main__':
#     # if st._is_running_with_streamlit:
#     if runtime.exists():
#         main()   
#     else:
#         sys.argv = ["streamlit", "run", sys.argv[0]]
#         sys.exit(stcli.main())
