#!/usr/bin/python3
from decouple import config
from os import path, getenv


BASE_DIR = path.join(path.dirname(path.realpath(__file__)))


class BaseConfig:
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = getenv("SQLALCHEMY_TRACK_MODIFICATIONS")


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = getenv("JAWSDB_URL")
    DEBUG = getenv("DEBUG")
    SQLALCHEMY_ECHO = True
    TEMPLATES_AUTO_RELOAD = getenv("TEMPLATES_AUTO_RELOAD")
    SESSION_COOKIE_HTTPONLY = False
    # TEMPLATES_FOLDER = config("TEMPLATES_FOLDER")



class ProductConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    pass
