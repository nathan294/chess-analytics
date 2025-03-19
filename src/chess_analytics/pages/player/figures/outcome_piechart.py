from typing import Literal

import dash_alternative_viz as dav
import plotly.express as px
import polars as pl


def prepare_data(df: pl.DataFrame, result: Literal["win", "draw", "loss"]):
    if result == "win":
        field = "opponent_outcome"
    else:
        field = "player_outcome"
    df = df.filter(pl.col("player_result") == result)
    df = df.group_by(field).len()
    df = df.select(pl.col(field).str.to_titlecase().alias("outcome"), pl.col("len"))
    return df


def create_outcome_piechart(df: pl.DataFrame, result: Literal["win", "draw", "loss"]):
    df = prepare_data(df, result)
    data = [{"name": outcome, "y": count} for outcome, count in df.rows()]

    # Tooltip text translation
    tooltip_text = {"win": "victoires", "draw": "matchs nuls", "loss": "défaites"}[result]

    # Select the color palette based on the result
    if result == "win":
        colors = px.colors.sequential.Greens[::-1]
    elif result == "loss":
        colors = px.colors.sequential.Reds[::-1]
    else:  # for draw
        colors = px.colors.sequential.Greys

    # Ensure the number of colors matches the data length
    if len(colors) < len(data):
        colors = colors * (len(data) // len(colors)) + colors[: len(data) % len(colors)]

    options = {
        "title": {"text": None},
        # Global chart config
        "chart": {"plotShadow": False, "backgroundColor": "transparent", "height": 320},
        # Hover tooltip
        "tooltip": {
            # "headerFormat": "{point.key}<br>",
            "pointFormat": "<b>{point.percentage:.1f}%</b>" + f" des {tooltip_text}<br>" + "<b>{point.y}</b> parties",
            # "footerFormat": "",
        },
        # Options for all series
        "plotOptions": {
            "pie": {
                "size": "90%",
                "allowPointSelect": True,
                "cursor": "pointer",
                "borderWidth": 0,
                # Text
                "dataLabels": {
                    "enabled": True,
                    "style": {"color": "white", "fontWeight": "normal", "fontSize": "12px"},
                    "format": "{point.name}<br> {point.percentage:.1f}%",
                },
                "showInLegend": False,
                "center": ["50%", "50%"],
            }
        },
        "legend": {"enabled": False},
        # Series
        "series": [
            {
                "type": "pie",
                "name": "pie",
                "innerSize": "50%",
                "colorByPoint": True,
                "data": data,
                "colors": colors,
            }
        ],
    }
    return dav.HighChart(constructorType="chart", options=options)
