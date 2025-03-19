import dash_alternative_viz as dav
import polars as pl


def prepare_data(df: pl.DataFrame):
    counts = df.select(pl.col("end_time").dt.year()).group_by("end_time").len().sort("end_time")

    # Convert to Highcharts format: [[year, count], ...]
    data = counts.rows()
    return data


def create_games_histogram(df: pl.DataFrame):
    data = prepare_data(df)

    options = {
        "title": {"text": None},
        # Global chart config
        "chart": {"plotShadow": False, "backgroundColor": "transparent", "height": 320},
        "xAxis": {"type": "category"},
        "yAxis": {
            "title": {"text": "Parties jouées"},
            "gridLineColor": "#364153",
            "gridLineWidth": 1,
        },
        # Hover tooltip
        "tooltip": {
            # "formatter": """function() {
            #     return "<b>" + this.y + "</b> " + (this.y > 1 ? "parties jouées" : "partie jouée");
            #     }""",
            "pointFormat": "<b>{point.y}</b> parties jouées",
        },
        # Options for all series
        "plotOptions": {
            "column": {
                "allowPointSelect": True,
                "cursor": "pointer",
                "borderWidth": 0,
                # Text
                "dataLabels": {
                    "enabled": True,
                    "style": {"color": "white", "fontWeight": "normal", "fontSize": "12px"},
                    "format": "{point.y} parties",
                },
                "showInLegend": False,
                "center": ["50%", "50%"],
            }
        },
        # Series
        "series": [
            {
                "type": "column",
                "name": "histogram",
                "data": data,  # Correct format
            }
        ],
    }
    return dav.HighChart(constructorType="chart", options=options)
