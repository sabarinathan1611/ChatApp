#config.py
import os
from pymongo import MongoClient

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(16))
    DEBUG = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('GMAIL_USERNAME')
    print('MAIL_USERNAME',MAIL_USERNAME)
    MAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')
    print('GMAIL_PASSWORD',MAIL_PASSWORD)
    ADMIN_MAIL = os.environ.get('ADMINMAIL','sabarinathan.project@gmail.com')

    WTF_CSRF_SECRET_KEY = os.environ.get('CSRF_SECRET_KEY', os.urandom(16))

    # MongoDB connection setup
    MONGO_URI = os.environ.get('MONGO_URI')
    print(MONGO_URI)
    client = MongoClient(MONGO_URI)
    DB_NAME = os.environ.get('DB_NAME', 'ChatApp')
    db = client[DB_NAME]
    users_db=db.get_collection("users")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

def get_config(mode='default'):
    return config_by_name.get(mode, DevelopmentConfig)
