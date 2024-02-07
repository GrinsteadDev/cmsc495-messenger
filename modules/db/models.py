from .db import db
from sqlalchemy.sql import func

class UserAccount(db.Model):
    __tablename__ = 'user_account'

    id =db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), unique=True, nullable=False)
    last_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    registered_date = db.Column(db.DateTime(timezone=True), default=func.now)
    last_login = db.Column(db.DateTime(timezone=True))