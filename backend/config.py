from decouple import config
from os import path


BASE_DIR = path.dirname(path.realpath(__file__))

class Config():
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATION = config('SQLALCHEMY_TRACK_MODIFICATION', cast = bool)


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductConfig(Config):
    pass


class TestConfig(Config):
    pass
