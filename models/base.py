#!/usr/bin/env python3
"""Base class for all models"""
import os
import uuid
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import TypeVar, List, Type, Iterable
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base

load_dotenv()
DB_TYPE = os.getenv('DB_TYPE')

Dbase = declarative_base()

class Base(Dbase):
    """base class for all models"""
    __abstract__ = True
    id = Column(String(100), primary_key=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, *args: list, **kwargs: dict) -> None:
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())

    def to_json(self, for_serialization: bool = False) -> dict:
        """converting the instance object to json"""
        return models.storage.to_json(self, for_serialization)

    def save(self):
        """Saving current instance object to DATA"""
        # self.updated_at = datetime.now()
        models.storage.save(self)

    @classmethod
    def search(cls, attr: dict) -> List[Type['Base']]:
        """returns the list of instances
        based on unique key"""
        return models.storage.search(cls, attr)

    def remove(self):
        """Remove object from DATA and save to file"""
        models.storage.remove(self)

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """return an object by id"""
        return models.storage.get(cls, id)

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """return all"""
        return models.storage.all(cls)


    def update(self, attr: dict):
        """update the instance in database"""
        models.storage.update(self, attr)

    @classmethod
    def _delete_all(cls):
        """deletes all instances from the file storage"""
        models.storage.delete_all(cls)