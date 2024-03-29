from os import listdir
from os.path import isfile, join, exists, abspath, dirname
from typing import Callable
from flask import Flask
from modules.session_handler import mysession
from modules.db.database import get_chat_rooms, get_online_users

# The object retrived by flask
template_extensions = {}

def template_extension(func: Callable) -> Callable:
    """
    Decorator to add extension methods too dict collection
    """
    template_extensions[func.__name__] = func
    return func

@template_extension
def get_required_js() -> list:
    """
    Fetches all of the required js files form the static/js/required directory
    """
    # Create a relative path from the current dir to the js/required dir
    path = join(dirname(abspath(__file__)), "../../static/js/required")
    
    if exists(path):
        # Loops over the js/required folder and pull all of the files in it
        return [f"js/required/{x}" for x in listdir(path) if isfile(join(path, x))]
    
    # Ensures that the function always returns a list
    return []

@template_extension
def get_required_css() -> list:
    """
    Fetches all of the required css files from the static/css/required directory
    """
    # Create a relative path from the current dir to the css/required dir
    path = join(dirname(abspath(__file__)), "../../static/css/required")
    
    if exists(path):
        # Loops over the css/required folder and pull all of the files in it
        return [f"css/required/{x}" for x in listdir(path) if isfile(join(path, x))]
    
    # Ensures that the function always returns a list
    return []

@template_extension
def get_current_user() -> str:
    """Fetches the current user session"""

    print(mysession.get('USER'))

    return mysession.get('USER')

@template_extension
def get_user_rooms() -> list:
    """
    Fetchs the user's aviable chat rooms
    
    returns
        list
            __item__ -> dict
                name: <room name>
                id: <room id>
    """
    rooms = [{ 'name': x.name, 'id': x.id } for x in get_chat_rooms()]

    print(rooms)

    return rooms

@template_extension
def get_user_friends() -> list:
    """
    Fetchs the user's friend list
    
    returns
        list
            __item__ -> dict
                name: <user display name>
                url: <user profile url>
    """
    users = [{'name': x.username} for x in get_online_users()]

    return users

def init_app(app: Flask):
    """Initalizes the Flask Object template settings"""
    from template import template_blueprint

    app.jinja_env.globals.update(template_extensions)
    app.register_blueprint(template_blueprint)