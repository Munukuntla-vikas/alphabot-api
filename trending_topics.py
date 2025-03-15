from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

def extract_topics(messages, num_clusters=5):
    """Cluster messages into trending topics using TF-IDF and KMeans."""
    vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
    X = vectorizer.fit_transform(messages)

    model = KMeans(n_clusters=num_clusters, random_state=42)
    model.fit(X)

    # Get top words per cluster
    words = vectorizer.get_feature_names_out()
    clusters = {i: [] for i in range(num_clusters)}

    for i, label in enumerate(model.labels_):
        clusters[label].append(messages[i])

    top_topics = {}
    for cluster, texts in clusters.items():
        text_combined = " ".join(texts)
        tfidf_scores = vectorizer.transform([text_combined])
        sorted_indices = np.argsort(tfidf_scores.toarray()).flatten()[::-1]
        top_words = [words[idx] for idx in sorted_indices[:5]]  # Top 5 words
        top_topics[f"Topic {cluster+1}"] = ", ".join(top_words)

    return top_topics
