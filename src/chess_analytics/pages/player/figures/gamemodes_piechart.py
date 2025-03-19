import dash_alternative_viz as dav
import polars as pl


def prepare_data(df: pl.DataFrame):
    df = df.group_by("gamemode").len()
    df = df.with_columns(pl.col("gamemode").str.replace("_chess", "").str.to_titlecase())
    return df


def create_gamemode_piechart(df: pl.DataFrame):
    df = prepare_data(df)
    data = [{"name": gamemode, "y": count} for gamemode, count in df.rows()]
    options = {
        "title": {"text": None},
        # Global chart config
        "chart": {"plotShadow": False, "backgroundColor": "transparent", "height": 320},
        # Hover tooltip
        "tooltip": {
            # "headerFormat": "{point.key}<br>",
            "pointFormat": "<b>{point.y}</b> parties (<b>{point.percentage:.1f}%</b>)",
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
                    "format": "{point.name}: {point.percentage:.1f}%",
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
                "name": "Gamemodes",
                "innerSize": "50%",
                "colorByPoint": True,
                "data": data,
            }
        ],
    }
    return dav.HighChart(constructorType="chart", options=options)
