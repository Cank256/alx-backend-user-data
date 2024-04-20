#!/usr/bin/env python3
"""
Auth module
"""
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
        if not path:
            return True

        if not excluded_paths or len(excluded_paths) == 0:
            return True

        # Ensure path ends with a slash for correct comparison
        path = path.rstrip("/") + "/"

        for excluded_path in excluded_paths:
            if path.startswith(excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to retrieve the authorization header from a request.

        Args:
            request: The HTTP request object.

        Returns:
            str: The authorization header value.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to retrieve the current user based on the request.

        Args:
            request: The HTTP request object.

        Returns:
            TypeVar('User'): The current user.
        """
        return None
