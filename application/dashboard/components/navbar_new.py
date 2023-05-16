import re

from flask import session, current_app
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from dash_extensions.enrich import DashBlueprint, Output, Input, State
from dash_iconify import DashIconify
from dash import html
from dash.exceptions import PreventUpdate

from ..utils.functions import get_icon
from ...API.internal_API import get_user


navbar_new = DashBlueprint()


navbar_new.layout = dmc.Navbar(
    p="md",
    width={"base": 80},
    fixed=True,
    position="left",
    bg="rgb(0,0,0)",
    style={
        "border": "0",
        "padding-top": "2em",
        "box-shadow": "4px 5px 21px -3px rgba(66, 68, 90, 1)",
        "justify-content": "space-between",
    },
    children=[
        dmc.Title(
            "QDT",
            order=2,
            transform="uppercase",
            variant="gradient",
            gradient={
                "from": "#0693e3",
                "to": "#8ed1fc",
            },
        ),
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
            trigger="hover",
            position="right-start",
            style={"padding-right": "5em"},
            className="nav navbar-nav dropdown",
        ),
    ],
)


@navbar_new.callback(
    Output("dashboard-title", "children", allow_duplicate=True),
    Output("stock-ticker", "disabled"),
    Input("url", "pathname"),
    prevent_initial_call=True,
)
def change_title(path):
    if path == current_app.config.get("URL_DASH"):
        return "Co2 Overview", True
    elif (
        path
        == f'{current_app.config.get("URL_DASH")[:-1]}{current_app.config.get("DASH_INDEX")}'
    ):
        return "Index overview", True
    else:
        return "Company fundamentals", False


@navbar_new.callback(
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
    """_summary_
    Callback to trigger modal for changing password
    Args:
        open (int): Value of the button to open the change password modal
        n_clicks (int): Is a value provided by the
        oldPassword (string): Old password
        newPassword (string): new password
        confirmNew (string): confirm new password
        opened (None, Bool): Value if the modal is open or not

    Returns:
        Error old password (string): Error message if something is not correct with the old password
        Error new password (string): Error message if something is not correct with the new password
        Modal open (bool): Value if the modal should still be open
        Notification message (string): Message for the notification system
        oldPassword (string): Value for old password input
        newPassword (string): Value for new password input
        confirmNew (string): Value for new confirm password input

    """

    if not opened:
        return False, False, not opened, "", oldPassword, newPassword, confirmNew

    # Check if the old password matches the new password
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

    # Check if the new password has one upper case, lower case letter, one digit and one special character
    # and is longer than 8
    pattern = re.compile("^((?=.*\d)(?=.*[A-Z])(?=.*\W).{8,20})$")
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
