#!/usr/bin/python3
"""
Module defines the recipe form for both add & edit a recipe.
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField, SearchField


class SearchForm(FlaskForm):
    """Class defines a form for searching a recipe"""
    searched = SearchField("searched", render_kw={"placeholder": "Search a recipe", "aria-label": "Search"})
    submit = SubmitField("submit")
