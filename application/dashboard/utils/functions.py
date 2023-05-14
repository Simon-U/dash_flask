import importlib
import json
import pandas as pd
import plotly.express as px
import pandas as pd

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from ...API.external_API import yahoo_finance


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


def make_performance_color(close_price, performance):
    if performance < 0:
        return dmc.Col(
            [dmc.Text(f"{close_price} ({performance}%)")],
            style={"color": "red", "padding": "0", "margine": "0"},
        )
    if performance == 0:
        return dmc.Col(
            [dmc.Text(f"{close_price} ({performance}%)")],
            style={"color": "black", "padding": "0", "margine": "0"},
        )
    else:
        return dmc.Col(
            [dmc.Text(f"{close_price} ({performance}%)")],
            style={"color": "green", "padding": "0", "margine": "0"},
        )


def make_indice_summary(indicies):
    summary = []
    for stock in indicies:
        values = yahoo_finance.get_performance_today(stock)
        new_col = dmc.Paper(
            [
                dmc.Chip(
                    f"{values.get('name')}",
                    value=stock,
                ),
                dmc.Text(f"{values.get('symbol')}", size="sm"),
                dmc.Divider(variant="solid"),
                dmc.Text(f"{values.get('close')} {values.get('currency')}"),
                make_performance_color(values.get("change"), values.get("performance")),
            ],
            style={"min-width": "30em"},
            radius="lg",
            p="xs",
        )
        summary.append(new_col)

    return summary


def get_stock_list(index):
    if index == "^DJI":
        ticker_list = pd.read_html(
            "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
        )
        df = ticker_list[1][["Symbol", "Company"]]
        temp_list = [
            {"value": f"{value}", "label": key}
            for value, key in zip(df["Symbol"], df["Company"])
        ]

    elif index == "^GSPC":
        ticker_list = pd.read_html(
            "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        )
        df = ticker_list[0][["Symbol", "Security"]]
        temp_list = [
            {"value": f"{value}", "label": key}
            for value, key in zip(df["Symbol"], df["Security"])
        ]

    elif index == "^NDX":
        ticker_list = pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")
        df = ticker_list[4][["Ticker", "Company"]]
        temp_list = [
            {"value": f"{value}", "label": key}
            for value, key in zip(df["Ticker"], df["Company"])
        ]

    elif index == "^GDAXI":
        ticker_list = pd.read_html("https://en.wikipedia.org/wiki/DAX")
        df = ticker_list[4][["Ticker", "Company"]]
        temp_list = [
            {"value": f"{value}", "label": key}
            for value, key in zip(df["Ticker"], df["Company"])
        ]

    return [temp_list, []]


def make_plot(df):
    if len(df) == 0:
        return px.line(
            [],
            x="Date",
            y=df.columns,
            hover_data={"Date": "|%B %d, %Y"},
            title="Your selected stocks",
        )

    fig = px.line(
        df,
        x="Date",
        y=df.columns,
        hover_data={"Date": "|%B %d, %Y"},
    )
    fig.update_xaxes(dtick="M1", tickformat="%b\n%Y")
    fig.update_layout(
        title="Historic Stock Price", xaxis_title="Date", yaxis_title="Price"
    )
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor="rgb(204, 204, 204)",
            linewidth=2,
            ticks="outside",
        ),
        yaxis=dict(
            showgrid=False,
            showline=True,
            showticklabels=True,
            linecolor="rgb(204, 204, 204)",
            linewidth=2,
        ),
        legend=dict(title="Stock"),
        plot_bgcolor="white",
    )
    return fig


def create_stocks_table(df):
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [
        html.Tr(
            [
                html.Td(html.A(cell, href="/dash/new_target", target="_blank"))
                if ind == 0
                else html.Td(cell)
                for ind, cell in enumerate(row)
            ]
        )
        for row in values
    ]
    return [html.Thead(header), html.Tbody(rows)]
