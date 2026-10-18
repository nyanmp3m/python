#!/usr/bin/env venv/bin/python

from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)


@app.route('/get-current-time', methods=['GET'])
def get_current_time():
    return jsonify({
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001)