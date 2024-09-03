#!/usr/bin/env python3
"""Basic Auth"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """Basic Authentication"""
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """Returns the Base64 part of the Authorization header"""
        if not (authorization_header and isinstance(authorization_header, str)
                and authorization_header.startswith('Basic ')):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """Returns the decoded value of a Base64 string"""
        if not(base64_authorization_header and
                isinstance(base64_authorization_header, str)):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except BaseException:
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """Returns the user email and password from the BAse64 decoded value"""
        if not(decoded_base64_authorization_header and
                isinstance(decoded_base64_authorization_header, str)
                and ':' in decoded_base64_authorization_header):
            return None, None

        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """Returns the User instance based on his email and password"""
        if not (user_email or isinstance(user_email, str)):
            return None
        if not(user_pwd or isinstance(user_pwd, str)):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request"""
        try:
            auth_header = self.authorization_header(request)
            encoded = self.extract_base64_authorization_header(auth_header)
            decoded = self.decode_base64_authorization_header(encoded)
            email, password = self.extract_user_credentials(decoded)
            return self.user_object_from_credentials(email, password)
        except Exception:
            return None
