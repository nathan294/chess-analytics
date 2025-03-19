import dash_alternative_viz as dav
import polars as pl


def create_demo_highchart_piechart(df: pl.DataFrame):
    return dav.HighChart(
        # id="test-highchart",
        constructorType="chart",
        options={
            "title": {"text": None},
            "chart": {"plotShadow": False, "backgroundColor": "transparent"},
            "tooltip": {
                "pointFormat": "{series.name}: <b>{point.percentage:.1f}%</b>",
            },
            "accessibility": {"point": {"valueSuffix": "%"}},
            "plotOptions": {
                "pie": {
                    "allowPointSelect": True,
                    "cursor": "pointer",
                    "dataLabels": {"enabled": True},
                    "showInLegend": False,
                }
            },
            "series": [
                {
                    "type": "pie",
                    "name": "Brands",
                    "colorByPoint": True,
                    "data": [
                        {"name": "Chrome", "y": 74.77},
                        {"name": "Edge", "y": 12.82},
                        {"name": "Firefox", "y": 4.63},
                        {"name": "Safari", "y": 2.44},
                        {"name": "Internet Explorer", "y": 2.02},
                        {"name": "Other", "y": 3.28},
                    ],
                }
            ],
        },
    )
