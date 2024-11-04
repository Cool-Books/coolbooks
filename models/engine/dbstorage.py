#!/usr/bin/env python3
"""db engine"""
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
import os
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from models.base import Dbase
from models.user import User
from models.book import Books
# import logging
# from sqlalchemy import create_engine

# # Set up logging for SQLAlchemy
# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
load_dotenv()

classes = {"User": User,  "Books": Books}
DB_USER = os.getenv('DB_USER')
DB_USER_PWD = os.getenv('DB_USER_PWD')
DB_ENGINE = os.getenv('DB_ENGINE')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

class DbStorage:
    """db engine"""
    __engine = __session = None

    def __init__(self) -> None:
        DATABASE_URL = f'mysql+mysqldb://{DB_USER}:{DB_USER_PWD}@{DB_HOST}:{DB_PORT}/{DB_ENGINE}'
        self.__engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20, pool_timeout=30, echo=False)

    def save(self, obj):
        """save obj to session"""
        try:
            obj.updated_at = datetime.now()
            self.__session.add(obj)
            self.__session.commit()
        except SQLAlchemyError as e:
            self.__session.rollback()
            print(f'this is the error: {e}')
            raise ValueError("couldn't save to database")
    
    def remove(self, obj):
        """deletes an object from database"""
        if obj is not None:
            self.__session.delete(obj)
            self.__session.commit()
    
    def search(self, cls, attr={}):
        """search an obj in db"""
        kwargs = {}
        keys = ['password', 'email', 'first_name', 'last_name', 'bio',
                'title', 'author', 'isbn', 'description', 'content']
        for key, val in attr.items():
            if key in keys:
                if not key.startswith('_'):
                    kwargs[f'_{key}'] = val
                else:
                    kwargs[key] = val
            else:
                kwargs[key] = val

        try:
            all_value = self.__session.query(cls).filter_by(**kwargs).all()
            return all_value
        except SQLAlchemyError as e:
            print(f'this is the error: {e}')
            raise ValueError('Couldn\'t process request')
    
    def to_json(self, obj, for_serial:bool):
        """converts an object to json"""
        results = {}
        mapper = inspect(obj).mapper
        
        for column in mapper.columns:
            value = getattr(obj, column.name)
            
            # Convert datetime fields to string format
            if isinstance(value, datetime):
                results[column.name] = value.strftime("%Y-%m-%dT%H:%M:%S")
            elif not for_serial and column.name == "_password":
                continue  # Skip sensitive fields like password
            else:
                results[column.name] = value
        return results
    
    def all(self, cls):
        """returns all instances"""
        return self.search(cls)

    def get(self, cls, get_id):
        """gets an object via id"""
        obj = self.search(cls, {'id': get_id})
        # if not obj or obj is None:
        #     raise ValueError('not found')
        return obj[0]

    def update(self, obj, attr:dict):
        """updates an object"""
        try:
            for key, val in attr.items():
                if hasattr(obj, key):
                    setattr(obj , key, val)
            self.save(obj)
        except SQLAlchemyError:
            return None
    def close(self):
        """closes the session"""
        if self.__session:
            self.__session.close()

    def delete_all(self, cls):
        """deletes all the data from a table
        this is just for testing purposes (WARNING)"""
        try:
            self.__session.query(cls).delete()
            self.__session.commit()
        except SQLAlchemyError:
            self.__session.rollback()
            raise
    
    def reload(self):
        """reloads the db"""
        Dbase.metadata.create_all(self.__engine)
        session_factory = sessionmaker(self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)