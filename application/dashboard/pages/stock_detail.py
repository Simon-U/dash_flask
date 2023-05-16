from dash_extensions.enrich import DashBlueprint, Output, Input, State
from dash import ctx, dcc
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate

from ..utils.functions import (
    make_stock_plot,
    make_text_table,
    make_numbers_table,
)
from ...API.external_API import yahoo_finance

stock_detail_bp = DashBlueprint()


stock_detail_bp.layout = dmc.Grid(
    [
        dmc.Title(
            order=2, id="company-name", style={"width": "100%"}
        ),  # Every 30 seconds
        dmc.Col(
            [
                dmc.Paper(
                    [
                        dmc.Table(
                            verticalSpacing="xs",
                            horizontalSpacing="xs",
                            id="company-information-table",
                        ),
                    ],
                    radius="lg",
                    p="xs",
                ),
                # dmc.Paper(
                #    [
                #        dmc.Table(
                #            verticalSpacing="xs",
                #            horizontalSpacing="xs",
                #            id="company-profile-table",
                #        )
                #    ],
                #    radius="lg",
                #    p="xs",
                # ),
            ],
            style={
                "display": "flex",
                "flex-flow": "row wrap",
                "gap": "10px",
                "padding": "0px",
                "margin": "0",
            },
            span=4,
        ),
        dmc.Col(
            [
                dmc.Paper(
                    [dcc.Graph(id="company-graph")],
                    radius="lg",
                    p="xs",
                    style={"min-height": "455px"},
                ),
            ],
            span=7,
            style={
                "padding": "0px",
                "margin": "0px",
            },
        ),
        dmc.Col(
            [
                dmc.Paper(
                    id="company-description",
                    radius="lg",
                    p="xs",
                    style={"overflow-wrap": "break-word"},
                ),
            ],
            span=4,
            style={
                "padding": "0px",
                "margin": "0",
            },
        ),
        dmc.Col(
            [
                dmc.Paper(
                    [
                        dmc.Table(
                            verticalSpacing="xs",
                            horizontalSpacing="xs",
                            id="company-fundemantals",
                        )
                    ],
                    radius="lg",
                    p="xs",
                ),
            ],
            style={
                "padding": "0px",
                "margin": "0px",
            },
            span=3,
        ),
        dmc.Col(
            [
                dmc.Paper(
                    [
                        dmc.Text(
                            id="company-stock",
                        ),
                    ],
                    radius="lg",
                    p="xs",
                ),
            ],
            style={
                "padding": "0px",
                "margin": "0px",
            },
            span=3,
        ),
    ],
    gutter="xl",
    align="start",
    style={
        "gap": "10px",
    },
)


@stock_detail_bp.callback(
    Output("company-name", "children"),
    Output("company-information-table", "children"),
    # Output("company-profile-table", "children"),
    Output("company-description", "children"),
    Output("company-fundemantals", "children"),
    Output("company-stock", "children"),
    Input("url", "search"),
)
def update(stock_symbol):
    if stock_symbol == "":
        raise PreventUpdate

    value_inputs = {
        "longName": "Company name",
        "longBusinessSummary": "Business Summary",
        "industry": "Industry",
        "sector": "Sector",
        "address1": "Adress",
        "city": "City",
        "state": "State",
        "zip": "Zip Code",
        "country": "Country",
        "website": "Website",
        "fullTimeEmployees": "Employees",
        "companyOfficers": "Officers",
        "enterpriseValue": "Enterprise Value",
        "marketCap": "Market Cap",
        "profitMargins": "Profit Margins",
        "revenuePerShare": "Revenue per Share",
        "grossProfits": "Gross Profit",
        "grossMargins": "Gross Margins",
        "ebitdaMargins": "Ebit Margins",
        "lastFiscalYearEnd": "Last Yeat",
        "mostRecentQuarter": "Recent Quater",
        "lastDividendValue": "Last Dividend Value",
        "lastDividendDate": "Last Dividend Date",
        "currentPrice": "Current Price",
        "targetLowPrice": "Low Target",
        "targetMeanPrice": "Average Target",
        "targetHighPrice": "High Target",
    }
    company_information = {
        "address1": "Adress",
        "city": "City",
        "state": "State",
        "zip": "Zip Code",
        "country": "Country",
        "industry": "Industry",
        "sector": "Sector",
        "website": "Website",
        "fullTimeEmployees": "Employees",
    }
    company_profile = {
        # "companyOfficers": "Officers",
    }

    company_fundamentals = {
        "enterpriseValue": "Enterprise Value",
        "lastFiscalYearEnd": "Last Yeat",
        "mostRecentQuarter": "Recent Quater",
        "profitMargins": "Profit Margins",
        "revenuePerShare": "Revenue per Share",
        "grossProfits": "Gross Profit",
        "grossMargins": "Gross Margins",
        "ebitdaMargins": "Ebit Margins",
    }

    company_stock = {
        "currentPrice": "Current Price",
        "marketCap": "Market Cap",
        "revenuePerShare": "Revenue per Share",
        "lastDividendValue": "Last Dividend Value",
        "lastDividendDate": "Last Dividend Date",
        "targetLowPrice": "Low Target",
        "targetMeanPrice": "Average Target",
        "targetHighPrice": "High Target",
    }

    company_data = yahoo_finance.get_company_data(
        list(value_inputs.keys()), stock_symbol.split("=")[1]
    )
    table_company_information = make_text_table(company_information, company_data)
    # table_company_profile = make_text_table(company_profile, company_data)
    table_company_fundamentals = make_numbers_table(company_fundamentals, company_data)
    table_company_stock = make_numbers_table(company_stock, company_data)
    return (
        company_data.get("longName"),
        table_company_information,
        # table_company_profile,
        company_data.get("longBusinessSummary"),
        table_company_fundamentals,
        table_company_stock,
    )


@stock_detail_bp.callback(
    Output("company-graph", "figure"),
    Input("stock-ticker", "n_intervals"),
    Input("stock-ticker", "disabled"),
    State("url", "search"),
)
def update(intervall, disabled, stock_symbol):
    if not disabled:
        data = yahoo_finance.get_current_company_price(stock_symbol.split("=")[1])
        data.reset_index(inplace=True)
        return make_stock_plot(data)
    else:
        raise PreventUpdate
