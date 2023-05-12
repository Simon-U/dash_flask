import os
import re

from flask import session, current_app

import dash_mantine_components as dmc
from dash import html, callback, Output, Input, ALL, State, ctx
from dash_iconify import DashIconify

from .components.navbar import navbar
from .components.modalPassword import modalPasswordChange
from ...API.internal_API import get_co2model, get_user
from ..utils.functions import load_module


def make_tabs(tab_names):
    list_tabs = [dmc.Tab(name, value=name) for name in tab_names]
    tabs = (
        dmc.TabsList(
            list_tabs,
            position="left",
        ),
    )
    return tabs


base_layout = dmc.MantineProvider(
    theme={},
    inherit=True,
    children=dmc.NotificationsProvider(
        [
            dmc.Grid(
                children=[
                    modalPasswordChange,
                    navbar,
                    dmc.Col(
                        [
                            dmc.Tabs(
                                make_tabs(get_co2model.get_model_names()),
                                value=get_co2model.get_model_names()[0],
                                placement="left",
                                orientation="vertical",
                                id="tabs",
                            ),
                            dmc.Space(h=20),
                            dmc.Button(
                                "Save Settings",
                                id="save-settings",
                                n_clicks=0,
                                className="btn btn-primary btn-block",
                                style={"max-width": "13em"},
                                leftIcon=DashIconify(
                                    icon="fluent:database-plug-connected-20-filled"
                                ),
                            ),
                            dmc.Text(id="test"),
                        ],
                        span=2,
                    ),
                    dmc.Col(html.Div(id="tabs-content"), span=10),
                    html.Div(id="notifications-container"),
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
                style={"margin": "0", "max-width": "100%", "background-color": "none"},
            ),
        ],
    ),
)


def get_icon(value):
    size = 30
    if value >= 1:
        return DashIconify(icon="mdi:circle-slice-8", width=size)
    elif 1 > value >= 0.6:
        return DashIconify(icon="mdi:circle-slice-6", width=size)
    elif 0.6 > value >= 0.5:
        return DashIconify(icon="circle-slice-4", width=size)
    elif 0.5 > value > 0:
        return DashIconify(icon="mdi:circle-slice-2", width=size)
    elif value == 0:
        return DashIconify(icon="mdi:circle-outline", width=size)


def create_table(df, weights):
    df.insert(0, "", list(df.index))
    df.insert(1, "Gewichtung", weights)
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [
        html.Tr(
            [
                #  ToDo Tooltip needs to be adjusted based onlist/dict
                html.Td(
                    dmc.Tooltip(
                        label="This is a tooltip",
                        position="left",
                        offset=3,
                        children=cell,
                    )
                )
                if ind == 0
                else html.Td(
                    dmc.NumberInput(
                        value=cell,
                        min=0,
                        max=10,
                        step=1,
                        style={"width": 70},
                        id={"type": "table-input", "index": ind},
                    )
                )
                if ind == 1
                else html.Td(get_icon(cell))
                for ind, cell in enumerate(row)
            ]
        )
        for row in values
    ]
    table = dmc.Table(
        verticalSpacing="xs",
        horizontalSpacing="xs",
        children=[html.Thead(header), html.Tbody(rows)],
    )
    return table


@callback(
    Output(component_id="tabs-content", component_property="children"),
    Input(component_id="tabs", component_property="value"),
    Input({"type": "table-input", "index": ALL}, "value"),
)
def update_graph(current_tab, input_weigts):
    file_name_excel = get_co2model.get_data_file(current_tab)
    excel_file = os.path.join(os.getcwd(), "application/data", file_name_excel)

    # loading the module at runtime
    file_name_processing = get_co2model.get_processing_file(current_tab)
    processing = os.path.join(
        os.getcwd(), "application/data/processing", file_name_processing
    )
    data_processing = load_module(file_name_processing, processing)

    if ctx.triggered_id is None:
        excel_file = os.path.join(os.getcwd(), "application/data", file_name_excel)
        weights = get_user.get_user_preferences(session["user"].get("id"), current_tab)
        df = data_processing.get_data(excel_file, weights)
        return create_table(df, list(weights.values()))

    elif ctx.triggered_id == "tabs":
        excel_file = os.path.join(os.getcwd(), "application/data", file_name_excel)
        weights = get_user.get_user_preferences(session["user"].get("id"), current_tab)
        df = data_processing.get_data(excel_file, weights)
        return create_table(df, list(weights.values()))

    elif len(input_weigts) > 0:
        weights = get_user.get_user_preferences(session["user"].get("id"), current_tab)
        weights_new = dict(zip(list(weights.keys()), input_weigts))

        df = data_processing.get_data(excel_file, weights_new)
        return create_table(df, weights_new)


@callback(
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


@callback(
    Output("notifications-container", "children"),
    Input("save-settings", "n_clicks"),
    State({"type": "table-input", "index": ALL}, "value"),
    State("tabs", "value"),
    prevent_initial_call=True,
)
def save_settings(n_clicks, weigths, current_tab):
    if n_clicks:
        current_weigths = get_user.get_user_preferences(
            session["user"].get("id"), current_tab
        )
        temp = [str(weight) for weight in weigths]

        new_weigts = dict(zip(list(current_weigths.keys()), temp))
        get_user.save_user_preferences(
            session["user"].get("id"), current_tab, new_weigts
        )
        message = dmc.Notification(
            title="Hey there!",
            id="simple-notify",
            action="show",
            message="Your settings are saved successfully",
            icon=DashIconify(icon="ic:round-celebration"),
        )
        return message
