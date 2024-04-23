#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """
    DB class to interact with the database.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.
        Args:
            email: The email of the user.
            hashed_password: The hashed password of the user.
        Returns:
            User: The newly created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by specified attributes.
        Args:
            **kwargs: Arbitrary keyword arguments representing user attributes.
        Returns:
            User: The first user found matching the criteria.
        """
        return self._session.query(User).filter_by(**kwargs).first()

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes.
        Args:
            user_id: The ID of the user to be updated.
            **kwargs: Arbitrary keyword arguments representing updated
            user attributes.
        """
        user = self._session.query(User).filter_by(id=user_id).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            self._session.commit()
        else:
            raise ValueError("User not found")
