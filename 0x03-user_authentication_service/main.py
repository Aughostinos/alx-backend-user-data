#!/usr/bin/env python3
"""
Main module for testing user authentication service
"""

import requests


def register_user(email: str, password: str) -> None:
    """
    Registers a new user.
    """
    url = "http://localhost:5000/users"
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    try to log in with a wrong password.
    """
    url = "http://localhost:5000/sessions"
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Logs in a user and returns the session ID
    """
    url = "http://localhost:5000/sessions"
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    session_id = response.cookies.get('session_id')
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """
    try to access the profile page without log in.
    """
    url = "http://localhost:5000/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Accesses the profile page while logged in.
    """
    url = "http://localhost:5000/profile"
    cookies = {'session_id': session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """
    Logs out the user.
    """
    url = "http://localhost:5000/sessions"
    cookies = {'session_id': session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200 or response.status_code == 302


def reset_password_token(email: str) -> str:
    """
    Requests a password reset token for the user.
    """
    url = "http://localhost:5000/reset_password"
    data = {'email': email}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    reset_token = response.json().get('reset_token')
    assert reset_token is not None
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Updates the user's password using the reset token.
    """
    url = "http://localhost:5000/reset_password"
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    response = requests.put(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    EMAIL = "guillaume@holberton.io"
    PASSWD = "b4l0u"
    NEW_PASSWD = "t4rt1fl3tt3"

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    session_id = log_in(EMAIL, NEW_PASSWD)
    profile_logged(session_id)
