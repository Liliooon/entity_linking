from typing import *

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jsonrpc import JSONRPC

from controller import EntityLinkingController

app = Flask(__name__)
CORS(app)
jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)

controller = EntityLinkingController()


@jsonrpc.method("API.get_entities")
def get_entities(
    text: str, return_html: bool = True, return_wiki_entities: bool = True
) -> Dict[str, Any]:
    result = controller.get_entities(text, return_html, return_wiki_entities)
    return result


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
