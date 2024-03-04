"""
Purpose:
    Banter Box Web Application Main Entry Point
Change Log:
    Changed by Devin Grinstead on 02-27-2024
        Refactored the app.py to use the init_app_settins method from modules.settings

Contributors:
    Devin Grinstead
    Catherine Casey
Methods:

Objects:
    app - the Flask object.
"""
import os
from flask import Flask
from git import Repo
# Custom Modules located at ./modules/*
from modules.settings import init_app_settings

app = Flask(__name__)

init_app_settings(app)

@app.route("/git-push/", methods=['GET', 'POST'])
def update_repository():
    curr_dir = os.path.dirname(os.path.realpath(__file__))

    # Validation to make sure this is a webhook from git here
    # ...

    # Retrives the pull request for the current directory
    repo = Repo(curr_dir)
    repo.remotes.origin.pull()

    # Restarts the cPanel passeneger server
    if os.path.isfile(curr_dir + "/../tmp/restart.txt"):
        os.utime(curr_dir + "/../tmp/restart.txt", None)

    # Returns the 200 S_OK Status code
    return "", 200


if __name__ == "__main__":
    """
    Only called when run during local execution or app debug
    """
    init_app_settings(app, True)
    app.run(debug=True)
