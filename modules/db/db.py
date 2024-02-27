# db.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# When imported from a top level db.db could mean db.db (module.module) or db.db (module.variable)
# chaning the name to db_obj or accessing as db.db.db (module.module.variable) will remove the python
# import moudle functions confusion
db = SQLAlchemy()

def init_app(app: Flask):
    """Initialize the application with the database"""
    db.init_app(app)

    # this is needed in order for database session calls (e.g. db.session.commit)
    with app.app_context():
      try:
          db.create_all()
      except Exception as exception:
          print("got the following exception when attempting db.create_all() in db.py: " + str(exception))
      finally:
          print("db.create_all() in db.py was successfull - no exceptions were raised")