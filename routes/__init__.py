#!/usr/bin/python3
"""
Initialize routes module as package
"""
from .auth_routes import auth_bp, init_login_manager
from .main_routes import main_bp
from .recipe_routes import recipes_bp, toggle_favorite
