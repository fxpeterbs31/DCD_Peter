import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt
import altair as alt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth

st.set_option('deprecation.showPyplotGlobalUse', False)

cid = 'df823112757f4efb9198fc69c25f2376'
secret = '83e1dff740194dac933212f552ff1de4'
redirect = 'http://localhost:3000'
scope = 'user-top-read'

sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        client_id = cid, 
        client_secret = secret, 
        redirect_uri = redirect, 
        scope = scope
    )
)

pio.templates.default = 'plotly'
# st.write('Di Home, kasih plot k-means buat song sm genre(?)')
# st.write('Kita bikin analisa cluster di hlmn ini')

data       = pd.read_csv('D:/Algoritma/DCD/DCD/data_new/data.csv')
genre_data = pd.read_csv('D:/Algoritma/DCD/DCD/data_new/data_by_genres.csv')

random.seed(100)

song_cluster_pipeline = Pipeline([('scaler', StandardScaler()), 
                                ('kmeans', KMeans(n_clusters=7, 
                                verbose=False, random_state = 42))
                                ], verbose=False)

X = data.select_dtypes(np.number)
number_cols = list(X.columns)
song_cluster_pipeline.fit(X)
song_cluster_labels = song_cluster_pipeline.predict(X)
data['cluster_label'] = song_cluster_labels

pca_pipeline = Pipeline([('scaler', StandardScaler()), ('PCA', PCA(n_components=2))])
song_embedding = pca_pipeline.fit_transform(X)
projection = pd.DataFrame(columns=['x', 'y'], data=song_embedding)
projection['title'] = data['name']
projection['cluster'] = data['cluster_label']

fig = px.scatter(
    projection, x='x', y='y', color='cluster', hover_data=['title']
)

_, title, _ = st.columns([3,4,3])
with title: 
    st.markdown('## Song Clusters')

st.markdown('### Berikut adalah hasil dari proses Clustering berdasarkan dataset lagu yang dimiliki')

st.plotly_chart(fig)

radio_cluster = st.radio('Choose the cluster you want to analyze', 
                         [
                             'Cluster 0',
                             'Cluster 1',
                             'Cluster 2',
                             'Cluster 3',
                             'Cluster 4',
                             'Cluster 5',
                             'Cluster 6'
                         ], horizontal = True)

projection = pd.merge(
    projection, data, \
    left_on = ['title'], right_on = ['name'], \
    how = 'inner'
)

cols_to_keep = [
    'title',
    'artists',
    'danceability',
    'energy',
    'loudness',
    'speechiness',
    'acousticness',
    'instrumentalness',
    'liveness',
    'valence',
    'tempo',
    'duration_ms',
    'cluster'
]

projection = projection[cols_to_keep]

projection['artists'] = \
    projection['artists']\
        .str.replace("'", "")\
        .str.replace('[', '')\
        .str.replace(']', '')

num_cols = [
    'danceability',
    'energy',
    'loudness',
    'speechiness',
    'acousticness',
    'instrumentalness',
    'liveness',
    'valence',
    'tempo',
    'duration_ms'
]

projection['duration_ms'] = projection['duration_ms'] / 60000

num_titles = [
    'Danceability',
    'Energy',
    'Loudness',
    'Speechiness',
    'Acousticness',
    'Instrumentalness',
    'Liveness',
    'Valence',
    'Tempo',
    'Duration'
]

