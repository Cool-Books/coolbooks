#!/usr/bin/env python3
"""testing books model"""
import unittest
from parameterized import parameterized
from datetime import datetime
from models.book import Books



class TestBooks(unittest.TestCase):
    """testing books"""
    def setUp(self):
        """before all test instances"""
        self.book = Books()
    
    @parameterized.expand([
        (None,),
        ('',),
        ('Mojibola'),
        ('Mojibola05'),
        ({},),
        ('name too long',)
    ])
    def test_author(self, name):
        """testing author"""
        if name == 'name too long':
            name = name * 30
            with self.assertRaises(ValueError) as context:
                self.book.author = name
                self.assertEqual(str(context.exception), 'Name too long')

        if name == 'Mojibola':
            self.book.author = name
            self.assertEqual(self.book.author, name)

        elif name == {} or 'Mojibola05':
            with self.assertRaises(ValueError) as context:
                self.book.author = name
                self.assertEqual(str(context.exception), 'Invalid name')
        else:
            with self.assertRaises(ValueError) as context:
                self.book.author = name
                self.assertEqual(str(context.exception), 'Name must not be empty')            

    def test_isbn(self):
        """test_isbn"""
        self.book.isbn = None
        self.assertIsInstance(self.book.isbn, str)
    @parameterized.expand([
        (None,),
        ('',),
        ('The sun')
    ])
    def test_title(self, title):
        """test_title"""
        if title == 'The sun':
            self.book.title = title
            self.assertEqual(self.book.title, title)
        else:
            with self.assertRaises(ValueError) as context:
                self.book.title = title
                self.assertEqual(str(context.exception), "Title cannot be empty")
    @parameterized.expand([
        (None,),
        ('time',)
    ])
    def test_year_of_publish(self, time):
        """test year of publish"""
        if time == 'time':
            time = datetime.strftime(datetime.now(), '%d-%m-%Y')
            self.book.year_of_publish = time
            self.assertEqual(self.book.year_of_publish, datetime.strptime(time, '%d-%m-%Y'))
        else:
            self.book.year_of_publish = time
            self.assertIsInstance(self.book.year_of_publish, datetime)
        
    def test_edition(self):
        """test_edition"""
        book = Books(edition='First edition')
        self.assertEqual(book.edition, 'First edition')
    @parameterized.expand([
        (None,),
        ('short desc',),
        ('long desc',)
    ])
    def test_description(self, desc):
        """testing description"""
        if desc is None:
            self.book.description = desc
            self.assertEqual(self.book.description, desc)
        elif desc == 'short desc':
            self.book.description = desc
            self.assertEqual(self.book.description, desc)
        else:
            desc = desc * 500
            with self.assertRaises(ValueError) as context:
                self.book.description = desc
                self.assertEqual(str(context.exception), 'description too long')

    def test_content(self):
        """test_content"""
        content = 'too short'
        with self.assertRaises(ValueError) as context:
            self.book.content = content
            self.assertEqual(str(context.exception), 'Content cannot be less than 500 words')
    