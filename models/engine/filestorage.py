#!/usr/bin/env python3
"""engine for filestorage"""
from os import path
import uuid
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import TypeVar, List, Type, Iterable
import json

# ----- all classes ----
# from models.user import User
# from models.book import Books
# --- end of classes

# classes = {'Books': Books, "User": User}

load_dotenv()

TIMESTAMP = "%Y-%m-%dT%H-%M-%S"
DATA = {} 

class FileStorage:
    """file storage engine"""
    def __init__(self):
        t_class = self.__class__.__name__
        if t_class not in DATA:
            DATA[t_class] = {}
            
    
    def to_json(self, obj, for_serialization: bool = False) -> dict:
        """converting the instance object to json"""
        result = {}
        for key, value in obj.__dict__.items():
            if not for_serialization and key == '_password':
                continue
            if type(value) is datetime:
                result[key] = datetime.strftime(value, TIMESTAMP)
            else:
                result[key] = value
        return result
    

    def save(self, obj=None):
        """save the instance of the obj to memory"""
        t_class = obj.__class__.__name__
        obj.updated_at = datetime.now()
        DATA.setdefault(t_class, {})[obj.id] = obj
        self.save_to_file(t_class)

    def save_to_file(self, t_class):
        """saving to file"""
        file_path = ".db_{}.json".format(t_class)
        t_obj = {}
        t_obj = {key: self.to_json(val, True) for key, val in DATA[t_class].items()}


        with open(file_path, 'w') as f:
            f.seek(0, os.SEEK_END)
            if f.tell() > 0:
                f.seek(f.tell() - 1, os.SEEK_SET)
                if f.read(1) != '\n':
                    f.write('\n')

            json.dump(t_obj, f)
            f.write('\n')
    
    def load_from_file(self, cls):
        """ Load all objects from file
        """
        t_class = cls.__name__
        file_path = ".db_{}.json".format(t_class)
        DATA[t_class] = {}
        if not path.exists(file_path):
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

    def search(self, cls, attr={}):
        """returns the list of instances
        based on unique key"""
        t_class = cls.__name__
        if not isinstance(attr, dict):
            return None

        def _search(obj):
            """for filter"""
            if len(attr) == 0:
                return True
            for key, val in attr.items():
                if getattr(obj, key) == val:
                    return True
                return False
        return list(filter(_search, DATA[t_class].values()))
    

    def remove(self, obj):
        """remove from memory"""
        s_class = obj.__class__.__name__
        if DATA[s_class].get(obj.id) is not None:
            del DATA[s_class][obj.id]
            self.save_to_file(s_class)
            return True
        return False
    
    def get(self, cls, id):
        """get by id"""
        t_class = cls.__name__
        return DATA[t_class].get(id)
    
    def all(self, cls):
        """return all"""
        return self.search(cls)
    
    def update(self, obj, attr: dict):
        """update the instance in database"""
        if attr is None or not isinstance(attr, dict):
            raise ValueError('Invalid request')
        for key, val in attr.items():
            if hasattr(obj, key):
                setattr(obj, key, val)
            else:
                raise ValueError("Invalid request")
        self.save(obj)
    
    def delete_all(self, cls):
        """deletes all instances from the file storage"""
        t_class = cls.__name__
        if t_class in DATA:
            DATA[t_class] = {}
        self.save_to_file(t_class)
    
    def close(self):
        """writes all obj to file"""
        for cls_name in DATA.keys():
            self.save_to_file(cls_name)