def show_tabs(df, cluster):
    df_stats = df[num_cols].describe()
    df_stats_small = df_stats.loc[['mean', '50%'], :]
    df_stats_small = df_stats_small.T.rename(columns = {
        'mean' : 'Mean',
        '50%'  : 'Median'
    }).T

    st.write(df_stats_small)

    df_danceability     = df_stats_small['danceability']
    df_energy           = df_stats_small['energy']
    df_loudness         = df_stats_small['loudness']
    df_speechiness      = df_stats_small['speechiness']
    df_acousticness     = df_stats_small['acousticness']
    df_instrumentalness = df_stats_small['instrumentalness']
    df_liveness         = df_stats_small['liveness']
    df_valence          = df_stats_small['valence']
    df_tempo            = df_stats_small['tempo']
    df_duration_ms      = df_stats_small['duration_ms']

    tab_1, tab_2, tab_3, tab_4, tab_5, tab_6, tab_7, tab_8, tab_9, tab_10 = st.tabs(num_titles)

    with tab_1:
        df_danceability.plot.bar(rot = 0)
        plt.title('Danceability')
        plt.ylim([0,1])
        plt.ylabel('')
        st.pyplot()

        if(cluster == 'Cluster 0'):
            st.write('Danceability pada Cluster 0 abu-abu. Tidak bisa diambil kesimpulan karena baik Mean maupun Median berkisar di 0.5')

        elif(cluster == 'Cluster 1'):
            st.write('Danceability pada Cluster 1 cukup tinggi. Ini bisa dilihat dengan Mean dan Median yang berada pada diatas 0.5 sehingga bisa diambil kesimpulan bahwa lagu-lagu di Cluster 1 cukup cocok untuk diberikan tarian / koreografi')

        elif(cluster == 'Cluster 2'):
            st.write('Danceability pada Cluster 2 rendah. Ini bisa dilihat dengan Mean dan Median yang berada pada dibawah 0.5 sehingga bisa diambil kesimpulan bahwa lagu-lagu di Cluster 2 tidak cocok untuk diberikan tarian / koreografi')
        
        elif(cluster == 'Cluster 3'):
            st.write('Danceability pada Cluster 3 tinggi. Ini bisa dilihat dengan Mean dan Median yang berada pada diatas 0.5 sehingga bisa diambil kesimpulan bahwa lagu-lagu di Cluster 3 cocok untuk diberikan tarian / koreografi')

        elif(cluster == 'Cluster 4'):
            st.write('Danceability pada Cluster 4 cukup tinggi. Ini bisa dilihat dengan Mean dan Median yang berada pada diatas 0.5 sehingga bisa diambil kesimpulan bahwa lagu-lagu di Cluster 4 cukup cocok untuk diberikan tarian / koreografi')

        elif(cluster == 'Cluster 5'):
            st.write('Danceability pada Cluster 5 abu-abu, namun mengarah ke cocoknya cluster untuk diberikan tarian / koreografi. Karena Mean dan Median berkisar di 0.55 sehingga lagu-lagu di Cluster 5 cukup cocok untuk diberikan tarian / koreografi')

        elif(cluster == 'Cluster 6'):
            st.write('Danceability pada Cluster 6 abu-abu, namun mengarah ke cocoknya cluster untuk diberikan tarian / koreografi. Karena Mean dan Median berkisar di 0.55 sehingga lagu-lagu di Cluster 6 cukup cocok untuk diberikan tarian / koreografi')

    with tab_2:
        df_energy.plot.bar(rot = 0)
        plt.title('Energy')
        plt.ylim([0,1])
        plt.ylabel('')
        st.pyplot()

        if(cluster == 'Cluster 0'):
            st.write('Energy pada Cluster 0 mengarah ke high energy karena Mean dan median berada diatas 0.5')

        elif(cluster == 'Cluster 1'):
            st.write('Energy pada Cluster 1 rendah. Ini bisa dilihat dengan Mean dan Median yang berada dibawah 0.5 sehingga bisa diambil kesimpulan bahwa Cluster 1 low energy')
        
        elif(cluster == 'Cluster 2'):
            st.write('Energy pada Cluster 2 rendah. Ini bisa dilihat dengan Mean dan Median yang berada dibawah 0.5 sehingga bisa diambil kesimpulan bahwa Cluster 2 low energy')

        elif(cluster == 'Cluster 3'):
            st.write('Energy pada Cluster 3 cukup tinggi. Ini bisa dilihat dengan Mean dan Median yang berada diatas 0.5 sehingga bisa diambil kesimpulan bahwa Cluster 3 high energy')

        elif(cluster == 'Cluster 4'):
            st.write('Energy pada Cluster 4 cukup tinggi. Ini bisa dilihat dengan Mean dan Median yang berada diatas 0.5 sehingga bisa diambil kesimpulan bahwa Cluster 4 high energy')

        elif(cluster == 'Cluster 5'):
            st.write('Energy pada Cluster 5 tinggi. Ini bisa dilihat dengan Mean dan Median yang berada diatas 0.5 sehingga bisa diambil kesimpulan bahwa Cluster 5 high energy')

        elif(cluster == 'Cluster 6'):
            st.write('Energy pada Cluster 6 rendah. Ini bisa dilihat dengan Mean dan Median yang berada dibawah 0.5 sehingga bisa diambil kesimpulan bahwa Cluster 6 low energy')
        
    with tab_3:
        df_loudness.plot.bar(rot = 0)
        plt.title('Loudness')
        plt.ylim([-60,0])
        plt.ylabel('decibel (dB)')
        st.pyplot()

        if(cluster == 'Cluster 0'):
            st.write('Loudness pada Cluster 0 tinggi. Ini bisa dilihat dengan Mean dan Median yang kurang lebih berada pada -10')

        elif(cluster == 'Cluster 1'):
            st.write('Loudness pada Cluster 1 cukup tinggi. Ini bisa dilihat dengan Mean dan Median yang kurang lebih berada pada -20')

        elif(cluster == 'Cluster 2'):
            st.write('Loudness pada Cluster 2 cukup tinggi. Ini bisa dilihat dengan Mean dan Median yang kurang lebih berada pada -20')

        elif(cluster == 'Cluster 3'):
            st.write('Loudness pada Cluster 3 tinggi. Ini bisa dilihat dengan Mean dan Median yang berada diatas -10')

        elif(cluster == 'Cluster 4'):
            st.write('Loudness pada Cluster 4 tinggi. Ini bisa dilihat dengan Mean dan Median yang berada diatas -10')

        elif(cluster == 'Cluster 5'):
            st.write('Loudness pada Cluster 5 tinggi. Ini bisa dilihat dengan Mean dan Median yang berada diatas -10')

        elif(cluster == 'Cluster 6'):
            st.write('Loudness pada Cluster 6 cukup tinggi. Ini bisa dilihat dengan Mean dan Median yang kurang lebih berada pada -12')     

    with tab_4:
        df_speechiness.plot.bar(rot = 0)
        plt.title('Speechiness')
        plt.ylim([0,1])
        plt.ylabel('')
        st.pyplot()

        if(cluster == 'Cluster 0'):
            st.write('Speechiness dari Cluster 0 sangat rendah. Ini bisa dilihat dengan Mean dan Median yang berada dibawah 0.1. Berdasarkan parameter Speechiness, Cluster 0 mencirikan cluster lagu yang tidak terdiri dari banyak vokal karena threshold dari lagu berada dibawah 0.33.')

        elif(cluster == 'Cluster 1'):
            st.write('Speechiness dari Cluster 1 sangat tinggi. Ini bisa dilihat dengan Mean dan Median hampir mencapai 1. Berdasarkan parameter Speechiness, Cluster 1 mencirikan cluster track yang cenderung diisi oleh vokal')

        elif(cluster == 'Cluster 2'):
            st.write('Speechiness dari Cluster 2 sangat rendah. Ini bisa dilihat dengan Mean dan Median yang berada dibawah 0.1. Berdasarkan parameter Speechiness, Cluster 2 mencirikan cluster lagu yang tidak terdiri dari banyak vokal karena threshold dari lagu berada dibawah 0.33.')

        elif(cluster == 'Cluster 3'):
            st.write('Speechiness dari Cluster 3 sangat rendah. Ini bisa dilihat dengan Mean dan Median yang kira-kira 0.1. Berdasarkan parameter Speechiness, Cluster 3 mencirikan cluster lagu yang tidak terdiri dari banyak vokal karena threshold dari lagu berada dibawah 0.33')

        elif(cluster == 'Cluster 4'):
            st.write('Speechiness dari Cluster 4 sangat rendah. Ini bisa dilihat dengan Mean dan Median yang berada dibawah 0.1. Berdasarkan parameter Speechiness, Cluster 4 mencirikan cluster lagu yang tidak terdiri dari banyak vokal karena threshold dari lagu berada dibawah 0.33.')

        elif(cluster == 'Cluster 5'):
            st.write('Speechiness dari Cluster 5 sangat rendah. Ini bisa dilihat dengan Mean dan Median yang berada dibawah 0.1. Berdasarkan parameter Speechiness, Cluster 5 mencirikan cluster lagu yang tidak terdiri dari banyak vokal karena threshold dari lagu berada dibawah 0.33.')

        elif(cluster == 'Cluster 6'):
            st.write('Speechiness dari Cluster 6 sangat rendah. Ini bisa dilihat dengan Mean dan Median yang berada dibawah 0.1. Berdasarkan parameter Speechiness, Cluster 6 mencirikan cluster lagu yang tidak terdiri dari banyak vokal karena threshold dari lagu berada dibawah 0.33.')
        
    with tab_5:
        df_acousticness.plot.bar(rot = 0)
        plt.title('Acousticness')
        plt.ylim([0,1])
        plt.ylabel('')
        st.pyplot()

        if(cluster == 'Cluster 0'):
            st.write('Acousticness dari Cluster 0 mengarah ke non-acoustic. Ini bisa dilihat dengan Mean dan Median yang berada sedikit dibawah 0.5')

        elif(cluster == 'Cluster 1'):
            st.write('Acousticness dari Cluster 1 mengarah ke acoustic. Ini bisa dilihat dengan Mean dan Median yang berada sedikit diatas 0.5')            

        elif(cluster == 'Cluster 2'):
            st.write('Acousticness dari Cluster 2 sangat tinggi. Ini bisa dilihat dengan Mean dan Median yang berada diatas 0.8')            

        elif(cluster == 'Cluster 3'):
            st.write('Acousticness dari Cluster 3 rendah. Ini bisa dilihat dengan Mean dan Median yang berada dibawah 0.5')

        elif(cluster == 'Cluster 4'):
            st.write('Acousticness dari Cluster 4 rendah. Ini bisa dilihat dengan Mean dan Median yang berada dibawah 0.5')

        elif(cluster == 'Cluster 5'):
            st.write('Acousticness dari Cluster 5 rendah. Ini bisa dilihat dengan Mean dan Median yang berada dibawah 0.5')

        elif(cluster == 'Cluster 6'):
            st.write('Acousticness dari Cluster 6 tinggi. Ini bisa dilihat dengan Mean dan Median yang berada diatas 0.5')

    with tab_6:
        df_instrumentalness.plot.bar(rot = 0)
        plt.title('Instrumentalness')
        plt.ylim([0,1])
        plt.ylabel('')
        st.pyplot()

        if(cluster == 'Cluster 0'):
            st.write('Instrumentalness dari Cluster 0 sangat rendah. Ini bisa dilihat dengan Mean dan Median yang berada dibawah 0.2, sehingga Cluster 0 bisa dibilang non-instrumental')

        elif(cluster == 'Cluster 1'):
            st.write('Instrumentalness dari Cluster 1 sangat rendah. Ini bisa dilihat dengan Mean dan Median hampir mendekati 0, sehingga Cluster 1 bisa dibilang non-instrumental')

        elif(cluster == 'Cluster 2'):
            st.write('Instrumentalness dari Cluster 2 sangat rendah. Ini bisa dilihat dengan Mean kira-kira 0.35 dan Median yang hampir mendekati 0, sehingga Cluster 1 bisa dibilang non-instrumental')

        elif(cluster == 'Cluster 3'):
            st.write('Instrumentalness dari Cluster 3 sangat rendah. Ini bisa dilihat dengan Mean dan Median hampir mendekati 0, sehingga Cluster 3 bisa dibilang non-instrumental')

        elif(cluster == 'Cluster 4'):
            st.write('Instrumentalness dari Cluster 4 sangat rendah. Ini bisa dilihat dengan Mean dan Median hampir mendekati 0, sehingga Cluster 4 bisa dibilang non-instrumental')

        elif(cluster == 'Cluster 5'):
            st.write('Instrumentalness dari Cluster 5 sangat rendah. Ini bisa dilihat dengan Mean dan Median hampir mendekati 0, sehingga Cluster 5 bisa dibilang non-instrumental')

        elif(cluster == 'Cluster 6'):
            st.write('Instrumentalness dari Cluster 6 sangat rendah. Ini bisa dilihat dengan Mean kira-kira 0.2 dan Median hampir mendekati 0, sehingga Cluster 6 bisa dibilang non-instrumental')
        

    with tab_7:
        df_liveness.plot.bar(rot = 0)
        plt.title('Liveness')
        plt.ylim([0,1])
        plt.ylabel('')
        st.pyplot()

        if(cluster == 'Cluster 0'):
            st.write('Liveness dari Cluster 0 cukup tinggi. Ini bisa dilihat dengan Mean dan Median yang nilainya berada diatas 0.5. Bisa diambil kesimpulan bahwa Cluster 0 memiliki kecenderungan untuk direkam pada kondisi live')

        elif(cluster == 'Cluster 1'):
            st.write('Liveness dari Cluster 1 cukup rendah. Ini bisa dilihat dengan Mean dan Median yang nilainya berada dibawah 0.5. Bisa diambil kesimpulan bahwa Cluster 1 memiliki kecenderungan untuk direkam di studio')

        elif(cluster == 'Cluster 2'):
            st.write('Liveness dari Cluster 2 rendah. Ini bisa dilihat dengan Mean dan Median yang nilainya berada dibawah 0.5. Bisa diambil kesimpulan bahwa Cluster 2 memiliki kecenderungan untuk direkam di studio')

        elif(cluster == 'Cluster 3'):
            st.write('Liveness dari Cluster 3 rendah. Ini bisa dilihat dengan Mean dan Median yang nilainya berada dibawah 0.5. Bisa diambil kesimpulan bahwa Cluster 3 memiliki kecenderungan untuk direkam di studio')

        elif(cluster == 'Cluster 4'):
            st.write('Liveness dari Cluster 4 rendah. Ini bisa dilihat dengan Mean dan Median yang nilainya berada dibawah 0.5. Bisa diambil kesimpulan bahwa Cluster 4 memiliki kecenderungan untuk direkam di studio')

        elif(cluster == 'Cluster 5'):
            st.write('Liveness dari Cluster 5 rendah. Ini bisa dilihat dengan Mean dan Median yang nilainya berada dibawah 0.5. Bisa diambil kesimpulan bahwa Cluster 5 memiliki kecenderungan untuk direkam di studio')

        elif(cluster == 'Cluster 6'):
            st.write('Liveness dari Cluster 6 rendah. Ini bisa dilihat dengan Mean dan Median yang nilainya berada dibawah 0.5. Bisa diambil kesimpulan bahwa Cluster 6 memiliki kecenderungan untuk direkam di studio')        

    with tab_8:
        df_valence.plot.bar(rot = 0)
        plt.title('Valence')
        plt.ylim([0,1])
        plt.ylabel('')
        st.pyplot()

        if(cluster == 'Cluster 0'):
            st.write('Valence dari Cluster 0 cukup abu-abu, namun mengarah ke energi positif. Mean dan median kira-kira berada pada 0.52')

        elif(cluster == 'Cluster 1'):
            st.write('Valence dari Cluster 1 cukup abu-abu, namun mengarah ke energi positif. Mean dan median kira-kira berada pada 0.52')

        elif(cluster == 'Cluster 2'):
            st.write('Valence dari Cluster 2 rendah. Mean dan median kira-kira berada dibawah 0.3')

        elif(cluster == 'Cluster 3'):
            st.write('Valence dari Cluster 3 cukup abu-abu, namun tidak terlihat mengarah ke energi positif atau negatif karena Mean sebesar 0.49 dan median sebesar 0.5')

        elif(cluster == 'Cluster 4'):
            st.write('Valence dari Cluster 4 cukup abu-abu, namun mengarah ke energi positif. Mean dan median kira-kira berada pada 0.55')

        elif(cluster == 'Cluster 5'):
            st.write('Valence dari Cluster 5 cukup abu-abu, namun mengarah ke energi positif. Mean dan median kira-kira berada pada 0.55')

        elif(cluster == 'Cluster 6'):
            st.write('Valence dari Cluster 6 cukup positif. Ini bisa dilihat dengan Mean sebesar 0.58 dan Median sebesar 0.6')
        

    with tab_9:
        df_tempo.plot.bar(rot = 0)
        plt.title('Tempo')
        plt.ylim([0,300])
        plt.ylabel('Beat per Minute (bpm)')
        st.pyplot()

        if(cluster == 'Cluster 0'):
            st.write('Tempo dari Cluster 0 adalah Moderato / Tempo Sedang. Ini bisa dilihat dengan Mean sebesar 119 bpm dan Median sebesar 117 bpm yang berada pada range Moderato, yaitu 108 - 120 bpm')

        elif(cluster == 'Cluster 1'):
            st.write('Tempo dari Cluster 1 adalah Andante. Andante tidak terlalu lambat dan mengarah ke Tempo Sedang. Ini bisa dilihat dengan Mean sebesar 108 bpm dan Median sebesar 104 bpm yang berada pada range Andante, yaitu 76 - 108 bpm')

        elif(cluster == 'Cluster 2'):
            st.write('Tempo dari Cluster 2 adalah Andante. Andante tidak terlalu lambat dan mengarah ke Tempo Sedang. Ini bisa dilihat dengan Mean sebesar 104 bpm dan Median sebesar 97 bpm yang berada pada range Andante, yaitu 76 - 108 bpm')

        elif(cluster == 'Cluster 3'):
            st.write('Tempo dari Cluster 3 adalah Moderato / Tempo Sedang. Ini bisa dilihat dengan Mean sebesar 119 bpm dan Median sebesar 115 bpm yang berada pada range Moderato, yaitu 108 - 120 bpm')

        elif(cluster == 'Cluster 4'):
            st.write('Tempo dari Cluster 4 adalah Moderato / Tempo Sedang. Ini bisa dilihat dengan Mean sebesar 120 bpm dan Median sebesar 118 bpm yang berada pada range Moderato, yaitu 108 - 120 bpm')

        elif(cluster == 'Cluster 5'):
            st.write('Tempo dari Cluster 5 adalah Allegro Moderato / Cukup Cepat. Ini bisa dilihat dengan Mean sebesar 121 bpm dan Median sebesar 119 bpm yang berada pada range Allegro Moderato, yaitu 112 - 124 bpm')

        elif(cluster == 'Cluster 6'):
            st.write('Tempo dari Cluster 6 adalah Moderato / Tempo Sedang. Ini bisa dilihat dengan Mean sebesar 120 bpm dan Median sebesar 118 bpm yang berada pada range Moderato, yaitu 108 - 120 bpm')       

    with tab_10:
        df_duration_ms.plot.bar(rot = 0)
        plt.title('Duration')
        plt.ylim([0,5])
        plt.ylabel('Minutes (m)')
        st.pyplot()

        if(cluster == 'Cluster 0'):
            st.write('Durasi dari Cluster 0 cukup lama. Ini bisa dilihat dengan Mean sebesar 4 menit 24 detik dan Median sebesar 3 menit 42 detik')

        elif(cluster == 'Cluster 1'):
            st.write('Durasi dari Cluster 1 kira-kira berkisar antara 2-3 menit. Ini bisa dilihat dengan Mean sebesar 2 menit 48 detik dan Median sebesar 2 menit')

        elif(cluster == 'Cluster 2'):
            st.write('Durasi dari Cluster 1 cukup lama. Ini bisa dilihat dengan Mean sebesar 3 menit 24 detik dan Median sebesar 4 menit 3 detik')

        elif(cluster == 'Cluster 3'):
            st.write('Durasi dari Cluster 3 kira-kira berkisar antara 3-4 menit. Ini bisa dilihat dengan Mean sebesar 3 menit 48 detik dan Median sebesar 3 menit 42 detik')

        elif(cluster == 'Cluster 4'):
            st.write('Durasi dari Cluster 4 cukup lama. Ini bisa dilihat dengan Mean sebesar 3 menit 48 detik dan Median sebesar 4 menit.')

        elif(cluster == 'Cluster 5'):
            st.write('Durasi dari Cluster 5 kira-kira berkisar antara 3-4 menit. Ini bisa dilihat dengan Mean sebesar 3 menit 48 detik dan Median sebesar 3 menit 36 detik.')

        elif(cluster == 'Cluster 6'):
            st.write('Durasi dari Cluster 6 kira-kira berkisar antara 3-4 menit. Ini bisa dilihat dengan Mean sebesar 3 menit dan Median sebesar 3 menit 12 detik.')
        
