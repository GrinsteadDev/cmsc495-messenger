from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import bcrypt
from models import UserAccount
from db import db


def get_user(username):
    user = UserAccount.query.filter_by(username=username).first()
    return user


def verify_user(username, password):
    user = get_user(username)
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return True
    else:
        print("user not found")
        return False


def register_user(first_name, last_name,  username, email, password):
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
        return new_user
    except IntegrityError as e:
        db.session.rollback()
        print(f"Integrity Error during registration: {e}")
        return {'error': 'IntegrityError', 'message': str(e)}
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"SQLAlchemy Error during registration: {e}")
        return {'error': 'SQLAlchemyError', 'message': str(e)}
