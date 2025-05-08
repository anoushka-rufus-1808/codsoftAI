import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('clean_movies_dataset.csv')
    df['title'] = df['title'].astype(str).str.strip()
    df['content'] = df['content'].fillna('')
    return df

# TF-IDF + SVD
@st.cache_data
def vectorize_and_reduce(text_data, n_components=100):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(text_data)
    svd = TruncatedSVD(n_components=n_components)
    reduced_matrix = svd.fit_transform(tfidf_matrix)
    return reduced_matrix

# Build Nearest Neighbors model
@st.cache_resource
def build_nn_index(vectors, n_neighbors=6):
    model = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
    model.fit(vectors)
    return model

# Recommend similar movies
def recommend(title, movie_titles, vectors, model, movies_df):
    title = title.strip().lower()
    matched_titles = [t for t in movie_titles.index if title == t.lower()]

    if not matched_titles:
        return ["❌ Movie not found."]
    
    matched_idx = movie_titles[matched_titles[0]]

    # Get dense vector
    if isinstance(vectors[matched_idx], np.ndarray):
        dense_vector = vectors[matched_idx]
    else:
        dense_vector = vectors[matched_idx].todense()

    # Reshape to 2D
    distances, indices = model.kneighbors(dense_vector.reshape(1, -1))

    neighbors = indices[0][1:]  # skip the input movie itself
    return movies_df['title'].iloc[neighbors].tolist()


# Load full data
movies = load_data()

# Streamlit UI
st.title("🎬 Movie Recommendation System")
st.write("Type the name of a movie, and get similar suggestions based on content.")

# Optional: Genre filter
if 'genre' in movies.columns:
    all_genres = sorted(set(g for s in movies['genre'].dropna() for g in s.split(',')))
    genre_filter = st.selectbox("🎭 Filter by genre (optional):", ["All"] + all_genres)
else:
    genre_filter = "All"

# Filter movies based on genre
if genre_filter != "All":
    filtered_movies = movies[movies['genre'].str.contains(genre_filter, na=False)]
else:
    filtered_movies = movies

# Handle edge case: No movies in filtered set
if filtered_movies.empty:
    st.warning("⚠️ No movies found in this genre.")
    st.stop()

# Recreate required data for filtered set
movie_titles = pd.Series(filtered_movies.index, index=filtered_movies['title'])
vectors = vectorize_and_reduce(filtered_movies['content'])
model = build_nn_index(vectors)

# Input + button (side by side)
col1, col2 = st.columns([4, 1])
with col1:
    search_input = st.text_input("🔍 Enter part of a movie title:")
with col2:
    search_clicked = st.button("Recommend")

# Recommendation logic after button click
if search_clicked:
    if not search_input.strip():
        st.warning("Please enter a movie title before clicking.")
    else:
        matched_options = [title for title in movie_titles.index if search_input.lower() in title.lower()]
        matched_options = list(dict.fromkeys(matched_options))

        if matched_options:
            selected_movie = st.selectbox("🎞️ extra recommendations:", matched_options)
            if selected_movie:
                st.subheader("📽️ You might also like:")
                recs = recommend(selected_movie, movie_titles, vectors, model, filtered_movies)
                if recs == ["❌ Movie not found."]:
                    st.error("Movie not found. Please try another.")
                else:
                    for movie in recs:
                        st.markdown(f"- {movie}")
        else:
            st.warning("No matching movies found.")