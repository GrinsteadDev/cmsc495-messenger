"""
Purpose:
   Defines data entities and their relationships enabling interatction with PostgreSQL database
Date:
   January 2024
Contributors:
   <Derrick Sanchez>
   <Contributor 1>
   <etc>
Methods:
   Public methods, privet methods don't need to be included here
"""
from datetime import datetime
from db.db import db
from sqlalchemy.sql import func

class UserAccount(db.Model):
    """Represents a user account entity in database"""
    __tablename__ = 'user_account'

    id =db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50),  nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    registered_date = db.Column(db.DateTime(timezone=True), default=func.now)
    last_login = db.Column(db.DateTime(timezone=True))

class Chatroom(db.Model):
    """Represents a chatroom where users can send messages"""
    __tablename__ = 'chatroom'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_on = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)

    owner = db.relationship('UserAccount', backref=db.backref('chatrooms', lazy=True))
    messages = db.relationship('Message', backref='chatroom', lazy=True)

class Message(db.Model):
    """Represents a message sent by a user"""
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chatroom.id'), nullable=False)

    user = db.relationship('UserAccount', backref=db.backref('messages', lazy=True))

class UserFile(db.Model):
    """Represents a file uploaded by user"""
    __tablename__ = 'user_files'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(50), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)

    user = db.relationship('UserAccount', backref=db.backref('files', lazy=True))

class UserRole(db.Model):
    """Represents a role that can be assigned to a user"""
    __tablename__ = 'user_role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserPermission(db.Model):
    """Represents a permission that can be granted to roles"""
    __tablename__ = 'user_permission'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    permission_name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserPermissionToRole(db.Model):
    """Associates permissions with roles"""
    __tablename__ = 'user_permission_to_role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'))
    user_permission_id = db.Column(db.Integer, db.ForeignKey('user_permission.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserRoleAssignment(db.Model):
    """Assigns roles to users"""
    __tablename__ = 'user_role_assignment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'))
    user_role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('UserAccount', backref=db.backref('role_assignments', lazy=True))
    user_role = db.relationship('UserRole', backref=db.backref('user_assignments', lazy=True))

class ChatRoomAccess(db.Model):
    """Manages access control f/users in chatrooms"""
    __tablename__ = 'chatroom_access'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chatroom.id'))
    user_role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'))
    user_permission_id = db.Column(db.Integer, db.ForeignKey('user_permission.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    chatroom = db.relationship('Chatroom', backref=db.backref('access_list', lazy=True))
    user_role = db.relationship('UserRole', backref=db.backref('chatroom_access_list', lazy=True))
    user_permission = db.relationship('UserPermission', backref=db.backref('chatroom_access_list', lazy=True))
    user = db.relationship('UserAccount', backref=db.backref('chatroom_access_list', lazy=True))
