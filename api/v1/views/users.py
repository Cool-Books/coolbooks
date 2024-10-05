#!/usr/bin/env python3
"""users endpoints"""
from email.policy import strict
from flask import request, abort
from models.user import User
from api.v1.views import app_views


@app_views.route('/create_user', strict_slashes=False, methods=['POST'])
def create_user():
    """this view creates a new user"""