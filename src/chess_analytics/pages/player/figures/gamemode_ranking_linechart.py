import locale
from typing import Literal

import dash_alternative_viz as dav
import plotly.express as px
import polars as pl


def prepare_data(df: pl.DataFrame):
    df = df.with_columns(pl.col("end_time").dt.date())
    df = df.group_by("end_time").first().select(pl.col("end_time"), pl.col("player_rating"))
    df = df.sort(by="end_time")

    # Format the dates into the locale set in the app
    df = df.select(pl.col("end_time").xdt.format_localized("%d %B %Y", locale.getlocale()[0]), pl.col("player_rating"))

    return df


def create_ranking_evolution_linechart(df: pl.DataFrame):
    df = prepare_data(df)
    data = [{"name": date_, "y": ranking} for date_, ranking in df.rows()]

    options = {
        "title": {"text": None},
        # Global chart config
        "chart": {"plotShadow": False, "backgroundColor": "transparent"},
        # Hover tooltip
        # "tooltip": {
        #     # "headerFormat": "{point.key}<br>",
        #     "pointFormat": "<b>{point.percentage:.1f}%</b>" + f" des {tooltip_text}",
        #     # "footerFormat": "",
        # },
        "xAxis": {
            "allowDecimals": False,
            # "labels": {
            #     "formatter": """function () {
            #     return this.value; // clean, unformatted number for year
            # }"""
            # },
        },
        "yAxis": {
            "title": {
                "text": None,
            },
            # "labels": {
            #     "formatter": """function () {
            #     return this.value / 1000 + 'k';
            # }"""
            # },
        },
        # Options for all series
        "plotOptions": {
            "area": {
                # "pointStart": 2025,
                "marker": {
                    "enabled": False,
                    "symbol": "circle",
                    "radius": 2,
                    "states": {"hover": {"enabled": True}},
                },
            }
        },
        "legend": {"enabled": False},
        # Series
        "series": [
            {
                "type": "area",
                "name": "area",
                "data": data,
            }
        ],
    }
    return dav.HighChart(constructorType="chart", options=options)
