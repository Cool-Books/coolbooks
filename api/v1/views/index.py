#!/usr/bin/env python3
"""index views"""
from flask import jsonify
from api.v1.views import app_views
from models.book import Books


@app_views.route('/all_books', strict_slashes=False, methods=['GET'])
def get_allbooks():
    """displays all books"""
    all_book = [book.title for book in Books.all()]
    return jsonify(all_book)


