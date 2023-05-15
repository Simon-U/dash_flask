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

stock_detail_bp = DashBlueprint()

index_values = ["^DJI", "^GSPC", "^NDX", "^GDAXI"]

stock_detail_bp.layout = dmc.Grid(
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
            dmc.Paper('test'))

    ],
    gutter="md",
    style={"padding-bottom": "60px"},
)