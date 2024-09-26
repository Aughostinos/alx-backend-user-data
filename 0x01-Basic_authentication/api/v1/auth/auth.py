#!/usr/bin/env python3
""" Module of auth
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class to manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Public method check if a given path requires authentication
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        for pattern in excluded_paths:
            if pattern.endswith('*'):
                if path.startswith(pattern[:-1]):
                    return False

            elif pattern == path or (pattern.rstrip('/') == path.rstrip('/')):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        return the value of the header request
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Public method that returns None
        """
        return None
