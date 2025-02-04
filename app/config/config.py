import os

class Config:
    ENV = os.getenv('FLASK_ENV', 'production')
    ENABLE_TALISMAN = os.getenv('ENABLE_TALISMAN', True)
    DEBUG = ENV == 'development'
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-super-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 900))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:toor@localhost:3306/educationDB')
    SQLALCHEMY_TRACK_MODIFICATIONS = False