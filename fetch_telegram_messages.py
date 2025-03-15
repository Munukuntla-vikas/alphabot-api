import requests
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download the VADER lexicon
nltk.download('vader_lexicon')

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Replace with your Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7925251700:AAE8zDclP8xTK0-VNNKZhTgf-ZfuMDSzHzE"

# Updated API URL
ALPHABOT_API_URL = "https://alphabot-api.onrender.com/openserv-agent"


def send_to_alphabot_api(message_text, sentiment):
    """Send analyzed sentiment to the Alphabot API."""
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "message": message_text,
        "sentiment": sentiment
    }

    response = requests.post(ALPHABOT_API_URL, json=data, headers=headers)

    if response.status_code == 200:
        print(f"✅ Successfully sent to Alphabot API: {sentiment}")
    else:
        print(f"❌ Error sending to Alphabot API: {response.text}")


def handle_messages(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    message_text = update.message.text

    # Perform Sentiment Analysis
    sentiment_score = sia.polarity_scores(message_text)['compound']

    # Classify Sentiment
    if sentiment_score >= 0.02:
        sentiment = "Bullish 🟢"
    elif sentiment_score <= -0.02:
        sentiment = "Bearish 🔴"
    else:
        sentiment = "Neutral ⚪"

    print(f"Chat ID: {chat_id}, Message: {message_text}, Sentiment: {sentiment}")

    # Send result to Alphabot API
    send_to_alphabot_api(message_text, sentiment)


def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

    # Start the bot
    print("Bot is listening for messages...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
