#!/usr/bin/env python3

from dotenv import load_dotenv
import os

load_dotenv()

DB_TYPE = os.getenv('DB_TYPE')

if DB_TYPE == 'db':
    from models.engine.dbstorage import DbStorage
    storage = DbStorage()
    storage.reload()
elif DB_TYPE == 'fs':
    from models.engine.filestorage import FileStorage
    from models.book import Books
    from models.user import User
    storage = FileStorage()
    storage.load_from_file(Books)
    storage.load_from_file(User)