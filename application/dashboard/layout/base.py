import glob
import importlib
import os
from datetime import date

import dash_mantine_components as dmc
from dash import Dash, html, dash_table, dcc, callback, Output, Input, ALL
import pandas as pd

from ..utils.functions import get_tab_names
from .components.navbar import navbar
import importlib
import pathlib
from ...data.processing.main import get_data
from dash_iconify import DashIconify


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
    theme={
        "fontFamily": "'Inter', sans-serif",
        "primaryColor": "indigo",
        "margin": "0px",
        "max-width": "100%",
        "components": {
            "Container": {"styles": {"maw": "100%"}},
            "Button": {"styles": {"root": {"fontWeight": 400}}},
            "Alert": {"styles": {"title": {"fontWeight": 500}}},
            "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
        },
    },
    inherit=True,
    children=[
        dmc.Container(
            dmc.Grid(
                children=[
                    navbar,
                    dmc.Col(
                        dmc.Tabs(
                            make_tabs(get_tab_names()),
                            value=get_tab_names()[0],
                            placement="left",
                            orientation="vertical",
                            id="tabs",
                        ),
                        span=2,
                    ),
                    dmc.Col(html.Div(id="tabs-content"), span=10),
                ],
                gutter="xl",
                grow=True,
                style={"margin": 0, "max-width": "100%"},
            ),
            style={"margin": 0, "max-width": "100%"},
        )
    ],
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
                html.Td(cell)
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
    weights = {
        "Technologie Readiness Level": 5,
        "verwendeter Kraftstoff": 6,
        "behandelte Rauchgasmenge": 7,
        "CO2 Rauchgaskonzentration": 3,
        "Anlage Eingangsdruck": 4,
        "Eingangs Prozesstemperatur": 5,
        "CO2 Reinheit": 3,
        "CO2 Abscheiderate": 7,
        "CO2 Temperatur vor Speicherung": 4,
        "Energiebedarf elektrisch": 9,
        "Energiebedarf thermisch": 7,
        "Prozessmittelverbrauch": 3,
        "Abgasvorbehandlung": 10,
        "Platzbedarf": 7,
    }

    list_tabs = get_tab_names()
    for tab in list_tabs:
        if current_tab == tab:
            if len(input_weigts) > 0:
                excel_file = os.path.join(
                    os.getcwd(), "application/data", f"{current_tab}.xlsx"
                )
                weights_new = dict(zip(list(weights.keys()), input_weigts))

                # ToDo Import the data function dynamically

                df = get_data(excel_file, weights_new)
                return create_table(df, weights_new)

            else:
                excel_file = os.path.join(
                    os.getcwd(), "application/data", f"{current_tab}.xlsx"
                )

                # ToDo Import the data function dynamically

                df = get_data(excel_file, weights)
                return create_table(df, list(weights.values()))
