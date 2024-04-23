#!/usr/bin/env python3
"""
App module
"""

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route('/register', methods=['POST'])
def register():
    """
    Endpoint to register a new user.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    try:
        user = auth.register_user(email, password)
        return jsonify({
            'message': f'User {user.email} registered successfully'
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint to log in a user.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if auth.valid_login(email, password):
        session_id = auth.create_session(email)
        return jsonify({'session_id': session_id}), 200
    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/user', methods=['GET'])
def get_user():
    """
    Endpoint to get user information.
    """
    session_id = request.headers.get('Authorization')
    if session_id:
        user = auth.get_user_from_session(session_id)
        if user:
            return jsonify({'email': user.email}), 200
    return jsonify({'error': 'Unauthorized'}), 401


if __name__ == '__main__':
    app.run(debug=True)
