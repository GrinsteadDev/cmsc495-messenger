import os
from flask import Flask, request
from git import Repo

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/git-push/", methods=['GET', 'POST'])
def update_repository():
    repo = Repo(os.path.dirname(os.path.realpath(__file__)))
    repo.remotes.orgin.pull()
    return "", 200

@app.route("/<string:name>/")
def say_hello(name):
    return f"Hello {name}!"

if __name__ == "__main__":
    app.run()
