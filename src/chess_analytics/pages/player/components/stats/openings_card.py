import dash_bootstrap_components as dbc
import polars as pl
from dash import Input, Output, State, callback, dcc, html

from chess_analytics.pages.player.components.stats.openings_ratio_bar import openingsRatioBar


def openingsCardContent(df: pl.DataFrame):
    table_header = html.Thead(
        html.Tr(
            [
                html.Th("Ouverture", style={"width": "40%"}),
                html.Th("Parties jouées", style={"width": "20%"}),
                html.Th("Résultats", style={"width": "40%"}),
            ]
        ),
        className="text-left",
    )

    table_rows = []
    rows = df.rows(named=True)[:20]  # Take only 20 most common openings

    for i, row in enumerate(rows):
        table_rows.append(
            html.Tr(
                children=[
                    html.Td(
                        [
                            html.A(
                                id={"type": "opening-name-url", "index": i},
                                className="underline",
                                children=row.get("opening_name"),
                                href=f"https://www.chess.com/openings/{str(row.get('opening_name')).replace(' ', '-')}",
                            ),
                            dbc.Tooltip(
                                children="Visiter la page chess.com de l'ouverture",
                                target={"type": "opening-name-url", "index": i},
                                placement="top",
                                className="tooltip",
                            ),
                        ],
                        style={"width": "40%"},
                        className="font-semibold",
                    ),
                    html.Td(row.get("total"), style={"width": "20%"}),
                    html.Td(
                        openingsRatioBar(win=row.get("win"), loss=row.get("loss"), draw=row.get("draw"), total=row.get("total")),
                        style={"width": "40%"},
                    ),
                ],
            )
        )

        # Add a divider row after each row except the last one
        if i < len(rows) - 1:
            table_rows.append(html.Tr(children=[html.Td(html.Hr(className="my-0 border-gray-700"), colSpan=3)]))

    table_body = html.Tbody(table_rows)

    table = dbc.Table(
        className="w-full border-separate border-spacing-y-4",
        children=[table_header, table_body],
        bordered=False,
        hover=True,
        responsive=True,
    )

    return table


def openingsCard(df: pl.DataFrame):
    df_openings = (
        df.group_by(["player_side", "opening_name", "player_result"])
        .len()
        .pivot(on="player_result", index=["player_side", "opening_name"], values="len", aggregate_function="sum")
        .fill_null(0)
        .with_columns(total=pl.col("win") + pl.col("loss") + pl.col("draw"))
        .sort(by="total", descending=True)
    )

    return html.Div(
        className="flex flex-col h-full rounded-lg bg-[var(--card-color)]",
        children=[
            dcc.Store(id="data-player-openings", data=df_openings.to_dicts()),
            html.Div(
                className="font-semibold h-12 rounded-t-lg content-center text-center text-lg w-full bg-[var(--card-color-selected)]",
                children="Ouvertures fréquentes",
            ),
            #
            # Side tabs
            html.Div(
                className="p-6",
                children=[
                    html.Div(
                        className="flex flex-row items-center gap-4",
                        children=[
                            html.Div(className="mb-1", children="En jouant les :"),
                            dcc.Tabs(
                                id="openingsCard-side-tabs",
                                value="white",
                                className="gap-4",
                                children=[
                                    dcc.Tab(
                                        label="Blancs",
                                        value="white",
                                        className="custom-tab-periodicity",
                                        selected_className="custom-tab-periodicity-selected",
                                    ),
                                    dcc.Tab(
                                        label="Noirs",
                                        value="black",
                                        className="custom-tab-periodicity",
                                        selected_className="custom-tab-periodicity-selected",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(id="openingsCard-content", className="", children=""),
                ],
            ),
        ],
    )


# Callback to update the data based on periodicity and gamemode
@callback(
    [
        Output("openingsCard-content", "children"),
    ],
    [
        Input("openingsCard-side-tabs", "value"),
    ],
    State("data-player-openings", "data"),
    # prevent_initial_call=True,
)
def update_gamemodeCard_content(side, data):
    df = pl.DataFrame(data)

    # Filter on side
    df = df.filter(pl.col("player_side") == side, pl.col("opening_name") != "Undefined")

    return (openingsCardContent(df),)
