import os
from flask import Flask, render_template, request, jsonify
from git import Repo
import jinja2
# Custom Modules located at ./modules/*
from modules import settings
from modules.rest import api
from modules.template_extensions import extension
from modules.db.db import init_app as init_db

app = Flask(__name__)
init_db(app)
app.register_blueprint(api.api_blueprint)
app.jinja_env.globals.update(extension.template_extensions)

@app.route("/", defaults={ "name":"home", "ext":"html" })
@app.route("/<string:name>", defaults={ "ext":"" })
@app.route("/<string:name>.<string:ext>")
def fetch_templates(name, ext):
    # Fetches a template as a webpage url or returns 404
    if ext in ["", "html", "htm"] and not settings.match_file_blacklist(name=f"{name}.*"):
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

if __name__ == "__main__":
    app.run()
