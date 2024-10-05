#!/usr/bin/env python3
"""test"""
from datetime import date, datetime
import unittest
import uuid
import json
from os import path
from parameterized import parameterized
from unittest.mock import mock_open, patch
from models.base import Base, DATA, TIMESTAMP

class Books(Base):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class TestingBase(unittest.TestCase):
    """testing the Base features"""
    def setUp(self):
        """should be called before every test"""
        global DATA
        global book
        global t_class
        DATA = {}
        book = Books(id='1', created_at="2024-09-23T05-47-37",
                             updated_at="2024-09-23T05-47-37", _password='abcd')
        t_class = book.__class__.__name__

    @patch('models.base.DATA', new_callable=dict)
    def test_init(self, mock_dict):
        """testing the init of base"""
        new_book = Books()
        s_class = new_book.__class__.__name__

        # ------- testing model exists in DATA -----
        self.assertIn(s_class, mock_dict)

        # ------- testing for object saved in DATA ---------
        self.assertEqual(mock_dict[s_class], {})

        # Ensure the actual DATA dictionary is unaffected after the test (mock test)
        self.assertNotIn(s_class, DATA)

        # ------- testing for the datetime object ------------
        kwargs = {'created_at': "2024-09-23T05-47-37"}
        expected = datetime.strptime(kwargs.get('created_at'), TIMESTAMP)
        self.assertEqual(book.created_at, expected)

    def test_equality(self):
        """making comparison between instances"""
        book_1 = Books(id=1)
        book_2 = Books(id=1)
        book_3 = Books(id=4)
        # ------ comparing instances of the same model --------
        self.assertEqual(book_1, book_2)
        self.assertNotEqual(book_1, book_3)

        # ------ comparing instances of different model ------
        base = Base(id=1)
        self.assertNotEqual(book_1, base)
        # more tests to be added here

    def test_json(self):
        """testing obj to json"""
        getJson = book.to_json(False)
        self.assertIsInstance(getJson, dict)
        self.assertIsNone(getJson.get('_password'))
        self.assertNotIsInstance(getJson.get('created_at'), datetime)
        self.assertIsInstance(getJson.get('created_at'), str)
        # more tests to be added here
    @patch('models.base.DATA', new_callable=dict)
    def test_save(self, mock_dict):
        """testing the save method"""
        # Initialize mock_dict[t_class] as an empty dictionary
        mock_dict[t_class] = {}

        get_created_at = book.to_json(False).get('created_at')
        get_updated_at = book.to_json(False).get('updated_at')

        book.save()
        book_id = book.id

        # Test if the book instance is correctly saved
        self.assertIn('1', mock_dict.get(t_class))
        self.assertEqual(book_id, '1')
        self.assertNotEqual(get_created_at, datetime.strftime(book.updated_at, TIMESTAMP))
        self.assertNotEqual(get_updated_at, datetime.strftime(book.updated_at, TIMESTAMP))
    

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_to_file(self, mock_dump, mock_fopen):
        """testing the save to file method"""

        # Mock the 'tell' method to simulate file behavior
        mock_file = mock_fopen.return_value  # Get the mock file handle
        mock_file.tell.return_value = 0  # Simulate an empty file by returning 0

        # Assuming 'book' is already defined as a valid instance of your Books class
        book.save()

        # --------- assert that the file path is called with expected mode ---------
        mock_fopen.assert_called_once_with('.db_{}.json'.format(t_class), 'a+')

        # --------- mock expected data to be saved into file ----------
        expected_data = {book.id: book.to_json(True)}

        # --------- assert that the expected data is saved into file -----------
        mock_dump.assert_called_once_with(expected_data, mock_file)


    @patch('builtins.open', new_callable=mock_open, read_data='{"1": {"name": "Sample Book", "id": "1"}}\n')
    @patch('os.path.exists', return_value=True)  # Ensure the file exists
    @patch('models.base.DATA', new_callable=dict)  # Ensure DATA is reset for each test
    def test_load_from_file(self, mock_dict, mock_exist, mock_fopen):
        """testing the load from file"""

        # Call the load_from_file method on the Books class
        Books.load_from_file()

        # Assert that os.path.exists was called with the correct file path
        mock_exist.assert_called_once_with('.db_Books.json')

        # Assert that open was called with the correct file path and mode ('r')
        mock_fopen.assert_called_once_with('.db_Books.json', 'r')

        # Ensure that the DATA dictionary was populated correctly
        self.assertIn(t_class, mock_dict)
        self.assertIn("1", mock_dict[t_class])  # Check if the key exists
    
    @parameterized.expand([
        ("id=1", []),  # testing with different type
        ({'id': '1'}, None), # testing with id
        # testing with not formatted created_at
        ({'created_at': "2024-09-23T05-47-37"}, []),
        # testing with formatted created_at
        ({'created_at': datetime.strptime("2024-09-23T05-47-37", TIMESTAMP)}, None),
        ({'id': '1', 'created_at': datetime.strptime("2024-09-23T05-47-37", TIMESTAMP)}, None), # testing with two keys
        ({}, None) # empty dictionary should return all instances
    ])
    @patch('models.base.DATA', new_callable=dict)
    def test_search(self, attr, value, mock_dict):
        """mocking and testing the search method"""
        mock_dict[t_class] = {}
        book.save()
        if value is None:
            value = [book]
        self.assertEqual(Books.search(attr), value)
    
    @parameterized.expand([
        ("1", True),
        ("2", None),
        ("", None)
    ])
    @patch('models.base.DATA', new_callable=dict)
    def test_get(self, key, val, mock_dict):
        """mocking and testing get method"""
        mock_dict[t_class] = {}
        book.save()
        if val == True:
            val = book
        self.assertEqual(Books.get(key), val)
