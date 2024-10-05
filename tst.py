#!/usr/bin/env python3
from flask import Flask, jsonify

app = Flask(__name__)

@app.errorhandler(ValueError)
def handle_value_error(error):
    """Handles ValueError exceptions"""
    return jsonify({
        'Error': 'ValueError occurred',
        'Message': str(error),
    }), 400  # 400 Bad Request (or any other status code you prefer)

@app.route('/')
def test_error():
    return jsonify({'success': 'book success'})

def ret_error():
    get_err()
def get_err():
    raise ValueError('This is an error')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    