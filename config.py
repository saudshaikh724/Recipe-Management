# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost:5432/recipes_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False