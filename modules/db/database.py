from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import bcrypt
from models import UserAccount
from db.db import db


def get_user(username):
    """Retrieve a user from the database by username"""
    user = UserAccount.query.filter_by(username=username).first()
    return user if user else None


def verify_user(username, password):
    """Verify user credentials against stored data"""
    user = get_user(username)
    if user:
      hashed_password = user.password
      provided_password = password.encode('utf-8')
      if bcrypt.checkpw(provided_password, hashed_password):
            return True
    return False


def register_user(first_name, last_name,  username, email, password):
    """Register a new user in the database"""

    # hash and salt password before storing in db
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

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
