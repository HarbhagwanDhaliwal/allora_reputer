from flask import Flask, jsonify, Response
import requests
import json
from reputer_topics import get_truth
import os

API_PORT = int(os.environ.get('API_PORT', 8099))

app = Flask(__name__)

HTTP_RESPONSE_CODE_404 = "404"


@app.route('/reputer/<topic>/<token>/<block_height>')
def get_price(topic, token, block_height):
    result = get_truth(topic, token, block_height)
    if result is not None:
        return str(result), 200
    else:
        return jsonify(
            {'error': 'No price data found for the specified token and block_height'}), HTTP_RESPONSE_CODE_404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=API_PORT)
