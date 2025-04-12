from flask import Flask
from .models import db
from config import Config
from .routes import bp  # <-- import the Blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(bp)  # <-- Register the Blueprint

    return app