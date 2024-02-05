# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flask_mail import Mail
from .config import get_config
import os
from flask_cors import CORS
from flask_socketio import SocketIO


db = SQLAlchemy()
mail = Mail()
DB_NAME = "database.db"
socketio = SocketIO()
def create_app(mode='default'):
    app = Flask(__name__)

    socketio.init_app(app,cors_allowed_origins="*")
    app.config.from_object(get_config(mode))
    
    CORS(app)


    # Configure the upload folder
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))


    # Initialize database
    db.init_app(app)




    # Initialize Flask-Mail
    mail.init_app(app)

    # Register blueprints
    from .auth import auth
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    # Import models and create tables
    from .models import User
    with app.app_context():
        db.create_all()

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not os.path.exists('app/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')