import os
import requests
from flask import Flask, request, jsonify
from influencer_monitoring import check_influencer_mentions
from preprocess_text import clean_text
from trending_topics import extract_topics
from data_store import save_message, get_messages, set_influencers

app = Flask(__name__)

OPEN_SERV_API_KEY = os.getenv("OPEN_SERV_API_KEY", "4d4eaf7cf09f468e9b7ef6f142aa46be")
OPEN_SERV_URL = "https://api.openserv.ai/v1/execute"

@app.route("/process-message", methods=["POST"])
def process_message():
    """Receives messages, checks influencers, tracks topics, and sends data to OpenServ."""
    data = request.json
    group_id = str(data.get("group_id"))
    message = data.get("message", "")

    if not group_id or not message:
        return jsonify({"error": "Group ID and message are required"}), 400

    # Clean and store message
    cleaned_message = clean_text(message)
    save_message(group_id, cleaned_message)

    # Check for influencer mentions
    influencers_mentioned = check_influencer_mentions(group_id, message)

    # Extract trending topics for the group
    trending_topics = extract_topics(get_messages(group_id), num_clusters=5)

    # Prepare data for OpenServ
    openserv_payload = {
        "type": "do-task",
        "task": {
            "description": "Sentiment & Trend Analysis",
            "input": message,
            "sentiment": "Neutral",  # You can integrate FinBERT here
            "trending_topics": trending_topics,
            "influencer_mentions": influencers_mentioned if influencers_mentioned else []
        }
    }

    headers = {
        "x-openserv-key": OPEN_SERV_API_KEY,
        "Content-Type": "application/json"
    }

    # Send to OpenServ
    response = requests.post(OPEN_SERV_URL, json=openserv_payload, headers=headers)
    openserv_response = response.json()

    return jsonify({
        "message": "Processed successfully",
        "openserv_response": openserv_response
    }), response.status_code

if __name__ == "__main__":
    app.run(debug=True, port=10000)
