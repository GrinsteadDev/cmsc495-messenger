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

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask import current_app
import bcrypt
from models import Message, UserAccount, UserFile, UserPermission, UserPermissionToRole, UserRoleAssignment, db

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
            return [{'file_id': file.id, 'file_name': file.file_name} for file in files]
        else:
            return {'message': 'No Files Found.'}
        
def store_message(user_id, chatroom_id, text):
    """Store a new message in the database"""
    new_message = Message(user_id=user_id, chatroom_id=chatroom_id, text=text)
    db.session.add(new_message)
    try:
        db.session.commit()
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