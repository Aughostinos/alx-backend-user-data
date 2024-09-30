#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request, Response, abort, make_response
from flask import redirect
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=['GET'])
def Bienvenue() -> str:
    """return a JSON payload of the form:
    {"message": "Bienvenue"}"""

    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> Response:
    """ Registers a new user."""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login() -> Response:
    """ respond to the POST /sessions route."""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)
    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=['DELETE'])
def logout() -> Response:
    """ respond to the DELETE /sessions route."""
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        return redirect('/')
    except Exception:
        abort(403)


@app.route("/profile", methods=['GET'])
def profile() -> Response:
    """respond to the GET /profile route."""
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> Response:
    """respond to the POST /reset_password route."""
    email = request.form.get('email')
    if not email:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> Response:
    """PUT /reset_password
    returnJSON response with the user's email and a message.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
