import os
import logging
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS


USERFEEDS_API_KEY = os.environ['USERFEEDS_API_KEY']
USERFEEDS_API_URL = os.environ.get('USERFEEDS_API_URL', 'https://api.userfeeds.io/beta')
DOMAINS = [i.strip() for i in os.environ['DOMAINS'].split(',')]


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
cors = CORS(app, resources={r'*': {'origins': DOMAINS}})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    if path == '':
        return render_template('home.html')

    url = '{base}/{path}'.format(base=USERFEEDS_API_URL, path=path)
    params = dict(request.args.items())

    if request.method == 'POST':
        response = requests.post(url, data=request.data, headers={
            'Authorization': USERFEEDS_API_KEY,
            'Content-Type': 'application/json'
        })
    else:
        response = requests.get(url, params=params, headers={
            'Authorization': USERFEEDS_API_KEY
        })

    if response.ok:
        data = response.json()
        return jsonify(data)

    return 'Not Found', 404
