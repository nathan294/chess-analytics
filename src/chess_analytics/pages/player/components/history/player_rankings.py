import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_iconify import DashIconify

from chess_analytics.pages.player.figures.piechart_win_ratio_plotly import create_piechart_win_ratio_plotly


def rankingCard(ranking_name: str, ranking_details: dict):
    ranking_name_formatted = ranking_name.replace("_", " ").capitalize()

    if ranking_name == "tactics":
        return None
    elif ranking_name == "puzzle_rush":
        return None
    elif ranking_name == "lessons":
        return None
    elif ranking_name == "fide":
        return None
    else:
        return html.Div(
            className="rounded-lg p-4 shadow-md bg-[var(--card-color)] relative flex flex-row",
            children=[
                html.Div(
                    className="flex flex-col grow",
                    children=[
                        html.Div(className="text-base font-semibold mb-1", children=ranking_name_formatted),
                        html.Div(className="font-normal text-gray-400 text-[0.65rem] mb-[-4px]", children="Points"),
                        html.Div(className="font-semibold text-3xl", children=ranking_details.get("last", {}).get("rating", 0)),
                        html.Div(
                            className="flex flex-row gap-1",
                            children=[
                                html.Div(className="font-normal text-sm text-gray-400", children="Le plus haut atteint: "),
                                html.Div(
                                    className="font-semibold text-sm",
                                    children=ranking_details.get("best", ranking_details.get("last")).get("rating", 0),
                                ),
                            ],
                        ),
                        html.Div(
                            className="text-sm flex flex-row gap-2 items-center",
                            children=[
                                html.Div(className="text-gray-400", children=f"RD: {ranking_details.get('last', {}).get('rd', 0)}"),
                                html.Div(
                                    className="",
                                    children=[
                                        DashIconify(
                                            id={"type": "ranking_rd_info", "index": ranking_name},
                                            icon="material-symbols:info-outline-rounded",
                                            className="opacity-70",
                                        ),
                                        dbc.Tooltip(
                                            target={"type": "ranking_rd_info", "index": ranking_name},
                                            children=[
                                                html.P(
                                                    "L'écart de fiabilité (Reliability Deviation) mesure la précision de la notation d'un joueur, où le RD est égal à un écart type."
                                                ),
                                                html.P(
                                                    "Par exemple, un joueur avec une note de 1500 et un RD de 50 a une force réelle entre 1400 et 1600 (deux écarts types par rapport à 1500) avec une confiance de 95 %."
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="flex flex-col gap-2 p-4 w-1/3 items-center justify-center mr-2",
                    children=[
                        dcc.Graph(
                            className="size-14",
                            id={"type": "ranking_win_ratio_graph", "index": ranking_name},
                            figure=create_piechart_win_ratio_plotly(ranking_details.get("record")),
                            responsive=True,
                            config={"displayModeBar": False},
                        ),
                        html.Div(
                            className="flex flex-row gap-2",
                            children=[
                                html.Div(
                                    className="flex flex-col items-center",
                                    children=[
                                        html.Div(className="text-gray-400 text-[0.65rem]", children="V"),
                                        html.Div(className="text-green-400 text-sm", children=ranking_details.get("record").get("win")),
                                    ],
                                ),
                                html.Div(
                                    className="flex flex-col justify-end",
                                    children=[
                                        html.Div(className="text-gray-400 text-sm", children="/"),
                                    ],
                                ),
                                html.Div(
                                    className="flex flex-col items-center",
                                    children=[
                                        html.Div(className="text-gray-400 text-[0.65rem]", children="D"),
                                        html.Div(className="text-red-400 text-sm", children=ranking_details.get("record").get("loss")),
                                    ],
                                ),
                                html.Div(
                                    className="flex flex-col justify-end",
                                    children=[
                                        html.Div(className="text-gray-400 text-sm", children="/"),
                                    ],
                                ),
                                html.Div(
                                    className="flex flex-col items-center",
                                    children=[
                                        html.Div(className="text-gray-400 text-[0.65rem]", children="N"),
                                        html.Div(className="text-yellow-400 text-sm", children=ranking_details.get("record").get("draw")),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )


def playerRankings(player_stats: dict):
    return html.Div(
        className="flex flex-col",
        children=[
            html.Div(className="text-gray-400 mb-2 text-sm", children="Classements"),
            html.Div(
                className="flex flex-col gap-6",
                children=[rankingCard(ranking_name, ranking_details) for ranking_name, ranking_details in player_stats.items()],
            ),
        ],
    )
