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
