#!/usr/bin/env python3
""" Authentication module. """

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from typing import Union

from user import User
from db import DB


def _hash_password(password: str) -> bytes:
    """Hash a password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a UUID.
    """
    from uuid import uuid4
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize a new Auth instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[User, None]:
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

    def valid_login(self, email: str, password: str) -> bool:
        """Check if a login is valid.
        """
        try:
            # Attempt to find the user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # If no user is found, return False
            return False

        # Check if the password is correct
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Create a session for a user.
        """
        try:
            # Attempt to find the user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # If no user is found, return None
            return None

        # Generate a session ID
        session_id = _generate_uuid()
        # Update the user's session ID
        self._db.update_user(user.id, session_id=session_id)
        # Return the session ID
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get a user from a session ID.
        """
        if session_id is None:
            # If the session ID is None, return None
            return None
        try:
            # Attempt to find the user by session ID
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            # If no user is found, return None
            return None
        # Return the user
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy a session.
        """
        # Set session_id to None to destroy the session
        self._db.update_user(user_id, session_id=None)
        # Commit the changes
        self._db._session.commit()

    def get_reset_password_token(self, email: str) -> str:
        """Get a reset password token.
        """
        try:
            # Attempt to find the user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # If no user is found, return None
            raise ValueError
        # Generate a reset token
        reset_token = _generate_uuid()
        # Update the user's reset token
        self._db.update_user(user.id, reset_token=reset_token)
        # Return the reset token
        return reset_token
