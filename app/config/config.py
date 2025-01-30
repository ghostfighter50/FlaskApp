# app/config/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path('.env') if Path('.env').exists() else None)

class Config:
    ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = ENV == 'development'
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-super-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 900))  # 15 minutes
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:toor@localhost:3306/educationDB')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
    PROPAGATE_EXCEPTIONS = True