from flask import Flask, render_template, request, jsonify
from model import chatbot_response
from utils import log_chat

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        response = chatbot_response(user_input)
        log_chat(user_input, response)
        return jsonify({"response": response})
    except Exception as e:
        print("Route Error:", e)
        return jsonify({"response": "Internal server error occurred."})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
