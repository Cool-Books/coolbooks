#!/usr/bin/env python3
"""Books endpoint"""
from models.book import Books
import os
from api.v1.views import app_views
from flask import jsonify, abort, request, session, current_app
from werkzeug.utils import secure_filename


@app_views.route('/all_books/<isbn>', strict_slashes=False, methods=['GET'])
def get_a_book(isbn):
    """
    Get a book from the available books
    ---
    tags:
      - books
    parameters:
      - in: path
        name: isbn
        type: string
        required: true
        description: ISBN of the book to retrieve
    responses:
      200:
        description: A book object
        schema:
          id: Book
          properties:
            id:
              type: string
            title:
              type: string
            author:
              type: string
            isbn:
              type: string
            published_date:
              type: string
            description:
              type: string
            edition:
              type: string
            genre:
              type: string
            cover:
              type: string
            content:
              type: string
      401:
        description: Unauthorized – user not logged in
      404:
        description: Book not found
    """
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
    """
Post a new book with cover image
---
tags:
  - books
consumes:
  - multipart/form-data
produces:
  - application/json
parameters:
  - in: formData
    name: title
    schema:
      type: string
    required: true
    description: Title of the book
  - in: formData
    name: author
    schema:
      type: string
    required: true
    description: Author of the book
  - in: formData
    name: isbn
    schema:
      type: string
    required: true
    description: ISBN identifier
  - in: formData
    name: published_date
    schema:
      type: string
    required: false
    description: Date of publication
  - in: formData
    name: description
    schema:
      type: string
    required: false
    description: Brief description
  - in: formData
    name: edition
    schema:
      type: string
    required: false
    description: Edition of the book
  - in: formData
    name: genre
    schema:
      type: string
    required: false
    description: Genre/category
  - in: formData
    name: content
    schema:
      type: string
    required: false
    description: Main content text
  - in: formData
    name: cover
    type: file
    required: true
    description: Cover image file (png/jpg/jpeg)
responses:
  200:
    description: Book successfully added
    content:
      application/json:
        schema:
          type: object
          properties:
            success:
              type: string
              example: "My Book successfully added!"
  400:
    description: Bad request (missing data, invalid file, or duplicate book)
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
    """
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
        return jsonify({'Error': 'No cover image uploaded'}), 400

    file = request.files['cover']
    if file and allowed_file(file.filename):
        upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        cover_url = f'{filename}'
        kwargs = {
            'title': title, 'author': author, 'cover': cover_url,
            'isbn': isbn, 'content': content, 'description': description,
            'user_id': None, 'published_date': published_date,
            'edition': edition, 'genre': genre
        }

        book = Books(**kwargs)
        # book.user_id = request.current_user.id
        book.save()
        return jsonify({'success': f'{book.title} successfully added!'})
    else:
        return jsonify({'Error': 'Invalid file format'}), 400



@app_views.route('/all_books/<isbn>', strict_slashes=False, methods=['DELETE'])
def del_book(isbn):
    """
Delete a book by ISBN
---
tags:
  - books
parameters:
  - in: path
    name: isbn
    schema:
      type: string
    required: true
    description: ISBN of the book to delete
responses:
  200:
    description: Deletion success message
    content:
      application/json:
        schema:
          type: object
          properties:
            Success:
              type: string
              example: "1234567890 successfully deleted"
  401:
    description: Unauthorized – user not logged in
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
              example: "User not logged in"
  403:
    description: Forbidden – user is not the owner of the book
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
              example: "You are not the owner of this book"
  404:
    description: Book not found
    content:
      application/json:
        schema:
          type: object
          properties:
            Error:
              type: string
              example: "Book not found"
    """
    # Your code for deleting the book by ISBN here
    if 'user_id' not in session:
        abort(401)
    book = Books.search({'isbn': isbn})
    if not book:
        abort(404)
    book = book[0]
    if book.user_id != request.current_user.id:
        abort(403)
    deleted_book = Books.delete_a_book(isbn)
    return jsonify({'Success': f'{deleted_book} successfully deleted'})


@app_views.route('/all_books/<isbn>', strict_slashes=False, methods=['PATCH'])
def update_book(isbn) -> str:
    """
Update an existing book’s fields
---
tags:
  - books
parameters:
  - in: path
    name: isbn
    schema:
      type: string
    required: true
    description: ISBN of the book to update
  - in: body
    name: data
    required: true
    description: JSON object with fields to update
    content:
      application/json:
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            published_date:
              type: string
            description:
              type: string
            edition:
              type: string
            genre:
              type: string
            cover:
              type: string
            content:
              type: string
responses:
  200:
    description: Update success message
    content:
      application/json:
        schema:
          type: object
          properties:
            Success:
              type: string
              example: "Some Book updated successfully"
  401:
    description: Unauthorized – user not logged in
  403:
    description: Forbidden – user is not the owner of the book
  404:
    description: Book not found
    """
    if 'user_id' not in session:
        abort(401)
    book = Books.search({'isbn': isbn})
    if not book:
        abort(404)
    book = book[0]
    if book.user_id != request.current_user.id:
        abort(403)
    data = request.get_json()
    book.update(data)
    return jsonify({'Success': f"{book.title} updated successfully"})
