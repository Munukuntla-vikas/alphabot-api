from flask import Flask, request, jsonify
from influencer_monitoring import check_influencer_mentions
from preprocess_text import clean_text
from trending_topics import extract_topics
from data_store import save_message, get_messages, set_influencers

app = Flask(__name__)

@app.route("/set-influencers", methods=["POST"])
def set_group_influencers():
    """Allows users to set influencers for their group."""
    data = request.json
    group_id = str(data.get("group_id"))
    influencers = data.get("influencers", [])

    if not group_id or not influencers:
        return jsonify({"error": "Group ID and influencers are required"}), 400

    set_influencers(group_id, influencers)
    return jsonify({"message": "Influencers updated successfully"}), 200

@app.route("/process-message", methods=["POST"])
def process_message():
    """Receives messages, checks influencers, and tracks trending topics."""
    data = request.json
    group_id = str(data.get("group_id"))
    message = data.get("message", "")

    if not group_id or not message:
        return jsonify({"error": "Group ID and message are required"}), 400

    # Clean message and store it
    cleaned_message = clean_text(message)
    save_message(group_id, cleaned_message)

    # Check for influencer mentions
    influencers_mentioned = check_influencer_mentions(group_id, message)

    # Extract trending topics for the group
    trending_topics = extract_topics(get_messages(group_id), num_clusters=5)

    response = {
        "message": "Processed successfully",
        "trending_topics": trending_topics,
        "influencer_mentions": influencers_mentioned if influencers_mentioned else "No influencers mentioned"
    }

    return jsonify(response), 200

if __name__ == "__main__":
    app.run(debug=True, port=10000)
