import pandas as pd
import ast

# Load data
movies = pd.read_csv("movies_metadata.csv", low_memory=False)
keywords = pd.read_csv("keywords.csv")

# Clean and merge
movies = movies[['id', 'title', 'overview', 'genres']]
keywords['id'] = keywords['id'].astype(str)
movies['id'] = movies['id'].astype(str)
movies = movies.merge(keywords, on='id')

# Parse genres and keywords
def parse(text):
    try:
        return " ".join([item['name'] for item in ast.literal_eval(text)])
    except:
        return ""

movies['genres'] = movies['genres'].apply(parse)
movies['keywords'] = movies['keywords'].apply(parse)

# Fill NaNs and create content field
movies['overview'] = movies['overview'].fillna('')
movies['content'] = movies['overview'] + ' ' + movies['genres'] + ' ' + movies['keywords']

# Save cleaned CSV
movies[['title', 'genres', 'overview', 'keywords', 'content']].to_csv("clean_movies_dataset.csv", index=False)