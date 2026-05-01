import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-for-qatar-foundation'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///admin_portal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
