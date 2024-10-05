#!/usr/bin/env python3
from models.base import DATA
from models.book import Books


kwargs = {'author': 'suko', 'title': 'suko is a boy', 'content': 'suko went to sch'}
book = Books(**kwargs)
print(book.id)
book.save()
get_book = Books.update({'author': 'suko'}, 'ola')
print(get_book.author)
