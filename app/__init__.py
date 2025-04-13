from flask import Flask
from .models import db, User
from config import Config
from .routes import bp  # main blueprint
from flask_login import LoginManager
from .auth import auth_bp  # authentication blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Setup LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # redirect if not authenticated
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    # Register Blueprints
    app.register_blueprint(bp)      # Routes for main functionalities
    app.register_blueprint(auth_bp)   # Routes for login, register, logout

    return app
