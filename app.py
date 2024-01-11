import os
from flask import Flask, request
from git import Repo

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/git-push/", methods=['GET', 'POST'])
def update_repository():
    curr_dir = os.path.dirname(os.path.realpath(__file__))

    # Retrives the pull request for the current directory
    repo = Repo(curr_dir)
    repo.remotes.origin.pull()
    
    # Restarts the cPanel passeneger server
    if os.path.isfile(curr_dir + "/../tmp/restart.txt"):
        os.utime(curr_dir + "/../tmp/restart.txt", None)
    
    # Returns the 200 S_OK Status code
    return "", 200

@app.route("/<string:name>/")
def say_hello(name):
    return f"Hello {name}!<br>Nice Name!<br> Testing Change"

if __name__ == "__main__":
    app.run()
