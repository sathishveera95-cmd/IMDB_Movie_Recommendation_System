import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

# Load processed dataset
df = pd.read_csv("dataset/imdb_movies_processed.csv")

print("=" * 60)
print("Dataset Loaded")
print("=" * 60)
print(df.shape)

# Create TF-IDF Vectorizer
vectorizer = TfidfVectorizer(
    max_features=15000,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.8,
    sublinear_tf=True
)



print("\nCreating TF-IDF Matrix...")

tfidf_matrix = vectorizer.fit_transform(
    df["Combined_Features"]
)

print("TF-IDF Matrix Shape:", tfidf_matrix.shape)

# Create models folder if it doesn't exist
os.makedirs("models", exist_ok=True)

# Save vectorizer and matrix
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")
joblib.dump(tfidf_matrix, "models/tfidf_matrix.pkl")

print("\nTF-IDF model saved successfully!")