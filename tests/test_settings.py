"""
Purpose:
    Banter Box Web Application Testing Flask Settings modules.settings
    The test_settings.py file tests the settings module by:
        Verifying the values for modules.settings.BaseConfig are correct
        Verifying the values for modules.settings.ReleaseConfig are correct
        Verifying the values for modules.settings.DebugConfig are correct
        Verifying that a Flask app object is able to load the settings
        Verifying that the instance file_blacklist is able to verfy if items are in the blacklist 
Change Log: 
    Created by Devin Grinstead on 02-27-2024
Contributors:
    Devin Grinstead
Methods:
    test_base_config
    test_release_config
    test_debug_config
    test_flask_app_config
    test_file_blasklist
"""

import pytest
from os.path import dirname, realpath
from os import environ
from datetime import timedelta
from sys import path
import re
from flask import Flask

# Needed to set path before accessing the  module at parent dir
path.append(f"{dirname(realpath(__file__))}/../")
from modules import settings

@pytest.fixture()
def base_cfg():
    return settings.BaseConfig()

@pytest.fixture()
def release_cfg():
    return settings.ReleaseConfig()

@pytest.fixture()
def debug_cfg():
    return settings.DebugConfig()

@pytest.fixture()
def file_blacklist():
    return settings.file_blacklist

def test_base_config(base_cfg):
    """Tests the BaseConfig Configuration Object"""
    rg_pattern = r'[a-z|A-Z|0-9_]*(?:\+[a-z|A-Z]*)?://[a-z|A-Z|0-9_]*:[a-z|A-Z|0-9_]*@[a-z|A-Z|0-9_]*(?:\:[a-z|A-Z|0-9_]*)?/[a-z|A-Z|0-9_]*'

    assert base_cfg.PERMANENT_SESSION_LIFETIME == timedelta(
        minutes=float(environ.get('SESSION_LIFETIME', '15'))
    )
    assert base_cfg.SESSION_TYPE == 'SqlAlchemySessionInterface'
    assert re.match(rg_pattern, base_cfg.SQLALCHEMY_DATABASE_URI) != None

def test_release_config(release_cfg):
    """Tests the ReleaseConfig Configuration Object"""
    assert release_cfg.SQLALCHEMY_TRACK_MODIFICATIONS == False
    assert release_cfg.SESSION_COOKIE_NAME == 'SESSidxbanterboxFLASKAPI'
    assert release_cfg.SESSION_COOKIE_DOMAIN == 'messenger.dgwebllc.com'

def test_debug_config(debug_cfg):
    """Tests the DebugConfig Configuration Object"""
    assert debug_cfg.EXPLAIN_TEMPLATE_LOADING == True
    assert debug_cfg.DEBUG == True
    assert debug_cfg.TESTING == True

def test_flask_app_config(release_cfg):
    """Test that the flask app accepts the Configuration Object"""
    app = Flask(__name__)
    rg_pattern = r'[a-z|A-Z|0-9_]*(?:\+[a-z|A-Z]*)?://[a-z|A-Z|0-9_]*:[a-z|A-Z|0-9_]*@[a-z|A-Z|0-9_]*(?:\:[a-z|A-Z|0-9_]*)?/[a-z|A-Z|0-9_]*'

    settings.init_app_settings(app)

    assert app.config['PERMANENT_SESSION_LIFETIME'] == timedelta(
        minutes=float(environ.get('SESSION_LIFETIME', '15'))
    )
    assert app.config['SESSION_TYPE'] == 'SqlAlchemySessionInterface'
    assert re.match(rg_pattern, app.config['SQLALCHEMY_DATABASE_URI']) != None
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False
    assert app.config['SESSION_COOKIE_NAME'] == 'SESSidxbanterboxFLASKAPI'
    assert app.config['SESSION_COOKIE_DOMAIN'] == 'messenger.dgwebllc.com'

def test_file_blasklist(file_blacklist):
    """Tests the file_blacklist FileBlacklist object instance"""
    assert file_blacklist.pattern_match('base.*') == True
    assert file_blacklist.pattern_match('base') == False
    assert file_blacklist.pattern_match('fff') == False
