#!/usr/bin/env python3
"""SessionDBAuth module"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid
from datetime import datetime, timedelta
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """Session Authentication with Database"""

    def create_session(self, user_id=None):
        """Create a Session ID and store it in the database."""
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """Return the User ID based on a Session ID retrieved from the
        database."""
        if session_id is None:
            return None

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None

        session_dict = user_sessions[0].to_json()
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

    def destroy_session(self, request=None):
        """Destroy the UserSession based on the Session ID from the
        request cookie."""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False

        user_sessions[0].remove()
        return True
