#!/usr/bin/python3

from decouple import config
from os import path, getenv


BASE_DIR = path.join(path.dirname(path.realpath(__file__)))


class BaseConfig:
    """
    Base configuration class.

    This class is the base class for all other configuration classes. It defines
    the common configuration options that are used by the application.

    Attributes:
        SECRET_KEY (str): Secret key for the application.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Track database modifications.
    """
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = config("SQLALCHEMY_TRACK_MODIFICATIONS")


class DevConfig(BaseConfig):
    """
    Configuration class for development environment.
    
    This class inherits from the BaseConfig class and overrides the
    SQLALCHEMY_DATABASE_URI attribute with the value obtained from the
    SQLALCHEMY_DATABASE_URI environment variable. It also sets the DEBUG
    attribute to True, which enables debug mode, and enables the SQLAlchemy
    echo feature, which prints all SQL queries to the console. Additionally,
    it sets the TEMPLATES_AUTO_RELOAD attribute to the value obtained from
    the TEMPLATES_AUTO_RELOAD environment variable. Finally, it sets the
    SESSION_COOKIE_HTTPONLY attribute to False, which allows the session cookie
    to be accessed from JavaScript.
        
    """
    SQLALCHEMY_DATABASE_URI = config("SQLALCHEMY_DATABASE_URI")
    DEBUG = True
    SQLALCHEMY_ECHO = True
    TEMPLATES_AUTO_RELOAD = config("TEMPLATES_AUTO_RELOAD")
    SESSION_COOKIE_HTTPONLY = False


class ProductConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    pass
