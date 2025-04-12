from flask import Flask
from .models import db, User
from config import Config
from .routes import bp
from flask_login import LoginManager
from .auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Setup LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # redirect to 'auth.login' if not logged in
    login_manager.init_app(app)

    # Load user from session
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    # Register Blueprints
    app.register_blueprint(bp)
    app.register_blueprint(auth_bp)

    return app