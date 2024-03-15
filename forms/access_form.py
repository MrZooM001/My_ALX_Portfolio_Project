from models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo

class RegisterForm(FlaskForm):
    """Register a new user"""

    first_name = StringField(
        validators=[Length(min=0, max=36)],
        render_kw={"placeholder": "First Name"},
    )
    last_name = StringField(
        validators=[Length(min=0, max=36)],
        render_kw={"placeholder": "Last Name"},
    )
    username = StringField(
        validators=[InputRequired(), Length(min=3, max=36)],
        render_kw={"placeholder": "Username"},
    )
    email = EmailField(
        validators=[InputRequired(), Length(min=5, max=72)],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=36)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username).first()

        if existing_username:
            raise ValidationError("Username already exists")


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=40)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=40)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Login")
