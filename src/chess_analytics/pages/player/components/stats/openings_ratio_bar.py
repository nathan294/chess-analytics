from dash import html
from dash_iconify import DashIconify

from chess_analytics.pages.player.components.stats.ratio_bar import format_results_wording


def openingsRatioBar(win: int, loss: int, draw: int, total: int):
    results = {"win": win, "loss": loss, "draw": draw}
    results_wording = format_results_wording(results)

    if total == 0:
        results_percent = {}
    else:
        results_percent = {
            "win": int(win / total * 100),
            "loss": int(loss / total * 100),
            "draw": int(draw / total * 100),
        }

    return html.Div(
        className="",
        children=[
            # Header
            html.Div(
                className="flex flex-row w-3/4",
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
                        style={
                            "flex-basis": str(results_percent.get("win", 33)) + "%",
                        },
                    ),
                    # Draw
                    html.Div(
                        className="text-yellow-400 mx-auto whitespace-nowrap",
                        children=html.Div(
                            className="flex flex-row items-center gap-1",
                            children=[
                                DashIconify(icon="tabler:square-dot-filled"),
                                html.Div(className="", children=str(results_percent.get("draw", 0)) + "%"),
                            ],
                        ),
                        style={
                            "flex-basis": str(results_percent.get("draw", 34)) + "%",
                            "visibility": "visible" if results_percent.get("draw", 1) > 0 else "hidden",
                        },
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
                className="flex flex-row w-3/4 h-4 bg-transparent rounded-xl overflow-hidden",
                children=[
                    html.Span(
                        className="bg-green-700 h-full inline-block whitespace-nowrap",
                        style={"flex-grow": str(results_percent.get("win", 1))},
                    ),
                    html.Span(
                        className="bg-yellow-400 h-full inline-block whitespace-nowrap",
                        style={"flex-grow": str(results_percent.get("draw", 1))},
                    ),
                    html.Span(
                        className="bg-red-700 h-full inline-block whitespace-nowrap",
                        style={"flex-grow": str(results_percent.get("loss", 1))},
                    ),
                ],
            ),
            # Footer
            html.Div(
                className="flex flex-row w-3/4",
                children=[
                    # Win
                    html.Div(
                        className="text-green-600 whitespace-nowrap",
                        children=results_wording.get("win", 0),
                        style={
                            "flex-basis": str(results_percent.get("win", 33)) + "%",
                        },
                    ),
                    # Draw
                    html.Div(
                        className="text-yellow-400 text-center whitespace-nowrap",
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
