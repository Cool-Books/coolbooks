#!/usr/bin/env python3
"""session auth model"""
import uuid
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from api.v1.auth.auth import Auth
from flask import request, session
from models.user import User

load_dotenv()

class SessionAuth(Auth):
    """session auth model"""

    def __init__(self):
        self.session_duration = int(os.getenv('SESSIONEXPIRY', '0'))  # Ensure SESSIONEXPIRY is set

    def create_session(self, user_id: str) -> str:
        """Generates a session ID for the user and stores it in Flask session"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())  # Generate a unique session ID
        
        # Store session data in Flask-Session
        session['session_id'] = session_id
        session['user_id'] = user_id
        session['created_at'] = datetime.now().isoformat()

        return session_id

    def current_user(self, request=None):
        """Returns the current user associated with the session"""
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.get_userid_by_sessionid(session_id)
        if user_id is None:
            return None
        return User.get(user_id)

    def get_userid_by_sessionid(self, session_id: str) -> str:
        """Retrieves the user ID by session ID from Flask session"""
        if session_id is None or not isinstance(session_id, str):
            return None
        
        # Check session in Flask-Session
        stored_session_id = session.get('session_id')
        if stored_session_id != session_id:
            return None

        # Handle session expiry logic
        created_at = session.get('created_at')
        if created_at is None:
            return None

        created_at = datetime.fromisoformat(created_at)
        if self.session_duration > 0:
            expires_at = created_at + timedelta(seconds=self.session_duration)
            if datetime.now() > expires_at:
                self.destroy_session(request)  # Session expired, destroy it
                return None

        return session.get('user_id')

    def destroy_session(self, request=None) -> bool:
        """Destroys the user session"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Remove the session from Flask-Session
        session.pop('session_id', None)
        session.pop('user_id', None)
        session.pop('created_at', None)
        
        return True
