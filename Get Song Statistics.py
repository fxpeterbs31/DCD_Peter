# Contents of ~/my_app/pages/page_3.py
import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt
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

# if(st.session_state.df):
df_recs_1 = st.session_state['df']

_, df_title, _ = st.columns([0.5, 4, 0.5])
with df_title:
    st.markdown('### Here are the songs recommended for you :bulb:')

_, df, _ = st.columns([0.8, 3.6, 0.8])
with df:
    st.write(df_recs_1)

def get_rec_song_details(df):
    li_song_id = []
    for i in range(len(df)):
        query = 'artist: {} track: {} year: {}'.format(df.loc[i, 'artists'], df.loc[i, 'name'], df.loc[i, 'year'])
        results = sp.search(q = query, type = 'track')
        song_id = results['tracks']['items'][0]['id']
        li_song_id.append(song_id)

    return li_song_id

li_song_id = get_rec_song_details(df_recs_1)
tes_search_song = sp.audio_features(li_song_id)

li_danceability     = []
li_energy           = []
li_key              = []
li_loudness         = []
li_mode             = []
li_speechiness      = []
li_acousticness     = []
li_instrumentalness = []
li_liveness         = []
li_valence          = []
li_tempo            = []
li_duration_ms      = []
li_time_signature   = []    

for i in range(len(tes_search_song)):
    danceability = tes_search_song[i]['danceability']
    li_danceability.append(danceability)
    
    energy = tes_search_song[i]['energy']
    li_energy.append(energy)
    
    key = tes_search_song[i]['key']
    li_key.append(key)
    
    loudness = tes_search_song[i]['loudness']
    li_loudness.append(loudness)
    
    mode = tes_search_song[i]['mode']
    li_mode.append(mode)
    
    speechiness = tes_search_song[i]['speechiness']
    li_speechiness.append(speechiness)
    
    acousticness = tes_search_song[i]['acousticness']
    li_acousticness.append(acousticness)
    
    instrumentalness = tes_search_song[i]['instrumentalness']
    li_instrumentalness.append(instrumentalness)
    
    liveness = tes_search_song[i]['liveness']
    li_liveness.append(liveness)
    
    valence = tes_search_song[i]['valence']
    li_valence.append(valence)
    
    tempo = tes_search_song[i]['tempo']
    li_tempo.append(tempo)
    
    duration_ms = tes_search_song[i]['duration_ms']
    li_duration_ms.append(duration_ms)
    
    time_signature = tes_search_song[i]['time_signature']
    li_time_signature.append(time_signature)

df_recs_audio_features = pd.DataFrame(data = {
    'danceability'     : li_danceability, 
    'energy'           : li_energy,  
    'key'              : li_key, 
    'loudness'         : li_loudness, 
    'mode'             : li_mode, 
    'speechiness'      : li_speechiness, 
    'acousticness'     : li_acousticness, 
    'instrumentalness' : li_instrumentalness, 
    'liveness'         : li_liveness, 
    'valence'          : li_valence, 
    'tempo'            : li_tempo, 
    'duration'         : li_duration_ms, 
    'time_signature'   : li_time_signature
})

df_recs_audio_features['mode'] = df_recs_audio_features['mode'].replace({
    0 : 'Minor',
    1 : 'Major'
})

df_recs_audio_features['key'] = df_recs_audio_features['key'].replace({
    0  : 'C',
    1  : 'C♯/D♭',
    2  : 'D',
    3  : 'D♯/E♭',
    4  : 'E',
    5  : 'F',
    6  : 'F♯/G♭',
    7  : 'G',
    8  : 'G♯/A♭',
    9  : 'A',
    10 : 'A♯/B♭',
    11 : 'B'
})

df_recs_audio_features['time_signature'] = df_recs_audio_features['time_signature'].replace({
    3 : '3/4',
    4 : '4/4',
    5 : '5/4',
    6 : '6/4',
    7 : '7/4'
})

df_recs_audio_features[['key', 'mode', 'time_signature']] = \
    df_recs_audio_features[['key', 'mode', 'time_signature']].astype('category')

if 'button_clicked_2' not in st.session_state:
    st.session_state['button_clicked_2'] = False

def callback_2():
    st.session_state.button_clicked_2 = True

