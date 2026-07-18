import joblib
import pandas as pd
from rapidfuzz import process


class MovieRecommender:

    def __init__(self):

        self.movies = pd.read_csv(
            "dataset/imdb_movies_processed.csv"
        )

        self.similarity = joblib.load(
            "models/similarity_matrix.pkl"
        )

    def recommend(self, movie_name, top_n=10):

        titles = self.movies["Movie Name"].tolist()

        match = process.extractOne(
            movie_name,
            titles,
            score_cutoff=60
        )

        if match is None:
            return None, None

        movie_name = match[0]

        movie_index = self.movies[
            self.movies["Movie Name"] == movie_name
        ].index[0]

        similarity_scores = list(
            enumerate(self.similarity[movie_index])
        )

        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )

        recommendations = []

        for idx, score in similarity_scores:

            if idx == movie_index:
                continue

            recommendations.append({

                "Movie Name":
                    self.movies.iloc[idx]["Movie Name"],

                "Similarity":
                    round(score, 4)

            })

            if len(recommendations) == top_n:
                break

        return movie_name, pd.DataFrame(recommendations)