#!/usr/bin/env python3
"""cool books app"""
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"coolbooks/*": {"origins": "*"}})

@app.errorhandler(ValueError)
def not_found(error):
    """handles 404"""
    return jsonify({
        'Error': str(error),
        'Status Code': 400,
    }), 400

@app.errorhandler(404)
def page_not_found(error):
    """handles 404"""
    return jsonify({"Error": "Page not found"})


if __name__ == '__main__':
    app.run(debug=True)