from dash import html

from chess_analytics.pages.player.components.history.player_rankings import playerRankings
from chess_analytics.pages.player.components.history.player_recent_games import playerRecentGames


def tabHistory(player_name: str, player_stats: dict, player_recent_games: list):
    return html.Div(
        id="player-history",
        className="animate__animated animate__fadeInUpBig animate__faster",
        children=html.Div(
            className="grid md:grid-cols-12 gap-4",
            children=[
                html.Div(className="col-span-12 md:col-span-3 h-full", children=playerRankings(player_stats)),
                html.Div(className="col-span-12 md:col-span-9 h-full", children=playerRecentGames(player_name, player_recent_games))
                if len(player_recent_games) > 0
                else html.Div(className="col-span-12 md:col-span-9 h-full mt-8 text-center", children="Aucune partie jouée."),
            ],
        ),
    )
