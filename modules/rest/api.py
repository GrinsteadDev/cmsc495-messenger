from flask import Flask, Blueprint

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/api/")
def sample():
    """
    """
    
