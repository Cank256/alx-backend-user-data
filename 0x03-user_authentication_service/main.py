#!/usr/bin/env python3
"""
Main module
"""

import requests


def register_user(email: str, password: str) -> None:
    """
    Register a new user via the API.
    """
    url = 'http://127.0.0.1:5000/register'
    data = {'email': email, 'password': password}
    response = requests.post(url, json=data)
    print(response.json())


def login(email: str, password: str) -> str:
    """
    Log in a user and return the session ID.
    """
    url = 'http://127.0.0.1:5000/login'
    data = {'email': email, 'password': password}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()['session_id']
    return None


def get_user(session_id: str) -> str:
    """
    Get user information using the session ID.
    """
    url = 'http://127.0.0.1:5000/user'
    headers = {'Authorization': session_id}
    response = requests.get(url, headers=headers)
    return response.json()


if __name__ == '__main__':
    # Test registration
    register_user('test@example.com', 'password')

    # Test login
    session_id = login('test@example.com', 'password')
    print(f'Session ID: {session_id}')

    # Test retrieving user information
    if session_id:
        user_info = get_user(session_id)
        print(user_info)
