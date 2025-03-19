import locale
from datetime import datetime

import dash
from flask import Flask

from chess_analytics.components.app_layout import app_layout
from chess_analytics.figures_template import apply_figures_template

try:
    locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
except locale.Error:
    locale.setlocale(locale.LC_ALL, "C")  # Use default locale if fr_FR is not supported


external_scripts = [
    # Add the tailwind cdn url hosting the files with the utility classes
    {"src": "https://cdn.tailwindcss.com"},
]
server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    title="Chess analytics",
    use_pages=True,
    # Add External scripts to the Dash app
    external_scripts=external_scripts,
    external_stylesheets=["https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"],
    # Ensure the dash app adapts to different screen sizes
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1",
        }
    ],
)

apply_figures_template()

app.layout = app_layout

if __name__ == "__main__":
    now = str(datetime.now())
    print(f"{now} Reload")
    print()
    app.run(debug=True, port=8050)
