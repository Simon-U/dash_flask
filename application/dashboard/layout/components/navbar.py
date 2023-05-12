import dash_mantine_components as dmc
from dash_iconify import DashIconify
from flask import current_app


def get_icon(icon, height=16):
    return DashIconify(icon=icon, height=height)


navbar = dmc.Col(
    [
        dmc.Image(src="/static/img/mes_rgb.png", width=300),
        dmc.Menu(
            [
                dmc.MenuTarget(
                    dmc.Anchor(
                        get_icon(icon="tabler:user", height=24),
                        className="nav-link dropdown-toggle",
                        href="",
                    ),
                ),
                dmc.MenuDropdown(
                    [
                        dmc.MenuItem(
                            "Change Password", id="button-change-password", n_clicks=0
                        ),
                        dmc.MenuItem(
                            "Logout",
                            href=current_app.config.get("URL_LOGOUT"),
                            refresh=True,
                        ),
                    ],
                ),
            ],
            style={"padding-right": "5em"},
            className="nav navbar-nav dropdown",
        ),
    ],
    style={
        "background": "none",
        "padding": "0",
        "margin": "0",
        "display": "flex",
        "justify-content": "space-between",
    },
    className="navbar navbar-expand-lg navbar-dark bg-primary mb-2",
)
