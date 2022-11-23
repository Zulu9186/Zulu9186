import pandas as pd
import streamlit as st



# Data import
system = pd.read_csv('/Users/brunocatel/WCS/Project 2/system2.csv')
#df = pd.read_csv('/Users/brunocatel/WCS/Project 2/df_base_frenchie.csv')
#df.drop(columns=['Unnamed: 0'], inplace=True)
#df['newRating'] = (df['numVotes']/(df['numVotes']+25000)) * df['averageRating'] + (25000/(df['numVotes']+25000))* 6.12
#df = df.sort_values('newRating', ascending=False)
#df = df.iloc[0:10000,:]

# Scrapping

import requests
from bs4 import BeautifulSoup as Soup

def get_url(num):

    url = 'https://www.imdb.com/title/' + num
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'})
    soup_data = Soup(page.content, 'html.parser')
    image = soup_data.find('div', {'class': "ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img"})
    lien = image.img['src']
    return lien

def synopsis (num):
    url = 'https://www.imdb.com/title/' + num
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'})
    soup_data2 = Soup(page.content, 'html.parser')
    synopsis = soup_data2.find('p', {'class': "sc-16ede01-6 cXGXRR"})
    synopsis = synopsis.span.text
    return synopsis

# System recommandation preparation
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

cv = CountVectorizer(max_features = 10000)
vectors = cv.fit_transform(system['keys']).toarray()
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)


def recommand(movie):
    movie_index = system[system['primaryTitle'] == movie].index[0]
    distances = similarity[movie_index]
    movie_liste = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:number+1]

    for i in movie_liste:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"{system.iloc[i[0]].primaryTitle} ({system.iloc[i[0]].startYear})")
            st.caption(f"French title : {system.iloc[i[0]].title}")
            st.image(get_url(system.iloc[i[0]].tconst))
            

        with col2:
            st.write(f"Actors : {system.iloc[i[0]].primaryName}")
            st.write(f"Director : {system.iloc[i[0]].directors}")
            st.write(f"Writer : {system.iloc[i[0]].writers}")
            st.write(f"Rating : {system.iloc[i[0]].averageRating}")
            st.write(f"Synopsis : {synopsis(system.iloc[i[0]].tconst)}")



# Display

st.title('IMDb : Recommandation de films')

## Research mod

with st.form(key='Recommandation'):
    #st.image('/Users/brunocatel/Downloads/IMDB.png', width=600)
    nav1, nav2, nav3= st.columns([2, 1, 1])
    with nav1:
        type1 = st.multiselect("Type the name of your favorite movie ", options=system['primaryTitle'], help='hello',
                               label_visibility="visible")
    with nav2:
        number = st.slider(label= 'Combien de recommandation(s) ?', min_value=1, max_value=10)
    with nav3:
        st.text('')
        submit = st.form_submit_button(label='Recherche')

## Resultats

    if submit:

        tab1, tab2 = st.tabs(["Informations", "Recommandations"])
        with tab1:
            filt_movie = system['primaryTitle'] == ''.join(type1)
            st.subheader(f"{''.join(type1)} ({system.loc[filt_movie, 'startYear'].values[0]})")
            st.caption(f"French title : {system.loc[filt_movie, 'title'].values[0]}")
            col1, col2 = st.columns(2)
            with col1:
                #st.success(f"Informations sur le film  {''.join(type1)} : ", icon="✅")
                filt_movie = system['primaryTitle'] == ''.join(type1)
                tconst = system.loc[filt_movie, 'tconst'].values[0]
                st.image(get_url(tconst))
                #st.write(f"French title : {system.loc[filt_movie, 'title'].values[0]}")

            with col2:
                st.write(f"Actors : {system.loc[filt_movie, 'primaryName'].values[0]}")
                st.write(f"Director : {system.loc[filt_movie, 'directors'].values[0]}")
                st.write(f"Writer : {system.loc[filt_movie, 'writers'].values[0]}")
                st.write(f"Rating : {system.loc[filt_movie, 'averageRating'].values[0]}")
                st.write(f"Synopsis : {synopsis(tconst)}")


        with tab2:
            #filt_movie = system['primaryTitle'] == ''.join(type1)
            # st.success(f"Recommandations de films similaires à {''.join(type1)} : ", icon="✅")
            st.write(recommand(''.join(type1)))
            #st.image(image)

