import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'trekking-secret-key-12345')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///trekking.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
