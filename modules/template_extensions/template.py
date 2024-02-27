from flask import Blueprint, render_template, request
from jinja2.exceptions import TemplateNotFound
from modules.common_objs import UpperMatchList

template_blueprint = Blueprint('template', __name__)
file_blacklist = UpperMatchList()

def set_file_blacklist(blacklist: UpperMatchList):
    global file_blacklist
    file_blacklist = blacklist

@template_blueprint.route("/", defaults={"name": "login", "ext": "html"})
@template_blueprint.route("/<string:name>", defaults={"ext": ""})
@template_blueprint.route("/<string:name>.<string:ext>")
def fetch_templates(name, ext):
    # Fetches a template as a webpage url or returns 404
    if ext in ["", "html", "htm"] and not file_blacklist.pattern_match(name=f"{name}.*"):
        try:
            return render_template(f"{name}.html", request_name=name, request_url=request.base_url)
        except TemplateNotFound as e:
            pass

    return "", 404
