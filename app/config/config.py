import os
from cryptography.fernet import Fernet


class Config:
    ENV = os.getenv('FLASK_ENV', 'production')
    ENABLE_TALISMAN = os.getenv('ENABLE_TALISMAN', True)
    DEBUG = ENV == 'development'
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-super-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 900))

    DB_USER = os.getenv('DATABASE_USER', 'root')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD', 'toor')
    DB_HOST = os.getenv('DATABASE_HOST', 'localhost')
    DB_PORT = os.getenv('DATABASE_PORT', '3306')
    DB_NAME = os.getenv('DATABASE_NAME', 'educationDB')

    SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', Fernet.generate_key().decode('utf-8'))
