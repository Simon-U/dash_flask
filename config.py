"""App configuration."""
from os import environ, path, system
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_DEBUG = environ.get("FLASK_DEBUG", False)
    SECRET_KEY = environ.get("SECRET_KEY")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    FLASK_PORT = environ.get("FLASK_PORT", "8080")

    # Admin User
    ADMIN_FIRST_NAME = environ.get("ADMIN_FIRST_NAME")
    ADMIN_LAST_NAME = environ.get("ADMIN_LAST_NAME")
    ADMIN_EMAIL = environ.get("ADMIN_EMAIL")
    ADMIN_PASSWORD = environ.get("ADMIN_PASSWORD")

    # URLS
    URL_BASE = "/"
    URL_LOGIN = "/login"
    URL_SIGNUP = "/signup"
    URL_RESET_PASSWORD = "/reset"
    URL_NEW_PASSWORD = "/new-password/<token>"
    URL_CHANGE_PASSWORD = "/change-password"
    URL_LOGOUT = "/logout"
    URL_VERIFY_EMAIL = "/vefify-email/<token>"
    URL_DASH = "/dash/"
    URL_USER_PREFERENCES = "/userpreferences"
    URL_PRIVACY_POLICY = "/privacy_policy"

    # Dash internal routes
    DASH_HOME = "/"
    DASH_STOCKS = "/stocks"

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URI", "sqlite:///database.db")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SMTP
    EMAIL_HOST = environ.get("EMAIL_HOST", "localhost")
    EMAIL_PORT = int(environ.get("EMAIL_PORT", 587))
    EMAIL_USERNAME = environ.get("EMAIL_USERNAME", None)
    EMAIL_PASSWORD = environ.get("EMAIL_PASSWORD", None)
    EMAIL_SENDER = environ.get("EMAIL_SENDER", None)

    # Admin Css configuration
    FLASK_ADMIN_SWATCH = environ.get("FLASK_ADMIN_SWATCH", "materia")

    # Token configuration
    TOKEN_EXPIRE = 24  # in hours
