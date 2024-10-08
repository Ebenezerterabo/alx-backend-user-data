#!/usr/bin/env python3
"""DB module.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add user to the database.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find user in the database.
        """
        # Query the user based on the keyword arguments
        user = self._session.query(User).filter_by(**kwargs).first()
        # If no user is found, raise an exception NoResultFound
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user in the database.
        """
        # Find the user by ID
        user = self.find_user_by(id=user_id)
        # Get all the attributes of the user
        valid_attrs = set(User.__table__.columns.keys())
        # Update the user's attributes
        for key, value in kwargs.items():
            if key not in valid_attrs:
                raise ValueError
            if key != "id":  # Avoid updating the id
                setattr(user, key, value)
        # Commit the changes
        self._session.commit()
