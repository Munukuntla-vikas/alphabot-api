from flask import Flask, request, jsonify
from trending_topics import extract_topics
from preprocess_text import clean_text

app = Flask(__name__)

messages_db = []  # Store processed messages temporarily

@app.route("/process-message", methods=["POST"])
def process_message():
    """Receives messages and updates trending topics."""
    data = request.json
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    # Clean message and store it
    cleaned_message = clean_text(message)
    messages_db.append(cleaned_message)

    # Extract trending topics
    trending_topics = extract_topics(messages_db, num_clusters=5)

    return jsonify({"message": "Processed successfully", "trending_topics": trending_topics}), 200

if __name__ == "__main__":
    app.run(debug=True, port=10000)
