import os
import datetime
import pandas as pd
from dateutil.relativedelta import *

from flask import session
from dash_extensions.enrich import DashBlueprint, html, Output, Input, State
from dash import html, callback, ALL, ctx, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash.exceptions import PreventUpdate

from ...API.internal_API import get_co2model, get_user
from ..utils.functions import (
    load_module,
    make_tabs,
    create_table,
    make_indice_summary,
    get_stock_list,
    make_plot,
)
from ...API.external_API import yahoo_finance


stocks = DashBlueprint()

index = ["^DJI", "^GSPC", "^NDX", "^GDAXI"]

stocks.layout = dmc.Grid(
    [
        dmc.ChipGroup(
            make_indice_summary(index),
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
                        data=yahoo_finance.get_indices(index),
                    ),
                    dmc.Space(h=20),
                    dmc.TransferList(id="transfer-list", value=[[], []]),
                ],
                radius="lg",
                p="xs",
            ),
            span=2,
        ),
        dmc.Col(
            dmc.Paper(
                [dcc.Graph(id="stocks-graph")],
                radius="lg",
                p="xs",
            ),
            span=10,
        ),
    ],
    gutter="md",
    style={"padding-bottom": "60px"},
)


@stocks.callback(
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


@stocks.callback(
    Output("transfer-list", "value"),
    Input("select-index", "value"),
    prevent_initial_call=True,
)
def populate_list(selected_index):
    if selected_index is None:
        raise PreventUpdate
    else:
        return get_stock_list(selected_index)


@stocks.callback(
    Output("stocks-graph", "figure"),
    Input("transfer-list", "value"),
    prevent_initial_call=True,
)
def update_graph(stocks_list):
    stock_list = stocks_list[1]
    if ctx.triggered_id is None:
        raise PreventUpdate
    elif stock_list == []:
        return []
    else:
        stock_list = " ".join([dict.get("value") for dict in stock_list])
        df = yahoo_finance.get_history_data(stock_list)
        df = df.reset_index()
        return make_plot(df)
