#!/usr/bin/env python3
""" Auth class module """
from flask import Flask
from typing import List

app = Flask(__name__)


class Auth:
    """ Auth class """
    def __init__(self):
        """ Initialize Auth class """
        pass

    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """ Require Auth """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        # Normalize the path
        if path[-1] != '/':
            path += '/'
        # check if the path is in the excluded paths
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header """
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> str:
        """ Current user """
        return None

    def session_cookie(self, request=None) -> str:
        """ Session cookie """
        if request is None:
            return None
        if request.cookies.get('_my_session_id') is None:
            return None
        return request.cookies.get('_my_session_id')
