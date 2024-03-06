"""
Purpose:
   Defines functions for interacting with the database such as retriving information, adding users, etc
Date:
   January 2024
Contributors:
   <Derrick Sanchez>
   <Contributor 1>
   <etc>
Methods:
   Public methods, privet methods don't need to be included here
"""

import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask import current_app
import bcrypt
from models import Chatroom, ChatroomMember, Message, PasswordRecovery, Settings, UserAccount, UserFile, UserPermission, UserPermissionToRole, UserRoleAssignment, UserVerificationToken, db
import secrets

def get_user(username):
    """Retrieve a user from the database by username"""
    print(current_app.config)

    with current_app.app_context():
        user = UserAccount.query.filter_by(username=username).first()
    
    return user if user else None


def verify_user(username, password):
    """Verify user credentials against stored data"""
    user = get_user(username)
    if user:
      hashed_password = user.password.encode('utf-8')
      provided_password = password.encode('utf-8')
      if bcrypt.checkpw(provided_password, hashed_password):
            return True
    return False


def register_user(first_name, last_name,  username, email, password):
    """Register a new user in the database"""
    # hash and salt password before storing in db
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    with current_app.app_context():
        new_user = UserAccount(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=hashed_password.decode('utf-8')
        )
        db.session.add(new_user)
        try:
            db.session.commit()
            return None
        except IntegrityError as e:
            db.session.rollback()
            print(f"Integrity Error during registration: {e}")
            return {'error': 'IntegrityError', 'message': str(e)}
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy Error during registration: {e}")
            return {'error': 'SQLAlchemyError', 'message': str(e)}

def user_has_permission(user_id, permission_name):
    """Query to check if user has specific permission through role"""
    permission_exists = db.session.query(
        db.exists().where(UserPermission.permission_name == permission_name)
        .join(UserPermissionToRole, UserPermissionToRole.user_permission_id == UserPermission.id)
        .join(UserRoleAssignment, UserRoleAssignment.user_role_id == UserPermissionToRole.user_role_id)
        .where(UserRoleAssignment.user_id == user_id)
    ).scalar()

    return permission_exists

def get_all_permissions():
    """Query to get all permissions from table"""
    permissions = UserPermission.query.all()
    return permissions


def upload_file_todb(user_id, file_name, file_data):
    """Upload a file to the database"""
    with current_app.app_context():
        new_file = UserFile(user_id=user_id, file_name=file_name, file_data=file_data)
        db.session.add(new_file)
        try:
            db.session.commit()
            update_user_last_login(user_id)
            return {'message': 'File Successfully Uploaded.'}
        except Exception as e:
            db.session.rollback()
            print(f"Error Uploading File: {e}")
            return {'error': 'UploadError', 'message': str(e)}
        
def get_file_from_db(file_id):
    """Retrieve a file from the database by the file id"""
    with current_app.app_context():
        file = UserFile.query.get(file_id)
        if file:
            return {'file_name': file.file_name, 'file_data': file.file_data}
        else:
            return {'message' : 'File Not Found'}
        
def search_files_by_name(user_id, file_name):
    """Search for files by name associated with a specific user"""
    with current_app.app_context():
        files = UserFile.query.filter_by(user_id=user_id, file_name=file_name).all()
        if files:
            update_user_last_login(user_id)
            return [{'file_id': file.id, 'file_name': file.file_name} for file in files]
        else:
            return {'message': 'No Files Found.'}
        
def store_message(user_id, chatroom_id, text):
    """Store a new message in the database"""
    new_message = Message(user_id=user_id, chatroom_id=chatroom_id, text=text)
    db.session.add(new_message)
    try:
        db.session.commit()
        update_user_last_login(user_id)
        return{'message': 'Message Successfully Stored', 'messge_id': new_message.id}
    except Exception as e:
        db.session.rollback()
        return {'error': 'Message storage failed', 'details': str(e)}
    
def get_message(message_id):
    """Retrieve a message by its id"""
    message = Message.query.get(message_id)
    if message:
        return {
            'message_id': message_id,
            'text': message.text,
            'user_id': message.user_id,
            'chatroom_id': message.chatroom_id
        }
    else:
        return {'message': 'Message Not Found.'}
    
def generate_verification_token(user_id):
    """Generates and stores a unique verification token for a user"""
    token = secrets.token_urlsafe()
    new_token = UserVerificationToken(token=token, user_id=user_id)
    db.session.add(new_token)
    db.session.commit()
    return token

def verify_user_email(token):
    """Verifies user email based on the provided token"""
    token_record = UserVerificationToken.query.filter_by(token=token).first()
    if token_record:
        user = token_record.user
        user.email_verified = True
        db.session.delete(token_record)
        db.session.commit()
        return True
    return False

def initiate_password_recovery(email):
    """Initiates password recovery by generating a token"""
    user = UserAccount.query.filter_by(email=email).first()
    if user:
        token = secrets.token_urlsafe()
        recovery_record = PasswordRecovery(token=token, user_id=user.id)
        db.session.add(recovery_record)
        db.session.commit()
        return token
    return None

def reset_password_with_token(token, new_password):
    """Resets user password using valid password recovery token"""
    recovery_record = PasswordRecovery.query.filter_by(token=token).first()
    if recovery_record:
        user = recovery_record.user
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password.decode('utf-8')
        db.session.delete(recovery_record)
        db.session.commit()
        return True
    return False

def create_room(name, owner_id):
    """Creates new Chatroom"""
    new_room = Chatroom(name=name, owner_id=owner_id)
    db.session.add(new_room)
    try:
      db.session.commit()
      update_user_last_login(owner_id)
      return new_room.id
    except Exception as e:
        db.session.rollback()
        return None

def delete_room(room_id, user_id):
    """Deletes Chatrooom"""
    room = Chatroom.query.get(room>id)
    if room and room.owner_id == user_id:
        db.session.delete(room)
        db.session.commit()
        update_user_last_login(user_id)
        return True
    return False

def get_chat_rooms():
    """Returns all chatrooms"""
    return Chatroom.query.all()

def join_room(user_id, room_id):
    """Allows user to join specific chatroom"""
    new_membership = ChatroomMember(user_id=user_id, chatroom_id=room_id)
    db.session.add(new_membership)
    try:
      db.session.commit()
      update_user_last_login(user_id)
      return True
    except Exception as e:
        db.session.rollback()
        return False

def update_settings(user_id, notififcation_enabled=None, theme=None):
    """Allows user to update settings"""
    settings = Settings.query.filter_by(user_id=user_id).first()
    if not settings:
        settings = Settings(user_id=user_id)
        db.session.add(settings)

    if notififcation_enabled is not None:
        settings.notification_enabled = notififcation_enabled
    if theme:
        settings.theme = theme

    db.session.commit()
    update_user_last_login(user_id)
    return True

def update_user_last_login(user_id):
    """Updates last_login field f/user"""
    user = UserAccount.query.get(user_id)
    if user:
        user.last_login = datetime.utcnow()
        try:
          db.session.commit()
        except Exception as e:
            print(f"Error updating last_login: {e}")
            db.session.rollback()

def get_online_users():
    """Tracks online users if they've been active within 15 minutes"""
    threshold = datetime.now() - datetime.timedelta(minutes=15)
    online_users = UserAccount.query.filter(UserAccount.last_login >= threshold).all()
    return online_users