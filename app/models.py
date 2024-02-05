from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import secrets


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    role =  db.Column(db.String(100),nullable=False,default='user')
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(32), default=secrets.token_urlsafe)

