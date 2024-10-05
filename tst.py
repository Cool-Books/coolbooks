#!/usr/bin/env python3
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.errorhandler(ValueError)
def handle_value_error(error):
    """Handles ValueError exceptions"""
    return jsonify({
        'Error': 'ValueError occurred',
        'Message': str(error),
    }), 400  # 400 Bad Request (or any other status code you prefer)

@app.route('/', methods=['POST'])
def test_error():
    data = request.get_json()
    data['id'] = '1234567'
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)