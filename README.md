# Movie Recommender

A modern movie recommendation website built with Streamlit that allows users to:
- Search for movies
- View popular movies
- Get personalized movie recommendations
- See movie ratings and details

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Get a TMDB API Key:
   - Sign up at https://www.themoviedb.org/
   - Go to your account settings
   - Get an API key
   - Create a `.streamlit/secrets.toml` file and add:
     ```toml
     TMDB_API_KEY = "your_api_key_here"
     ```

3. Run the application:
```bash
streamlit run app.py
```

## Features
- Modern, responsive UI
- Real-time movie search
- Popular movies showcase
- Movie recommendations based on selection
- Movie ratings and details
- Clean and intuitive interface
