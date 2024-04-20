#!/usr/bin/env python3
"""
Route module for the API.
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)

# Enable Cross-Origin Resource Sharing (CORS) for all routes under /api/v1/*
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize authentication object
auth = None
auth_type = getenv("AUTH_TYPE")
if auth_type == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif auth_type == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.before_request
def before_request():
    """
    Handler function executed before each request.
    Performs authentication and authorization checks.
    """
    if auth is None:
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]
    if request.path in excluded_paths:
        return

    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handler function for 404 Not Found errors.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """
    Handler function for 401 Unauthorized errors.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """
    Handler function for 403 Forbidden errors.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
