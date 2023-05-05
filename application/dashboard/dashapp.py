"""
#ToDo here we will write the dash app
"""
import flask
import dash
import dash_html_components as html
import base64
import pandas as pd
import os
from application.auth.decorators import login_required


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
    app = dash.Dash(
        __name__,
        server=server,
        url_base_pathname="/dash/",
    )
    app.config["suppress_callback_exceptions"] = True
    app.title = "My Dash App"
    protect_dashviews(app)

    app.layout = html.Div(html.P(f"Protected Dash app"))

    # End of create_app method, return the flask app aka server (not the dash app)
    return app.server
