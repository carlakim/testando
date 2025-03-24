import streamlit as st
import pandas as pd
import plotly.express as px
import ast
import os

# ------------------------------
# 1. File Path Configuration
# ------------------------------
# Set the absolute file path to your CSV file.
# Make sure the file "netflix_data_cleaned.csv" exists in this location.
file_path = "/Users/carlagaieski/Documents/Project/netflix_data_cleaned.csv"

# ------------------------------
# 3. Page Configuration and Title
# ------------------------------
st.set_page_config(layout="wide",page_title="Film Analysis",page_icon="📊")
st.title("📊 Film Analysis")


# ------------------------------
# 2. Data Loading and Processing
# ------------------------------
@st.cache_data
def load_and_process_data(path):
    # Read the CSV file
    df = pd.read_csv(path)
    
    # Helper function to parse list-like string representations into actual lists
    def parse_list_column(column):
        return column.apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
    
    # Convert columns that store lists as strings
    if 'genres' in df.columns:
        df['genres'] = parse_list_column(df['genres'])
    if 'country' in df.columns:
        df['country'] = parse_list_column(df['country'])
    if 'production_countries' in df.columns:
        df['production_countries'] = parse_list_column(df['production_countries'])
    
    return df

# Load the data using the defined file path
df = load_and_process_data(file_path)

# ------------------------------
# 4. Graph Selection Dropdown
# ------------------------------
graph_option = st.sidebar.selectbox("Select Analysis Type", [
    "Genre Popularity Over Time",
    "Genre by Country",
    "Most Popular Genre by IMDb Score",
    "Genre with Highest Votes",
    "Runtime vs IMDb Score & Distribution"
])

# ------------------------------
# 5. Analysis Option 1: Runtime vs IMDB score
# ------------------------------
if graph_option == "Runtime vs IMDb Score & Distribution":
    st.subheader("Runtime vs IMDb Score with Distribution")

    # 1. Year Range Slider
    min_year = int(df['release_year'].min())
    max_year = int(df['release_year'].max())
    year_range = st.slider(
        "Select Release Year Range:",
        min_value=min_year,
        max_value=max_year,
        value=(2000, 2022),
        step=1
    )

    # 2. Filter data by year and remove missing runtime/imdb_score
    df_plot = df[
        (df['release_year'] >= year_range[0]) &
        (df['release_year'] <= year_range[1])
    ].dropna(subset=["runtime", "imdb_score"])

    # 3. Compute Pearson correlation (optional to show or hide)
    correlation = df_plot["runtime"].corr(df_plot["imdb_score"])
    st.write(f"**Correlation between Runtime and IMDb score:** {correlation:.2f}")

    # 4. Create a scatter plot WITHOUT any trendline
    fig = px.scatter(
        df_plot,
        x="runtime",
        y="imdb_score",
        color="type",               # Show legend for Movie/Show
        hover_data=["title", "genres"],
        marginal_x="histogram",     # Histogram on top for runtime distribution
        # No trendline parameter => No overall line
        title=(
            f"Runtime vs. IMDb Score (Years {year_range[0]}–{year_range[1]}) "
            f"[Correlation = {correlation:.2f}]"
        ),
        labels={
            "runtime": "Runtime (minutes)",
            "imdb_score": "IMDb Score",
            "type": "Type"
        }
    )

    # 5. Optional: Keep the legend so we can see "Movie" vs "Show"


    # 6. Customize figure size
    fig.update_layout(
        autosize=False,
        width=1000,
        height=700
    )

    # 7. Display the chart
    st.plotly_chart(fig, use_container_width=False)


