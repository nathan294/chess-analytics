import dash
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

app_layout = html.Div(
    className="flex flex-col min-h-[calc(100vh-18px)]",
    children=[
        dcc.Location(id="url", refresh="callback-nav"),
        # Header avec logo, barre de recherche et bouton
        html.Header(
            className="flex items-center justify-center p-4 bg-[var(--header-background)] h-24 relative",
            children=[
                dcc.Link(
                    href="/",
                    children=html.Div(
                        className="flex flex-row",
                        children=[
                            html.Img(
                                src="/assets/images/my_logo.png",
                                alt="Logo",
                                className="h-16",
                            ),
                            html.Div(
                                className="h-full hidden md:block ml-2 my-auto text-white text-[1.4rem] font-medium",
                                children="Chess analytics",
                            ),
                        ],
                    ),
                ),
                dcc.Input(
                    id="search-field-user",
                    type="text",
                    placeholder="Rechercher un joueur...",
                    className="w-72 h-11 ml-8 px-3 py-2 border-none rounded-lg text-black",
                ),
                html.Button(
                    children="Rechercher",
                    id="search-button",
                    className="ml-4 h-11 px-4 py-2 bg-[var(--card-color)] border-none hover:bg-[--card-color-selected] rounded-xl text-white",
                ),
                html.A(
                    className="absolute hidden md:block right-10",
                    children=DashIconify(icon="mdi:github", height=40),
                    href="https://github.com/nathan294/chess-analytics",
                ),
            ],
        ),
        html.Div(className="flex grow", id="dash-page-container", children=dash.page_container),
    ],
)


@callback(
    Output("url", "pathname"),
    Input("search-field-user", "n_submit"),
    Input("search-button", "n_clicks"),
    State("search-field-user", "value"),
    prevent_initial_call=True,
)
def update_link_href(n_submit, n_clicks, player_name: str):
    if (n_submit or n_clicks) and player_name:
        return f"/player/{player_name}"
    raise PreventUpdate
