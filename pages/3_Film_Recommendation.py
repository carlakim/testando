import streamlit as st
import pandas as pd

#%% Data Processing
# read netflix data
df = pd.read_csv("/Users/carlagaieski/Documents/Project/netflix_data_cleaned.csv")

# extract unique type for dropdown menu
show_type = df['type'].dropna().unique()

# extract unique genre for dropdown menu
genres = df['genres'].apply(lambda genre: [i.strip() for i in genre.strip("[]").replace("'", "").split(',') if i.strip() != '']).explode()
genres = sorted(genres.dropna().unique())

# extract unique production_country for dropdown menu
countries = df['country'].apply(lambda country: [i.strip() for i in country.strip("[]").replace("'", "").split(',') if i.strip() != '']).explode()
countries = sorted(countries.dropna().unique())

# extract unique netflix_owned for dropdown menu
netflix_owned = df["netflix_owned"].dropna().unique()

#%% Page setting
st.set_page_config(
    layout="wide",
    page_title="Film Recommendation",
    page_icon="🎥",
)

#%% Page title
st.title("🎥 Film Recommendation")

#%% Page content
# Sidebar section for filters
select_year_range = st.sidebar.slider(
    "Release Year:",
    min_value = int(df["release_year"].min()),  # min year
    max_value = int(df["release_year"].max()),  # max year
    value = (int(df["release_year"].min()), int(df["release_year"].max())), step=1,) # default year
    
select_imdb_score = st.sidebar.slider(
    "IMDB Score:",
    min_value = 0.0,  # min score
    max_value = 10.0,  # max score
    value = (0.0, 10.0), step=0.1,) # default score range (0 to 10)

select_imdb_votes = st.sidebar.slider(
    "IMDB Votes:",
    min_value = 0,  # min votes
    max_value = int(df["imdb_votes"].max()),  # max votes
    value = (int(df["imdb_votes"].min()), int(df["imdb_votes"].max())), step=100,) # default votes
    
select_show_type = st.sidebar.selectbox("Show Type:", show_type)
select_film_genre = st.sidebar.multiselect("Film Genres:", genres)
select_country = st.sidebar.multiselect("Production Countries:", countries)
select_netflix_film = st.sidebar.multiselect("Netflix Film:", netflix_owned)
    

# Apply filters to the dataframe
filtered_df = df[
    (df['release_year'] >= select_year_range[0]) & 
    (df['release_year'] <= select_year_range[1]) & 
    (df['imdb_score'] >= select_imdb_score[0]) & 
    (df['imdb_score'] <= select_imdb_score[1]) &
    (df['imdb_votes'] >= select_imdb_votes[0]) &
    (df['imdb_votes'] <= select_imdb_votes[1]) &
    (df['type'].apply(lambda x: select_show_type in x))
    ]
    
if select_film_genre:
    filtered_df = filtered_df[filtered_df['genres'].apply(lambda x: any(i in x for i in select_film_genre))]
    
if select_country:
    filtered_df = filtered_df[filtered_df['country'].apply(lambda x: any(i in x for i in select_country))]
    
if select_netflix_film:
    filtered_df = filtered_df[filtered_df['netflix_owned'].isin(select_netflix_film)] 


# Film Metrics
if not filtered_df.empty:
    avg_imdb_score = filtered_df["imdb_score"].mean()
    avg_imdb_votes = filtered_df["imdb_votes"].mean()
    avg_runtime = filtered_df["runtime"].mean()
    avg_runtime_hours = int(avg_runtime) // 60  # Calculate hours
    avg_runtime_minutes = int(avg_runtime) % 60  # Calculate remaining minutes

    # Display these averages in boxes
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Average IMDB Score", value=f"{avg_imdb_score:.2f}")
    with col2:
        st.metric(label="Average IMDB Votes", value=f"{int(avg_imdb_votes):,}")
    with col3:
        st.metric(label="Average Runtime", value=f"{avg_runtime_hours:02d}:{avg_runtime_minutes:02d}")


# Film Recommendation
if filtered_df.empty:
    st.write("No films match your filters. Please reselect!")
    
else:
    # Sort by imdb_score from high to low and take the top 12
    top_movies = filtered_df.sort_values(by="imdb_score", ascending=False).head(12)

    # Create 4 columns for displaying images with spacing
    cols = st.columns(4, gap="medium")

    # No-image URL
    no_image_url = "https://i.postimg.cc/KYZrNQkN/no-image-2.jpg"

    for i, (index, row) in enumerate(top_movies.iterrows()):
        # Cycle through the 4 columns
        col = cols[i % 4]

        # Modify caption with title, release year, and IMDb score
        search_url = f"https://www.google.com/search?q={row['title']}" # Create the search URL
        title_text = f"<a href='{search_url}' target='_blank' style='text-decoration: none; color: black; font-weight: bold;'>{row['title']}</a>"
        year_text = f"📅 Year: {row['release_year']}"
        score_text = f"⭐ IMDB score: {row['imdb_score']}/10"

        # Check if the poster_url is valid, else use no image url
        image_url = row["poster_url"] if isinstance(row["poster_url"], str) and row["poster_url"].startswith("http") else no_image_url

        # st.container() makes sure the height is the same
        with col:
            with st.container():
                st.image(image_url)
                st.markdown(f"<p style='text-align: left; font-weight: bold; margin: 2px 0;'>{title_text}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: left; margin: 0.5px 0;'>{year_text}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: left; margin: 0.5px 0;'>{score_text}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: left; margin: 1px 0;'></p>", unsafe_allow_html=True)
