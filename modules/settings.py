"""
Purpose:
    Banter Box Web Application Setting Module settings.py
    Exposes two settings objects called ReleaseConfig and DebugConfig
Change Log:
    Created by Devin Grinstead :
        Created Dict object file_blacklist and function match_file_blacklist
    Changed by Derrick Sanches
        Created a config dict object for setting SQLAlchemy info
    Changed by Devin Grinstead
        Created a debug_config dict object
    Changed by Devin Grinstead on 02-27-2024:
        Refactored code to object based config from dictionary based config
            config(dict) to ReleaseConfig(object)
            debug_config(dict) to DebugConfig(object)
        Refactored code to object based file black list
            file_blacklist(dict) to FileBlacklist
Contributors:
    Devin Grinstead
    Derrick Sanchez

Methods:
    init_app_settings
        Configures the passed Flask app
Objects:
    BaseConfig
    ReleaseConfig
    DebugConfig
    file_blacklist - Instance of modules.common_objs.UpperMatchList object def
"""
from os import environ
from datetime import timedelta
# Initializes the Modules that need initialization
from flask import Flask, current_app
from modules.db.db import init_app as init_app_db
from modules.session_handler.mysession import init_sess as init_app_sess
from modules.rest.api import api_blueprint as app_blueprint
from modules.template_extensions.extension import init_app as init_app_template
from modules.template_extensions.template import set_file_blacklist
from modules.common_objs import UpperMatchList

class BaseConfig(object):
    """Base config, stages the database"""
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)
    SESSION_TYPE = 'SqlAlchemySessionInterface'
    
    @property
    def PERMANENT_SESSION_LIFETIME(self):
        """Fetches the session lifetime in minutes from the .env or returns 15"""
        return timedelta(minutes=float(environ.get('SESSION_LIFETIME', '15')))
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        """
        Builds the Database Connection URL based on the Environment Variables
        
        DB URL FORMAT '{db_type}{db_driver}://{db_user}:{db_pwd}@{db_url}{db_port}/{db_db}'
        DB URL EXAMPLE 'postgresql://user:password@localhost/mydatabase
        """
        db_type = environ.get('DB_TYPE')
        db_driver = '+' + environ.get('DB_DRIVER') if environ.get('DB_DRIVER', False) else ''
        db_user = environ.get('DB_USER')
        db_pwd = environ.get('DB_PWD')
        db_url = environ.get('DB_URL')
        db_port = ':' + environ.get('DB_PORT') if environ.get('DB_PORT', False) else ''
        db_db = environ.get('DB_DATABASE')

        return f"{db_type}{db_driver}://{db_user}:{db_pwd}@{db_url}{db_port}/{db_db}"


class ReleaseConfig(BaseConfig):
    """
    Release Flask Config
    
    Sets the config to the settings required for release settings
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_NAME = 'SESSidxbanterboxFLASKAPI'
    SESSION_COOKIE_DOMAIN = 'messenger.dgwebllc.com'

class DebugConfig(BaseConfig):
    """
    Debug Flask Config

    Sets the config to the basic settings desired for debug testing
    """
    EXPLAIN_TEMPLATE_LOADING = True
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

file_blacklist = UpperMatchList([
    "base.html",
    "head.html"
])

def init_app_settings(app: Flask = None, debug: bool = False)-> Flask:
    """
    Initializes the Settings object and modules

    Defaults to a new app object if no app object is supplied
    """
    if app is None:
        app = Flask(__name__)
    
    with app.app_context():
        if not debug:
            debug = bool(environ.get('DEBUG', False))

        if debug:
            app.config.from_object(DebugConfig())
        else:
            app.config.from_object(ReleaseConfig())

        set_file_blacklist(file_blacklist)

        # Sets sql alchemy to drop the existing tables when ran in debug mode
        if debug:
            init_app_db(app, True)
        else:
            init_app_db(app)
        
        init_app_sess(app)
        init_app_template(app)
        app.register_blueprint(app_blueprint)

    return app
