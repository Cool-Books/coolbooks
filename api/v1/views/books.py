#!/usr/bin/env python3
"""books endpoint"""
from crypt import methods

from models.book import Books
from api.v1.views import app_views
from flask import jsonify, abort, request

@app_views.route('/all_books/<isbn>', strict_slashes=False, methods=['GET'])
def get_a_book(isbn: str):
    """get a book from the available books"""
    get_book = Books.search({'isbn': isbn})[0]
    if get_book is None or not get_book:
        abort(404)
    get_book.incr_time_called()
    return jsonify(Books.get(get_book.id).to_json())

@app_views.route('/post_book', strict_slashes=False, methods=['POST'])
def post_a_book():
    """allows for posting a book"""
    kwargs = request.get_json()
    # ----------- to be implemented later -------------
    # kwargs.id = request.current_user.id
    # ---------- end ---------------
    book = Books(**kwargs)
    book.save()
    return jsonify({'Success': f'{book.title} successfully addded!'})

@app_views.route('/all_books/<isbn>', strict_slashes=False, methods=['DELETE'])
def del_book(isbn):
    """deletes a book"""
    deleted_book = Books.delete_a_book(isbn)
    return jsonify({'Success': f'{deleted_book} successfully deleted'})

@app_views.route('/all_books/<isbn>', strict_slashes=False, methods=['PATCH'])
def update_book(isbn: str) -> str:
    """update a book"""
    book = Books.search({'isbn': isbn})
    if book is None or not book:
        abort(404)
    book = book[0]
    data = request.get_json()
    book.update(data)
    return jsonify({'Success': f"{book.title} updated successfully"})
