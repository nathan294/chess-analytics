import locale

import plotly.graph_objects as go
import polars as pl
import polars_xdt  # noqa: F401


def prepare_data(df: pl.DataFrame):
    df = df.with_columns(pl.col("end_time").dt.date())
    df = df.group_by("end_time").first().select(pl.col("end_time"), pl.col("player_rating"))

    # Format the dates into the locale set in the app
    df = df.with_columns(pl.col("end_time").xdt.format_localized("%d %B %Y", locale.getlocale()[0]).alias("end_time_formatted"))

    df = df.sort(by="end_time")
    return df


def create_gamemode_ranking_linechart_plotly(df: pl.DataFrame):
    df_prepared = prepare_data(df)

    hov_text = [
        f"{date_}<br><span style='font-size:16px';>{rating} points</span>"
        for date_, rating in zip(df_prepared["end_time_formatted"], df_prepared["player_rating"])
    ]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_prepared["end_time"],
            y=df_prepared["player_rating"],
            mode="lines",
            text=df_prepared["end_time_formatted"],
            line=dict(shape="spline"),
            hoverinfo="text",
            hovertext=hov_text,
            # hovertemplate="%{text}: <b>%{y}</b><extra></extra>",
        )
    )
    fig.update_layout(hovermode="x unified")
    fig.update_layout(
        autosize=True,
        hoverdistance=1000,  # Ensure the hover appears
    )

    return fig
