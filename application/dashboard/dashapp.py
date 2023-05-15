import os

from flask import current_app
from dash_extensions.enrich import DashProxy

from application.auth.decorators import login_required
from .base import make_base_layout
from .pages.overview import overview
from .pages.index import index_bp
from .pages.stock_detail import stock_detail_bp


def protect_dashviews(dash_app):
    """_summary_
    Function to protect the dash application with flask login
    Args:
        dash_app (_type_): input is the app
    """
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
        # assets_folder=assets_path,
    )
    # Set favicon
    app._favicon = f"{assets_path}/img/favicon.ico"
    app.config["suppress_callback_exceptions"] = True
    app.title = "Dashboard"
    protect_dashviews(app)

    overview.register(
        app,
        "pages.overview",
        path=current_app.config["DASH_HOME"],
        title="co2 onboard Dashboard",
        name="co2 onboard Dashboard",
    )

    index_bp.register(
        app,
        "pages.index",
        path=current_app.config["DASH_INDEX"],
        title="Index overview",
        name="Index overview",
    )

    stock_detail_bp.register(
        app,
        "pages.stock_detail",
        path=current_app.config["DASH_STOCK_DETAIL"],
        title="Stock detail",
        name="Stock detail",
    )

    app.layout = make_base_layout(app)

    # Here the overview page with path is registered

    return app.server
