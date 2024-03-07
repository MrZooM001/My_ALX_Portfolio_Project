#!/usr/bin/python3
""" Module to configure flask application """
from api.v1.authn import auth_namespace
from api.v1.extentions import db
from models.recipe import Recipe
from models.user import  User
from api.v1.recipes import recipe_namespace
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api


# region app initialization
def create_app(config):

    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate = Migrate(app, db)
    JWTManager(app)

    api = Api(app, doc="/docs")
    api.add_namespace(auth_namespace)
    api.add_namespace(recipe_namespace)

    # region Flask interactive shell
    @app.shell_context_processor
    def make_shell_context():
        """
        makes app objects available in the Python Flask interactive shell

        Examples:
        >>> flask shell
        or
        >>> flask db init
        """
        return {"db": db, "Recipe": Recipe, "User": User}

    # endregion Flask interactive shell

    return app


# endregion app initialization
