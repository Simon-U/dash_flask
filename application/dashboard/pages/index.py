from dash_extensions.enrich import DashBlueprint, Output, Input
from dash import ctx, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash.exceptions import PreventUpdate

from ..utils.functions import (
    make_indice_summary,
    get_stock_list,
    make_plot,
    create_stocks_table,
)
from ...API.external_API import yahoo_finance

index_bp = DashBlueprint()

index_values = ["^DJI", "^GSPC", "^NDX", "^GDAXI"]

index_bp.layout = dmc.Grid(
    [
        dmc.ChipGroup(
            make_indice_summary(index_values),
            id="chip-index",
            style={
                "display": "flex",
                "flex-grow": "0",
                "flex-basis": "100%",
                "flex-direction": "row",
                "width": "100%",
                "justify-content": "space-between",
                "flex-wrap": "wrap",
                "height": "auto",
                "min-height": "2em",
                "margin-bottom": "5em",
            },
        ),
        dmc.Space(h=40),
        dmc.Col(
            dmc.Paper(
                [
                    dmc.Select(
                        id="select-index",
                        label="Select a index",
                        data=yahoo_finance.get_indices(index_values),
                    ),
                    dmc.Space(h=20),
                    dmc.TransferList(
                        id="transfer-list",
                        showTransferAll=False,
                        value=[[], []],
                    ),
                ],
                radius="lg",
                p="xs",
                style={"min-height": "470px"},
            ),
            span=2,
        ),
        dmc.Col(
            dmc.Paper(
                [
                    dmc.Table(
                        verticalSpacing="xs", horizontalSpacing="xs", id="company-table"
                    )
                ],
                radius="lg",
                p="xs",
                style={"min-height": "470px"},
            ),
            span=5,
        ),
        dmc.Col(
            dmc.Paper(
                [dcc.Graph(id="stocks-graph")],
                radius="lg",
                p="xs",
                style={"min-height": "455px"},
            ),
            span=5,
        ),
    ],
    gutter="md",
    style={"padding-bottom": "60px"},
)


@index_bp.callback(
    Output("select-index", "value"),
    Output("chip-index", "value"),
    Input("select-index", "value"),
    Input("chip-index", "value"),
    prevent_initial_call=True,
)
def syncro_chip_select(select_value, chip_value):
    if ctx.triggered_id is None:
        raise PreventUpdate
    if ctx.triggered_id == "chip-index":
        return chip_value, chip_value
    elif ctx.triggered_id == "select-index":
        return select_value, select_value


@index_bp.callback(
    Output("transfer-list", "value"),
    Input("select-index", "value"),
    prevent_initial_call=True,
)
def populate_list(selected_index):
    if selected_index is None:
        raise PreventUpdate
    else:
        return get_stock_list(selected_index)


@index_bp.callback(
    Output("stocks-graph", "figure"),
    Output("company-table", "children", allow_duplicate=True),
    Output("notifications-container", "children"),
    Input("transfer-list", "value"),
    prevent_initial_call=True,
)
def update_graph(stocks_list):
    stock_list = stocks_list[1]

    if ctx.triggered_id is None:
        raise PreventUpdate

    elif stock_list == []:
        return [], [], []
    else:
        message = dmc.Notification(
            id="my-notification",
            title="Data loaded",
            message="Thank you for waiting",
            color="green",
            action="update",
            icon=DashIconify(icon="akar-icons:circle-check"),
        )

        history, company_data = yahoo_finance.get_history_data(stock_list)
        history = history.reset_index()
        return ((make_plot(history)), create_stocks_table(company_data), message)


@index_bp.callback(
    Output("notifications-container", "children", allow_duplicate=True),
    Input("transfer-list", "value"),
)
def update_graph(stocks_list):
    stock_list = stocks_list[1]

    if ctx.triggered_id is None:
        raise PreventUpdate

    elif stock_list == []:
        raise PreventUpdate

    return dmc.Notification(
        id="my-notification",
        title="Preparing Data",
        message="The process has started.",
        loading=True,
        color="orange",
        action="show",
        autoClose=False,
        disallowClose=True,
    )
