import os

class Config:
    # Get the Heroku database URL or fallback to SQLite for local testing
    raw_uri = os.getenv('postgres://ueort80m5dgt2i:p0bd5f5a95ed0119765550bb118a9f139fa5655d2dba73105ad23475f1faad464@c7s7ncbk19n97r.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d35vdctb6f2dnh', 'sqlite:///d35vdctb6f2dnh.db')

    # Fix deprecated Heroku-style URI prefix (postgres:// → postgresql://)
    if raw_uri.startswith('postgres://'):
        raw_uri = raw_uri.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = raw_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Required for forms
    SECRET_KEY = os.getenv('SECRET_KEY', '0779ba5c3606b130fd2287f261ad487e6035b73610ad477a')