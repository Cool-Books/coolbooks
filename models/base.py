#!/usr/bin/env python3
"""Base class for all models"""
from os import path
import uuid
from datetime import datetime
from typing import TypeVar
import json

TIMESTAMP = "%Y-%m-%dT%H-%M-%S"
DATA = {}  # data which will be persisted into the file
class Base:
    """base class for all models"""
    def __init__(self, *args: list, **kwargs: dict) -> None:
        t_class = str(self.__class__.__name__)
        if DATA.get(t_class) is None:
            DATA[t_class] = {}  # create a dictionary for model in data

        self.id = kwargs.get('id', str(uuid.uuid4()))
        if kwargs.get('created_at') is not None:
            self.created_at = datetime.strptime(kwargs.get('created_at'), TIMESTAMP)
        else:
            self.created_at = datetime.now()
        if kwargs.get('updated_at') is not None:
            self.updated_at = datetime.strptime(kwargs.get('updated_at'), TIMESTAMP)
        else:
            self.updated_at = datetime.now()
    
    # ----- implementing comparison check --------
    def __eq__(self, other: TypeVar) -> bool:
        """making comparison between instances"""
        if type(self) != type(other):
            return False
        if not isinstance(other, Base):
            return False
        return (self.id == other.id)
    
    def to_json(self, for_serialization: bool = False) -> dict:
        """converting the instance object to json"""
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key[0] == '_':
                continue
            if type(value) is datetime:
                result[key] = datetime.strftime(value, TIMESTAMP)
            else:
                result[key] = value
        return result


    def save(self):
        """saving current instance object to DATA"""
        t_class = self.__class__.__name__
        self.updated_at = datetime.now()
        DATA[t_class][self.id] = self
        self.__class__.save_to_file()


    @classmethod
    def save_to_file(cls):
        """saving model object to file"""
        t_class = cls.__name__
        file_path = ".db_{}.json".format(t_class)
        t_obj = {}
        for key, val in DATA[t_class].items():
            t_obj[key] = val.to_json(True)
        
        with open(file_path, 'w') as f:
            json.dump(t_obj, f)


    @classmethod
    def load_from_file(cls):
        t_class = cls.__name__
        file_path = ".db_{}.json".format(t_class)
        DATA[t_class] = {}
        if not path.exists(file_path):
            return
        with open(file_path, 'r') as f:
            obj = json.load(f)
            for obj_id, val in obj.items():
                DATA[t_class][obj_id] = cls(**val)


    def remove(self):
        pass

    def get(self):
        pass

    def search(self):
        pass