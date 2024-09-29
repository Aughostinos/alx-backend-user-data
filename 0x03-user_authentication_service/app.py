#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request, Response, abort, make_response
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
