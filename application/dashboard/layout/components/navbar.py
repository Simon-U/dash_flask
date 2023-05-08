import dash_mantine_components as dmc
from dash_iconify import DashIconify


def get_icon(icon):
    return DashIconify(icon=icon, height=16)


navbar = dmc.Navbar(
    [
        dmc.Grid(
            [
                dmc.Col(
                    dmc.Image(src="/static/img/mes_rgb.png", width=300), span="content"
                ),
                dmc.Col(
                    dmc.Menu(
                        [
                            dmc.MenuTarget(
                                dmc.ActionIcon(get_icon(icon="tabler:user"))
                            ),
                            dmc.MenuDropdown(
                                [
                                    dmc.MenuItem(
                                        "Logout",
                                        href="/logout",
                                        refresh=True,
                                        icon=DashIconify(icon="tabler:logout"),
                                    ),
                                ]
                            ),
                        ]
                    ),
                    span=2,
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                    },
                ),
            ],
            justify="space-between",
            gutter="xl",
        )
    ],
    height="auto",
    style={"marginTop": "5px", "width": "100%", "background-color": "var(--mes_blue)"},
)
