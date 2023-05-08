"""
#ToDo here we will write the dash app
"""
import flask
import dash
from dash import html
import base64
import pandas as pd
import os
from application.auth.decorators import login_required
from flask import current_app
from .layout.base import base_layout


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
    app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname=current_app.config["URL_DASH"],
        assets_folder=assets_path,
    )
    app._favicon = f"{assets_path}/img/favicon.ico"
    app.config["suppress_callback_exceptions"] = True
    app.title = "MES Dashboard"
    protect_dashviews(app)

    app.layout = base_layout

    # End of create_app method, return the flask app aka server (not the dash app)
    return app.server
