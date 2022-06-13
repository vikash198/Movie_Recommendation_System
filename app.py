import streamlit as st
import pandas as pd
import pickle
import requests

# title of the our application details.
st.title('Movie Recommendation System')

# load the pickle file that is in dictionary format
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
 # load the similarity file which is in our def function.

similarity = pickle.load(open('similarity.pkl','rb'))

# creating the def function for fetching poster
def fetch_poster(movie_id):
    responce = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=dfd881e17ec1c41af65fc5206fa9203d&language=en-US'.format(movie_id))
    data = responce.json()
    return 'https://image.tmdb.org/t/p/w185/' + data['poster_path']

# Creating a def function for our model

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list= sorted(list(enumerate(distances)), reverse=True, key=lambda x : x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

# Now creating the text box below the title

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values)

# Now creating the search button
if st.button("Recommend"):
    names, poster = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])
