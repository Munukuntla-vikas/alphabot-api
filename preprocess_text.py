import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK data (run this once)
nltk.download("punkt")
nltk.download("stopwords")

def clean_text(text):
    """Remove special characters, links, and tokenize text."""
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)  # Remove links
    text = re.sub(r"\W", " ", text)  # Remove special characters
    words = word_tokenize(text.lower())  # Convert to lowercase and tokenize
    words = [word for word in words if word not in stopwords.words("english")]  # Remove stopwords
    return " ".join(words)
