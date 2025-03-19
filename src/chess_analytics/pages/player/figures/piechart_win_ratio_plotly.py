import plotly.graph_objects as go


def create_piechart_win_ratio_plotly(gamemode_record: dict):
    win = gamemode_record.get("win", 0)
    loss = gamemode_record.get("loss", 0)
    draw = gamemode_record.get("draw", 0)

    labels = ["Victoires", "Défaites", "Matchs nuls"]
    values = [win, loss, draw]
    colors = ["#2ecc71", "#e74c3c", "#f1c40f"]  # Green for wins, red for losses, yellow for draws
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.7,  # Creates the donut effect
                marker=dict(colors=colors),
                textinfo="none",
                hoverinfo="none",
                # hovertemplate="<b>%{value}</b> %{label} (<b>%{percent}</b> du total)<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot area
        margin=dict(l=0, r=0, t=0, b=0),  # Remove margins (handled in dash)
        showlegend=False,
    )

    return fig
