#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Optional


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a new user with email and password"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"user {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """locating the user by email. If it exists,
        check the password with bcrypt.checkpw.
        If it matches return True.
        In any other case, return False."""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """find the user corresponding to the email,
        generate a new UUID and store it in the database
        as the user’s session_id, then return the session ID"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """It takes a single session_id string argument
        and returns the corresponding User or None"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ updates the corresponding user’s session ID to None"""
        if user_id is None:
            return None
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Find the user corresponding to the email.
        If the user does not exist, raise a ValueError exception.
        If it exists, generate a UUID and update the user’s reset_token
        database field. Return the token."""
        if email is None:
            return None
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError("user does not exist")
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token
    
    def update_password(self, reset_token: str, password: str) -> None:
        """ find the corresponding user. If it does not exist,
        raise a ValueError exception. Otherwise, hash the password
        and update the user’s hashed_password field with the new
        hashed password and the reset_token field to None"""
        if reset_token is None:
            return None
        if password is None:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except ValueError:
            raise ValueError("Invalid reset token")
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt hashing algorithm
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid.uuid4())
