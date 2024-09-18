#!/usr/bin/env python3
from flask import Flask
from typing import List

app = Flask(__name__)


class Auth:
    def __init__(self):
        pass

    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        return False

    def authorization_header(self, request=None) -> str:
        return None

    def current_user(self, request=None) -> str:
        return None
