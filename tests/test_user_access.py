"""
Purpose:
   Banter Box Web Application Testing user Registration
Date: 
   
Contributors:
   Devin Grinstead
   
Methods:
   
Objects:
   app - the Flask object/ Flask test client
"""

import pytest
from os.path import dirname, realpath
from sys import path

# Needed to set path before accessing the  module at parent dir
path.append(f"{dirname(realpath(__file__))}/../")
from app import app as flask_app
from modules.settings import debug_config

print(__name__)

@pytest.fixture
def app():
   # flask_app.config.update(debug_config)
   app = flask_app
   app.testing = True
   return app

@pytest.fixture
def client(app):
   return app.test_client()

def test_register_user(client):
   """
   Test registering a user
   """
   data = {
      'first-name': 'John',
      'last-name': 'Doe',
      'username': 'johndoe',
      'email': 'johndoe@example.com',
      'password': 'password',
      'password-confirm': 'password',
      'status': 'active',
   }
   response = client.post('/api/register', data=data)
   assert response.status_code == 200
    
   # Check response data
   json_data = response.get_json()
   assert json_data['message'] == 'User registered successfully'
   assert json_data['user_info']['username'] == 'johndoe'

'''
def test_user_login(client):
   """
   Test user login with valid credentials
   """
   data = {
      'username': 'johndoe',
      'password': 'password',
      'status': 'active'
   }
   response = client.post('/api/login', data=data)
   assert response.status_code == 200

   json_data = response.get_json()
   assert json_data['message'] == 'Login successful'
   assert json_data['user_info']['username'] == 'johndoe'

def test_user_logout(client):
   """
   Test user logout once logined
   """
   data = {}
   response = client.post('/api/logout', data=data)

   json_data = response.get_json()
   assert json_data['message'] == 'Logout successful'

'''