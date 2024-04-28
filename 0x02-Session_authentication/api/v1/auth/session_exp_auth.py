#!/usr/bin/env python3
""" Module of Session Exp Auth"""

from api.v1.auth.session_auth import SessionAuth
import uuid
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """Session Authentication with Expiration"""

    def __init__(self):
        """Initialize SessionExpAuth"""
        super().__init__()
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """Create a Session ID with expiration for a user_id."""
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """Return the User ID based on a Session ID with expiration."""
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        user_id = session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        if self.session_duration <= 0:
            return user_id

        if not created_at:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        return user_id
