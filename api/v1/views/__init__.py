#!/usr/bin/env python3
"""start point"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix='/coolbooks')
from api.v1.views.index import *
from api.v1.views.books import *

Books.load_from_file()