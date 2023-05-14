import pickle
import streamlit as st
import requests
import pandas as pd


def fetch_poster(movie_id): #For fetching posters based on movie_id
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):#For Content Based Recommender System
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


#For Genre(Top 10) based recommender system
def genre_top10(choice_genre):
    filtered_movies = genre_df[genre_df['genres'].apply(lambda x: len(x)>0 and x[0] == choice_genre)]#.sort_values(by='popularity',ascending=False) #The error "list index out of range" occurs when there is an empty list in the genres column. To fix this, you can add a check to ensure that the list is not empty before accessing its first element.This code checks if the length of the list is greater than zero before checking if the first element is equal to "Action".
    filtered_movies=filtered_movies[filtered_movies['vote_count']>2000][:10]
    filtered_movies=filtered_movies[['title','movie_id']]
    return filtered_movies




#Web Page Main Title
st.header('Movie Recommender System')




# Content Based Recommender System(Main)
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
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
        

        
 
#Top 50 popular movies       
if st.button("Popular Movies of All Time"):        
    st.header("Popular Movies of All Time")
    popular = pickle.load(open('popular_lst.pkl','rb'))
    popular_id = pickle.load(open('popular_id.pkl','rb'))

    for i in range(10):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(popular.values[i*5])
            st.image(fetch_poster(popular_id[i*5].values[0]))
            
        with col2:
            st.text(popular.values[i*5+1])
            st.image(fetch_poster(popular_id[i*5+1].values[0]))
            
        with col3:
            st.text(popular.values[i*5+2])
            st.image(fetch_poster(popular_id[i*5+2].values[0]))
            
        with col4:
            st.text(popular.values[i*5+3])
            st.image(fetch_poster(popular_id[i*5+3].values[0]))
            
        with col5:
            st.text(popular.values[i*5+4])
            st.image(fetch_poster(popular_id[i*5+4].values[0]))





#Top 50 rated movies
if st.button("G.O.A.T."):
    st.header("G.O.A.T.")
    ratings = pickle.load(open('ratings_lst.pkl','rb'))
    ratings_id = pickle.load(open('ratings_id.pkl','rb'))

    for i in range(10):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(ratings.values[i*5])
            st.image(fetch_poster(ratings_id[i*5].values[0]))
            
        with col2:
            st.text(ratings.values[i*5+1])
            st.image(fetch_poster(ratings_id[i*5+1].values[0]))
            
        with col3:
            st.text(ratings.values[i*5+2])
            st.image(fetch_poster(ratings_id[i*5+2].values[0]))
            
        with col4:
            st.text(ratings.values[i*5+3])
            st.image(fetch_poster(ratings_id[i*5+3].values[0]))
            
        with col5:
            st.text(ratings.values[i*5+4])
            st.image(fetch_poster(ratings_id[i*5+4].values[0]))




# Latest trending
if st.button("Latest Trending"):
    st.header("Latest Trending")
    movies_latest_list = pickle.load(open('movies_latest_list.pkl','rb'))
    movies_latest_id = pickle.load(open('movies_latest_id.pkl','rb'))
    
    for i in range(10):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(movies_latest_list.values[i*5])
            st.image(fetch_poster(movies_latest_id[i*5].values[0]))
            
        with col2:
            st.text(movies_latest_list.values[i*5+1])
            st.image(fetch_poster(movies_latest_id[i*5+1].values[0]))
            
        with col3:
            st.text(movies_latest_list.values[i*5+2])
            st.image(fetch_poster(movies_latest_id[i*5+2].values[0]))
            
        with col4:
            st.text(movies_latest_list.values[i*5+3])
            st.image(fetch_poster(movies_latest_id[i*5+3].values[0]))
            
        with col5:
            st.text(movies_latest_list.values[i*5+4])
            st.image(fetch_poster(movies_latest_id[i*5+4].values[0]))
            
            
            
# Top 10 Genre
genre = pickle.load(open('genres.pkl','rb'))
genre_df=pd.DataFrame(pickle.load(open('genre_dict.pkl','rb')))
selected_genre = st.selectbox(
    "Select Genre",
    genre)
if st.button("Top 5 Genre Movies"):
    # selected_genre = st.selectbox(
    # "Select Genre",
    # genre)
    # if(st.button("Show top 10")):
    filtered_movies = genre_top10(selected_genre)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    #col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
    with col1:
        st.text(filtered_movies.title.iloc[0])
        st.image(fetch_poster(filtered_movies.movie_id.iloc[0]))
            
    with col2:
        st.text(filtered_movies.title.iloc[1])
        st.image(fetch_poster(filtered_movies.movie_id.iloc[1]))
    
    with col3:
        st.text(filtered_movies.title.iloc[2])
        st.image(fetch_poster(filtered_movies.movie_id.iloc[2]))
        
    with col4:
        st.text(filtered_movies.title.iloc[3])
        st.image(fetch_poster(filtered_movies.movie_id.iloc[3]))
        
    with col5:
        st.text(filtered_movies.title.iloc[4])
        st.image(fetch_poster(filtered_movies.movie_id.iloc[4]))
        
    # with col6:
    #     st.text(filtered_movies.title.iloc[5])
    #     st.image(fetch_poster(filtered_movies.movie_id.iloc[5]))
        
    # with col7:
    #     st.text(filtered_movies.title.iloc[6])
    #     st.image(fetch_poster(filtered_movies.movie_id.iloc[6]))
        
    # with col8:
    #     st.text(filtered_movies.title.iloc[7])
    #     st.image(fetch_poster(filtered_movies.movie_id.iloc[7]))
        
    # with col9:
    #     st.text(filtered_movies.title.iloc[8])
    #     st.image(fetch_poster(filtered_movies.movie_id.iloc[8]))
    
    # with col10:
    #     st.text(filtered_movies.title.iloc[9])
    #     st.image(fetch_poster(filtered_movies.movie_id.iloc[9]))