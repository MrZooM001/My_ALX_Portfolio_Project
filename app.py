#!/usr/bin/python3
"""
Module creates a Flask application with three blueprints: auth, main, and recipes.
The auth blueprint handles authentication and registration.
The main blueprint handles the homepage and other non-user-specific pages.
The recipes blueprint handles recipe-related routes.
It also sets up the database, registers the blueprints, initializes the login manager,
and configures the app for development. Finally, the script loads the.env file and runs the app.
"""

from flask import Flask
from config import DevConfig
from extensions import db
from routes import auth_bp, init_login_manager
from routes import main_bp
from routes import recipes_bp
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(recipes_bp)
app.app_context()

init_login_manager(app)

migrate = Migrate(app, db)


if __name__ == "__main__":
    dotenv_file = os.path.join(os.getcwd(), ".env")
    load_dotenv(dotenv_file)
    app.run()
