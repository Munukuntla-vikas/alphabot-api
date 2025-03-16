from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def extract_topics(messages, num_clusters=5):
    if len(messages) < num_clusters:
        num_clusters = max(1, len(messages))  # Ensure at least 1 cluster

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(messages)

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(X)

    topic_keywords = {}
    for i, center in enumerate(kmeans.cluster_centers_):
        keywords = [vectorizer.get_feature_names_out()[index] for index in center.argsort()[-5:]]
        topic_keywords[f"Topic {i+1}"] = ", ".join(keywords)

    return topic_keywords
