from flask import current_app

import dash_mantine_components as dmc
from dash import html, page_container

from .components.navbar import navbar
from .components.modalPassword import modalPasswordChange


def make_base_layout(app):
    base_layout = dmc.MantineProvider(
        theme={},
        inherit=True,
        children=dmc.NotificationsProvider(
            [
                dmc.Grid(
                    children=[
                        modalPasswordChange,
                        navbar.embed(app),
                        html.Div(id="notifications-container"),
                        html.Div(
                            page_container,
                            style={"padding": "2em"},
                        ),
                        dmc.Footer(
                            height=60,
                            children=[
                                dmc.Anchor(
                                    "Privacy Policy",
                                    href=current_app.config.get("URL_PRIVACY_POLICY"),
                                    refresh=True,
                                    target="_blank",
                                    className="privacy",
                                ),
                            ],
                            className="footer_privacy",
                            style={"width": "100%", "border": "none"},
                        ),
                    ],
                    gutter="xl",
                    style={
                        "margin": "0",
                        "max-width": "100%",
                        "background-color": "none",
                    },
                ),
            ],
        ),
    )
    return base_layout
