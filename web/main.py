import requests
from flask import Flask, render_template, request
import requests
from api_client import JsonRpcApiClient

app = Flask(__name__)
client = JsonRpcApiClient()


@app.route("/")
def index():
    return render_template("index.html.j2")


@app.route("/", methods=["POST"])
def form_submit():
    text = request.form["input_text"]
    result = client.process_text(text)
    if result is not None:
        return render_template(
            "index.html.j2",
            display='ok',
            output_text=result['html'],
            entity_result=result['entities']
        )
    else:
        return render_template(
            "index.html.j2",
            display='error',
            entity_result="Error communicating with api",
            entities=[]
        )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9000)
