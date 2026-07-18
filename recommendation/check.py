import pandas as pd

df = pd.read_csv("dataset/imdb_movies_processed.csv")

movies = [
    "Dune: Part Two",
    "Mafia the Don"
]

for movie in movies:
    row = df[df["Movie Name"] == movie]

    print("=" * 80)
    print(movie)
    print("=" * 80)

    print("\nOriginal Storyline:\n")
    print(row["Storyline"].values[0])

    print("\nClean Storyline:\n")
    print(row["Clean_Storyline"].values[0])