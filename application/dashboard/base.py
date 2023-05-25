import dash_mantine_components as dmc
from dash import html, page_container, dcc
from flask import session, current_app

from .components.navbar import navbar
from .components.navbar_new import navbar_new
from .components.modalPassword import modalPasswordChange
from .utils.functions import get_icon


def make_base_layout(app):
    base_layout = dmc.MantineProvider(
        theme={
            "components": {
                "Grid": {
                    "style": {
                        "root": {
                            "padding": "0px",
                            "margin": "0px",
                        }
                    },
                },
                "Col": {
                    "styles": {
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
                dcc.Interval(id="stock-ticker", interval=30000, disabled=True),
                dmc.Grid(
                    children=[
                        modalPasswordChange,
                        navbar_new.embed(app),
                        html.Div(id="notifications-container"),
                        html.Div(
                            [
                                dmc.Title(id="dashboard-title", order=1),
                                html.Div(
                                    [
                                        dmc.NavLink(
                                            label="Index Overview",
                                            icon=get_icon(
                                                icon="arcticons:stockswidget"
                                            ),
                                            fw="bold",
                                            w="10em",
                                            href=current_app.config.get("URL_DASH"),
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "flex-direction": "row",
                                        "justify-content": "flex-start",
                                    },
                                ),
                            ],
                            style={
                                "padding": "2em 2em 2em 100px",
                            },
                        ),
                        html.Div(
                            page_container,
                            style={
                                "margin": "2em 2em 2em 110px",
                            },
                        ),
                    ],
                    gutter="xl",
                    style={
                        "margin": "0",
                        "max-width": "100%",
                    },
                ),
            ],
        ),
    )
    return base_layout
