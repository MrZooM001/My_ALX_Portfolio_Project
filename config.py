#!/usr/bin/python3
from decouple import config
from os import path


BASE_DIR = path.join(path.dirname(path.realpath(__file__)))


class BaseConfig:
    SECRET_KEY = config("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = config("SQLALCHEMY_TRACK_MODIFICATIONS", cast=bool)


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = config("SQLALCHEMY_DATABASE_URI")
    DEBUG = True
    SQLALCHEMY_ECHO = True
    TEMPLATES_AUTO_RELOAD = config("TEMPLATES_AUTO_RELOAD")
    SESSION_COOKIE_HTTPONLY = False
    # TEMPLATES_FOLDER = config("TEMPLATES_FOLDER")



class ProductConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    pass
