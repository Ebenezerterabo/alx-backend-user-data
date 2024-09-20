#!/usr/bin/env python3
""" Session with Auth class module """
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """ Session Auth class """

    def __init__(self):
        """ Initialize Session Auth class """
        pass

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a session """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ User ID for Session ID """
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)
