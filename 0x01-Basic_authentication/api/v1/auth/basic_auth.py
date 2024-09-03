#!/usr/bin/env python3
"""Basic Auth"""
from api.v1.auth.auth import Auth


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
