import streamlit as st

#%% Page setting
st.set_page_config(
    layout="wide",
    page_title="About the App",
    page_icon="📱",
)

#%% Page title
st.title("📱 About the App")

#%% Page content
st.markdown(
    """
    ### Welcome to Netflix Recommendation & Analysis App!
    This app was developed to provide an intuitive and effective film recommendation and analysis platform based on Netflix USA's catalog.  
    And for analyzing Netflix's stock performance, based on its own produced content. 

    Film Recommendation 🎥 page is an user friendly recommendation system for movies and TV shows that are avaiable on Netflix USA.
    Users can apply filters based on their preferences and receive the top 12 personalized recommendations.

    The filtering system was created based on:
    1. Release Year
    2. IMDB Score
    3. Show Type (Movie or TV)
    4. Genre
    5. Production Countries
    6. If it is a Netflix Production or not

    On the Film Analysis 📊 Page, users delimit their desired released year range, through a slide bar, and choose between 5 types of analysis:
    1. Genre Popularity Over Time
    2. Genre by Country
    3. Most Popular Genre by IMDb Score
    4. Genre with Highest Votes
    5. Runtime vs IMDb Score & Distribution

    So they are able to explore and gain insights from the entretaiment world.

    ### Datasets
    Our first dataset was sourced from [Kaggle](https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies/data?select=titles.csv), which contained:
       -  id: The title ID on JustWatch.
       -  title: The name of the title.
       -  show_type: TV show or movie.
       -  description: A brief description.
       -  release_year: The release year.
       -  age_certification: The age certification.
       -  runtime: The length of the episode (SHOW) or movie.
       -  genres: A list of genres.
       -  production_countries: A list of countries that produced the title.
       -  seasons: Number of seasons if it's a SHOW.
       -  imdb_id: The title ID on IMDB.
       -  imdb_score: Score on IMDB.
      -   imdb_votes: Votes on IMDB.
      -   tmdb_popularity: Popularity on TMDB.
      -   tmdb_score: Score on TMDB.
    
    Additionally, a new boolean column was created to identify if the movie/tv show was a Netflix Original productions. To generate this column, IMDb's [All Netflix Origials](https://www.imdb.com/list/ls093971121/) list was scraped and matched with our dataset. Creating a boolean column - True or False - if it was a Netflix Original production or not. 

    A different dataset containing the country codes for the "production_countries" was also created to change abreviations, such as "US" to "America", and later matched with "production_countries" to change the names and changing column name to "country".

    Lastly, the movies and tv shows posters url were scrapped from TMDB website and added to the main dataset, under "poster_url"

    Therefore, the final data set was composed of the final dataset contained: 5849 entries and 18 columns. To create this app, the dataset was filtered and only id, title, show_type, release_year, genres, country, imdb_score, poster_url, columns were used.

   """
)
st.write("") #to make space
st.write("")

st.markdown("**This project was developed by:**")
st.markdown(
    """
    - [Juyin HSU](https://www.linkedin.com/in/juyinhsu/)  
    - [Yi-Chieh LEE](https://www.linkedin.com/in/yichiehlee1234/)  
    - [Carla KIM GAIESKI](https://www.linkedin.com/in/carlakg/)
    """
)
