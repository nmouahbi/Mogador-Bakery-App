import os

class Config:
    # Use PostgreSQL if DATABASE_URL is set (for Heroku), else fallback to local SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///bakery.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False