import re

from flask import session, current_app
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from dash_extensions.enrich import DashBlueprint, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from ..utils.functions import get_icon
from ...API.internal_API import get_user


navbar = DashBlueprint()


navbar.layout = dmc.Col(
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


@navbar.callback(
    Output("old-password", "error"),
    Output("new-password", "error"),
    Output("modal-change-password", "opened"),
    Output("notifications-container", "children", allow_duplicate=True),
    Output("old-password", "value"),
    Output("new-password", "value"),
    Output("confirm-new-password", "value"),
    Input("button-change-password", "n_clicks"),
    Input("submitt-password-change", "n_clicks"),
    State("old-password", "value"),
    State("new-password", "value"),
    State("confirm-new-password", "value"),
    State("modal-change-password", "opened"),
    prevent_initial_call=True,
)
def change_password(open, n_clicks, oldPassword, newPassword, confirmNew, opened):
    if not opened:
        return False, False, not opened, "", oldPassword, newPassword, confirmNew

    pattern = re.compile("^((?=.*\d)(?=.*[A-Z])(?=.*\W).{8,20})$")

    if not get_user.check_password(session["user"].get("id"), oldPassword):
        return (
            "The old password is incorrect",
            False,
            opened,
            "",
            oldPassword,
            newPassword,
            confirmNew,
        )

    if not pattern.match(newPassword):
        return (
            False,
            "The new password does not match the criteria",
            opened,
            "",
            oldPassword,
            newPassword,
            confirmNew,
        )

    if confirmNew != newPassword:
        return (
            False,
            "New password and confirmation does not match",
            opened,
            "",
            oldPassword,
            newPassword,
            confirmNew,
        )

    get_user.change_password(session["user"].get("id"), newPassword)

    message = dmc.Notification(
        title="Hey there!",
        id="simple-notify",
        action="show",
        message="The password was changed successfully",
        icon=DashIconify(icon="ic:round-celebration"),
    )
    return False, False, not opened, message, "", "", ""
