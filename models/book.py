#!/usr/bin/env python3
"""book model"""
from datetime import datetime
from multiprocessing import Value
import uuid
import random
from models.base import Base
from models.user import User

TIMESTAMP = "%Y-%m-%dT%H-%M-%S"


class Books(Base):
    """model for all books"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = kwargs.get('title')  # Use setter
        self.author = kwargs.get('author')  # Use setter
        self.isbn = kwargs.get('isbn')  # Use setter
        self.year_of_publish = kwargs.get('year_of_publish')  # Use setter
        self.edition = kwargs.get('edition')
        self.genre = kwargs.get('genre')
        self.description = kwargs.get('description')  # Use setter
        self.content = kwargs.get('content')  # Use setter

    @property
    def author(self) -> str:
        """returns author"""
        return self._author
    
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
            self.is_valid_isbn10(get_isbn)
            if Books.search({'isbn': get_isbn}):
                raise ValueError('Book with the same ISBN exists')
            self._isbn = get_isbn

    @property
    def year_of_publish(self):
        """return year of publish"""
        return self._year_of_publish

    @year_of_publish.setter
    def year_of_publish(self, year):
        if year is None:
            self._year_of_publish = self.created_at
        else:
            self._year_of_publish = datetime.strptime(year, TIMESTAMP)

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
        # Generate first 9 random digits
        isbn_digits = [random.randint(0, 9) for _ in range(9)]

        # Calculate checksum (the 10th digit)
        checksum = sum((i + 1) * digit for i, digit in enumerate(isbn_digits)) % 11
        if checksum == 10:
            checksum = 'X'

        # Join digits and checksum into a full ISBN-10 string
        return ''.join(map(str, isbn_digits)) + str(checksum)
    
    @staticmethod
    def is_valid_isbn10(isbn: str) -> bool:
        """Validate an ISBN-10"""
        if len(isbn) != 10:
            raise ValueError('Invalid ISBN provided')
        
        # Calculate checksum
        total = 0
        for i in range(9):
            if not isbn[i].isdigit():
                raise ValueError('Invalid ISBN provided')
            total += (i + 1) * int(isbn[i])
        
        # Handle checksum character
        checksum = isbn[-1]
        if checksum == 'X':
            total += 10 * 10
        elif checksum.isdigit():
            total += 10 * int(checksum)
        else:
            raise ValueError('Invalid ISBN provided')
        
        # ISBN-10 is valid if the total modulo 11 is 0
        return total % 11 == 0
    
    @classmethod
    def delete_a_book(cls, isbn: str):
        """Delete a book from the database."""
        if isbn is None or not isbn or not isinstance(isbn, str):
            raise ValueError('Invalid request')

        # Search for the book by ISBN
        get_book_for_delete = Books.search({'isbn': isbn})
        
        if not get_book_for_delete:
            raise ValueError('Book not found')

        # Get the first book found
        book_to_delete = get_book_for_delete[0]
        
        # Extract the book's title for return
        book_title = book_to_delete.title

        if book_to_delete.remove():
            return book_title
        else:
            raise ValueError("Couldn't process the request")
