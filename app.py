import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# OpenServ API details
OPEN_SERV_API_KEY = "4d4eaf7cf09f468e9b7ef6f142aa46be"  # Your actual API key
OPEN_SERV_URL = "https://api.openserv.ai/execute"  # Update if needed

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Alphabot API is running"}), 200

@app.route("/openserv-agent", methods=["POST"])
def openserv_agent():
    data = request.json
    print(f"Received data: {data}")

    # Prepare data for OpenServ
    openserv_payload = {
        "type": "do-task",
        "task": {
            "description": "Sentiment Analysis",
            "input": data["message"],
            "result": data["sentiment"]
        }
    }

    headers = {
        "x-openserv-key": OPEN_SERV_API_KEY,
        "Content-Type": "application/json"
    }

    # Send sentiment result to OpenServ
    response = requests.post(OPEN_SERV_URL, json=openserv_payload, headers=headers)

    if response.status_code == 200:
        return jsonify({"message": "Sent to OpenServ", "data": data}), 200
    else:
        return jsonify({"error": "Failed to send to OpenServ", "details": response.text}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