if(radio_cluster == 'Cluster 0'):
    df_cluster_0 = projection[
        projection['cluster'] == 0
    ]
    show_tabs(df_cluster_0, radio_cluster)

elif(radio_cluster == 'Cluster 1'):
    df_cluster_1 = projection[
        projection['cluster'] == 1
    ]
    show_tabs(df_cluster_1, radio_cluster)

elif(radio_cluster == 'Cluster 2'):
    df_cluster_2 = projection[
        projection['cluster'] == 2
    ]
    show_tabs(df_cluster_2, radio_cluster)

elif(radio_cluster == 'Cluster 3'):
    df_cluster_3 = projection[
        projection['cluster'] == 3
    ]
    show_tabs(df_cluster_3, radio_cluster)

elif(radio_cluster == 'Cluster 4'):
    df_cluster_4 = projection[
        projection['cluster'] == 4
    ]
    show_tabs(df_cluster_4, radio_cluster)

elif(radio_cluster == 'Cluster 5'):
    df_cluster_5 = projection[
        projection['cluster'] == 5
    ]
    show_tabs(df_cluster_5, radio_cluster)

elif(radio_cluster == 'Cluster 6'):
    df_cluster_6 = projection[
        projection['cluster'] == 6
    ]
    show_tabs(df_cluster_6, radio_cluster)