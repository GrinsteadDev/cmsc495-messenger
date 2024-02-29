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
from models import UserAccount, UserPermission, UserPermissionToRole, UserRoleAssignment, db

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
