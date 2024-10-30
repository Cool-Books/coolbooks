#!/usr/bin/env python3
"""base class for the auth"""
from flask import request
from typing import List
import os
from dotenv import load_dotenv


load_dotenv()

class Auth:
    """auth model"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require authentication"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        for get_path in excluded_paths:
            if get_path.endswith('*') and path.startswith(get_path[:-1]):
                return False
            elif path == get_path:
                return False
        return True

    def authorization_header(self, request) -> str:
        """check and get authorization header"""
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        return auth_header  # this returns the auth header for use later

    def session_cookie(self, request) -> str:
        """extracts the cookie"""
        if request is None:
            return None
        return request.cookies.get('session_id')
    