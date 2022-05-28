# Content-based Movie Recommendation System

Built a movie recommendation system where user can choose to get recommendations based on movies (using overview, keywords, cast, crew, etc) or based on genres.

For movie based recommendation - content based filtering is used.This system suggests similar items based on a particular item. This system uses item metadata, such as genre, director, description, actors, etc. for movies, to make these recommendations. The general idea behind these recommender systems is that if a person liked a particular item, he or she will also like an item that is similar to it.
Most similar movies are picked using cosine similarity scores.Cosine similarity is a metric used to measure how similar the documents are irrespective of their size. Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space. The cosine similarity is advantageous because even if the two similar documents are far apart by the Euclidean distance (due to the size of the document), chances are they may still be oriented closer together. The smaller the angle, higher the cosine similarity.

For genre based recommendation - movies belonging to particular genre are sorted based on their weighted score which is calculated using formula given on IMDB site using vote average and vote count.

Link for the application: https://sj-movie-recommender-system.herokuapp.com/

Dataset used: [TMDB 5000 movie dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

## To run project on local machine:
1. Clone or download this repository to your local machine.
2. Run jupyter notebook to create cosine_sim.pkl in main directory.
3. Install all the libraries mentioned in the requirements.txt.
4. Get your API key from https://www.themoviedb.org/.
5. Replace API key in lines 36, 60, 82 of helper.py file with your API key.
6. Open your terminal/command prompt from your project directory and run the file `app.py` by executing the command `streamlit run app.py`.
