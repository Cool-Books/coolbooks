#!/usr/bin/env python3
"""testing user model"""
import unittest
from parameterized import parameterized
from models.user import User


class TestingUser(unittest.TestCase):
    """testing user model"""
    def setUp(self):
        """before all tests"""
        self.user = User(first_name='Olalekan', last_name="Mojibola", email='mojibola0534')
    
    @parameterized.expand([
        ("abcd", "Password must be at least 8 characters"),
        ("abcdefgh", "Password must contain at least one uppercase letter"),
        ("Abcdefgh", 'Password must contain at least one number'),
        ("Abcdefgh1", "Password must contain at least one symbol")
    ])
    def test_password(self, pwd, exception_raised):
        """making all tests on password with this test,
        the following password related
        method will be tested:
            **password getter and setter**
            **validate_pwd**
        """
        with self.assertRaises(ValueError) as context:
            self.user.password = pwd
            self.assertEqual(str(context.exception), exception_raised)

    def test_password_is_none(self):
        """test with no password"""
        self.assertIsNone(self.user.password)

    def test_valid_password(self):
        """testing valid password"""
        self.user.password = "Mojibola@0534"
        hashed_pwd = self.user.password
        self.assertNotEqual(hashed_pwd, "Mojibola@0534")
    
    def test_is_valid_pwd(self):
        """testing if password is correct"""
        self.user.password = "Mojibola@534"
        self.assertTrue(self.user.is_valid_pwd("Mojibola@534"))
    
    @parameterized.expand([
        ('My name is Olalekan, I am a software engineer',), # with bio
        ('',),  # empty str
        (None,), # bio is None
        ({},),  # not a string
        ('bio too long',)
    ])
    def test_bio(self, bio):
        """testing bio"""
        if bio == {}:
            self.user.bio = {}
            self.assertEqual(self.user.bio, None)
        elif bio == 'bio too long':
            with self.assertRaises(ValueError) as context:
                bio = 'this bio should be really long, like really!' * 10
                self.user.bio = bio
                self.assertEqual(str(context.exception), "Bio must be less than 250")
        else:
            self.user.bio = bio
            self.assertEqual(self.user.bio, bio)

    @parameterized.expand([
        ('Olalekan',),  # should have no problem
        ('Olalekan3',),  # should raise error
        ('olalekan@',),  # should raise error
        ('name too long',),  # should raise error
        (None,),  # should raise error
        ({},) # should raise error
    ])
    def test_first_name(self, name):
        """testing the validity of names"""
        if name == 'Olalekan':
            self.user.first_name = name
            self.assertEqual(self.user.first_name, 'Olalekan')
        elif name == 'name too long':
            name = name * 5
            with self.assertRaises(ValueError) as context:
                self.user.first_name = name
                self.assertEqual(str(context.exception), "Name too long")
        elif name is None:
            with self.assertRaises(ValueError) as context:
                self.user.first_name = name
                self.assertEqual(str(context.exception), "Name must not be empty")
        else:
            with self.assertRaises(ValueError) as context:
                self.user.first_name = name
                self.assertEqual(str(context.exception), "Invalid name")
        ## same tests applies to last_name
    
    @parameterized.expand([
        ('lekanmojibola@gmail.com',), # valid email
        ('lekanmojibola',),  # invalid email
        (None,),  # email cannot be empty
        ({},),  # invalid email
        ('email too long',)  # email too long
    ])
    def test_email(self, email):
        """testing emails"""
        if email == 'lekanmojibola@gmail.com':
            self.user.email = email
            self.assertEqual(self.user.email, email)
        elif email is None:
            with self.assertRaises(ValueError) as context:
                self.user.email = None
                self.assertEqual(str(context.exception), "Email cannot be empty")
        elif email == 'email too long':
            email = 'email too long' * 5
            with self.assertRaises(ValueError) as context:
                self.user.email = email
                self.assertEqual(str(context.exception), "Email too long")      
        else:
            with self.assertRaises(ValueError) as context:
                self.user.email = email
                self.assertEqual(str(context.exception), "Email is invalid")
