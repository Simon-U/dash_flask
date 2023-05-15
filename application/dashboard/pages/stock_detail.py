from dash_extensions.enrich import DashBlueprint, Output, Input
from dash import ctx, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash.exceptions import PreventUpdate

from ..utils.functions import (
    make_indice_summary,
    get_stock_list,
    make_stock_plot,
    make_table,
    make_profile_table,
    make_company_information,
)
from ...API.external_API import yahoo_finance

stock_detail_bp = DashBlueprint()

index_values = ["^DJI", "^GSPC", "^NDX", "^GDAXI"]

stock_detail_bp.layout = dmc.Grid(
    [
        dcc.Interval(id="stock-ticker", interval=30000),  # Every 30 seconds
        dmc.Col(
            [
                dmc.Col(
                    [
                        dmc.Paper(
                            [
                                dmc.Text(id="company-name"),
                            ],
                            radius="lg",
                            p="xs",
                        ),
                        dmc.Paper(
                            [
                                dmc.Table(
                                    verticalSpacing="xs",
                                    horizontalSpacing="xs",
                                    id="company-profile-table",
                                )
                            ],
                            radius="lg",
                            p="xs",
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flex-flow": "row wrap",
                        "gap": "10px",
                        "padding": "0px",
                        "margin": "0",
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
                    style={
                        "display": "flex",
                        "flex-flow": "row wrap",
                        "gap": "10px",
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
                        "display": "flex",
                        "flex-flow": "row wrap",
                        "gap": "10px",
                        "padding": "0px",
                        "margin": "0",
                    },
                ),
            ],
            span="auto",
            style={
                "display": "flex",
                "flex-flow": "row wrap",
                "gap": "10px",
                "padding": "0px",
                "margin": "0",
            },
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
            span=8,
            style={
                "padding": "0px",
                "margin": "0px",
            },
        ),
    ],
    gutter="md",
    style={
        "padding-bottom": "60px",
        "gap": "10px",
    },
)


@stock_detail_bp.callback(
    Output("company-name", "children"),
    Output("company-description", "children"),
    Output("company-profile-table", "children"),
    Output("company-fundemantals", "children"),
    Output("company-stock", "children"),
    Input("url", "search"),
)
def update(stock_symbol):
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
    }
    company_profile = {
        "industry": "Industry",
        "sector": "Sector",
        "website": "Website",
        "fullTimeEmployees": "Employees",
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
    layout_company_information = make_company_information(
        company_information, company_data
    )
    table_company_profile = make_profile_table(company_profile, company_data)
    table_company_fundamentals = make_table(company_fundamentals, company_data)
    table_company_stock = make_table(company_stock, company_data)
    return (
        layout_company_information,
        company_data.get("longBusinessSummary"),
        table_company_profile,
        table_company_fundamentals,
        table_company_stock,
    )


@stock_detail_bp.callback(
    Output("company-graph", "figure"),
    Input("url", "search"),
    Input("stock-ticker", "n_intervals"),
)
def update(stock_symbol, intervall):
    print(ctx.triggered_id)
    data = yahoo_finance.get_current_company_price(stock_symbol.split("=")[1])
    data.reset_index(inplace=True)
    return make_stock_plot(data)
