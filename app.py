import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for modern UI
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .movie-container {
        padding: 20px;
        border-radius: 10px;
        background-color: #1e1e1e;
        margin: 10px 0;
    }
    .title {
        color: #ffffff;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# TMDB API configuration
TMDB_API_KEY = st.secrets.get("TMDB_API_KEY", "e0eb77c8694fd5d891c6d5fe7e1cab5e")  # Replace with your TMDB API key
TMDB_BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

def fetch_genres():
    """Fetch all available movie genres"""
    try:
        response = requests.get(
            f"{TMDB_BASE_URL}/genre/movie/list",
            params={"api_key": TMDB_API_KEY, "language": "en-US"}
        )
        return response.json()["genres"]
    except Exception as e:
        st.error(f"Error fetching genres: {str(e)}")
        return []

def fetch_movies(page=1):
    """Fetch movies with filters"""
    try:
        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US",
            "page": page,
            "sort_by": "popularity.desc"
        }
        
        # Apply year filter if selected
        if st.session_state.get('year_filter'):
            params["primary_release_year"] = st.session_state['year_filter']
        
        # Apply genre filter if selected
        if st.session_state.get('genre_filter') and st.session_state['genre_filter'] != "All":
            params["with_genres"] = st.session_state['genre_filter']
            
        # Apply vote average filter if selected
        if st.session_state.get('rating_filter'):
            params["vote_average.gte"] = st.session_state['rating_filter']

        response = requests.get(
            f"{TMDB_BASE_URL}/discover/movie",
            params=params
        )
        return response.json()["results"]
    except Exception as e:
        st.error(f"Error fetching movies: {str(e)}")
        return []

def search_movies(query):
    """Search for movies based on user query"""
    try:
        response = requests.get(
            f"{TMDB_BASE_URL}/search/movie",
            params={
                "api_key": TMDB_API_KEY,
                "language": "en-US",
                "query": query,
                "page": 1
            }
        )
        return response.json()["results"]
    except Exception as e:
        st.error(f"Error searching movies: {str(e)}")
        return []

def get_movie_recommendations(movie_id):
    """Get movie recommendations based on a movie ID"""
    try:
        response = requests.get(
            f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations",
            params={"api_key": TMDB_API_KEY, "language": "en-US", "page": 1}
        )
        return response.json()["results"]
    except Exception as e:
        st.error(f"Error fetching recommendations: {str(e)}")
        return []

# Header
st.markdown('<p class="title">🎬 Movie Recommender</p>', unsafe_allow_html=True)

# Initialize session state for filters
if 'year_filter' not in st.session_state:
    st.session_state['year_filter'] = None
if 'genre_filter' not in st.session_state:
    st.session_state['genre_filter'] = "All"
if 'rating_filter' not in st.session_state:
    st.session_state['rating_filter'] = 0.0

# Sidebar filters
with st.sidebar:
    st.markdown('## Filters')
    
    # Year filter
    current_year = datetime.now().year
    year_range = range(1900, current_year + 1)
    selected_year = st.selectbox(
        "Release Year",
        ["All"] + list(reversed(list(year_range))),
        index=0
    )
    st.session_state['year_filter'] = None if selected_year == "All" else selected_year
    
    # Genre filter
    genres = fetch_genres()
    genre_options = {"All": "All"} | {str(genre["id"]): genre["name"] for genre in genres}
    selected_genre = st.selectbox(
        "Genre",
        options=list(genre_options.keys()),
        format_func=lambda x: genre_options[x]
    )
    st.session_state['genre_filter'] = selected_genre
    
    # Rating filter
    rating = st.slider(
        "Minimum Rating",
        min_value=0.0,
        max_value=10.0,
        value=0.0,
        step=0.5
    )
    st.session_state['rating_filter'] = rating

# Search bar
search_query = st.text_input("Search for a movie...", placeholder="Enter a movie title")

if search_query:
    movies = search_movies(search_query)
else:
    movies = fetch_movies()

# Display movies in a grid
cols = st.columns(4)
for idx, movie in enumerate(movies[:8]):  # Show top 8 movies
    with cols[idx % 4]:
        poster_path = movie.get("poster_path")
        if poster_path:
            poster_url = f"{POSTER_BASE_URL}{poster_path}"
            st.image(poster_url, use_container_width=True)
        
        st.markdown(f"**{movie['title']}**")
        st.write(f"⭐ {movie['vote_average']:.1f}")
        
        if st.button(f"Get Recommendations", key=f"btn_{idx}"):
            st.markdown("### Similar Movies")
            recommendations = get_movie_recommendations(movie['id'])
            
            rec_cols = st.columns(4)
            for rec_idx, rec in enumerate(recommendations[:4]):
                with rec_cols[rec_idx]:
                    rec_poster = rec.get("poster_path")
                    if rec_poster:
                        st.image(f"{POSTER_BASE_URL}{rec_poster}", use_container_width=True)
                    st.markdown(f"**{rec['title']}**")
                    st.write(f"⭐ {rec['vote_average']:.1f}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and TMDB API")
