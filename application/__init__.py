"""Initialize app."""
import datetime
import json
import os
from flask import Flask, current_app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_redmail import RedMail
from flask_admin import Admin
import os.path as op
from .templates.admin.custom_views import (
    customFileAdmin,
    customModelView,
    MyAdminIndexView,
)
from flask_login import logout_user


db = SQLAlchemy()
login_manager = LoginManager()
mail = RedMail()

test_preferences = {
    "EU Norm 1": {
        "Technologie Readiness Level": "5",
        "verwendeter Kraftstoff": "6",
        "behandelte Rauchgasmenge": "7",
        "CO2 Rauchgaskonzentration": "3",
        "Anlage Eingangsdruck": "4",
        "Eingangs Prozesstemperatur": "5",
        "CO2 Reinheit": "3",
        "CO2 Abscheiderate": "7",
        "CO2 Temperatur vor Speicherung": "4",
        "Energiebedarf elektrisch": "9",
        "Energiebedarf thermisch": "7",
        "Prozessmittelverbrauch": "3",
        "Abgasvorbehandlung": "10",
        "Platzbedarf": "7",
    }
}


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
        from .models import User, co2model

        admin_manager.add_view(customModelView(User, db.session))
        admin_manager.add_view(customModelView(co2model, db.session))
        admin_manager.add_view(customFileAdmin(path, name="Excel Tables"))

        # Register Blueprints, which are layouts
        app.register_blueprint(auth.auth_bp)

        # Create Database Models
        db.create_all()
        """
        if co2model.query.filter_by(name="EU Norm 1").first() is None:
            co2mod = co2model(
                name="EU Norm 1",
                inital_preferences=json.dumps(test_preferences),
                path_datafile="01_aussichtsreichsteTechnologien.xlsx",
                path_processingfile="dataProcessing.py",
            )
            db.session.add(co2mod)
            db.session.commit()

        if (
            User.query.filter_by(email=current_app.config["ADMIN_EMAIL"]).first()
            is None
        ):
            user = User(
                first_name=current_app.config["ADMIN_FIRST_NAME"],
                last_name=current_app.config["ADMIN_LAST_NAME"],
                email=current_app.config["ADMIN_EMAIL"],
                preferences=json.dumps(test_preferences),
                is_admin=True,
                verified=True,
                created=datetime.datetime.now(),
                data_consent=True,
            )
            user.set_password(current_app.config["ADMIN_PASSWORD"])
            db.session.add(user)
            db.session.commit()
        """
        # Integrate the dasg application
        from .dashboard.dashapp import create_dashapp

        app = create_dashapp(app)

        # app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
        return app
