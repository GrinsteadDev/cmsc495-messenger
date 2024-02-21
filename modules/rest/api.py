"""
Purpose:
   Banter Box Web Application Main API endpoints
Date:
   
Contributors:
   Catherine Casey
   Devin Grinstead - Ammened on 2-20-2024
Methods:
   
Objects:
   app - the Flask object.
"""
# TODO Add comment docs
from datetime import datetime
from flask import Blueprint, request, jsonify
from modules.db.database import register_user as db_register_user, verify_user as db_verify_user, get_user as db_get_user
from modules.session_handler import mysession

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/api/")
def sample():
    """
    """

@api_blueprint.route("/api/register", methods=['POST'])
def register_user():
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    password_confim = request.form.get('password-confirm')

    # Verfiys that the passwords match
    # TODO Add password complexity checks
    if password_confim == password:
        register_user_rp = db_register_user(first_name, last_name, username, email, password)
        if register_user_rp is None:
            response = {
                'message': 'User registered successfully',
                'user_info': {
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username,
                    'email': email,
                    'status': 'active'
                }
            }
        else:
            response = {
                'message': 'User Registration Failed'
            }
    else:
        response = {
            'message': 'Passwords must match'
        }
    
    return jsonify(response)

@api_blueprint.route('/api/login', methods=['POST'])
def user_login():
    # Get data from the form
    username = request.form.get('username')
    password = request.form.get('password')

    # Clears active session if any
    mysession.clear()

    # Check credentials on database
    if db_verify_user(username, password):
        # Updates user login
        user = db_get_user(username)
        user.last_login = datetime.now()
        # Sets Session information
        mysession.set('USER', username)
        mysession.set('STATUS', 'logged-in')

        response = {
            'message': 'Login successful',
            'user_info': {
                'username': mysession.get('USER'),
                'status': mysession.get('STATUS')
            }
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Invalid credentials'}), 401  # Unauthorized status code

@api_blueprint.route('/api/logout', methods=['POST'])
def user_logout():
    # User Authorization handled by session handler 'mysession'
    # Authorization headers are used by .htaccess and apache. Making
    # them rarely accessed from the code directly.
    """
    authorization_header = request.headers.get('Authorization')
    if not authorization_header or not authorization_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized'}), 401  

    access_token = authorization_header.split(' ')[1]

    logout_message = request.form.get('message')
    """

    # Logout logic
    # By clearing the session the user is affectively logged out
    mysession.clear()
    response = {
        'message': 'Logout successful'
    }
    return jsonify(response)

# New route for email verification
@api_blueprint.route("/api/verify-email/<verification_token>", methods=['POST'])
def verify_email(verification_token):
    # need to check token on database
    if verification_token == "valid_token":
        return jsonify({'message': 'Email verification successful'})
    else:
        return jsonify({'error': 'Invalid verification token'}), 400

@api_blueprint.route('/api/password-recovery', methods=['POST'])
def password_recovery():
    user_email = request.form.get('email')

    # Perfrom user recovery, (recovery email and generate token)
    response = {
        'message': 'Password recovery email sent.',
        'user_info': {
            'email': user_email
        }
    }
    return jsonify(response)
  
@api_blueprint.route('/api/chat-rooms', methods=['GET'])
def get_chat_rooms():

    chat_rooms = [
        {'id': 1, 'name': 'Room 1'},
        {'id': 2, 'name': 'Room 2'},
        {'id': 3, 'name': 'Room 3'}
    ]
    return jsonify(chat_rooms)

@api_blueprint.route('/api/join-room', methods=['GET'])
def join_room():

    room_id = request.args.get('room_id')
    user_id = request.args.get('user_id')

    response = {
        'message': f'User {user_id} joined room {room_id}'
    }

    return jsonify(response)    

@api_blueprint.route('/api/online-users', methods=['GET'])
def get_online_users():

    online_users = [
        {'id': 1, 'username': 'user1'},
        {'id': 2, 'username': 'user2'},
        {'id': 3, 'username': 'user3'}
    ]
    return jsonify(online_users)

@api_blueprint.route('/api/send-message', methods=['POST'])
def send_message():

    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')
    timestamp = data.get('timestamp')

    response = {
        'message': 'Message sent successfully',
        'user_id': user_id,
        'message': message,
        'timestamp': timestamp
    }

    return jsonify(response)

@api_blueprint.route('/api/peek-message', methods=['GET'])
def peek_message():
 
    message = {
        'sender': 'user1',
        'content': 'Hello there!',
        'timestamp': '2024-02-06T12:00:00Z'
    }
    return jsonify(message)

def get_message():
    
    message = {
        'sender': 'user1',
        'content': 'This is a sample message.',
        'timestamp': '2024-02-06T12:00:00Z'
    }
    return jsonify(message)

@api_blueprint.route('/api/create-room', methods=['POST'])
def create_room():
    data = request.json
    # Assuming the JSON contains 'room_name' and 'creator_id'
    room_name = data.get('room_name')
    creator_id = data.get('creator_id')

    # Dummy response for logic to create room
    response = {
        'message': f'Room "{room_name}" created successfully by user {creator_id}.',
        'room_name': room_name,
        'creator_id': creator_id
    }

    return jsonify(response)  

@api_blueprint.route('/api/delete-room', methods=['POST'])
def delete_room():
    data = request.json
    # Assuming the JSON contains 'room_id' and 'admin_id'
    room_id = data.get('room_id')
    admin_id = data.get('admin_id')

    response = {
        'message': f'Room {room_id} deleted successfully by admin {admin_id}.',
        'room_id': room_id,
        'admin_id': admin_id
    }

    return jsonify(response)

@api_blueprint.route('/api/settings/<setting_id>', methods=['POST'])
def update_setting(setting_id):
    data = request.json
    new_value = data.get('value')

    # Dummy response for settings
    response = {
        'message': f'Setting {setting_id} updated successfully.',
        'setting_id': setting_id,
        'new_value': new_value
    }

    return jsonify(response)

@api_blueprint.route('/api/settings', methods=['POST'])
def update_settings():
    setting_id = request.form.get('<setting-id>')
    new_value = request.form.get('<new-value>')

    response = {
        'message': f'Setting {setting_id} updated successfully.',
        'setting_id': setting_id,
        'new_value': new_value
    }

    return jsonify(response)
