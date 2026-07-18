import pandas as pd

# Load dataset
df = pd.read_csv("dataset/imdb_movies_2024.csv")

print("=" * 60)
print("Original Dataset")
print("=" * 60)
print(df.shape)

# Remove duplicate rows
df = df.drop_duplicates()

# Remove rows where storyline is missing
df = df.dropna(subset=["Storyline"])

# Remove rows with empty storylines
df["Storyline"] = df["Storyline"].astype(str).str.strip()
df = df[df["Storyline"] != ""]

# Reset index
df = df.reset_index(drop=True)

print("\nAfter Cleaning")
print(df.shape)

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

# Save cleaned dataset
df.to_csv(
    "dataset/imdb_movies_cleaned.csv",
    index=False,
    encoding="utf-8"
)

print("\nCleaned dataset saved successfully!")