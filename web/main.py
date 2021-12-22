from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    firstname = request.args.get('firstname', '')
    res = requests.post('http://api:8000/people/', data={'firstname': firstname})
    print(f'!!!!!!! {res}', flush=True)
    items = requests.get('http://api:8000/people/').json().get('_items', [])
    return render_template('index.html.j2', firstname=firstname, items=items)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
