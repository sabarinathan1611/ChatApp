# __init__.py
from flask import Flask

from flask_login import LoginManager

from flask_mail import Mail
from .config import get_config
import os
from flask_cors import CORS
from flask_socketio import SocketIO
from pymongo import MongoClient


mail = Mail()

socketio = SocketIO()
def create_app(mode='default'):
    app = Flask(__name__)   


    socketio.init_app(app,cors_allowed_origins="*")
    app.config.from_object(get_config(mode))
    
    CORS(app)

    # Configure the upload folder
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))


 



    # Initialize Flask-Mail
    mail.init_app(app)

    # Register blueprints
    from .auth import auth
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    from .models import get_user
    # Initialize login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(username):
        return get_user(username)

    return app

