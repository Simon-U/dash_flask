"""
#ToDo here we will write the dash app
"""
import os

from flask import current_app
import pandas as pd
from dash_extensions.enrich import DashProxy
import dash_labs as dl

from application.auth.decorators import login_required
from .base import make_base_layout
from .pages.overview import overview


def protect_dashviews(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_func] = login_required(
                dash_app.server.view_functions[view_func]
            )


def create_dashapp(server):
    """
    Init our dashapp, to be embedded into flask
    """
    assets_path = os.getcwd() + "/application/static/"
    app = DashProxy(
        __name__,
        server=server,
        url_base_pathname=current_app.config["URL_DASH"],
        use_pages=True,
        plugins=[dl.plugins.pages]
        # assets_folder=assets_path,
    )
    app._favicon = f"{assets_path}/img/favicon.ico"
    app.config["suppress_callback_exceptions"] = True
    app.title = "MES Dashboard"
    protect_dashviews(app)

    app.layout = make_base_layout(app)
    overview.register(
        app,
        "pages.overview",
        path="/",
        title="Our Analytics Dashboard",
        name="Our Analytics Dashboard",
    )

    # End of create_app method, return the flask app aka server (not the dash app)
    return app.server
