import os
from flask import Flask, render_template, request
from git import Repo
import jinja2

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/<string:name>", defaults={"ext":""})
@app.route("/<string:name>.<string:ext>")
def fetch_templates(name, ext):
    # Attemps to fetch a template
    if ext in ["", "html", "htm"]:
        try:
            return render_template(f"{name}.html")
        except jinja2.exceptions.TemplateNotFound as e:
            pass
    
    return "", 404

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

@app.route("/<string:name>/")
def say_hello(name):
    return f"Hello {name}!<br>Nice Name!<br> Testing Change<br> New Changes"



if __name__ == "__main__":
    app.run()
