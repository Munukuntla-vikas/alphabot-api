import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# OpenServ API details
OPEN_SERV_API_KEY = os.getenv("OPEN_SERV_API_KEY", "4d4eaf7cf09f468e9b7ef6f142aa46be")
OPEN_SERV_URL = "https://api.openserv.ai/execute"  # Update if needed

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Alphabot API is running"}), 200

@app.route("/openserv-agent", methods=["POST"])
def openserv_agent():
    data = request.json
    print(f"📥 Received data from Telegram Bot: {data}")

    # Validate input data
    if not data or "message" not in data or "sentiment" not in data:
        return jsonify({"error": "Invalid request. 'message' and 'sentiment' are required"}), 400

    # Prepare data for OpenServ
    openserv_payload = {
        "type": "do-task",
        "task": {
            "description": "Sentiment Analysis",
            "input": data.get("message", ""),
            "result": data.get("sentiment", "")
        }
    }

    headers = {
        "x-openserv-key": OPEN_SERV_API_KEY,
        "Content-Type": "application/json"
    }

    print(f"🚀 Sending data to OpenServ: {openserv_payload}")

    # Send sentiment result to OpenServ
    response = requests.post(OPEN_SERV_URL, json=openserv_payload, headers=headers)

    print(f"🔄 OpenServ Response Code: {response.status_code}")
    print(f"📩 OpenServ Response Data: {response.text}")

    if response.status_code == 200:
        return jsonify({"message": "Sent to OpenServ successfully", "data": response.json()}), 200
    else:
        return jsonify({"error": "Failed to send to OpenServ", "details": response.text}), 400

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))  # Use Render-assigned port
    app.run(host="0.0.0.0", port=PORT, debug=True)
