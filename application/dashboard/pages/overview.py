import os

from flask import session
from dash_extensions.enrich import DashBlueprint, html, Output, Input, State
from dash import html, callback, ALL, ctx
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from ...API.internal_API import get_co2model, get_user
from ..utils.functions import load_module, make_tabs, create_table

overview = DashBlueprint()


overview.layout = dmc.Grid(
    [
        dmc.Col(
            dmc.Paper(
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
                ],
                radius="lg",
                p="xs",
            ),
            span=2,
        ),
        dmc.Col(
            dmc.Paper(
                html.Div(id="tabs-content"),
                radius="lg",
                p="xs",
            ),
            span=10,
        ),
    ],
    gutter="xl",
    style={"padding-bottom": "60px"},
)


@overview.callback(
    Output(component_id="tabs-content", component_property="children"),
    Input(component_id="tabs", component_property="value"),
    Input({"type": "table-input", "index": ALL}, "value"),
)
def update_graph(current_tab, input_weigts):
    """_summary_
    Callback to update the tabs based on the selection
    Args:
        current_tab (string): Value of the current tab from the component
        input_weigts (List): List of input weights from the table

    Returns:
        Returns new table based on the input values
    """

    path_excel = get_co2model.get_data_file(current_tab)

    # loading the module at runtime
    path_processing_file = get_co2model.get_processing_file(current_tab)
    data_processing = load_module(path_excel, path_processing_file)

    # Triggered on inital load of the page or tabs changes
    # Get the user weights for the current tab/model and process the data
    # Create the table
    weights = get_user.get_user_preferences(session["user"].get("id"), current_tab)
    if (ctx.triggered_id is None) or (ctx.triggered_id == "tabs"):
        df = data_processing.get_data(path_excel, weights)
        return create_table(df, list(weights.values()))

    # Triggered if the user changes the input weights
    elif len(input_weigts) > 0:
        weights_new = dict(zip(list(weights.keys()), input_weigts))
        df = data_processing.get_data(path_excel, weights_new)
        return create_table(df, weights_new)


@callback(
    Output("notifications-container", "children"),
    Input("save-settings", "n_clicks"),
    State({"type": "table-input", "index": ALL}, "value"),
    State("tabs", "value"),
    prevent_initial_call=True,
)
def save_settings(n_clicks, weigths, current_tab):
    """_summary_
    This callback saves the user input values to the database
    Args:
        n_clicks (int): Button trigger
        weigths (List): List of the input weights
        current_tab (string): Current selected tab/model

    Returns:
        string: Returns a notification message
    """
    if n_clicks:
        current_weigths = get_user.get_user_preferences(
            session["user"].get("id"), current_tab
        )

        # Make values as string for the json
        temp = [str(weight) for weight in weigths]

        # Combine the keys/column names and input values
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