if(st.button('Show Stats', on_click = callback_2) or st.session_state.button_clicked_2):
    choose_radio = st.radio('Choose Parameter Types', ['Numeric', 'Categoric'], horizontal = True)
        
    def show_tabs_num():
        params_num = [
            'danceability', 'energy',
            'loudness', 'speechiness', 
            'acousticness', 'instrumentalness', 
            'liveness', 'valence', 
            'tempo', 'duration'
        ]

        params_title = [x.title() for x in params_num]

        df_recs_audio_features['duration'] = df_recs_audio_features['duration'] / 60000
        df_recs_audio_features_stats = df_recs_audio_features[params_num].describe()
        df_recs_audio_features_stats_small = df_recs_audio_features_stats.loc[['mean', '50%'], :]
        df_recs_audio_features_stats_small = df_recs_audio_features_stats_small.T.rename(columns = {
            'mean' : 'Mean',
            '50%' : 'Median'
        }).T

        df_danceability     = df_recs_audio_features_stats_small['danceability']
        df_energy           = df_recs_audio_features_stats_small['energy']
        df_loudness         = df_recs_audio_features_stats_small['loudness']
        df_speechiness      = df_recs_audio_features_stats_small['speechiness']
        df_acousticness     = df_recs_audio_features_stats_small['acousticness']
        df_instrumentalness = df_recs_audio_features_stats_small['instrumentalness']
        df_liveness         = df_recs_audio_features_stats_small['liveness']
        df_valence          = df_recs_audio_features_stats_small['valence']
        df_tempo            = df_recs_audio_features_stats_small['tempo']
        df_duration_ms      = df_recs_audio_features_stats_small['duration']

        tab_1, tab_2, tab_3, tab_4, tab_5, tab_6, tab_7, tab_8, tab_9, tab_10 = st.tabs(params_title)

        with tab_1:
            df_danceability.plot.bar(rot = 0)
            plt.title('Danceability')
            plt.ylim([0,1])
            plt.ylabel('')
            st.pyplot()

            mean = df_danceability.loc['Mean']
            median = df_danceability.loc['Median']

            if(mean <= 0.2 and median <= 0.2):
                verdict = 'Rendah'

            elif((mean > 0.2 and mean <= 0.4) and (median > 0.2 and median <= 0.4)):
                verdict = 'Cukup Rendah'

            elif((mean > 0.4 and mean <= 0.48) and (median > 0.4 and median <= 0.48)):
                verdict = 'Abu-abu, namun mengarah ke tidak cocok untuk diberikan tarian / koreografi'

            elif((mean > 0.48 and mean <= 0.53) and (median > 0.48 and median <= 0.53)):
                verdict = 'Abu-abu, namun tidak bisa diambil kesimpulan apakah cocok atau tidak cocok untuk diberikan tarian / koreografi'

            elif((mean > 0.53 and mean <= 0.6) and (median > 0.53 and median <= 0.6)):
                verdict = 'Abu-abu, namun mengarah ke cocok untuk diberikan tarian / koreografi'

            elif((mean > 0.6 and mean <= 0.8) and (median > 0.6 and median <= 0.8)):
                verdict = 'Cukup Tinggi'

            elif(mean > 0.8 and median > 0.8):
                verdict = 'Tinggi'

            else:
                if(mean < 0.5 and median < 0.5):
                    verdict = 'Cukup Rendah'
                elif(mean >= 0.5 and median >= 0.5):
                    verdict = 'Cukup Tinggi'
                else:
                    verdict = 'Abu-abu'

            st.write('Danceability: {}'.format(verdict))

        with tab_2:
            df_energy.plot.bar(rot = 0)
            plt.title('Energy')
            plt.ylim([0,1])
            plt.ylabel('')
            st.pyplot()

            mean = df_energy.loc['Mean']
            median = df_energy.loc['Median']

            if(mean <= 0.2 and median <= 0.2):
                verdict = 'Rendah'

            elif((mean > 0.2 and mean <= 0.4) and (median > 0.2 and median <= 0.4)):
                verdict = 'Cukup Rendah'

            elif((mean > 0.4 and mean <= 0.48) and (median > 0.4 and median <= 0.48)):
                verdict = 'Abu-abu, namun mengarah ke low energy'

            elif((mean > 0.48 and mean <= 0.53) and (median > 0.48 and median <= 0.53)):
                verdict = 'Abu-abu, namun tidak bisa diambil kesimpulan apakah high atau low energy'

            elif((mean > 0.53 and mean <= 0.6) and (median > 0.53 and median <= 0.6)):
                verdict = 'Abu-abu, namun mengarah ke high energy'

            elif((mean > 0.6 and mean <= 0.8) and (median > 0.6 and median <= 0.8)):
                verdict = 'Cukup Tinggi'

            elif(mean > 0.8 and median > 0.8):
                verdict = 'Tinggi'

            else:
                if(mean < 0.5 and median < 0.5):
                    verdict = 'Cukup Rendah'
                elif(mean >= 0.5 and median >= 0.5):
                    verdict = 'Cukup Tinggi'
                else:
                    verdict = 'Abu-abu'

            st.write('Energy: {}'.format(verdict))

        with tab_3:
            df_loudness.plot.bar(rot = 0)
            plt.title('Loudness')
            plt.ylim([-60,0])
            plt.ylabel('Decibel (dB)')
            st.pyplot()

            mean = df_loudness.loc['Mean']
            median = df_loudness.loc['Median']

            if(mean <= -50 and median <= -50):
                verdict = 'Sangat Rendah'

            elif((mean > -50 and mean <= -40) and (median > -50 and median <= -40)):
                verdict = 'Rendah'

            elif((mean > -40 and mean <= -30) and (median > -40 and median <= -30)):
                verdict = 'Abu-abu, namun mengarah ke volume rendah'

            elif((mean > -30 and mean <= -25) and (median > -30 and median <= -25)):
                verdict = 'Abu-abu, namun tidak bisa diambil kesimpulan apakah volume tinggi atau rendah'

            elif((mean > -25 and mean <= -20) and (median > -25 and median <= -20)):
                verdict = 'Abu-abu, namun mengarah ke volume tinggi'

            elif((mean > -20 and mean <= -10) and (median > -20 and median <= -10)):
                verdict = 'Cukup Tinggi'

            elif(mean > -10 and median > -10):
                verdict = 'Tinggi'

            else:
                if(mean < 0.5 and median < 0.5):
                    verdict = 'Cukup Rendah'
                elif(mean >= 0.5 and median >= 0.5):
                    verdict = 'Cukup Tinggi'
                else:
                    verdict = 'Abu-abu'

            st.write('Loudness: {}'.format(verdict))

        with tab_4:
            df_speechiness.plot.bar(rot = 0)
            plt.title('Speechiness')
            plt.ylim([0,1])
            plt.ylabel('')
            st.pyplot()

            mean = df_speechiness.loc['Mean']
            median = df_speechiness.loc['Median']

            if(mean <= 0.33 and median <= 0.33):
                verdict = 'Vokal dengan sedikit lagu'

            elif((mean > 0.33 and mean <= 0.66) and (median > 0.33 and median <= 0.66)):
                verdict = 'Lagu dan vokal berimbang'

            elif(mean > 0.66 and median > 0.66):
                verdict = 'Lagu dengan sedikit vokal'

            st.write('Speechiness: {}'.format(verdict))

        with tab_5:
            df_acousticness.plot.bar(rot = 0)
            plt.title('Acousticness')
            plt.ylim([0,1])
            plt.ylabel('')
            st.pyplot()

            mean = df_acousticness.loc['Mean']
            median = df_acousticness.loc['Median']

            if(mean <= 0.2 and median <= 0.2):
                verdict = 'Rendah'

            elif((mean > 0.2 and mean <= 0.4) and (median > 0.2 and median <= 0.4)):
                verdict = 'Cukup Rendah'

            elif((mean > 0.4 and mean <= 0.48) and (median > 0.4 and median <= 0.48)):
                verdict = 'Abu-abu, namun mengarah ke bukan acoustic'

            elif((mean > 0.48 and mean <= 0.53) and (median > 0.48 and median <= 0.53)):
                verdict = 'Abu-abu, namun tidak bisa diambil kesimpulan apakah acoustic atau bukan acoustic'

            elif((mean > 0.53 and mean <= 0.6) and (median > 0.53 and median <= 0.6)):
                verdict = 'Abu-abu, namun mengarah ke acoustic'

            elif((mean > 0.6 and mean <= 0.8) and (median > 0.6 and median <= 0.8)):
                verdict = 'Cukup Tinggi'

            elif(mean > 0.8 and median > 0.8):
                verdict = 'Tinggi'

            else:
                if(mean < 0.5 and median < 0.5):
                    verdict = 'Cukup Rendah'
                elif(mean >= 0.5 and median >= 0.5):
                    verdict = 'Cukup Tinggi'
                else:
                    verdict = 'Abu-abu'

            st.write('Acousticness: {}'.format(verdict))

        with tab_6:
            df_instrumentalness.plot.bar(rot = 0)
            plt.title('Instrumentalness')
            plt.ylim([0,1])
            plt.ylabel('')
            st.pyplot()

            mean = df_instrumentalness.loc['Mean']
            median = df_instrumentalness.loc['Median']

            if(mean <= 0.2 and median <= 0.2):
                verdict = 'Rendah'

            elif((mean > 0.2 and mean <= 0.4) and (median > 0.2 and median <= 0.4)):
                verdict = 'Cukup Rendah'

            elif((mean > 0.4 and mean <= 0.48) and (median > 0.4 and median <= 0.48)):
                verdict = 'Abu-abu, namun mengarah ke non-instrumental'

            elif((mean > 0.48 and mean <= 0.53) and (median > 0.48 and median <= 0.53)):
                verdict = 'Abu-abu, namun tidak bisa diambil kesimpulan apakah instrumental atau non instrumental'

            elif((mean > 0.53 and mean <= 0.6) and (median > 0.53 and median <= 0.6)):
                verdict = 'Abu-abu, namun mengarah ke instrumental'

            elif((mean > 0.6 and mean <= 0.8) and (median > 0.6 and median <= 0.8)):
                verdict = 'Cukup Tinggi'

            elif(mean > 0.8 and median > 0.8):
                verdict = 'Tinggi'

            else:
                if(mean < 0.5 and median < 0.5):
                    verdict = 'Cukup Rendah'
                elif(mean >= 0.5 and median >= 0.5):
                    verdict = 'Cukup Tinggi'
                else:
                    verdict = 'Abu-abu'

            st.write('Instrumentalness: {}'.format(verdict))

        with tab_7:
            df_liveness.plot.bar(rot = 0)
            plt.title('Liveness')
            plt.ylim([0,1])
            plt.ylabel('')
            st.pyplot()

            mean = df_liveness.loc['Mean']
            median = df_liveness.loc['Median']

            if(mean <= 0.2 and median <= 0.2):
                verdict = 'Rendah'

            elif((mean > 0.2 and mean <= 0.4) and (median > 0.2 and median <= 0.4)):
                verdict = 'Cukup Rendah'

            elif((mean > 0.4 and mean <= 0.48) and (median > 0.4 and median <= 0.48)):
                verdict = 'Abu-abu, namun mengarah ke track direkam di studio'

            elif((mean > 0.48 and mean <= 0.53) and (median > 0.48 and median <= 0.53)):
                verdict = 'Abu-abu, namun tidak bisa diambil kesimpulan apakahtrack direkam di studio atau tidak'

            elif((mean > 0.53 and mean <= 0.6) and (median > 0.53 and median <= 0.6)):
                verdict = 'Abu-abu, namun mengarah ke track direkam tidak di studio'

            elif((mean > 0.6 and mean <= 0.8) and (median > 0.6 and median <= 0.8)):
                verdict = 'Cukup Tinggi'

            elif(mean > 0.8 and median > 0.8):
                verdict = 'Tinggi'

            else:
                if(mean < 0.5 and median < 0.5):
                    verdict = 'Cukup Rendah'
                elif(mean >= 0.5 and median >= 0.5):
                    verdict = 'Cukup Tinggi'
                else:
                    verdict = 'Abu-abu'

            st.write('Liveness: {}'.format(verdict))

        with tab_8:
            df_valence.plot.bar(rot = 0)
            plt.title('Valence')
            plt.ylim([0,1])
            plt.ylabel('')
            st.pyplot()

            mean = df_valence.loc['Mean']
            median = df_valence.loc['Median']

            if(mean <= 0.2 and median <= 0.2):
                verdict = 'Suasana Negatif'

            elif((mean > 0.2 and mean <= 0.4) and (median > 0.2 and median <= 0.4)):
                verdict = 'Suasana Cukup Negatif'

            elif((mean > 0.4 and mean <= 0.48) and (median > 0.4 and median <= 0.48)):
                verdict = 'Abu-abu, namun mengarah ke suasana negatif'

            elif((mean > 0.48 and mean <= 0.53) and (median > 0.48 and median <= 0.53)):
                verdict = 'Abu-abu, namun tidak bisa diambil kesimpulan apakah suasana positif atau negatif'

            elif((mean > 0.53 and mean <= 0.6) and (median > 0.53 and median <= 0.6)):
                verdict = 'Abu-abu, namun mengarah ke suasana positif'

            elif((mean > 0.6 and mean <= 0.8) and (median > 0.6 and median <= 0.8)):
                verdict = 'Suasana Cukup Positif'

            elif(mean > 0.8 and median > 0.8):
                verdict = 'Suasana Positif'

            else:
                if(mean < 0.5 and median < 0.5):
                    verdict = 'Suasana Cukup Negatif'
                elif(mean >= 0.5 and median >= 0.5):
                    verdict = 'Suasana Cukup Positif'
                else:
                    verdict = 'Suasana Abu-abu'

            st.write('Valence: {}'.format(verdict))

        with tab_9:
            df_tempo.plot.bar(rot = 0)
            plt.title('Tempo')
            plt.ylim([0,300])
            plt.ylabel('Beat per Minute (bpm)')
            st.pyplot()

            mean = df_tempo.loc['Mean']
            median = df_tempo.loc['Median']

            if(mean <= 20 and median <= 20):
                verdict = 'Larghissimo (Lambat)'

            elif((mean > 20 and mean <= 40) and (median > 20 and median <= 40)):
                verdict = 'Grave (Lambat)'

            elif((mean > 40 and mean <= 60) and (median > 40 and median <= 60)):
                verdict = 'Lento (Lambat)'

            elif((mean > 60 and mean <= 66) and (median > 60 and median <= 66)):
                verdict = 'Larghetto (Lambat)'

            elif((mean > 66 and mean <= 76) and (median > 66 and median <= 76)):
                verdict = 'Adagio (Lambat)'

            elif((mean > 76 and mean <= 108) and (median > 76 and median <= 108)):
                verdict = 'Andante (Sedang)'

            elif((mean > 108 and mean <= 120) and (median > 108 and median <= 120)):
                verdict = 'Moderato (Sedang)'

            elif((mean > 120 and mean <= 168) and (median > 120 and median <= 168)):
                verdict = 'Allegro (Cepat)'

            elif((mean > 168 and mean <= 176) and (median > 168 and median <= 176)):
                verdict = 'Vivace (Cepat)'

            elif((mean > 176 and mean <= 200) and (median > 176 and median <= 200)):
                verdict = 'Presto (Sangat Cepat)'

            elif(mean > 200 and median > 200):
                verdict = 'Prestissimo (Sangat Sangat Cepat)'

            else:
                if(mean <= 76 and median <= 76):
                    verdict = 'Lambat'
                elif((mean > 76 and mean <= 120) and (median > 76 and median <= 120)):
                    verdict = 'Sedang'
                elif((mean > 120 and mean <= 168) and (median > 120 and median <= 168)):
                    verdict = 'Cepat',
                elif((mean > 168 and mean <= 176) and (median > 168 and median <= 176)):
                    verdict = 'Sangat Cepat'
                else:
                    verdict = 'Tidak dapat ditentukan'

            st.write('Tempo: {}'.format(verdict))

        with tab_10:
            df_duration_ms.plot.bar(rot = 0)
            plt.title('Duration')
            plt.ylim([0,5])
            plt.ylabel('Minutes (m)')
            st.pyplot()

            mean = df_duration_ms.loc['Mean']
            median = df_duration_ms.loc['Median']

            if(mean <= 2.5 and median <= 2.5):
                verdict = 'Sangat Cepat'
            elif((mean > 2.5 and mean <= 3) and (median > 2.5 and median <= 3)):
                verdict = 'Cepat'
            elif((mean > 3 and mean <= 4.5) and (median > 3 and median <= 3.5)):
                verdict = 'Sedang'  
            elif((mean > 3.5 and mean <= 4.5) and (median > 3.5 and median <= 4.5)):
                verdict = 'Lama'
            elif(mean > 4.5 and median > 4.5):
                verdict = 'Sangat Lama'
            else:
                if(mean < 3.5 and median < 3.5):
                    verdict = 'Cukup Cepat'
                elif(mean >= 3.5 and median >= 3.5):
                    verdict = 'Cukup Lama'
                else:
                    verdict = 'Tidak dapat Disimpulkan'

            st.write('Duration: {}'.format(verdict))

    if(choose_radio == 'Numeric'):
        show_tabs_num()

    elif(choose_radio == 'Categoric'):
        params_cat = ['key', 'mode', 'time_signature']
        check_cat = []

        params_cat_title = ['Key', 'Mode', 'Time Signature']

        df_key            = pd.DataFrame(df_recs_audio_features[params_cat[0]].value_counts())
        df_mode           = pd.DataFrame(df_recs_audio_features[params_cat[1]].value_counts())
        df_time_signature = pd.DataFrame(df_recs_audio_features[params_cat[2]].value_counts())

        tab_1, tab_2, tab_3 = st.tabs(params_cat_title)

        with tab_1:
            st.write(df_key)
            df_key.plot.bar(rot = 0)
            plt.title(params_cat_title[0])
            st.pyplot()

            df_max = df_key[
                df_key['key'] == df_key['key'].max()
            ].reset_index()

            if(df_max.shape[0] == 1):
                modus = df_max.iloc[0,0]

            else:
                for i in range(len(df_max)):
                    mod = df_max.iloc[i, 0]

                    if(i == len(df_max)):
                        modus = mod + ''
                    else:
                        modus = mod + ', '

            st.write('Key: {}'.format(modus))

        with tab_2:
            df_mode.plot.bar(rot = 0)
            plt.title(params_cat_title[1])
            st.pyplot()

            df_max = df_mode[
                df_mode['mode'] == df_mode['mode'].max()
            ].reset_index()

            if(df_max.shape[0] == 1):
                modus = df_max.iloc[0,0]

            else:
                modus = df_max.iloc[0,0] + ' and ' + df_max.iloc[1,0]

            st.write('Mode: {}'.format(modus))

        with tab_3:
            st.write(df_time_signature)
            df_time_signature.plot.bar(rot = 0)
            plt.title(params_cat_title[2])
            st.pyplot()

            df_max = df_time_signature[
                df_time_signature['time_signature'] == df_time_signature['time_signature'].max()
            ].reset_index()

            if(df_max.shape[0] == 1):
                modus = df_max.iloc[0,0]

            else:
                for i in range(len(df_max)):
                    mod = df_max.iloc[i, 0]

                    if(i == len(df_max)):
                        modus = mod + ''
                    else:
                        modus = mod + ', '

            st.write('Time Signature: {}'.format(modus))


        # st.write('Categoric Parameters') 
        # check_key            = st.checkbox('Key')
        # check_cat.append(check_key)
        
        # check_mode           = st.checkbox('Mode')
        # check_cat.append(check_mode)
        
        # check_time_signature = st.checkbox('Time Signature')
        # check_cat.append(check_time_signature)

        # df_cat = pd.DataFrame(data = {
        #     'params' : params_cat,
        #     'value' : check_cat
        # })

        # df_cat['value'] = df_cat['value'].replace({
        #     True : 1,
        #     False : 0
        # })

        # # plots
        # cat_true = df_cat[df_cat['value'] == 1]                
        # st.write('\n\n')
        
        # if(cat_true.shape[0] == 1):
        #     col_1, df_1 = generate_df_to_plot_cat(cat_true, cat_true.shape[0])  
        #     ax = df_1.plot.bar(rot = 0)

        #     st.write(col_1)
        #     st.pyplot(ax.figure)

        # elif(cat_true.shape[0] == 2):
        #     col_1, col_2 = st.columns(2)

        #     cols, dfs = generate_df_to_plot_cat(cat_true, cat_true.shape[0])

        #     col_name_1 = cols[0]
        #     col_name_2 = cols[1]

        #     df_1 = dfs[0]
        #     df_2 = dfs[1]

        #     with col_1:
        #         ax = df_1.plot.bar(rot = 0)

        #         st.write(col_name_1)
        #         st.pyplot(ax.figure)

        #     with col_2:
        #         ax = df_2.plot.bar(rot = 0)

        #         st.write(col_name_2)
        #         st.pyplot(ax.figure)

        # elif(cat_true.shape[0] == 3):
        #     col_1, col_2, col_3 = st.columns(3)

        #     cols, dfs = generate_df_to_plot_cat(cat_true, cat_true.shape[0])

        #     col_name_1 = cols[0]
        #     col_name_2 = cols[1]
        #     col_name_3 = cols[2]

        #     df_1 = dfs[0]
        #     df_2 = dfs[1]
        #     df_3 = dfs[2]

        #     with col_1:
        #         ax = df_1.plot.bar(rot = 0)

        #         st.write(col_name_1)
        #         st.pyplot(ax.figure)

        #     with col_2:
        #         ax = df_2.plot.bar(rot = 0)

        #         st.write(col_name_2)
        #         st.pyplot(ax.figure)

        #     with col_3:
        #         ax = df_3.plot.bar(rot = 0)

        #         st.write(col_name_3)
        #         st.pyplot(ax.figure)

        # check_cat = []
# else:
#     st.markdown('## Please Enter the Song Details at the **Get Song Recommendations** page')