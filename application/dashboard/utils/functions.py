import importlib

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def load_module(name, path):
    """_summary_
    Function to load a python module at runtime given a name and path
    Args:
        name (string): name of the module to load
        path (string): path where the module is stored

    Returns:
        object: return the loaded module as object
    """
    spec = importlib.util.spec_from_file_location(name, path)
    data_processing = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(data_processing)
    return data_processing


def make_tabs(tab_names):
    """_summary_
    Function to create the tabs
    Args:
        tab_names (list): List of tab names

    Returns:
        returns: html components with tabs
    """
    list_tabs = [dmc.Tab(name, value=name) for name in tab_names]
    tabs = (
        dmc.TabsList(
            list_tabs,
            position="left",
        ),
    )
    return tabs


def get_icon(icon, height=16):
    """_summary_
    Make a icon with given hieght
    """
    return DashIconify(icon=icon, height=height)


def make_table_icon(value):
    """_summary_
    Function to make circle icon based on borders
    Args:
        value (int): value to check

    Returns:
        html: returns the respectif icon
    """
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
    """_summary_
    Creates html table with weights and values
    Args:
        df (dataframe): dataframe to be passed into the table
        weights (dict): dict with row names as keys

    Returns:
        html: Table
    """
    # Adding two columns, Row names and the weights
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
                else html.Td(make_table_icon(cell))
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
