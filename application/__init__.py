"""Initialize app."""
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_redmail import RedMail
from flask_admin import Admin
import os.path as op
from .templates.admin.custom_views import (
    customFileAdmin,
    customModelView,
    MyAdminIndexView,
)

db = SQLAlchemy()
login_manager = LoginManager()
mail = RedMail()


admin_manager = Admin(template_mode="bootstrap4", index_view=MyAdminIndexView())
path = op.join(op.dirname(__file__), "data")


def create_app():
    """Construct the core flask_session_tutorial."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    # Session(app)

    # Initialize Plugins and register them with the app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin_manager.init_app(app)

    with app.app_context():
        """
        The context is the integral part of our flask application. Here we need to register everything.
        If it is not here, than it does not exists for the flask application
        """

        # Include our Routes / URL adresses
        from .auth import routes as auth

        # Register admin views for managing user and uploading files
        from .models import User

        admin_manager.add_view(customModelView(User, db.session))
        admin_manager.add_view(customFileAdmin(path, name="Excel Tables"))

        # Register Blueprints, which are layouts
        app.register_blueprint(auth.auth_bp)

        # Create Database Models
        db.create_all()

        # Integrate the dasg application
        from .dashboard.dashapp import create_dashapp

        app = create_dashapp(app)

        # app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
        return app