# ------------------------------
# 6. Analysis Option 2: Genre Popularity Over Time
# ------------------------------
if graph_option == "Genre Popularity Over Time":
    st.subheader("Genre Popularity Over Time (Binned by Decade)")

    # 1. Year range slider
    min_year = int(df['release_year'].min())
    max_year = int(df['release_year'].max())
    year_range = st.slider(
        "Select Release Year Range:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )
    
    # 2. Filter data by year
    df_filtered = df[(df['release_year'] >= year_range[0]) & (df['release_year'] <= year_range[1])]
    df_filtered = df_filtered.sample(min(len(df_filtered), 5000), random_state=42)
    
    # 3. Group by decade and genre
    df_filtered['decade'] = (df_filtered['release_year'] // 10) * 10
    genre_decade = (
        df_filtered
        .explode('genres')
        .groupby(['decade', 'genres'])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    
    # 4. Reshape from wide to long
    df_long = genre_decade.melt(
        id_vars='decade',
        var_name='Genre',
        value_name='Count'
    )

    # 5. Identify Top 5 genres by total popularity
    genre_totals = (
        df_long.groupby('Genre')['Count']
        .sum()
        .sort_values(ascending=False)
    )
    top5_genres = genre_totals.head(5).index.tolist()

    # 6. Create an interactive line chart with Plotly Express
    fig = px.line(
        df_long,
        x='decade',
        y='Count',
        color='Genre',
        markers=True,
        title="Genre Popularity Over Time (by Decade) - Top 5 Genre line marked in bold",
        labels={
            "decade": "Decade",
            "Count": "Count of Movies/TV Shows",
            "Genre": "Genre"
        }
    )
    
    # 7. Make the figure wider (optional)
    fig.update_layout(
        autosize=False,
        width=1000,
        height=500)

    # 8. Highlight Top 5 genres in the legend by making lines thicker (and optionally color)
    for trace in fig.data:
        # trace.name is the genre name in the legend
        if trace.name in top5_genres:
            # Make the line thicker
            trace.line.width = 7
            
            # Optionally, set a bright color (this overrides the default color):
            # trace.line.color = "crimson"
        else:
            # Optionally, make non-top-10 lines thinner or lighter:
            trace.line.width = 1
            # trace.line.color = "lightgray"

    # 9. Display the chart (disable container width to respect custom size)
    st.plotly_chart(fig, use_container_width=False)


# ------------------------------
# 7. Analysis Option 3: Genre by Country
# ------------------------------
if graph_option == "Genre by Country":
    st.subheader("Stacked Histogram: Top 10 Countries in Top 10 Genres")

    # 1. Compute top 10 genres
    genre_counts = df.explode('genres').groupby('genres').size().sort_values(ascending=False)
    top10_genres = genre_counts.head(10).index.tolist()

    # 2. Filter rows that contain at least one of the top 10 genres
    df_top_genres = df[df['genres'].apply(lambda x: any(g in top10_genres for g in x))]

    # 3. Compute top 10 countries
    country_counts = df_top_genres.explode('country').groupby('country').size().sort_values(ascending=False)
    top10_countries = country_counts.head(10).index.tolist()

    # 4. Create pivot table
    pivot = (
        df_top_genres
        .explode('genres')
        .explode('country')
        .groupby(['genres', 'country'])
        .size()
        .unstack()
        .fillna(0)
        .loc[top10_genres, top10_countries]
        .reset_index()
    )

    # 5. Melt pivot table into long-form:
    #    - "genres" stays as an identifier
    #    - "Country" becomes the column names
    #    - "Count" becomes the numeric values
    df_long = pivot.melt(
        id_vars="genres",       # keep 'genres' as is
        var_name="Country",     # rename 'variable' to 'Country'
        value_name="Count"      # rename 'value' to 'Count'
    )

    # 6. Create a horizontal stacked bar chart
    fig = px.bar(
        df_long,
        y="genres",     # genres on the y-axis
        x="Count",      # numeric counts on the x-axis
        color="Country", 
        orientation="h", 
        title="Top 10 Genres and Their Top 10 Producing Countries",
        labels={
            "genres": "Genre",
            "Count": "Count of Movies/TV Shows",
            "Country": "Country"
        },
        barmode="stack"
    )

    # 7. (Optional) Make the figure wider/taller
    fig.update_layout(
        autosize=False,
        width=1000,
        height=500
    )

    # 8. Show the chart with custom size
    st.plotly_chart(fig, use_container_width=False)


# ------------------------------
# 8. Analysis Option 4: Most Popular Genre by IMDb Score
# ------------------------------
if graph_option == "Most Popular Genre by IMDb Score":
    st.subheader("Top 10 Most Popular Genres by Average IMDb Score")
    
    # 1. Group by genre and calculate average IMDb score (explode 'genres' if needed)
    genre_imdb = (
        df.explode('genres')
        .groupby('genres')['imdb_score']
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    
    # 2. Create a bar chart with text labels = 'imdb_score'
    fig = px.bar(
        genre_imdb,
        x='genres',
        y='imdb_score',
        text='imdb_score',  # Put the numeric value as the label
        title="Top 10 Genres by Average IMDb Score",
        labels={
            'genres': 'Genre',
            'imdb_score': 'Average IMDb Score'
        }
    )

    # 3. Position the text labels above the bars
    #    Format the text to show, for example, 1 decimal place
    fig.update_traces(
        textposition='outside', 
        texttemplate='%{text:.1f}'  # 1 decimal place, e.g. 6.3
    )

    # 4. Customize the y-axis ticks to show increments of 0.1
    #    and optionally set a range if you know your scores fall between certain values
    fig.update_layout(
        yaxis=dict(
            tickmode='linear',
            dtick=0.1,         # step of 0.1 between ticks
            range=[6.0, 7.5]   # adjust lower and upper range to fit your data
        ),
        autosize=False,
        width=1000,
        height=500
    )

    # 5. Display the chart
    st.plotly_chart(fig, use_container_width=False)


# ------------------------------
# 9. Analysis Option 5: Genre with Highest Votes
# ------------------------------
if graph_option == "Genre with Highest Votes":
    st.subheader("Top 10 Genres with Highest Total IMDb Votes Counts")
    
    # Calculate total IMDb votes for each genre
    genre_votes = (
        df.explode('genres')
        .groupby('genres')['imdb_votes']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    
    # Create a bar chart with numeric labels
    fig = px.bar(
        genre_votes,
        x='genres',
        y='imdb_votes',
        text='imdb_votes',
        title="Top 10 Genres by Total IMDb Votes",
        labels={
            'genres': 'Genre',
            'imdb_votes': 'Total IMDb Votes Counts'
        }
    )
    
    # Format labels with commas
    fig.update_traces(
        textposition='outside',
        texttemplate='%{text:,.0f}'  # Use commas as thousand separators, zero decimals
    )
    
    st.plotly_chart(fig, use_container_width=True)
