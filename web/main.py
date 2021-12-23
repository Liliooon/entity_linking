from flask import Flask, render_template, request, jsonify
from api_client import JsonRpcApiClient
from flask_cors import CORS
from typing import *

app = Flask(__name__)
CORS(app)
client = JsonRpcApiClient()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/rpc", methods=["POST"])
def api_request():
    text: str = request.json['text']
    response: Dict[str, Any] = client.process_text(text, decode_html=False)
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9000)
