#!/usr/bin/python3
from decouple import config
from os import path


BASE_DIR = path.join(path.dirname(path.realpath(__file__)), "api/v1")

class Config():
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATION = config('SQLALCHEMY_TRACK_MODIFICATION', cast = bool)


class DevConfig(Config):
    # SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://hazem:0100@localhost/recipe_planner_web_dev"
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductConfig(Config):
    pass


class TestConfig(Config):
    pass
