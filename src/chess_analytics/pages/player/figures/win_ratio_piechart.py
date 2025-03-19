import dash_alternative_viz as dav
import polars as pl


def prepare_data(df: pl.DataFrame):
    df = df.group_by("player_result").len()
    df = df.select(pl.col("player_result").str.to_titlecase(), pl.col("len"))
    return df


def create_win_ratio_piechart(df: pl.DataFrame):
    df = prepare_data(df)
    data = [{"name": outcome, "y": count} for outcome, count in df.rows()]

    # Define color mapping based on result type
    color_mapping = {
        "win": "#15803d",  # Shades of green
        "draw": "gray",  # Shades of gray
        "loss": "#b91c1c",  # Shades of red
    }
    data = [{"name": outcome, "y": count, "color": color_mapping[str(outcome).lower()]} for outcome, count in df.rows()]

    options = {
        "title": {"text": None},
        # Global chart config
        "chart": {"plotShadow": False, "backgroundColor": "transparent", "height": 320},
        # Hover tooltip
        "tooltip": {
            # "headerFormat": "{point.key}<br>",
            "pointFormat": "<b>{point.percentage:.1f}%</b> des parties" + "<br><b>{point.y}</b> parties",
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
            }
        ],
    }
    return dav.HighChart(constructorType="chart", options=options)
