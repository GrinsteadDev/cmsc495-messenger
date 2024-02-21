# db.py
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

# When imported from a top level db.db could mean db.db (module.module) or db.db (module.variable)
# chaning the name to db_obj or accessing as db.db.db (module.module.variable) will remove the python
# import moudle functions confusion
db = SQLAlchemy()

def init_app(app):
    """Initialize the application with the database"""
    db.init_app(app=app)

    print("Current app is flask app {}".format(current_app == app))
    # this is needed in order for database session calls (e.g. db.session.commit)
    with app.app_context():
      try:
          db.create_all()
      except Exception as exception:
          print("got the following exception when attempting db.create_all() in db.py: " + str(exception))
      finally:
          print("db.create_all() in db.py was successfull - no exceptions were raised")