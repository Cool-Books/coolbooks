#!/usr/bin/env python3
"""Base class for all models"""
from os import path
import uuid
import os
from datetime import datetime
from typing import TypeVar, List, Type, Iterable
import json


TIMESTAMP = "%Y-%m-%dT%H-%M-%S"
DATA = {}  
class Base:
    """base class for all models"""
    def __init__(self, *args: list, **kwargs: dict) -> None:
        t_class = str(self.__class__.__name__)
        if DATA.get(t_class) is None:
            DATA[t_class] = {}  
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
            if not for_serialization and key == '_password':
                continue
            if type(value) is datetime:
                result[key] = datetime.strftime(value, TIMESTAMP)
            else:
                result[key] = value
        return result


    def save(self):
        """Saving current instance object to DATA"""
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
            f.seek(0, os.SEEK_END)
            if f.tell() > 0:
                f.seek(f.tell() - 1, os.SEEK_SET)
                if f.read(1) != '\n':
                    f.write('\n')

            json.dump(t_obj, f)
            f.write('\n')

    @classmethod
    def load_from_file(cls):
        """Load model objects from file, processing each JSON object line by line."""
        t_class = cls.__name__
        file_path = ".db_{}.json".format(t_class)
        DATA[t_class] = {}


        if not os.path.exists(file_path):
            return


        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    obj = json.loads(line)
                    for obj_id, val in obj.items():

                        transformed_val = {}
                        for key, value in val.items():
                            if key.startswith('_'):

                                new_key = key[1:]
                                transformed_val[new_key] = value
                            else:
                                transformed_val[key] = value
                        transformed_val.pop('is_loading', None)

                        DATA[t_class][obj_id] = cls(is_loading=True, **transformed_val)

    @classmethod
    def search(cls, attr: dict = {}) -> List[Type['Base']]:
        """returns the list of instances
        based on unique key"""
        t_class = cls.__name__
        cls.load_from_file()
        if not isinstance(attr, dict):
            return None
        def _search(obj):
            """for filter"""
            if len(attr) == 0:
                return True
            for key, val in attr.items():
                if getattr(obj, key) != val:
                    return False
                return True
        return list(filter(_search, DATA[t_class].values()))

    def remove(self):
        """Remove object from DATA and save to file"""
        self.load_from_file()
        s_class = self.__class__.__name__
        if DATA[s_class].get(self.id) is not None:
            del DATA[s_class][self.id]
            self.__class__.save_to_file()
            return True
        return False


    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """return an object by id"""
        t_class = cls.__name__
        return DATA[t_class].get(id)

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """get all instances from storage"""
        return cls.search()


    def update(self, attr: dict):
        """update the instance in database"""
        if attr is None or not isinstance(attr, dict):
            raise ValueError('Invalid request')
        for key, val in attr.items():
            if hasattr(self, key):
                setattr(self, key, val)
            else:
                raise ValueError("Invalid request")
        self.save()

    @classmethod
    def _delete_all(cls):
        """deletes all instances from the file storage"""
        cls.load_from_file()
        t_class = cls.__name__
        if t_class in DATA:
            DATA[t_class].clear()
        cls.save_to_file()
