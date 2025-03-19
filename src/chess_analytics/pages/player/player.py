import asyncio
import os

import dash
import dash_extensions as de
from dash import Input, Output, State, callback, dcc, html

from api_requests.async_requests import fetch_all_archives, fetch_player_data
from api_requests.data_prep import get_games_dataframe
from chess_analytics.components.player_info_banner import playerInfoBanner
from chess_analytics.components.player_not_found import playerNotFound
from chess_analytics.pages.player.components.tab_history import tabHistory
from chess_analytics.pages.player.components.tab_stats import tabStats

dash.register_page(__name__, name="player", path_template="/player/<player_name>", title=None)


def layout(player_name: str, **kwargs):
    return html.Div(
        children=[
            dcc.Store(id="page-parameters", data={"player_name": player_name}),
            html.Div(id="player-main-content"),
            html.Div(
                id="player-main-content-loading-animation",
                className="size-48 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2",
                children=de.Lottie(
                    options=dict(loop=True, autoplay=False, rendererSettings=dict(preserveAspectRatio="xMidYMid slice")),
                    width="100%",
                    url="/assets/animations/among_us.json",
                ),
            ),
        ],
    )


@callback(
    Output("player-main-content", "children"),
    Input("player-main-content", "id"),
    State("page-parameters", "data"),
    running=(Output("player-main-content-loading-animation", "style"), {"display": "block"}, {"display": "none"}),
)
def init_page(_, page_parameters):
    player_name = page_parameters.get("player_name")
    # Fetch player information
    #
    # For dev purposes :
    #
    if os.getenv("RUNNING_LOCALLY") == 1:
        player_name = "nathan294"
        from api_requests.temp_static_data import player_archives, player_info, player_recent_games, player_stats
    else:
        # Retrieve all games played by the player
        player_info, player_stats, player_recent_games, player_archives = asyncio.run(fetch_player_data(player_name))

    if not player_info:
        return playerNotFound(player_name)
    return html.Div(
        id="main-content",
        children=[
            dcc.Store(
                id="player-data",
                data={
                    "player_name": player_name,
                    "player_info": player_info,
                    "player_stats": player_stats,
                    "player_recent_games": player_recent_games,
                    "player_archives": player_archives,
                },
            ),
            dcc.Store(id="player-games"),
            html.Div(
                id="player-info-banner",
                className="bg-[var(--card-color)]",
                children=playerInfoBanner(player_info, player_stats),
            ),
            html.Div(
                className="container mx-auto",
                children=[
                    dcc.Tabs(
                        id="player-tabs",
                        value="tab-history",
                        className="gap-8 mt-8",
                        children=[
                            dcc.Tab(
                                label="Historique",
                                value="tab-history",
                                className="custom-tab",
                                selected_className="custom-tab-selected",
                            ),
                            dcc.Tab(
                                label="Statistiques",
                                value="tab-stats",
                                className="custom-tab",
                                selected_className="custom-tab-selected",
                            ),
                        ],
                    ),
                    html.Div(
                        id="player-tabs-content",
                        className="my-8",
                    ),
                    html.Div(
                        className="size-48 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2",
                        id="player-tabs-content-loading-animation",
                        children=de.Lottie(
                            options=dict(loop=True, autoplay=False, rendererSettings=dict(preserveAspectRatio="xMidYMid slice")),
                            width="100%",
                            url="/assets/animations/among_us.json",
                        ),
                    ),
                ],
            ),
        ],
    )


@callback(
    [
        Output("player-tabs-content", "children"),
        Output("player-games", "data"),
    ],
    Input("player-tabs", "value"),
    [
        State("player-data", "data"),
    ],
    running=[
        (Output("player-tabs-content-loading-animation", "style"), {"display": "block"}, {"display": "none"}),
        (Output("player-tabs-content", "style"), {"display": "none"}, {"display": "block"}),
    ],
)
def render_content(tab, player_data):
    player_name = player_data.get("player_name")
    # player_info = player_data.get("player_info")
    player_stats = player_data.get("player_stats")
    player_recent_games = player_data.get("player_recent_games")
    player_archives = player_data.get("player_archives")

    if tab == "tab-history":
        return (tabHistory(player_name=player_name, player_stats=player_stats, player_recent_games=player_recent_games), dash.no_update)
    elif tab == "tab-stats":
        # Retrieve all games played by the player
        all_player_games = asyncio.run(fetch_all_archives(player_archives))
        df = get_games_dataframe(player_name, all_player_games)

        return (tabStats(df), df.to_dicts())
