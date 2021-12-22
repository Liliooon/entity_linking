from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html.j2')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['input_text']
    processed_text = text.upper()
    return render_template('index.html.j2', output_text=processed_text)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
