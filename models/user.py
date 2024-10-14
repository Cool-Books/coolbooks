#!/usr/bin/env python3
"""user model"""
import re
import unittest
from models.base import Base, DATA
import bcrypt
import base64



class User(Base):
    """user model"""
    def __init__(self, *args, **kwargs):
        self.is_loading = kwargs.get('is_loading', False)
        super().__init__(*args, **kwargs)
        self.email = kwargs.get("email")
        self.password = kwargs.get('password')
        self.bio = kwargs.get('bio')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.other_names = kwargs.get('other_names')
        self.is_author = kwargs.get('is_author', "NO")
    
    
    @property
    def password(self) -> str:
        """return the password"""
        return self._password
    
    @password.setter
    def password(self, pwd: str) -> None:
        """setting the password: defining constraints"""
        if not self.is_loading:
            self.validate_pwd(pwd)
            hashed_pwd = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
            self._password = hashed_pwd.decode('utf-8')  # Store directly without base64 encoding
        else:
            self._password = pwd


    def is_valid_pwd(self, pwd: str) -> bool:
        """check the validity of the password"""
        if pwd is None or not isinstance(pwd, str) or not pwd:
            raise ValueError('Incorrect password')
        
        # Assuming `self._password` is the stored hashed password (without base64 encoding)
        return bcrypt.checkpw(pwd.encode('utf-8'), self.password.encode('utf-8'))


    @property
    def bio(self) -> str:
        """return bio"""
        return self._bio


    @bio.setter
    def bio(self, in_bio: str) -> None:
        """setter for bio"""
        if in_bio is None or not isinstance(in_bio, str) or not in_bio:
            self._bio = None
        else:
            self.validate_bio(in_bio)
            self._bio = in_bio

    @property
    def first_name(self) -> str:
        """returns first name"""
        return self._first_name

    @first_name.setter
    def first_name(self, name: str) -> None:
        """sets first name and must not be empty"""
        self.validate_name(name)
        self._first_name = name

    @property
    def last_name(self) -> str:
        """return last name"""
        return self._last_name
    
    @last_name.setter
    def last_name(self, name: str) -> None:
        """sets last name"""
        self.validate_name(name)
        self._last_name = name

    @property
    def email(self) -> str:
        """return email"""
        return self._email
    
    @email.setter
    def email(self, mail) -> None:
        """sets email"""
        self.validate_email(mail)
        self._email = mail

    @staticmethod
    def validate_bio(bio):
        """validate bio"""
        if len(bio) > 250:
            raise ValueError("Bio must be less than 250")
        return True

    @property
    def is_author(self) -> str:
        """return author"""
        return self._is_author

    @is_author.setter
    def is_author(self, author: str) -> None:
        """sets author"""
        if author is None:
            self._is_author = "NO"
        else:
            author = author.upper()
            self._is_author = author


    @staticmethod
    def validate_pwd(pwd: str) -> bool:
        """validate the password"""
        if pwd is None or not isinstance(pwd, str):
            raise ValueError('Invalid password')
        if len(pwd) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r'[A-Z]', pwd):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[0-9]', pwd):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', pwd):
            raise ValueError("Password must contain at least one symbol")
        return True

    @staticmethod
    def validate_name(name: str) -> bool:
        """validate first name"""
        if name is None or not name:
            raise ValueError("Name must not be empty")        
        if not isinstance(name, str):
            raise ValueError("Invalid name")
        if re.search(r'[0-9]', name):
            raise ValueError("Name cannot contain numbers")
        if re.search(r'[!@#$%^&*(),?":{}|<>]', name):
            raise ValueError("Name cannot contain special characters")
        if len(name) > 50:
            raise ValueError("Name too long")
        return True

    @staticmethod
    def validate_email(mail: str) -> bool:
        """validate mail"""
        if mail is None or not mail:
            raise ValueError("Email cannot be empty")
        if '@' not in mail or mail.count('@') != 1 or not isinstance(mail, str):
            raise ValueError("Email is invalid")
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, mail):
            raise ValueError("Email is invalid")
        if len(mail) > 100:
            raise ValueError("Email too long")
        return True
