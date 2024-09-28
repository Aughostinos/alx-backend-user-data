#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', method=['GET'])
def Bienvenue() -> str:
    """eturn a JSON payload of the form:
    {"message": "Bienvenue"}"""

    return jsonify({"message": "Bienvenue"})
