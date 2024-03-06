"""
Purpose:
    Access point for Initializing the sql flask database
Change Log:
    Created by Derrick Sanchez on January 2024
    Changed by Devin Grinstead on 02-27-2024
        Moved the db object from moduels.db.db to modules.db.models
            Moving the db object was nessary to fix ALL app context issues
Contributors:
    Derrick Sanchez
    Devin Grinstead
Methods:
    init_app(app: Flask)
        Initializes the sql flask database
"""
from flask import Flask
from models import *

def init_app(app: Flask, drop_tables: bool = False):
    """Initialize the application with the database"""
    global db
    db.init_app(app)
    # this is needed in order for database session calls (e.g. db.session.commit)
    try:
        if drop_tables:
            # Added to allow for changes to the database
            db.drop_all()
        
        db.create_all()
    except Exception as exception:
        print("got the following exception when attempting db.create_all() in db.py: " + str(exception))
    finally:
        print("db.create_all() in db.py was successfull - no exceptions were raised")

