#!/usr/bin/env python3
from models.base import DATA
from models.book import Books
Books.load_from_file()

book = Books.search({'id': 'da92c6c3-f66e-41f9-873a-4ab170818668'})
book = book[0]
book.update({'genre': 'drama', 'author': 'suko'})
print(book.to_json())
