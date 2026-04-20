#!/usr/bin/env python3
"""start point"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix='/coolbooks', static_folder='../static', static_url_path='/static')
from api.v1.views.index import *
from api.v1.views.books import *
from api.v1.views.users import *

