"""
Purpose:
    Defines data entities and their relationships enabling interatction with PostgreSQL database
Change Log:
    Created by Derrick Sanchez on January 2024
    Changed by Devin Grinstead on 02-27-2024
        Moved the db object from moduels.db.db to modules.db.models
            Moving the db object was nessary to fix ALL app context issues
        Called all time functions was orginally pass method handle instead of method value
Contributors:
    Derrick Sanchez
    Devin Grinstead
Methods:
    * no public methods *
Objects:
    db - Instance of flask_sqlalchemy.SQLAlchemy
"""
from datetime import datetime
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

# HAD to moved to the same file as the models
db = SQLAlchemy()

class UserAccount(db.Model):
    """Represents a user account entity in database"""
    __tablename__ = 'user_account'

    id =db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50),  nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    registered_date = db.Column(db.DateTime(timezone=True), default=func.now())
    last_login = db.Column(db.DateTime(timezone=True))
    email_verified = db.Column(db.Boolean, default=False, nullable=False)

class Chatroom(db.Model):
    """Represents a chatroom where users can send messages"""
    __tablename__ = 'chatroom'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_on = db.Column(db.Date, nullable=False, default=datetime.utcnow())
    owner_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)

    owner = db.relationship('UserAccount', backref=db.backref('chatrooms', lazy=True))
    messages = db.relationship('Message', backref='chatroom', lazy=True)

class Message(db.Model):
    """Represents a message sent by a user"""
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chatroom.id'), nullable=False)

    user = db.relationship('UserAccount', backref=db.backref('messages', lazy=True))

class UserFile(db.Model):
    """Represents a file uploaded by user"""
    __tablename__ = 'user_files'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=True)

    user = db.relationship('UserAccount', backref=db.backref('files', lazy=True))
    message = db.relationship('Message', backref=db.backref('attachments', lazy='dynamic'))

class UserRole(db.Model):
    """Represents a role that can be assigned to a user"""
    __tablename__ = 'user_role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

class UserPermission(db.Model):
    """Represents a permission that can be granted to roles"""
    __tablename__ = 'user_permission'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    permission_name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

class UserPermissionToRole(db.Model):
    """Associates permissions with roles"""
    __tablename__ = 'user_permission_to_role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'))
    user_permission_id = db.Column(db.Integer, db.ForeignKey('user_permission.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

class UserRoleAssignment(db.Model):
    """Assigns roles to users"""
    __tablename__ = 'user_role_assignment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'))
    user_role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

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
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    chatroom = db.relationship('Chatroom', backref=db.backref('access_list', lazy=True))
    user_role = db.relationship('UserRole', backref=db.backref('chatroom_access_list', lazy=True))
    user_permission = db.relationship('UserPermission', backref=db.backref('chatroom_access_list', lazy=True))
    user = db.relationship('UserAccount', backref=db.backref('chatroom_access_list', lazy=True))

class UserVerificationToken(db.Model):
    """Stores tokens for email verification linked to user accounts"""
    __tablename__ = 'user_verification_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    user = db.relationship('UserAccount', backref=db.backref('verification_tokens', lazy=True))

class PasswordRecovery(db.Model):
    """Holds password recovery tokens for users to reset their passwords"""
    __tablename__ = 'password_recovery'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utc.now())

    user = db.relationship('UserAccount', backref=db.backref('recovery_tokens', lazy=True))

class ChatroomMember(db.Model):
    """Tracks membership of users in chatrroms"""
    __tablename__ = 'chatroom_member'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chatroom.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    chatroom = db.relationship('Chatroom', backref=db.backref('members', lazy='dynamic'))
    user = db.relationship('UserAccount', backref=db.backref('chatroom_memberships', lazy='dynamic'))

class Settings(db.Model):
    """user settings"""
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)
    notification_enabled = db.Column(db.Boolean, default=True)
    theme = db.Column(db.String(50), default='light')

    user = db.relationships('UserAccount', backref=db.backref('settings', uselist=False))