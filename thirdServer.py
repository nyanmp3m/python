#!/usr/bin/env venv/bin/python

from flask import Flask, jsonify, request

import random

app = Flask(__name__)


@app.route('/generate-random-chars', methods=['POST'])
def get_random_nums():
    try:
        data = request.get_json()
        count = data.get('count', 5)
        chars = [random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ') for _ in range(count)]
        return jsonify({'chars': chars})
    except ValueError:
        return jsonify({'error': 'invalid number'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5003)