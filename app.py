import pickle as pkl
import pandas as pd
import streamlit as st
from helper import get_recommendations, get_genre_based_recommendation, set_png_as_page_bg

movie_dict = pkl.load(open('movie_dict.pkl', 'rb'))
cosine_sim = pkl.load(open('cosine_sim.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

# Get list of all titles
title = movies['title'].values

# List of all genres
genres = ['Adventure', 'Family', 'Drama', 'History', 'Mystery', 'Romance', 'Comedy', 'Action', 'Crime', 'Music',
          'Fantasy', 'Western', 'War',
          'Foreign', 'Thriller', 'Animation', 'TV Movie', 'Science Fiction', 'Documentary', 'Horror']

# Set background image
set_png_as_page_bg('./static/background.jpg')

# Set title
st.title("SJ's Movie Recommender")

recommend_type = st.selectbox('Select recommendation type (based on genres or movies)',
                              ['Movie based recommendation', 'Genre based recommendation'])

if recommend_type == "Movie based recommendation":
    movie_name = st.selectbox(
        'Type or select a movie from dropdown menu',
        title)
else:
    genre_name = st.selectbox('Type or select a genre from dropdown menu',
                              genres)

number_of_movies = st.slider("Select number of movies to recommend", min_value=3, max_value=10, step=1)

sort = st.checkbox("Sort movies based on rating")

if st.button('Show Recommendations'):
    if recommend_type == 'Movie based recommendation':
        movie_name_list, movie_poster_list, movie_overview_list, movie_crew_list, movie_cast_list, movie_score_list, movie_link_list = get_recommendations(
            movie_name, number_of_movies)

    else:
        movie_name_list, movie_poster_list, movie_overview_list, movie_crew_list, movie_cast_list, movie_score_list, movie_link_list = get_genre_based_recommendation(
            genre_name, number_of_movies)

    # Convert lists into dataframe
    recommended_movies = pd.DataFrame(list(
        zip(movie_name_list, movie_poster_list, movie_overview_list, movie_crew_list, movie_cast_list,
            movie_score_list,
            movie_link_list)),
        columns=['Title', 'Poster', 'Overview', 'Crew', 'Cast', 'Weighted_score', 'Link'])

    # Sort based on popularity if checkbox selected
    if sort:
        recommended_movies = recommended_movies.sort_values(by="Weighted_score", ascending=False)

    if recommend_type == 'Movie based recommendation':
        st.write("If you liked ", movie_name, " you may also like: ")
    else:
        st.write("Best ", genre_name, " movies of all time are: ")
    for i in range(1, number_of_movies + 1):
        c = st.container()
        with c:
            st.subheader(str(recommended_movies['Title'].iloc[i-1]))
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(recommended_movies['Poster'].iloc[i-1])
            with col2:
                st.write("Overview: ", recommended_movies['Overview'].iloc[i-1])
                st.write("Cast: ", ", ".join(str(e) for e in recommended_movies['Cast'].iloc[i-1]))
                st.write("Director: ", ", ".join(str(e) for e in recommended_movies['Crew'].iloc[i-1]))
                link = recommended_movies['Link'].iloc[i-1]
                st.write("To know more check out this [link](%s)" % recommended_movies['Link'].iloc[i-1])
