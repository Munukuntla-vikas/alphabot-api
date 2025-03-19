import requests
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from sentiment_analysis import analyze_sentiment

# Replace with your Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7925251700:AAE8zDclP8xTK0-VNNKZhTgf-ZfuMDSzHzE"
ALPHABOT_API_URL = "https://alphabot-api-2.onrender.com/process-message"
"

def send_to_alphabot_api(message_text, sentiment):
    """Send analyzed sentiment to the Alphabot API."""
    headers = {"Content-Type": "application/json"}
    data = {"message": message_text, "sentiment": sentiment}

    response = requests.post(ALPHABOT_API_URL, json=data, headers=headers)
    if response.status_code == 200:
        print(f"✅ Sent to Alphabot API: {sentiment}")
    else:
        print(f"❌ Error sending to Alphabot API: {response.text}")

def handle_messages(update: Update, context: CallbackContext):
    """Handle incoming messages and analyze sentiment."""
    chat_id = update.message.chat_id
    message_text = update.message.text

    # Perform Sentiment Analysis using FinBERT
    sentiment = analyze_sentiment(message_text)

    print(f"Chat ID: {chat_id}, Message: {message_text}, Sentiment: {sentiment}")

    # Send result to Alphabot API
    send_to_alphabot_api(message_text, sentiment)

def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

    # Start the bot
    print("🤖 Telegram bot is listening for messages...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
