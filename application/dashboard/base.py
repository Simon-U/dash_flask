from flask import current_app

import dash_mantine_components as dmc
from dash import html, page_container, dcc

from .components.navbar import navbar
from .components.modalPassword import modalPasswordChange


def make_base_layout(app):
    base_layout = dmc.MantineProvider(
        theme={
            "components": {
                "Grid": {
                    "style": {
                        "root": {
                            "padding": "0em",
                        }
                    },
                },
                "Paper": {
                    "styles": {
                        "root": {
                            "box-shadow": "4px 5px 21px -3px rgba(66, 68, 90, 1)",
                            "padding": "1em",
                        }
                    },
                },
                "Chip": {
                    "styles": {
                        "root": {},
                        "label": {"border": "none", "font-size": "large", "gap": "0px"},
                    }
                },
                "ChipGroup": {
                    "styles": {
                        "root": {
                            "padding": "0",
                            "margin": "0",
                            "row-gap": 0,
                            "column-gap": 0,
                        },
                        "label": {},
                    }
                },
            },
        },
        inherit=True,
        children=dmc.NotificationsProvider(
            [
                dcc.Location(id="url", refresh=False),
                dmc.Grid(
                    children=[
                        modalPasswordChange,
                        navbar.embed(app),
                        html.Div(id="notifications-container"),
                        html.Div(
                            page_container,
                            style={"padding": "2em"},
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
