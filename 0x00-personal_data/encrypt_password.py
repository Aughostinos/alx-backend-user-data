#!/usr/bin/env python3
"""
Module 0x00-personal_data
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    make sure that password matches the hashed password.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
