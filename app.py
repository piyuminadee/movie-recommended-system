import streamlit as st
import pickle
import pandas as pd
import requests

# Fetch movie poster from TMDB API
def fetch_poster(movie_id):
    
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=d6206ea70b4705bd5ce0b4726b669362&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    # Sort movies based on similarity scores
    similar_movies = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for movie_info in similar_movies:
        # Get movie index from the tuple (index, similarity_score)
        movie_idx = movie_info[0]
       
        # Fetch the TMDB ID from the DataFrame
        movie_id = movies_df.iloc[movie_idx]['movie_id']  # Ensure column name matches your data
        recommended_movies.append(movies_df.iloc[movie_idx]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_df = pickle.load(open('movies.pkl', 'rb'))  # This should be a DataFrame
similarity = pickle.load(open('similarity.pkl','rb'))
movies_list = movies_df['title'].values


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations',
     movies_list
)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])




