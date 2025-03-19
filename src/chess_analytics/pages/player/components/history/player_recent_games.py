from datetime import datetime

import dash_bootstrap_components as dbc
from dash import html
from dash_iconify import DashIconify

from api_requests.api_data_formatting import format_accuracy, format_last_connection, get_game_outcome, get_number_of_moves, get_outcome_icon


def gameCard(username: str, game: dict):
    white = game.get("white")
    black = game.get("black")
    outcome, winner, color = get_game_outcome(username, game)
    white_accuracy, black_accuracy, accuracy_status = format_accuracy(game)
    number_of_moves = get_number_of_moves(game)
    gamemode = game.get("time_class", "rapid") + "_" + game.get("rules", "chess")
    loser, outcome_icon, end_reason = get_outcome_icon(game)

    # Dates formatting
    end_time_timestamp = datetime.fromtimestamp(game.get("end_time"))
    end_time_formatted = format_last_connection(end_time_timestamp)
    if end_time_formatted == "En ligne":
        end_time_formatted = "Maintenant"

    card_color = color + "-400"
    return html.Div(
        className=f"flex flex-row rounded-lg border-none border-gray-300 shadow-md bg-{card_color} bg-opacity-20",
        children=[
            html.Div(className=f"game-decoration w-[0.375rem] rounded-s-lg bg-{color}-700", children=[]),
            html.Div(
                className="game-content grow flex flex-row p-4 pt-7 size-full relative",
                children=[
                    # Infos
                    html.Div(
                        className="flex flex-col relative",
                        children=[
                            html.Div(className="text-xs text-gray-400 absolute top-[-12px]", children=outcome),
                            html.Div(
                                className="text-xs text-gray-400 absolute top-[4px] whitespace-nowrap",
                                children=end_time_formatted,
                            ),
                            html.Div(
                                className="inline-block self-stretch border-b border-gray-200 opacity-25 mt-8 mb-2 w-[75%] mx-auto"
                            ),  # Separator
                            # Icon of game mode
                            html.Div(
                                className="flex flex-col gap-2 items-center mx-5 my-auto",
                                children=[
                                    html.Div(className="text-xs text-gray-400", children=str(game.get("time_class", "rapid")).capitalize()),
                                    html.Img(className="size-[28px]", src=f"/assets/images/gamemodes_icons/{gamemode}.png"),
                                ],
                            ),
                        ],
                    ),
                    # Opponents
                    html.Div(
                        className="flex flex-col gap-1 ml-6 relative pt-3 xl:ml-14 grow max-w-[220px]",
                        children=[
                            html.Div(
                                className="text-gray-400 absolute top-[-12px] text-xs",
                                children="Joueurs",
                            ),
                            # White
                            html.Div(
                                className="flex flex-row gap-1 items-center",
                                children=[
                                    DashIconify(className="opacity-90 text-white", icon="material-symbols:chess-pawn-rounded", width=14),
                                    html.Div(
                                        className="flex flex-row gap-1",
                                        children=[
                                            html.Div(className="text-base font-semibold", children=white.get("username")),
                                            html.Div(className="text-base font-normal text-gray-400", children=f"({white.get('rating')})"),
                                        ],
                                    ),
                                    html.Img(className="size-[16px]", src="/assets/images/chess_com_icons/winner.png") if winner == "white" else None,
                                    # html.Div(
                                    #     className=f"text-[8px] bg-{color}-500 bg-opacity-50 border border-{color}-600 rounded-sm px-1",
                                    #     children="WINNER",
                                    # )
                                    # if winner == "white"
                                    # else None,
                                ],
                            ),
                            html.Div(className="text-sm text-gray-400", children="VS"),
                            # Black
                            html.Div(
                                className="flex flex-row gap-1 items-center",
                                children=[
                                    DashIconify(className="opacity-90 text-black", icon="material-symbols:chess-pawn-rounded", width=14),
                                    html.Div(
                                        className="flex flex-row gap-1",
                                        children=[
                                            html.Div(className="text-base font-semibold", children=black.get("username")),
                                            html.Div(className="text-base font-normal text-gray-400", children=f"({black.get('rating')})"),
                                        ],
                                    ),
                                    html.Img(className="size-[16px]", src="/assets/images/chess_com_icons/winner.png") if winner == "black" else None,
                                    # html.Div(
                                    #     className=f"text-[8px] bg-{color}-500 bg-opacity-50 border border-{color}-600 rounded-sm px-1",
                                    #     children="WINNER",
                                    # )
                                    # if winner == "black"
                                    # else None,
                                ],
                            ),
                        ],
                    ),
                    #
                    # Precision
                    html.Div(
                        className="flex flex-col items-center justify-center relative w-28 md:mx-4 lg:mx-6",
                        children=[
                            html.Div(
                                className="text-gray-400 absolute top-[-12px] text-xs",
                                children="Précision",
                            ),
                            html.Div(className="text-base font-semibold", children=white_accuracy),
                            html.Div(className="text-sm text-gray-400", children="VS"),
                            html.Div(className="text-base font-semibold", children=black_accuracy),
                        ],
                    )
                    if accuracy_status == "found"
                    else html.Div(
                        className="flex flex-col items-center justify-center relative w-28 md:mx-4 lg:mx-6",
                        children=[
                            html.Div(
                                className="text-gray-400 absolute top-[-12px] text-xs",
                                children="Précision",
                            ),
                            html.Div(className="", children="Pas calculée"),
                        ],
                    ),
                    #
                    # Number of moves
                    html.Div(
                        className="flex flex-col items-center justify-center relative w-28 md:mx-4 lg:mx-6",
                        children=[
                            html.Div(
                                className="text-gray-400 absolute top-[-12px] text-xs",
                                children="Coups",
                            ),
                            html.Div(className="", children=number_of_moves),
                        ],
                    ),
                    #
                    # End of the game
                    html.Div(
                        id={"type": "game-end-div", "index": game.get("url")},
                        className="flex flex-col items-center justify-center relative w-28 md:mx-4 lg:mx-6",
                        children=[
                            html.Div(
                                className="text-gray-400 absolute top-[-12px] text-xs",
                                children="Fin",
                            ),
                            html.Div(
                                className="",
                                children=html.Img(className="mx-5 my-auto size-[28px]", src=f"/assets/images/chess_com_icons/{outcome_icon}.png"),
                            ),
                            dbc.Tooltip(target={"type": "game-end-div", "index": game.get("url")}, children=end_reason, placement="top"),
                        ],
                    ),
                ],
            ),
            html.Div(
                className=f"game-action bg-{color}-800 bg-opacity-50 hover:bg-opacity-65 rounded-e-lg w-16 border-l border-{color}-900 border-opacity-50",
                children=html.A(href=game.get("url"), children=DashIconify(className=f"text-{color}-300 size-full p-5", icon="mdi:export-variant")),
            ),
        ],
    )


def playerRecentGames(player_name: str, player_games: list):
    return html.Div(
        className="flex flex-col",
        children=[
            html.Div(className="text-gray-400 mb-2 text-sm", children="Parties récentes"),
            html.Div(className="flex flex-col gap-3", children=[gameCard(player_name, game) for game in player_games]),
        ],
    )
