#!/usr/bin/env python3
"""
Database module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import User, Base


class DB:
    """manage User-related operations"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """takes in arbitrary keyword arguments and
        returns:
        the first row found in the users table as filtered
        by the method’s input arguments."""

        if not kwargs:
            raise InvalidRequestError(" wrong query arguments are passed")
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user

        except NoResultFound:
            raise NoResultFound("no user found")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid arguments provided")

    def update_user(self, user_id: int, **kwargs) -> None:
        """method will use find_user_by to locate the user to update,
        then will update the user’s attributes as passed in the method’s
        arguments then commit changes to the database."""
        user = self.find_user_by(id=user_id)
        valid_columns = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in valid_columns:
                raise ValueError(f"{key} is not a valid attribute of User")
            setattr(user, key, kwargs[key])

        self._session.commit()
