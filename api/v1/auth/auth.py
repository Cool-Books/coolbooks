#!/usr/bin/env python3
"""base class for the auth"""
from flask import request
import os
from dotenv import load_dotenv


load_dotenv()

class Auth:
    """auth model"""
    def require_auth(self, path: str, exc_path: list) -> bool:
        """check if a path requires authentication"""
        if not path or path is None or not exc_path or exc_path is None:
            return True
        path = path if path.endswith('/') else path + '/'
        if path in exc_path:
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
    