#!/usr/bin/env venv/bin/python

from flask import Flask, jsonify, request

import random

app = Flask(__name__)


@app.route('/get-random-nums', methods=['GET'])
def get_random_nums():
    try:
        numbers = [random.randint(-100, 100) for _ in range(10)]
        return jsonify({'numbers': numbers})
    except ValueError:
        return jsonify({'error': 'invalid number'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5002)