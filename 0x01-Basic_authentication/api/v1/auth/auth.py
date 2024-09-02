#!/usr/bin/env python3
"""Auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Manages the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns a boolean value"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        if path[-1] == '/':
            path = path[:-1]

        slash = False
        for excluded_path in excluded_paths:
            if excluded_path[-1] == '/':
                excluded_path = excluded_path[:-1]
                slash = True

            if excluded_path.endswith('*'):
                idx = excluded_path.rfind('/') + 1
                excluded = excluded_path[idx:-1]
                index = path.rfind('/') + 1
                temp_path = path[index:]

                if excluded in temp_path:
                    return False
        if slash:
            slash = False

        path += '/'

        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user method"""
        return None
