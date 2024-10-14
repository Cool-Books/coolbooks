#!/usr/bin/env python3
"""Books endpoint"""
from models.book import Books
from api.v1.views import app_views
from flask import jsonify, abort, request, session

@app_views.route('/all_books/<isbn>', strict_slashes=False, methods=['GET'])
def get_a_book(isbn):
    """Get a book from the available books"""
    if 'user_id' not in session:
        abort(401)
    get_book = Books.search({'isbn': isbn})
    if get_book is None or not get_book:
        abort(404)
    get_book = get_book[0]
    return jsonify(get_book.to_json())

@app_views.route('/post_book/', strict_slashes=False, methods=['POST'])
def post_a_book():
    """Allows for posting a book"""
    if 'user_id' not in session:
        abort(401)
    kwargs = request.get_json()
    book = Books(**kwargs)
    book.user_id = request.current_user.id
    book.save()
    return jsonify({'Success': f'{book.title} successfully added!'})

@app_views.route('/all_books/<isbn>', strict_slashes=False, methods=['DELETE'])
def del_book(isbn):
    """Deletes a book"""
    if 'user_id' not in session:
        abort(401)
    book = Books.search({'isbn': isbn})
    if book is None or not book:
        abort(404)
    book = book[0]
    if book.user_id != request.current_user.id:
        abort(403)
    deleted_book = Books.delete_a_book(isbn)
    return jsonify({'Success': f'{deleted_book} successfully deleted'})

@app_views.route('/all_books/<isbn>', strict_slashes=False, methods=['PATCH'])
def update_book(isbn) -> str:
    """Updates a book"""
    if 'user_id' not in session:
        abort(401)
    book = Books.search({'isbn': isbn})
    if book is None or not book:
        abort(404)
    book = book[0]
    if book.user_id != request.current_user.id:
        abort(403)
    data = request.get_json()
    book.update(data)
    return jsonify({'Success': f"{book.title} updated successfully"})
