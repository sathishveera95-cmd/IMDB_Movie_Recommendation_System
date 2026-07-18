import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


# Stopwords
STOP_WORDS = set(stopwords.words("english"))

# Lemmatizer
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    """
    Clean movie storyline text.

    Steps:
    1. Lowercase
    2. Remove HTML tags
    3. Remove URLs
    4. Remove punctuation
    5. Remove numbers
    6. Remove extra spaces
    7. Tokenize
    8. Remove stopwords
    9. Lemmatize
    """

    if not isinstance(text, str):
        return ""

    # Lowercase
    text = text.lower()

    # Remove HTML
    text = re.sub(r"<.*?>", " ", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Remove punctuation
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Remove numbers
    text = re.sub(r"\d+", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Tokenization
    tokens = word_tokenize(text)

    # Stopword removal + Lemmatization
    cleaned = []

    for word in tokens:

        if word not in STOP_WORDS and len(word) > 2:

            cleaned.append(
                lemmatizer.lemmatize(word)
            )

    return " ".join(cleaned)