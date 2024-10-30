#!/usr/bin/env python3
"""Books endpoint"""
from models.book import Books
import os
from api.v1.views import app_views
from flask import jsonify, abort, request, session, current_app
from werkzeug.utils import secure_filename


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

def allowed_file(filename):
    """checks the validity of the book cover"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@app_views.route('/post_book/', strict_slashes=False, methods=['POST'])
def post_a_book():
    """Allows for posting a book"""
    # if 'user_id' not in session:
    #     abort(401)


    # Retrieve form data
    title = request.form.get('title')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
    published_date = request.form.get('published_date')
    description = request.form.get('description')
    edition = request.form.get('edition')
    genre = request.form.get('genre')
    content = request.form.get('content')


    existing_book = Books.search({'title': title, 'author': author})
    if existing_book:
        return jsonify({'Error': "Book already exists"}), 400

    if 'cover' not in request.files:
        return jsonify({'error': 'No cover image uploaded'}), 400

    file = request.files['cover']
    if file and allowed_file(file.filename):
        upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        cover_url = f'{filename}'
        kwargs = {'title': title, 'author': author, 'cover': cover_url, 'isbn': isbn, 'content': content,
                  'description': description, 'user_id': None, 'published_date': published_date,
                  'edition': edition, 'genre': genre}

        book = Books(**kwargs)
        #book.user_id = request.current_user.id
        book.save()
        return jsonify({'success': f'{book.title} successfully added!'})
    else:
        return jsonify({'error': 'Invalid file format'}), 400


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
