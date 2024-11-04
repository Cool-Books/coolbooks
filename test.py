#!/usr/bin/env python3
from models.book import Books
from models.user import User

User._delete_all()
# Books._delete_all()
# kwargs = {'author': 'fatty', 'title': 'suko is a boy', 'content': 'suko went to sch'}
# book = Books(**kwargs)
# print(book.id)
# book.save()
# print(Books.get("4007edf9-535c-4d4b-b255-546210ac8337"))
# book_to_delete = Books.search({'_author': "fatty"})
# print(book_to_delete[0].to_json())
# book_to_delete[0].update({'author': 'james'})
# print(book_to_delete[0].to_json())
# print(Books.all())
# print(Books.search({'author': 'King'})[0].to_json())
# print(DATA)
# get_book = Books.update({'author': 'suko'}, 'ola')
# print(get_book.author)
