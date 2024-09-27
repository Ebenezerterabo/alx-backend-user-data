#!/usr/bin/env python3
""" Authentication module. """

import bcrypt
from sqlalchemy.exc import NoResultFound
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

    def register_user(self, email: str, password: str) -> None:
        """Register a new user.
        """
        try:
            # Check if the user already exists
            user = self._db.find_user_by(email=email)
            if user is not None:
                raise ValueError(
                    "User {} already exists".format(email)
                )
            self._db.add_user(email, _hash_password(password))
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))

        return user
