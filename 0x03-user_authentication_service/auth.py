#!/usr/bin/env python3
"""
Auth module
"""

import bcrypt
import uuid
from db import DB
from user import User


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.
        Args:
            email: The email of the user.
            password: The password of the user.
        Returns:
            User: The newly registered User object.
        Raises:
            ValueError: If the user already exists.
        """
        existing_user = self._db.find_user_by(email=email)
        if existing_user:
            raise ValueError(f"User {email} already exists")
        hashed_password = self._hash_password(password)
        return self._db.add_user(email=email, hashed_password=hashed_password)

    def _hash_password(self, password: str) -> bytes:
        """
        Hash the password using bcrypt.
        Args:
            password: The password to be hashed.
        Returns:
            bytes: The hashed password.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user credentials.
        Args:
            email: The email of the user.
            password: The password of the user.
        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        user = self._db.find_user_by(email=email)
        if user:
            hashed_password = user.hashed_password.encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
        return False

    def create_session(self, email: str) -> str:
        """
        Create a session for the user.
        Args:
            email: The email of the user.
        Returns:
            str: The session ID.
        """
        session_id = str(uuid.uuid4())
        user = self._db.find_user_by(email=email)
        if user:
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        return None

    def get_user_from_session(self, session_id: str) -> User:
        """
        Get the user associated with the session.
        Args:
            session_id: The session ID.
        Returns:
            User: The user associated with the session.
        """
        return self._db.find_user_by(session_id=session_id)
