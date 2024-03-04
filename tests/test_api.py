"""
Purpose:
   Banter Box Web Application testing api endpoints
Date: 
   
Contributors:
   Catherine Casey
   
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
from modules.settings import DebugConfig

@pytest.fixture
def app():
    flask_app.config.from_object(DebugConfig())
    app = flask_app
    app.testing = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_user(client):
    # Test registering a user
    data = {
        'first-name': 'John',
        'last-name': 'Doe',
        'username': 'johndoe',
        'email': 'johndoe@example.com',
        'password': 'password',
        'status': 'active'
    }
    response = client.post('/api/register', data=data)
    assert response.status_code == 200
    
      # Check response data
    json_data = response.get_json()
    assert json_data['message'] == 'User registered successfully'
    assert json_data['user_info']['username'] == 'johndoe'

def test_verify_email(client):
    # Email verification with valid token
    response = client.post('/api/verify-email/valid_token')
    assert response.status_code == 200
    
    json_data = response.get_json()
    assert json_data['message'] == 'Email verification successful'

def test_user_login(client):
    # Test user login with valid credentials
    data = {
        'username': 'demo',
        'password': 'password',
        'status': 'active'
    }
    response = client.post('/api/login', data=data)
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data['message'] == 'Login successful'
    assert json_data['user_info']['username'] == 'demo'

def test_password_recovery(client):
    data = {
        'email': 'user@example.com'
    }
    response = client.post('/api/password-recovery', data=data)
    assert response.status_code == 200

def test_get_chat_rooms(client):
    response = client.get('/api/chat-rooms')
    assert response.status_code == 200

    chat_rooms = response.get_json()
    assert isinstance(chat_rooms, list)
    assert len(chat_rooms) == 3

def test_join_room(client):
    # joining a room
    response = client.get('/api/join-room?room_id=1&user_id=1')
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data['message'] == 'User 1 joined room 1'

def test_get_online_users(client):
    # getting online users
    response = client.get('/api/online-users')
    assert response.status_code == 200

    online_users = response.get_json()
    assert isinstance(online_users, list)
    assert len(online_users) == 3

def test_send_message(client):
    data = {
        'user_id': 1,
        'message': 'Test message',
        'timestamp': '2024-02-13T12:00:00Z'
    }
    response = client.post('/api/send-message', json=data)
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data['message'] == 'Message sent successfully'

def test_peek_message(client):
    response = client.get('/api/peek-message')
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data['sender'] == 'user1'
    assert json_data['content'] == 'Hello there!'

def test_create_room(client):
    data = {
        'room_name': 'Test Room',
        'creator_id': 1
    }
    response = client.post('/api/create-room', json=data)
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data['message'] == 'Room "Test Room" created successfully by user 1'

def test_delete_room(client):
    # Test deleting a room
    data = {
        'room_id': 1,
        'admin_id': 1
    }
    response = client.post('/api/delete-room', json=data)
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data['message'] == 'Room 1 deleted successfully by admin 1'

def test_update_setting(client):
    # Test updating a setting
    data = {
        'value': 'new_value'
    }
    response = client.post('/api/settings/setting_id', json=data)
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data['message'] == 'Setting setting_id updated successfully'
    assert json_data['setting_id'] == 'setting_id'
    assert json_data['new_value'] == 'new_value'

def test_update_settings(client):
    data = {
        '<setting-id>': 'setting_id',
        '<new-value>': 'new_value'
    }
    response = client.post('/api/settings', data=data)
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data['message'] == 'Setting setting_id updated successfully'
    assert json_data['setting_id'] == 'setting_id'
    assert json_data['new_value'] == 'new_value'
