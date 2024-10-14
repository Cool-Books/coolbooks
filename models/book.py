#!/usr/bin/env python3
"""book model"""
from datetime import datetime
import uuid
import random
from models.base import Base
from models.user import User



class Books(Base):
    """model for all books"""

    def __init__(self, *args, **kwargs):
        self.is_loading = kwargs.get('is_loading', False)
        super().__init__(*args, **kwargs)
        self.title = kwargs.get('title')
        self.author = kwargs.get('author')
        self.isbn = kwargs.get('isbn')
        self.published_date = kwargs.get('published_date')
        self.edition = kwargs.get('edition')
        self.genre = kwargs.get('genre')
        self.description = kwargs.get('description')
        self.content = kwargs.get('content')
        self.time_called = kwargs.get('time_called', 0)
        self.user_id = kwargs.get('user_id')

    @property
    def author(self) -> str:
        """returns author"""
        return self._author

    def incr_time_called(self):
        """this method increments how many times a book
        has been called"""
        self.time_called += 1
        self.save()

    @author.setter
    def author(self, auth: str):
        """sets the author"""
        User.validate_name(auth)
        self._author = auth

    @property
    def isbn(self) -> str:
        """return isbn"""
        return self._isbn

    @isbn.setter
    def isbn(self, get_isbn: str):
        """sets isbn"""
        if get_isbn is None or not get_isbn:
            self._isbn = self.generate_isbn10()
        else:
            if not self.is_loading:
                self.is_valid_isbn10(get_isbn)
                if Books.search({'isbn': get_isbn}):
                    raise ValueError('Book with the same ISBN exists')
            self._isbn = get_isbn

    @property
    def published_date(self):
        """return year of publish"""
        return self._published_date

    @published_date.setter
    def published_date(self, year):
        if year is None:
            self._published_date = datetime.now().year
        else:
            self._published_date = year

    @property
    def description(self) -> str:
        """returns description"""
        return self._description

    @description.setter
    def description(self, desc: str):
        if desc is None or not desc:
            self._description = None
        elif not isinstance(desc, str):
            raise ValueError("Description must be a string")
        else:
            words = desc.split()
            if len(words) > 200:
                raise ValueError("Description too long")
            self._description = desc

    @property
    def title(self) -> str:
        """returns title"""
        return self._title

    @title.setter
    def title(self, get_title: str):
        """sets title"""
        if get_title is None or not isinstance(get_title, str) or not get_title:
            raise ValueError('Title cannot be empty')
        self._title = get_title

    @property
    def content(self) -> str:
        """return content"""
        return self._content

    @content.setter
    def content(self, cont: str):
        """sets content"""
        if cont is None or not cont:
            raise ValueError('Content cannot be empty')
        if not isinstance(cont, str):
            raise ValueError('Contents not recognized')
        self._content = cont

    @staticmethod
    def generate_isbn10() -> str:
        """Generate a valid ISBN-10"""

        isbn_digits = [random.randint(0, 9) for _ in range(9)]


        checksum = sum((i + 1) * digit for i, digit in enumerate(isbn_digits)) % 11
        if checksum == 10:
            checksum = 'X'


        return ''.join(map(str, isbn_digits)) + str(checksum)

    @staticmethod
    def is_valid_isbn10(isbn: str) -> bool:
        """Validate an ISBN-10"""
        if len(isbn) != 10:
            raise ValueError('Invalid ISBN provided')


        total = 0
        for i in range(9):
            if not isbn[i].isdigit():
                raise ValueError('Invalid ISBN provided')
            total += (i + 1) * int(isbn[i])


        checksum = isbn[-1]
        if checksum == 'X':
            total += 10 * 10
        elif checksum.isdigit():
            total += 10 * int(checksum)
        else:
            raise ValueError('Invalid ISBN provided')


        return total % 11 == 0

    @classmethod
    def delete_a_book(cls, isbn: str):
        """Delete a book from the database."""
        if isbn is None or not isbn or not isinstance(isbn, str):
            raise ValueError('Invalid request')


        get_book_for_delete = Books.search({'isbn': isbn})

        if not get_book_for_delete:
            raise ValueError('Book not found')


        book_to_delete = get_book_for_delete[0]


        book_title = book_to_delete.title

        if book_to_delete.remove():
            return book_title
        else:
            raise ValueError("Couldn't process the request")
