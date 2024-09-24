#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

auth_type = os.getenv('AUTH_TYPE')
if auth_type == 'basic_auth':
    auth = BasicAuth()
else:
    auth = Auth()

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error):
    """Handle 401 Unauthorized error"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Handle 403 Unauthorized error """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """Method that runs before any request"""
    if auth is None:
        return

    exc_paths = (['/api/v1/status/', '/api/v1/unauthorized/',
                  '/api/v1/forbidden/'])
    if not auth.require_auth(request.path, exc_paths):
        return

    if auth.authorization_header(request) is None:
        return abort(401)

    if auth.current_user(request) is None:
        return abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
