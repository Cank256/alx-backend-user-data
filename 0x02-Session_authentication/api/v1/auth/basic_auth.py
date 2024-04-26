#!/usr/bin/env python3
"""
Basic Auth Class
"""
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """Basic authentication class."""

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for Basic Authentication.

        Args:
            authorization_header: The Authorization header
            string.

        Returns:
            str: The Base64 part of the Authorization header,
            or None if not found or invalid.
        """
        if authorization_header is None or not isinstance(
            authorization_header, str
        ):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        # Get the Base64 part after "Basic "
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Decodes a Base64 string.

        Args:
            base64_authorization_header: The Base64 string to decode.

        Returns:
            str: The decoded value as UTF8 string, or None if not valid.
        """
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Extracts user credentials from a decoded Base64 authorization header.

        Args:
            decoded_base64_authorization_header: The decoded Base64
            authorization header string.

        Returns:
            tuple: A tuple containing user email and password,
            or (None, None) if not found or invalid.
        """
        if decoded_base64_authorization_header is None or not isinstance(
            decoded_base64_authorization_header, str
        ):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> User:
        """
        Retrieves the User instance based on email and password.

        Args:
            user_email: The email of the user.
            user_pwd: The password of the user.

        Returns:
            User: The User instance, or None if not found
            or invalid password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        user = User.search({'email': user_email})
        if not user or not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> User:
        """
        Retrieves the User instance for a request.

        Args:
            request: The HTTP request object.

        Returns:
            User: The User instance, or None if not found
            or invalid.
        """
        if request is None:
            return None

        authorization_header = self.authorization_header(request)
        if not authorization_header:
            return None

        base64_header = self.extract_base64_authorization_header(
            authorization_header
        )
        if not base64_header:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)
        if not decoded_header:
            return None

        email, password = self.extract_user_credentials(decoded_header)
        if not email or not password:
            return None

        return self.user_object_from_credentials(email, password)
