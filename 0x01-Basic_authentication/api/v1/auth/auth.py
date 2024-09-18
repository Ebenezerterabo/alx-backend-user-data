#!/usr/bin/env python3
from flask import Flask
from typing import List

app = Flask(__name__)


class Auth:
    def __init__(self):
        pass

    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
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
        return None

    def current_user(self, request=None) -> str:
        return None
