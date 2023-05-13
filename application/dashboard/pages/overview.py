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
    ]
)


@overview.callback(
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
