import streamlit as st
import pickle
import pandas as pd

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    # Sort movies based on similarity scores
    similar_movies = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
    
    recommended_movies = []
    for i in similar_movies:
        #fetch poster from API
        recommended_movies.append(movies_df.iloc[i[0]]['title'])
    return recommended_movies

movies_df = pickle.load(open('movies.pkl', 'rb'))  # This should be a DataFrame
similarity = pickle.load(open('similarity.pkl','rb'))
movies_list = movies_df['title'].values


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations',
     movies_list
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    for i in recommendations: 
       st.write(i)