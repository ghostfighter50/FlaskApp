# app/app.py

from flask import Flask
from . import create_app

app: Flask = create_app()
