import os
import joblib

from sklearn.metrics.pairwise import cosine_similarity

print("=" * 60)
print("Loading TF-IDF Matrix")
print("=" * 60)

tfidf_matrix = joblib.load("models/tfidf_matrix.pkl")

print("Matrix Shape :", tfidf_matrix.shape)

print("\nCalculating Cosine Similarity...")

similarity_matrix = cosine_similarity(tfidf_matrix)

print("Similarity Matrix Shape :", similarity_matrix.shape)

os.makedirs("models", exist_ok=True)

joblib.dump(
    similarity_matrix,
    "models/similarity_matrix.pkl"
)

print("\nSimilarity Matrix Saved Successfully!")