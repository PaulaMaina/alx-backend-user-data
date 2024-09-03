#!/usr/bin/env python3
"""Basic Auth"""
from api.v1.auth.auth import Auth
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
