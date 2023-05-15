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
    make_profile_table,
    make_company_information,
)
from ...API.external_API import yahoo_finance

stock_detail_bp = DashBlueprint()

index_values = ["^DJI", "^GSPC", "^NDX", "^GDAXI"]

stock_detail_bp.layout = dmc.Grid(
    [
        dmc.Paper(
            [
                dmc.Text(id="company-name"),
            ],
            radius="lg",
            p="xs",
        ),
        dmc.Col(
            [
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
                dmc.Paper(
                    [
                        dmc.Text(
                            id="company-description",
                        ),
                    ],
                    radius="lg",
                    p="xs",
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "row",
                "gap": "10px",
                "padding": "0px",
                "margin": "0",
            },
        ),
    ],
    gutter="md",
    style={"padding-bottom": "60px", "gap": "3em"},
)


@stock_detail_bp.callback(
    Output("company-name", "children"),
    Output("company-description", "children"),
    Output("company-profile-table", "children"),
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

    company_data = yahoo_finance.get_company_data(
        list(value_inputs.keys()), stock_symbol.split("=")[1]
    )
    layout_company_information = make_company_information(
        company_information, company_data
    )
    table_company_profile = make_profile_table(company_profile, company_data)

    return (
        layout_company_information,
        company_data.get("longBusinessSummary"),
        table_company_profile,
    )
