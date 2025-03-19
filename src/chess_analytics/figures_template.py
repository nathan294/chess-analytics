import copy

import plotly.io as pio


def apply_figures_template():
    # Create a copy of "plotly_dark" to avoid modifying the original
    custom_template = copy.deepcopy(pio.templates["plotly_dark"])

    # Apply custom styles
    custom_template.layout.paper_bgcolor = "#242424"
    custom_template.layout.plot_bgcolor = "#242424"
    custom_template.layout.font.family = "Inter,Arial"
    custom_template.layout.margin = dict(l=20, r=20, t=20, b=20)  # We handle margins in Dash
    custom_template.layout.colorway = ["#5383e8"]

    # Register and set the new template as default
    pio.templates["custom_dark"] = custom_template
    pio.templates.default = "custom_dark"
