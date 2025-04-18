import pandas as pd

# Step 1: Load the data
try:
    movies_df = pd.read_csv('mymoviedb.csv',
                            engine='python',
                            on_bad_lines='skip',
                            encoding='utf-8')
    print("Data loaded successfully!\n")

    # Step 2: Clean column names (optional but safe)
    movies_df.columns = movies_df.columns.str.strip().str.lower()
    print("Available columns:", movies_df.columns.tolist())

    # Step 3: Convert vote_average to numbers
    movies_df['vote_average'] = pd.to_numeric(movies_df['vote_average'], errors='coerce')

    print("\nSample data:")
    print(movies_df.head())

except pd.errors.ParserError as e:
    print(f"Parser Error while reading CSV: {e}")
    movies_df = None
except Exception as e:
    print(f"An error occurred: {e}")
    movies_df = None

# Step 4: Define Recommendation Functions
if movies_df is not None:

    def recommend_by_genre(movie_name, movies_df):
        movie = movies_df[movies_df['title'] == movie_name]

        if movie.empty:
            return f"Movie '{movie_name}' not found."

        genre = movie['genre'].values[0]

        recommended_movies = movies_df[(movies_df['genre'] == genre) & (movies_df['title'] != movie_name)]

        if recommended_movies.empty:
            return f"No recommendations found for genre: {genre}"

        return recommended_movies[['title', 'genre', 'vote_average']]


    def recommend_by_rating_range(movie_name, movies_df):
        bins = [0, 2, 4, 6, 8, 10]
        labels = ['0-2', '2-4', '4-6', '6-8', '8-10']

        movies_df['rating_range'] = pd.cut(movies_df['vote_average'], bins=bins, labels=labels, include_lowest=True)

        movie = movies_df[movies_df['title'] == movie_name]

        if movie.empty:
            return f"Movie '{movie_name}' not found."

        rating_range = movie['rating_range'].values[0]

        recommended_movies = movies_df[(movies_df['rating_range'] == rating_range) & (movies_df['title'] != movie_name)]

        if recommended_movies.empty:
            return f"No recommendations found for rating range: {rating_range}"

        return recommended_movies[['title', 'vote_average', 'rating_range']]


    # Step 5: Example Usage
    movie_name = 'Inception'  # Change to any movie name from your dataset
    print("\nRecommendations by Genre:")
    print(recommend_by_genre(movie_name, movies_df))

    print("\nRecommendations by Rating Range:")
    print(recommend_by_rating_range(movie_name, movies_df))

else:
    print("Movie data could not be loaded, please check your CSV file.")
