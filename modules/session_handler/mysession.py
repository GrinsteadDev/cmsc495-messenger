"""
Purpose:
   Creates a sets up a session manager using the Flask-Session api. This is a
   global session manager that will save session data to the database
Date:
   02-14-2024
Contributors:
   Devin Grinstead
Methods:
   
Objects:
   app - the Flask object.
"""
from flask import Flask, session
from flask_session import Session

sess = Session()

def init_sess(app: Flask):
    """
    Initializes the session
    """
    sess.init_app(app)

def sid() -> str:
    """
    Gets the current session ID
    """
    return get('sid')

def get(key: str):
    """
    Get a session value
    """
    if not sess.app is None:
        return session.get(key)

def set(key: str, value):
    """
    Sets a session value
    """
    if not sess.app is None:
        session[key] = value

def pop(key: str):
    """
    Removes a session value
    """
    if not sess.app is None:
        session.pop(key)

def clear():
    """
    Clears the session
    """
    if not sess.app is None:
        session.clear()