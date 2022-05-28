import pickle as pkl
import pandas as pd
import requests
import streamlit as st
import base64

movie_dict = pkl.load(open('movie_dict.pkl', 'rb'))
cosine_sim = pkl.load(open('cosine_sim.pkl', 'rb'))
movies_genres = pkl.load(open('movies_genres.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

#Set background image
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
.stApp {
  background-image: url("data:image/png;base64,%s");
  background-size: cover;
}
</style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


# Function to fetch moive poster using tmdb API
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=<<api_key>>&language=en-US".format(
        movie_id)
    data = requests.get(url)

    # Check if status is 200 or throw error
    if data.ok:
        data = data.json()
        poster_path = data["poster_path"]

        # Check if movie poster path is empty
        try:
            full_path = 'https://image.tmdb.org/t/p/w500/' + poster_path
        except Exception:
            full_path = './static/movie_icon_default.jpg'
        return full_path
    else:
        st.write("Oops! Something went wrong in fetching movie poster. Please try again.")
        with st.expander("Click to see error details: "):
            st.write(err)


# Function to fetch movie details
def fetch_movie_details(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=<<api_key>>&language=en-US".format(
            movie_id)
        data = requests.get(url)

        # Raise error if exception in calling API
        data.raise_for_status()
        data = data.json()

        # Fetching overview and popularity score of movie
        overview = data["overview"]
        if overview == "":
            overview = "Overview not available."
        return overview
    except Exception as err:
        st.write("Oops! Something went wrong in fetching movie details. Please try again.")
        with st.expander("Click to see error details: "):
            st.write(err)


# Function to fetch cast and crew of movie
def fetch_movie_cast_crew(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}/credits?api_key=<<api_key>>&language=en-US".format(
            movie_id)
        data = requests.get(url)
        data.raise_for_status()
        data = data.json()
        cast = data["cast"]

        # Taking top 3 actors in movie
        cast_list = []
        j = 0
        for i in cast:
            if i["known_for_department"] == "Acting":
                cast_list.append(i["name"])
                j += 1
                if j == 3:
                    break
        crew = data["crew"]
        crew_list = []

        # Taking directors of movie
        for i in crew:
            if i["job"] == "Director":
                crew_list.append(i["name"])
        return cast_list, crew_list
    except Exception as err:
        st.write("Oops! Something went wrong in fetching movie details. Please try again.")
        with st.expander("Click to see error details: "):
            st.write(err)


# Function to get link of each movie
def fetch_movie_link(movie_id, title):
    try:
        # Replace spaces with "-"
        title = title.replace(" ", "-")
        title = str(title)
        movie_id = str(movie_id)
        link = "https://www.themoviedb.org/movie/{}-{}/watch?locale=IN".format(movie_id, title)
        return link
    except Exception as err:
        st.write("Oops! Something went wrong in fetching movie details. Please try again.")
        with st.expander("Click to see error details: "):
            st.write(err)


# Gives the best movies according to genre based on weighted score which is calculated using IMDB formula
def get_genre_based_recommendation(genre, number_of_movies):
    temp = movies_genres.loc[(movies_genres[genre] == 1)]
    temp = temp.sort_values(by=['weighted_score'], ascending=False)
    temp = temp.iloc[:number_of_movies]
    features = ['id', 'title', 'genres', 'weighted_score']
    temp = temp[features]

    movie_indices = temp['id'].tolist()
    movie_name_list = []
    movie_poster_list = []
    movie_overview_list = []
    movie_crew_list = []
    movie_cast_list = []
    movie_score_list = []
    movie_link_list = []

    # Get movie details
    for i in movie_indices:
        id = i
        title = movies[movies['id'] == i].title
        title = title.squeeze()
        poster = fetch_poster(id)
        movie_name_list.append(title)
        movie_poster_list.append(poster)
        overview = fetch_movie_details(id)
        score = movies[movies['id'] == i].weighted_score
        movie_overview_list.append(overview)
        movie_score_list.append(float(score))
        cast, crew = fetch_movie_cast_crew(id)
        movie_crew_list.append(crew)
        movie_cast_list.append(cast)
        link = fetch_movie_link(id, title)
        movie_link_list.append(link)
    return movie_name_list, movie_poster_list, movie_overview_list, movie_crew_list, movie_cast_list, movie_score_list, movie_link_list


# Main function to get recommendations based on movie
def get_recommendations(title, number_of_movies):
    # Get the index of the movie that matches the title
    index = movies[movies['title'] == title].index[0]

    # Calculate sim_scores based on distances
    sim_scores = sorted(list(enumerate(cosine_sim[index])), reverse=True, key=lambda x: x[1])

    # Get the scores of the most similar movies
    sim_scores = sim_scores[1:number_of_movies + 1]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    movie_name_list = []
    movie_poster_list = []
    movie_overview_list = []
    movie_crew_list = []
    movie_cast_list = []
    movie_score_list = []
    movie_link_list = []

    # Get movie details
    for i in movie_indices:
        for i in movie_indices:
            id = movies['id'].iloc[i]
            title = movies[movies['id'] == id].title
            title = title.squeeze()
            poster = fetch_poster(id)
            movie_name_list.append(title)
            movie_poster_list.append(poster)
            overview = fetch_movie_details(id)
            score = movies[movies['id'] == id].weighted_score
            movie_overview_list.append(overview)
            movie_score_list.append(float(score))
            cast, crew = fetch_movie_cast_crew(id)
            movie_crew_list.append(crew)
            movie_cast_list.append(cast)
            link = fetch_movie_link(id, title)
            movie_link_list.append(link)

    return movie_name_list, movie_poster_list, movie_overview_list, movie_crew_list, movie_cast_list, movie_score_list, movie_link_list
