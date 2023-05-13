"""Data models."""
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from . import db


class User(UserMixin, db.Model):
    """Data model for user accounts."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False, unique=False)
    last_name = db.Column(db.String(100), nullable=False, unique=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password = db.Column(
        db.String(200), primary_key=False, unique=False, nullable=False
    )
    is_admin = db.Column(
        db.Boolean, index=False, unique=False, nullable=False, default=False
    )
    verified = db.Column(
        db.Boolean, index=False, unique=False, nullable=False, default=False
    )
    data_consent = db.Column(
        db.Boolean, index=False, unique=False, nullable=False, default=False
    )
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    preferences = db.Column(db.JSON, nullable=True)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="scrypt")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)


class co2model(db.Model):
    __tablename__ = "co2model"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    inital_preferences = db.Column(db.JSON, nullable=True)
    path_datafile = db.Column(db.String(200), unique=False, nullable=False)
    path_processingfile = db.Column(db.String(200), unique=False, nullable=False)
