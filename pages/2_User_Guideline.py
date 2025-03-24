import streamlit as st

#%% Page setting
st.set_page_config(
    layout="wide",
    page_title="User Guideline",
    page_icon="📢",
)

#%% Page title
st.title("📢 User Guideline")

#%% Page content
st.write(
    """
    On the side bar you will be able to find three different pages: _About the App_, _User Guidline_, _Film Recommendation_, and _Film Analysis_.  
    You can click in any of them, and the content on the main page will change accordingly.

    You're currently on the _User Guideline_ page, where you'll find everything you need to know to use the app effectively!""")

st.write("")

st.write("""    
    ##### **📱About the App**

    On the About the App page you will be able to get more insights regarding the methodologies and development of the app!""")

st.write("")

st.write("""    
    ##### **🎥 Film Recommendation**

    When selecting the Film Recommendation you will be directed to a page in which you will be able to use six filter controls on the left sidebar to narrow down your preferences on movies and TV shows that are avaiable on Netflix USA, getting a personalized recommendation of 12 shows/movies.

    - **Release Year**: A slider that you can drag to define the year range. 
    - **IMDB Score**: A slider that you can drag to define the year IMDB score. 
    - **Show Type**: A dropdown button to select _Movie_ or _Show_. 
    - **Film Genres:** A dropdown menu that lets you select one or multiple genres from a list of 19 options. 
    (Action / Animation / Comedy / Crime / Documentation / Drama / European / Family / Fantasy / History / Horror / Music / Reality / Romance / Sci-fi / Sport / Thriller / War / Western)
    - **Production Countries**: A dropdown button to select one or many production countries. 
    - **Netflix Production**: A dropdown button to filter selection with Netflix produced content only or not.""")

st.write("") 

st.write("""
    ##### **📊 Film Analysis**
    When selecting the Film Analysis you will be directed to a page in which you will be able to select one type of analysis on a dropdown button:
    - **Genre Popularity Over Time**
    - **Genre by Country**
    - **Most Popular Genre by IMDb Score**
    - **Genre with Highest Votes**
    - **Runtime vs IMDb Score & Distribution**
    
     Select a release year range using the slider — the graph will update instantly based on your selection.
         
         """
)

st.title(":orange[_Enjoy the app_!]")