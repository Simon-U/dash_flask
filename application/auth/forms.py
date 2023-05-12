"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from flask import request
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    validators,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    InputRequired,
    Regexp,
)
from wtforms.validators import DataRequired

SUBMIT_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def _is_submitted():
    """Consider the form submitted if there is an active request and
    the method is ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
    """

    return bool(request) and request.method in SUBMIT_METHODS


class SignupForm(FlaskForm):
    """User Sign-up Form."""

    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    email = StringField(
        "Email",
        validators=[
            Length(min=6),
            Email(message="Enter a valid email."),
            DataRequired(),
        ],
    )
    is_admin = BooleanField("Is admin")
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Regexp(
                "(?=.*[a-z])", message="Password must contain at least one lower letter"
            ),
            Regexp(
                "(?=.*[A-Z])", message="Password must contain at least one upper letter"
            ),
            Regexp("(?=.*\d)", message="Password must contain at least one digit"),
            Regexp(
                "(?=.*\W)",
                message="Password must contain at least one special character",
            ),
            validators.EqualTo("confirm", message="Passwords must match."),
            Length(min=8, message="Password needs to have 8 characters"),
        ],
    )
    confirm = PasswordField(
        "Confirm Your Password",
        validators=[DataRequired()],
    )
    data_consent = BooleanField(
        "Did you read and consent to our",
        validators=[DataRequired()],
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    """User Log-in Form."""

    email = StringField(
        "Email", validators=[DataRequired(), Email(message="Enter a valid email.")]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class ResetPasswordForm(FlaskForm):
    """User Sign-up Form."""

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(min=8, message="Select a stronger password."),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    confirm = PasswordField(
        "Confirm Your Password",
        validators=[
            DataRequired(),
        ],
    )
