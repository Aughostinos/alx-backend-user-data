#!/usr/bin/env python3
""" Module of basic_auth
"""

import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth that inherits from Auth"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization
        header for a Basic Authentication"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        parts = authorization_header.split(" ")
        if len(parts) != 2:
            return None

        return parts[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns the decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None
