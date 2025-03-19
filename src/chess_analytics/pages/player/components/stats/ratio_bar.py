import uuid

import polars as pl
from dash import html
from dash_iconify import DashIconify


def format_results_wording(results: dict):
    results_wording = {}
    if results.get("win", 0) > 1:
        results_wording["win"] = f"{results.get('win')} victoires"
    else:
        results_wording["win"] = f"{results.get('win', 0)} victoire"
    if results.get("draw", 0) > 1:
        results_wording["draw"] = f"{results.get('draw')} matchs nuls"
    else:
        results_wording["draw"] = f"{results.get('draw', 0)} match nul"
    if results.get("loss", 0) > 1:
        results_wording["loss"] = f"{results.get('loss')} défaites"
    else:
        results_wording["loss"] = f"{results.get('loss', 0)} défaite"
    return results_wording


def ratioBar(df: pl.DataFrame):
    results = dict(
        zip(df.group_by("player_result", maintain_order=True).len()["player_result"], df.group_by("player_result", maintain_order=True).len()["len"])
    )

    total_games = sum(results.values())

    if total_games == 0:
        results_percent = {}
    else:
        results_percent = {
            "win": int(results.get("win", 0) / total_games * 100),
            "loss": int(results.get("loss", 0) / total_games * 100),
            "draw": int(results.get("draw", 0) / total_games * 100),
        }
    results_wording = format_results_wording(results)
    return html.Div(
        className="ratio-bar my-12 animate__animated animate__fadeIn animate__faster",
        key=str(uuid.uuid4()),  # Forces re-render to trigger the animation
        children=[
            # Header
            html.Div(
                className="flex flex-row mx-auto w-3/4",
                children=[
                    # Win
                    html.Div(
                        className="text-green-600 whitespace-nowrap",
                        children=html.Div(
                            className="flex flex-row items-center gap-1",
                            children=[
                                DashIconify(icon="fluent:checkbox-checked-16-filled"),
                                html.Div(className="", children=str(results_percent.get("win", 0)) + "%"),
                            ],
                        ),
                        style={"flex-basis": str(results_percent.get("win", 33)) + "%"},
                    ),
                    # Draw
                    html.Div(
                        className="text-yellow-400 whitespace-nowrap",
                        children=html.Div(
                            className="flex flex-row items-center gap-1",
                            children=[
                                DashIconify(icon="tabler:square-dot-filled"),
                                html.Div(className="", children=str(results_percent.get("draw", 0)) + "%"),
                            ],
                            style={
                                "flex-basis": str(results_percent.get("draw", 34)) + "%",
                                "visibility": "visible" if results_percent.get("draw", 1) > 0 else "hidden",
                            },
                        ),
                    ),
                    # Loss
                    html.Div(
                        className="text-red-600 whitespace-nowrap ml-auto",
                        children=html.Div(
                            className="flex flex-row items-center gap-1",
                            children=[
                                DashIconify(icon="entypo:squared-cross"),
                                html.Div(className="", children=str(results_percent.get("loss", 0)) + "%"),
                            ],
                        ),
                    ),
                ],
            ),
            # Main content (bar)
            html.Div(
                className="flex flex-row mx-auto w-3/4 h-4",
                children=[
                    html.Span(
                        className="bg-green-700 rounded-l-xl h-full inline-block whitespace-nowrap",
                        style={"flex-grow": str(results_percent.get("win", 1))},
                    ),
                    html.Span(
                        className="bg-yellow-400 h-full inline-block whitespace-nowrap",
                        style={"flex-grow": str(results_percent.get("draw", 1))},
                    ),
                    html.Span(
                        className="bg-red-700 rounded-r-xl h-full inline-block whitespace-nowrap",
                        style={"flex-grow": str(results_percent.get("loss", 1))},
                    ),
                ],
            ),
            # Footer
            html.Div(
                className="flex flex-row mx-auto w-3/4",
                children=[
                    # Win
                    html.Div(
                        className="text-green-600 whitespace-nowrap",
                        children=results_wording.get("win", 0),
                        style={"flex-basis": str(results_percent.get("win", 33)) + "%"},
                    ),
                    # Draw
                    html.Div(
                        className="text-yellow-400 whitespace-nowrap",
                        children=results_wording.get("draw", 0),
                        style={
                            "flex-basis": str(results_percent.get("draw", 34)) + "%",
                            "visibility": "visible" if results_percent.get("draw", 1) > 0 else "hidden",
                        },
                    ),
                    # Loss
                    html.Div(
                        className="text-red-600 whitespace-nowrap ml-auto",
                        children=results_wording.get("loss", 0),
                    ),
                ],
            ),
        ],
    )
