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
        if path in excluded_paths:
            return False
        if path[-1] != '/':
            path += '/'
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header """
        return None

    def current_user(self, request=None) -> str:
        """ Current user """
        return None
