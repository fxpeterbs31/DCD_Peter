# Contents of ~/my_app/main_page.py
import streamlit as st
from PIL import Image

def main():
    img = Image.open('D:/Algoritma/DCD/DCD/spotify_logo.png')
    st.sidebar.image(img)

    st.markdown('# Spotify Recommender System Using Cosine Distance')
    st.markdown("## Overview :house:")

    st.markdown('### What is This Application?')
    st.write(
        'This app is a Spotify Recommender System App. This app gives you a number of songs based on your preference based on the song(s) you will input. You can also view the stats from the dataset used to recommend songs and your personalized recommended songs. '
    )

    st.markdown('### How To Use This App')
    st.write('This app has 4 pages. ')

    st.markdown('#### 1. Home')
    st.write(
        'This page gives you an overview of the app and the link to the github repository of this project.'
    )

    st.markdown('#### 2. Get Cluster Analysis')
    st.write(
        'This page gives you the process of Clustering based on the dataset songs and the analysis of each cluster.'
    )

    st.markdown('#### 3. Get Song Recommendations')
    st.write(
        'This page is the input page. You will input the songs you want to check to get your personalized recommended songs. It is mandatory to fill 2 of the 3 blanks in the song details, with song name being the mandatory of the 2. If possible, you can insert all 3 blanks. If you cannot fill all 3 blanks, it is recommended to fill the song name and the song year blanks. '
    )

    st.markdown('#### 4. Get Song Statistics')
    st.write(
        'This page will give you the statistics of the songs recommended to you. Keep in mind that you will be able to use this page if you have completed all processes in the **Get Song Recommendations** page.'
    )


    st.markdown('#### Link Github: ')

if __name__ == '__main__':
    main()