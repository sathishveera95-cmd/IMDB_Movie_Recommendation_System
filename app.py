import streamlit as st

from recommendation.recommender import MovieRecommender
from recommendation.storyline_recommender import StorylineRecommender

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="IMDb Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# ----------------------------------------------------
# Load Models
# ----------------------------------------------------

@st.cache_resource
def load_models():
    return MovieRecommender(), StorylineRecommender()

movie_recommender, storyline_recommender = load_models()

# ----------------------------------------------------
# Header
# ----------------------------------------------------

st.title("🎬 IMDb Movie Recommendation System")

st.markdown("""
Discover similar movies using **Natural Language Processing (NLP)**,
**TF-IDF Vectorization**, and **Cosine Similarity**.
""")


# ----------------------------------------------------
# Tabs
# ----------------------------------------------------

tab1, tab2 = st.tabs([
    "🎥 Movie Search",
    "📝 Storyline Search"
])

with tab1:

    st.subheader("Search by Movie Name")

    movie_name = st.text_input(
        "Movie Name",
        placeholder="Example: Dune"
    )

    top_n_movie = st.slider(
        "Number of Recommendations",
        5,
        20,
        10,
        key="movie_slider"
    )

    if st.button(
        "Recommend Movies",
        key="movie_btn"
    ):

        if movie_name.strip():

            selected_movie, recommendations = movie_recommender.recommend(
                movie_name,
                top_n_movie
            )

            if recommendations is not None:

                st.success(
                    f"Recommendations for **{selected_movie}**"
                )

                st.dataframe(
                    recommendations,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.error("Movie not found.")

        else:

            st.warning("Please enter a movie name.")


with tab2:

    st.subheader("Search by Storyline")

    storyline = st.text_area(
        "Enter Storyline",
        placeholder="Example: A young prince seeks revenge after his family is destroyed while fighting for control of a desert planet.",
        height=180
    )

    top_n_story = st.slider(
        "Number of Recommendations",
        5,
        20,
        10,
        key="story_slider"
    )

    if st.button(
        "Find Similar Movies",
        key="story_btn"
    ):

        if storyline.strip():

            recommendations = storyline_recommender.recommend(
                storyline,
                top_n_story
            )

            st.success("Recommended Movies")

            st.dataframe(
                recommendations,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning("Please enter a storyline.")