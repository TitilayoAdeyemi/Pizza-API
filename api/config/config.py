import os
from decouple import config
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config():
    SECRET_KEY = config('SECRET_KEY', 'secrets')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(BASE_DIR, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')
    DEBUG = config('DEBUG', cast=bool)

config_dict={
    'dev' : DevConfig,
    'test' : TestConfig,
    'prod' : ProdConfig
}