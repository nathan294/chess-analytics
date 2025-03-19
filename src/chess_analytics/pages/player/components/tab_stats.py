# import asyncio

import polars as pl
from dash import html

# from api_requests.async_requests import fetch_all_archives
from chess_analytics.pages.player.components.stats.gamemode_card import gamemodeCard
from chess_analytics.pages.player.components.stats.graph_card import graphCard
from chess_analytics.pages.player.components.stats.openings_card import openingsCard
from chess_analytics.pages.player.figures.gamemodes_piechart import create_gamemode_piechart
from chess_analytics.pages.player.figures.games_histogram import create_games_histogram
from chess_analytics.pages.player.figures.outcome_piechart import create_outcome_piechart
from chess_analytics.pages.player.figures.win_ratio_piechart import create_win_ratio_piechart


def tabStats(df: pl.DataFrame):
    # Get latest gamemode played
    latest_gamemode = df.row(0)[df.columns.index("gamemode")]
    return html.Div(
        id="player-tab-stats",
        className="flex flex-col gap-8 animate__animated animate__fadeInUpBig animate__faster",
        children=[
            gamemodeCard(latest_gamemode=latest_gamemode, df=df),
            html.Div(className="h-[500px]", children=graphCard(title="Parties jouées", graph=create_games_histogram(df))),
            html.Div(className="h-[400px]", children=graphCard(title="Vos modes de jeu préférés", graph=create_gamemode_piechart(df))),
            html.Div(className="h-[400px]", children=graphCard(title="Votre taux de victoires", graph=create_win_ratio_piechart(df))),
            html.Div(
                className="h-[400px]", children=graphCard(title="Les raisons de vos victoires", graph=create_outcome_piechart(df, result="win"))
            ),
            html.Div(
                className="h-[400px]", children=graphCard(title="Les raisons de vos matchs nuls", graph=create_outcome_piechart(df, result="draw"))
            ),
            html.Div(
                className="h-[400px]",
                children=graphCard(title="Les raisons de vos défaites", graph=create_outcome_piechart(df, result="loss")),
            ),
            openingsCard(df),
        ],
    )
