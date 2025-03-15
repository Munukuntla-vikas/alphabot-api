from transformers import pipeline

# Load FinBERT Sentiment Analysis Model
sentiment_pipeline = pipeline("text-classification", model="ProsusAI/finbert")


def analyze_sentiment(message_text):
    """Analyze sentiment using FinBERT"""
    result = sentiment_pipeline(message_text)[0]
    label = result['label']  # Returns 'positive', 'negative', or 'neutral'

    # Convert FinBERT labels to financial sentiment labels
    if label == "positive":
        return "Bullish 🟢"
    elif label == "negative":
        return "Bearish 🔴"
    else:
        return "Neutral ⚪"
