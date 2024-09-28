#!/usr/bin/env python3
""" Authentication module. """

import bcrypt
from sqlalchemy.exc import NoResultFound

from user import User
from db import DB


def _hash_password(password: str) -> bytes:
    """Hash a password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize a new Auth instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user.
        """
        try:
            # Check if the user already exists
            self._db.find_user_by(email=email)
        except NoResultFound:
            # add the user if it doesn't exist
            return self._db.add_user(email, _hash_password(password))

        else:
            # if user already exists
            raise ValueError("User {} already exists".format(email))
