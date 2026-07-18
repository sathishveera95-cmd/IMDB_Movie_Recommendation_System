import joblib
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.metrics.pairwise import cosine_similarity

from preprocessing.text_utils import clean_text


class StorylineRecommender:

    def __init__(self):

        print("Loading models...")

        self.movies = pd.read_csv(
            "dataset/imdb_movies_processed.csv"
        )

        self.vectorizer = joblib.load(
            "models/tfidf_vectorizer.pkl"
        )

        self.tfidf_matrix = joblib.load(
            "models/tfidf_matrix.pkl"
        )

        print("Models Loaded Successfully!")

    def recommend(self, storyline, top_n=10):

        # Clean user input
        clean_story = clean_text(storyline)

        # Convert to TF-IDF vector
        query_vector = self.vectorizer.transform(
            [clean_story]
        )

        # Compute cosine similarity
        similarity_scores = cosine_similarity(
            query_vector,
            self.tfidf_matrix
        ).flatten()

        # Get indices of top similar movies
        top_indices = similarity_scores.argsort()[::-1][:top_n]

        recommendations = []

        for idx in top_indices:

            recommendations.append({

                "Movie Name":
                    self.movies.iloc[idx]["Movie Name"],

                "Similarity":
                    round(float(similarity_scores[idx]), 4)

            })

        return pd.DataFrame(recommendations)


if __name__ == "__main__":

    recommender = StorylineRecommender()

    storyline = input(
        "\nEnter Storyline:\n"
    )

    result = recommender.recommend(storyline)

    print("\nRecommended Movies\n")

    print(result)