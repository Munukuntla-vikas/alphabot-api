from flask import Flask, request, jsonify

app = Flask(__name__)

# Home route to check if the API is running
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Alphabot API is running"}), 200

# Endpoint to receive sentiment data from Telegram bot
@app.route("/openserv-agent", methods=["POST"])
def openserv_agent():
    data = request.json
    print(f"Received data: {data}")

    # Simulate processing and response
    return jsonify({"message": "Received successfully!", "data": data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Change port to 5000 for Render
