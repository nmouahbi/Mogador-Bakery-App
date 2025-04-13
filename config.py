import os

class Config:
    raw_uri = os.getenv('DATABASE_URL')

    if raw_uri and raw_uri.startswith("postgres://"):
        raw_uri = raw_uri.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = raw_uri or 'sqlite:///bakery.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
