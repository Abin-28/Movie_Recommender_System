import streamlit as st
import pickle
import pandas as pd
import requests

# Page configuration (UI only)
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# function for fetching movies poster using API
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# same function as done in jupyter of recommending 5 movies
def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]   #here distances act as a array
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    #here rather than displaying we are storing 5 movies in recommended_movies list
    recommended_movies_names = []
    recommended_movie_posters = []
    recommended_movie_ids = []
    for i in movies_list:
        movie_id=i[0]
        #fetch poster from API
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_ids.append(movie_id)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies_names.append(movies.iloc[i[0]].title)
    
    return recommended_movies_names,recommended_movie_posters,recommended_movie_ids

# importing movies_dict.pkl for using in drop box
movies_dict=pickle.load(open('movie-recommender-system/movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
# importing similarity.pkl
similarity=pickle.load(open('movie-recommender-system/similarity.pkl','rb'))

# Sidebar (UI-only helpers)
with st.sidebar:
    st.markdown('<h1 style="color:#FF0000; margin-bottom:0.5rem;">About</h1>', unsafe_allow_html=True)
    st.write("Select a movie to get five similar recommendations.")
    st.caption("A simple content-based movie recommender with a Streamlit UI. It uses the `TMDB 5000 Movies and Credits datasets` to compute movie-to-movie similarity and then recommends the top 5 similar titles, displaying their posters.")

# Displaying Title name
st.title('🎬 Movie Recommender System')
st.caption('Content-based recommendations using TMDB metadata')

# Minimal CSS for responsive, clickable cards (no fullscreen icon)
st.markdown(
    """
    <style>
      .movie-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; }
      @media (max-width: 1200px) { .movie-grid { grid-template-columns: repeat(4, 1fr); } }
      @media (max-width: 900px) { .movie-grid { grid-template-columns: repeat(3, 1fr); } }
      @media (max-width: 640px) { .movie-grid { grid-template-columns: repeat(2, 1fr); } }
      @media (max-width: 420px) { .movie-grid { grid-template-columns: repeat(1, 1fr); } }
      .movie-card { cursor: pointer; text-align: center; }
      .movie-card img { width: 100%; height: auto; border-radius: 8px; }
      .movie-card .title { font-weight: 600; margin-top: 6px; }
      .movie-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.15); transition: all .15s ease; }
      .movie-link { text-decoration: none; color: inherit; }
    </style>
    """,
    unsafe_allow_html=True,
)

# making a drop box
selected_movie=st.selectbox(
    'Select a movie to get recommendations:',
   movies['title'].values)

# making a button
if st.button('Recommend'):
    recommended_movie_names,recommended_movie_posters,recommended_movie_ids = recommend(selected_movie)
    st.subheader('Top 5 recommendations')
    # responsive grid of cards
    cards_html = [
        f'''<a class="movie-link" href="https://www.themoviedb.org/movie/{recommended_movie_ids[idx]}" target="_blank">
               <div class="movie-card">
                 <img src="{recommended_movie_posters[idx]}" alt="{recommended_movie_names[idx]}">
                 <div class="title">{recommended_movie_names[idx]}</div>
               </div>
             </a>'''
        for idx in range(len(recommended_movie_names))
    ]
    st.markdown('<div class="movie-grid">' + "".join(cards_html) + '</div>', unsafe_allow_html=True)
