from datetime import datetime

import dash_bootstrap_components as dbc
from dash import html
from dash_iconify import DashIconify

from api_requests.api_data_formatting import format_friends, format_games_played, format_last_connection, get_league_icon


def playerInfoBanner(player_info: dict, player_stats: dict):
    # Extract player country from the country api link
    player_country = player_info.get("country").split("/")[-1]

    # Extract player name if provided by the player
    player_name = player_info.get("name")

    # Dates formatting
    last_online_timestamp = datetime.fromtimestamp(player_info.get("last_online"))
    joined_timestamp = datetime.fromtimestamp(player_info.get("joined"))

    return (
        html.Div(
            className="container mx-auto py-10 flex flex-row",
            children=[
                html.Div(
                    className="w-full grid md:grid-cols-12 gap-4",
                    children=[
                        html.Div(
                            className="col-span-12 md:col-span-5 h-full flex flex-row",
                            children=[
                                html.Img(
                                    className="h-32 rounded-md",
                                    src=player_info.get("avatar", "https://www.chess.com/bundles/web/images/user-image.007dad08.svg"),
                                ),
                                html.Div(
                                    className="flex flex-col ml-6 gap-1",
                                    children=[
                                        # Username & name
                                        html.Div(
                                            className="flex flex-row",
                                            children=[
                                                html.Div(
                                                    className="flex flex-row items-center gap-2 text-3xl font-semibold",
                                                    children=[
                                                        f"{player_info.get('username')}",
                                                        DashIconify(id="user-country-icon", icon=f"circle-flags:{player_country.lower()}"),
                                                        dbc.Tooltip(
                                                            children=player_country,
                                                            target="user-country-icon",
                                                            placement="top",
                                                            className="tooltip",
                                                        ),
                                                    ],
                                                ),
                                                html.Div(
                                                    className="inline-block self-stretch border-l border-gray-200 opacity-25 mx-2 h-[75%] my-auto"
                                                )
                                                if player_name
                                                else None,
                                                html.Div(className="mt-auto text-lg text-black-600", children=player_name) if player_name else None,
                                            ],
                                        ),
                                        # Member since
                                        html.Div(
                                            className="text-gray-400 text-sm", children=f"Membre depuis le {joined_timestamp.strftime('%d %B %Y')}"
                                        ),
                                        # See on chess.com
                                        html.A(
                                            html.Button(
                                                className="bg-[var(--primary-color)] text-white hover:bg-[var(--primary-hover)] text-base p-2.5 rounded-md mt-4",
                                                children="Consulter le profil chess.com",
                                            ),
                                            href=player_info.get("url"),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="col-span-12 md:col-span-7 h-full flex flex-row justify-evenly items-center gap-8",
                            children=[
                                #
                                # Last seen
                                html.Div(
                                    id="indicator-last-seen",
                                    className="flex flex-col items-center gap-3",
                                    children=[
                                        DashIconify(className="opacity-100", icon="material-symbols:history-rounded", height=40),
                                        html.Div(className="", children=format_last_connection(last_online_timestamp)),
                                    ],
                                ),
                                dbc.Tooltip(
                                    children="Dernière connexion",
                                    target="indicator-last-seen",
                                    placement="top",
                                    className="tooltip",
                                ),
                                #
                                # Friends
                                html.Div(
                                    id="indicator-friends",
                                    className="flex flex-col items-center gap-3",
                                    children=[
                                        DashIconify(className="opacity-100", icon="fa-solid:user-friends", height=40),
                                        html.Div(className="", children=format_friends(player_info)),
                                    ],
                                ),
                                dbc.Tooltip(
                                    children="Amis",
                                    target="indicator-friends",
                                    placement="top",
                                    className="tooltip",
                                ),
                                #
                                # Games played
                                html.Div(
                                    id="indicator-games-played",
                                    className="flex flex-col items-center gap-3",
                                    children=[
                                        DashIconify(className="opacity-100", icon="streamline:chess-pawn-solid", height=40),
                                        html.Div(className="", children=format_games_played(player_stats)),
                                    ],
                                ),
                                dbc.Tooltip(
                                    children="Parties jouées",
                                    target="indicator-games-played",
                                    placement="top",
                                    className="tooltip",
                                ),
                                #
                                # League
                                html.Div(
                                    id="indicator-league",
                                    className="flex flex-col items-center gap-3",
                                    children=[
                                        html.Img(className="h-[40px]", src=get_league_icon(player_info.get("league"))),
                                        html.Div(className="", children=player_info.get("league", "Aucune division")),
                                    ],
                                ),
                                dbc.Tooltip(
                                    children="Division",
                                    target="indicator-league",
                                    placement="top",
                                    className="tooltip",
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )
