#!/usr/bin/env python3
""" Session with Auth class module """
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Session Auth class """

    def __init__(self):
        """ Initialize Session Auth class """
        pass

    # def create_session(self, user_id: str = None) -> str:
    #     """ Create a session """
    #     if user_id is None or not isinstance(user_id, str):
    #         return None
    #     try:
    #         user = User.search({"id": user_id})
    #     except Exception:
    #         return None
    #     if user:
    #         session_id = self._generate_uuid()
    #         user[0].session_id = session_id
    #         user[0].save()
    #         return session_id
