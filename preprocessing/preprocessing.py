import pandas as pd

from text_utils import clean_text

df = pd.read_csv("dataset/imdb_movies_cleaned.csv")

print("Cleaning storylines...")

df["Clean_Storyline"] = df["Storyline"].apply(clean_text)

print(df[["Movie Name",
          "Storyline",
          "Clean_Storyline"]].head())

df["Combined_Features"] = (
    df["Movie Name"].fillna("") + " " +
    df["Clean_Storyline"].fillna("")
)

df.to_csv(
    "dataset/imdb_movies_processed.csv",
    index=False
)

print(df[["Movie Name",
          "Storyline",
          "Clean_Storyline",
          "Combined_Features"]].head())

print("\nProcessed dataset saved successfully!")