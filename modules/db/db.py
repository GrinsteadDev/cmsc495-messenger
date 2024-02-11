# db.py
from flask_sqlalchemy import SQLAlchemy

# When imported from a top level db.db could mean db.db (module.module) or db.db (module.variable)
# chaning the name to db_obj or accessing as db.db.db (module.module.variable) will remove the python
# import moudle functions confusion
db = SQLAlchemy() 

def init_app(app):
    """Initialize the application with the database"""
    db.init_app(app)