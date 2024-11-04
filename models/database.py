#!/usr/bin/env python3
"""db"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_TYPE = os.getenv("DB_TYPE", "file")  # Default to file-based if not set
DB_USER = os.getenv('DB_USER')
DB_USER_PWD = os.getenv('DB_USER_PWD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_ENGINE = os.getenv('DB_ENGINE')
DATABASE_URI = f'mysql+mysqldb://{DB_USER}:{DB_USER_PWD}@{DB_HOST}:{DB_PORT}/{DB_ENGINE}'

# Set up SQLAlchemy
engine = create_engine(DATABASE_URI)
SQLAlchemyBase = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Create tables if using database storage
if DB_TYPE == 'db':
    SQLAlchemyBase.metadata.create_all(engine)
