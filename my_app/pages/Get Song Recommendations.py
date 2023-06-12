import streamlit as st
import pandas as pd
import plotly.express as px 
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from collections import defaultdict
from sklearn.metrics import euclidean_distances
from scipy.spatial.distance import cdist
import difflib

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict

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

_, title, _ = st.columns([0.25, 4.5, 0.25])
with title:
    st.markdown('# Get Song Recommendations :musical_note:')

st.write('\n\n\n')

songs = pd.read_csv('D:/Algoritma/DCD/DCD/data_new/data.csv')
min_year = songs['year'].min()
max_year = songs['year'].max()

st.markdown('### Please Enter the number of songs you want to check')

number_of_songs = st.number_input(
    label = 'Enter number of songs you want to insert: ',
    min_value = 1,
    value = 1,
    format = '%d'
)

if(int(number_of_songs) == 1):
    st.write('You choose to enter {} song'.format(int(number_of_songs)))
else:    
    st.write('You choose to enter {} songs'.format(int(number_of_songs)))

st.write('\n')

li_song_name    = []
li_artist_name  = []
li_release_year = []

st.markdown('### Please enter the song details')

for i in range(int(number_of_songs)):
    inp_1, inp_2, inp_3 = st.columns(3)

    with inp_1:
        song_name = st.text_input('Enter the song name', key = 'song_name_{}'.format(i+1))
    with inp_2:
        release_year = st.number_input(
            label = 'Enter the release year of the song: ',
            min_value = 0,
            value = 0,
            format = '%d',
            key = 'release_year_{}'.format(i+1)
        )
    with inp_3:
        artist_name = st.text_input('Enter the artist(s) name', key = 'artist_name_{}'.format(i+1))

    li_song_name.append(song_name)    
    li_artist_name.append(artist_name)
    li_release_year.append(release_year)

    song_name    = ''
    artist_name  = ''
    release_year = 0

df_songs_to_rec = pd.DataFrame(data = {
    'name' : li_song_name,
    'year' : li_release_year,
    'artists' : li_artist_name
})

st.write('\n')
st.markdown('### Please enter the year range')
col_1, col_2 = st.columns((5,5))

with col_1:
    start_year = st.number_input(
        label = 'Start Year',
        min_value = min_year,
        max_value = max_year,
        value = 1921,
        format = '%d'
    )

with col_2:
    end_year = st.number_input(
        label = 'End Year',
        min_value = min_year,
        max_value = max_year,
        value = 2020,
        format = '%d'
    )

small_song_df = songs[
    (songs['year'] >= start_year) & 
    (songs['year'] <= end_year)
]

song_cluster_pipeline = Pipeline([('scaler', StandardScaler()), 
                                  ('kmeans', KMeans(n_clusters=7, 
                                   verbose=False))
                                 ], verbose=False)

X = small_song_df.select_dtypes(np.number)
number_cols = list(X.columns)
song_cluster_pipeline.fit(X)
song_cluster_labels = song_cluster_pipeline.predict(X)
small_song_df['cluster_label'] = song_cluster_labels

def find_song(name, year, artist):
    song_data = defaultdict()
    
    if(name != '' and year != '' and artist != ''):
        query = 'artist: {} track: {} year: {}'.format(artist, name, year)
    
    elif(name != '' and year != '' and artist == ''):
        query = 'track: {} year: {}'.format(name, year)

    elif(name != '' and year == '' and artist != ''):
        query = 'artist: {} track: {}'.format(artist, name)
        
    elif(name == ''):
        return -1

    results = sp.search(q = query, type = 'track')
    if results['tracks']['items'] == []:
        return 0

    results = results['tracks']['items'][0]
    track_id = results['id']
    artist = results['artists'][0]['name']
    audio_features = sp.audio_features(track_id)[0]

    song_data['name'] = [name]
    song_data['year'] = [year]
    song_data['artist'] = [artist]
    song_data['explicit'] = [int(results['explicit'])]
    song_data['duration_ms'] = [results['duration_ms']]
    song_data['popularity'] = [results['popularity']]

    for key, value in audio_features.items():
        song_data[key] = value

    return pd.DataFrame(song_data)

