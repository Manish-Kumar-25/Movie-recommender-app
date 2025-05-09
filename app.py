import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = f"http://www.omdbapi.com/?i={movie_id}&apikey=48824946"
    response = requests.get(url)
    data = response.json()
    return data.get('Poster') or "https://via.placeholder.com/200x300?text=No+Image"
st.title("Movie Recommender System")
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
selected_movie_name = st.selectbox("Select a movie you like:", movies['title'].values)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(len(names))
    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(posters[i])
