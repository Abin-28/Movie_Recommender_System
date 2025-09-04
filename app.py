import streamlit as st
import pickle
import pandas as pd
import requests

#function for fetching movies poster using API
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

#same function as done in jupyter of recommending 5 movies
def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]   #here distances act as a array
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    #here rather than displaying we are storing 5 movies in recommended_movies list
    recommended_movies_names = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id=i[0]
        #fetch poster from API
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies_names.append(movies.iloc[i[0]].title)
    
    return recommended_movies_names,recommended_movie_posters

#importing movies_dict.pkl for using in drop box
movies_dict=pickle.load(open('movie-recommender-system/movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
#importing similarity.pkl
similarity=pickle.load(open('movie-recommender-system/similarity.pkl','rb'))

#Displaying Title name
st.title('Movie Recommender System')

# making a drop box
selected_movie=st.selectbox(
    'How would you like to be connected?',
   movies['title'].values)

#making a button
if st.button('Recommend'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    #displaying the Poster and Name column wise
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