number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit',
 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']

def get_song_data(song, spotify_data):
    if('artists' in song.keys() and 'year' not in song.keys()):
        song['year'] = 0
    elif('artists' not in song.keys() and 'year' in song.keys()):
        song['artists'] = ''

    if('name' not in song.keys()):
        song['name'] = ''

    try:
        song_data = spotify_data[
            (spotify_data['name'] == song['name']) & 
            ((spotify_data['year'] == song['year']) | 
            (spotify_data['artists'] == song['artists']))
        ].iloc[0]
        return song_data
    
    except IndexError:
        check_song = find_song(song['name'], song['year'], song['artists'])
        return check_song       

def get_mean_vector(song_list, spotify_data):    
    song_vectors = []
    
    for song in song_list:
        song_data = get_song_data(song, spotify_data)

        if(isinstance(song_data, int)):
            if song_data == 0:
                st.write('Warning: {} does not exist in Spotify or in database'.format(song['name']))
                continue
            
            elif song_data == -1:
                return None
        
        song_vector = song_data[number_cols].values
        song_vectors.append(song_vector)  
    
    song_matrix = np.array(list(song_vectors))
    return np.mean(song_matrix, axis=0)

def flatten_dict_list(dict_list):    
    flattened_dict = defaultdict()
    for key in dict_list[0].keys():
        flattened_dict[key] = []
    
    for dictionary in dict_list:
        for key, value in dictionary.items():
            flattened_dict[key].append(value)
            
    return flattened_dict

def recommend_songs(song_list, spotify_data, n_songs):
    metadata_cols = ['name', 'year', 'artists']
    song_dict = flatten_dict_list(song_list)
    song_center = get_mean_vector(song_list, spotify_data)
    if(song_center is None):
        return -1

    scaler = song_cluster_pipeline.steps[0][1]
    scaled_data = scaler.transform(spotify_data[number_cols])
    scaled_song_center = scaler.transform(song_center.reshape(1, -1))
    distances = cdist(scaled_song_center, scaled_data, 'cosine')
    index = list(np.argsort(distances)[:, :n_songs][0])
    
    rec_songs = spotify_data.iloc[index]
    rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
    
    return rec_songs[metadata_cols].to_dict(orient='records')

st.write('\n')
st.markdown('### Please enter number of recommended songs')

if(df_songs_to_rec[df_songs_to_rec['name'] == ''].shape[0] == 0):
    number_of_recs = st.number_input(
        label = 'Enter the number songs you want to be recommended: ',
        min_value = 0,
        value = 10,
        format = '%d'
    )

    recs_inp = recommend_songs(
        song_list    = df_songs_to_rec.to_dict('records'),
        spotify_data = small_song_df,
        n_songs      = number_of_recs
    )

    df_recs_1 = pd.DataFrame.from_dict(recs_inp)

    df_recs_1['year'] = df_recs_1['year'].astype(str)
    
    df_recs_1['artists'] = df_recs_1['artists'].str.replace("'", "").str.replace('[', '').str.replace(']', '')
    # df_recs_1.index = np.arange(1, len(df_recs_1) + 1)

    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False

    def callback():
        st.session_state.button_clicked = True

    if(st.button('Show Results', on_click = callback) or st.session_state.button_clicked):
        st.write('\n\n\n')
        _, df_title, _ = st.columns([0.5, 2.55, 0.5])
        with df_title:
            st.markdown('## Songs recommended for you :musical_note:'.format(number_of_recs))
        _, df, _ = st.columns([1,3,1])
        with df:
            
            st.write(df_recs_1)

    if 'df' not in st.session_state:
        st.session_state['df'] = df_recs_1

else:
    st.write('Please insert the remaining blank song title box')