import uuid
from typing import Literal

import polars as pl
from dash import Input, Output, State, callback, dcc, html
from dash_iconify import DashIconify

from api_requests.data_prep import filter_df_on_gamemode, filter_df_on_periodicity, get_ranking_evolution
from chess_analytics.pages.player.components.stats.ratio_bar import ratioBar
from chess_analytics.pages.player.figures.gamemode_ranking_linechart_plotly import create_gamemode_ranking_linechart_plotly


def gamemodeCardContent(df_filtered: pl.DataFrame, player_ranking: int):
    ranking_evolution = get_ranking_evolution(df_filtered)
    return [
        # Ranking, Games etc
        html.Div(
            className="flex flex-row mt-12 items-center justify-evenly",
            children=[
                # Ranking
                html.Div(
                    className="flex flex-col",
                    children=[
                        html.Div(
                            className="flex flex-row gap-3 items-center font-bold",
                            children=[
                                html.Div(className="text-5xl", children=player_ranking),
                                html.Div(
                                    key=str(uuid.uuid4()),  # Forces re-render to trigger the animation
                                    className=f"animate__animated animate__flipInX animate__faster flex flex-row gap-1 text-xl items-center font-bold text-{'green' if ranking_evolution > 0 else 'yellow' if ranking_evolution == 0 else 'red'}-500",
                                    children=[
                                        DashIconify(
                                            icon=f"mingcute:arrow-{'up' if ranking_evolution > 0 else 'right' if ranking_evolution == 0 else 'down'}-fill",
                                        ),
                                        html.Div(
                                            children=abs(ranking_evolution),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Div(className="text-gray-400 -mt-1", children="Classement"),
                    ],
                ),
                # Total gamemode games
                html.Div(
                    className="flex flex-col items-center gap-2",
                    children=[
                        DashIconify(className="", icon="streamline:chess-king-solid", height=40),
                        html.Div(
                            className="flex flex-row items-center gap-1",
                            children=[
                                html.Div(
                                    className="text-lg animate__animated animate__flipInX animate__faster",
                                    key=str(uuid.uuid4()),  # Forces re-render to trigger the animation
                                    children=len(df_filtered),
                                ),
                                html.Div(className="text-base", children="parties"),
                            ],
                        ),
                    ],
                ),
                # Best ranking
                html.Div(
                    className="flex flex-col items-center",
                    children=[
                        html.Div(
                            className="text-3xl animate__animated animate__flipInX animate__faster",
                            key=str(uuid.uuid4()),  # Forces re-render to trigger the animation
                            children=df_filtered["player_rating"].max()
                            if df_filtered["player_rating"].max()
                            else player_ranking
                            if player_ranking
                            else None,
                        ),
                        html.Div(className="text-gray-400", children="Meilleur classement"),
                    ],
                ),
            ],
        ),
        # Win/Loss Ratio bar
        ratioBar(df_filtered),
        # Linechart
        # html.Div(className="mt-8 h-[300px] graph", children=create_ranking_evolution_linechart(df_filtered)),
        html.Div(
            className="mt-8 h-[300px]",
            children=dcc.Graph(
                id="",
                config={
                    "displayModeBar": False,
                },
                figure=create_gamemode_ranking_linechart_plotly(df_filtered),
                responsive=True,
            ),
        ),
    ]


def gamemodeCard(
    latest_gamemode: str,
    df: pl.DataFrame,
    periodicity: Literal["tab-7days", "tab-30days", "tab-90days", "tab-1year", "tab-total"] = "tab-90days",
):
    all_gamemodes = df["gamemode"].unique().to_list()

    # Get filtered dataframe based on periodicity & gamemode
    df_filtered = filter_df_on_gamemode(df, latest_gamemode)
    df_filtered = filter_df_on_periodicity(df_filtered, periodicity)

    try:
        player_ranking = df_filtered.filter(pl.col("gamemode") == latest_gamemode).row(0)[df_filtered.columns.index("player_rating")]
    except Exception:
        player_ranking = "Inconnu"
    return html.Div(
        className="rounded-lg p-4 shadow-md bg-[var(--card-color)]",
        children=[
            html.Div(
                className="",
                children=dcc.Dropdown(
                    id="gamemode-dropdown",
                    value=latest_gamemode,
                    options=[
                        {
                            "label": html.Span(
                                className="flex flex-row items-center",
                                children=[
                                    html.Img(src=f"/assets/images/gamemodes_icons/{i}.png", className="size-[24px]"),
                                    html.Span(str(i).replace("_chess", "").replace("_", " - ").title(), className="pl-2"),
                                ],
                            ),
                            "value": i,
                        }
                        for i in all_gamemodes
                    ],
                    className="custom-dropdown",
                    clearable=False,
                    searchable=False,
                ),
            ),
            #
            # Periodicity tabs
            dcc.Tabs(
                id="gamemodeCard-periodicity-tabs",
                value=periodicity,
                className="gap-0 mt-4",
                children=[
                    dcc.Tab(
                        label="7 jours",
                        value="tab-7days",
                        className="custom-tab-periodicity",
                        selected_className="custom-tab-periodicity-selected",
                    ),
                    dcc.Tab(
                        label="30 jours",
                        value="tab-30days",
                        className="custom-tab-periodicity",
                        selected_className="custom-tab-periodicity-selected",
                    ),
                    dcc.Tab(
                        label="90 jours",
                        value="tab-90days",
                        className="custom-tab-periodicity",
                        selected_className="custom-tab-periodicity-selected",
                    ),
                    dcc.Tab(
                        label="1 an",
                        value="tab-1year",
                        className="custom-tab-periodicity",
                        selected_className="custom-tab-periodicity-selected",
                    ),
                    dcc.Tab(
                        label="Total",
                        value="tab-total",
                        className="custom-tab-periodicity",
                        selected_className="custom-tab-periodicity-selected",
                    ),
                ],
            ),
            html.Div(id="gamemodeCard-content", children=gamemodeCardContent(df_filtered, player_ranking)),
        ],
    )


# Callback to update the data based on periodicity and gamemode
@callback(
    [
        Output("gamemodeCard-content", "children"),
    ],
    [
        Input("gamemode-dropdown", "value"),
        Input("gamemodeCard-periodicity-tabs", "value"),
    ],
    State("player-games", "data"),
    prevent_initial_call=True,
)
def update_gamemodeCard_content(gamemode, periodicity, data):
    df = pl.DataFrame(data)
    df = df.with_columns(pl.col("end_time").str.to_datetime("%Y-%m-%dT%H:%M:%S"))
    # Get filtered dataframe based on periodicity & gamemode
    df_filtered = filter_df_on_gamemode(df, gamemode)
    df_filtered = filter_df_on_periodicity(df_filtered, periodicity)
    player_ranking = df.filter(pl.col("gamemode") == gamemode).row(0)[df.columns.index("player_rating")]
    return (gamemodeCardContent(df_filtered, player_ranking),)
