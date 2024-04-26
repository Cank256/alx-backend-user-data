#!/usr/bin/env python3
""" Module of Session Auth
"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session Authentication

    This class provides functionality for session-based authentication.

    Attributes:
        user_id_by_session_id (dict): A dictionary to store user IDs
        associated with session IDs.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The generated Session ID if successful, None otherwise.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
