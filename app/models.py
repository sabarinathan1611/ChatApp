from pymongo.errors import OperationFailure
from pymongo import MongoClient
from .config import Config as user
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

class User:
    def __init__(self, username, email, password, verification_token=None, is_verified=False):
        self.username = username
        self.email = email
        self.password = password
        self.verification_token = verification_token
        self.is_verified = is_verified

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    def check_password(self, input_password):
        return check_password_hash(self.password, input_password)

def get_user(username):
    user_data = user.users_db.find_one({'_id': username})

    if user_data:
        return User(user_data['_id'], user_data['email'], user_data['password'], user_data['verification_token'], user_data['is_verified'])
    else:
        return None

def save_user(username, email, password):
    try:
        password_hash = generate_password_hash(password)
        verification_token = secrets.token_urlsafe()

        user.users_db.insert_one({
            '_id': username,
            'email': email,
            'password': password_hash,
            'verification_token': verification_token,
            'is_verified': False
        })

        print("User saved successfully.")
    except OperationFailure as e:
        print(f"Failed to save user: {e}")
