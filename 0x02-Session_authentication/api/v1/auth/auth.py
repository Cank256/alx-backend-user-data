#!/usr/bin/env python3
"""
Auth module
"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class for handling authentication methods.

    Attributes:
        None
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to check if authentication is required for a given path.

        Args:
            path (str): The path to check for authentication requirement.
            excluded_paths (List[str]): A list of paths excluded from
            authentication requirement.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True

        # Iterate over excluded paths
        for excluded_path in excluded_paths:
            # Check if the current excluded path ends with "*"
            if excluded_path.endswith("*"):
                # Check if the path matches the excluded path prefix
                if path.startswith(excluded_path[:-1]):
                    return False
            # If excluded path doesn't end with "*", perform direct match
            elif path == excluded_path:
                return False

        # If no match found, authentication is required
        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to retrieve the authorization header from a request.

        Args:
            request: The HTTP request object.

        Returns:
            str: The authorization header value.
        """
        if request is None:
            return None

        if "Authorization" not in request.headers:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to retrieve the current user based on the request.

        Args:
            request: The HTTP request object.

        Returns:
            TypeVar('User'): The current user.
        """
        return None

    def session_cookie(self, request: request = None) -> str:
        """Retrieve the session cookie value from a request.

        Args:
            request (Request): The Flask request object.

        Returns:
            str: The value of the session cookie, or None if not found.
        """
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
