from dash import html


def graphCard(title: str, graph):
    return html.Div(
        className="flex flex-col h-full rounded-lg bg-[var(--card-color)]",
        children=[
            html.Div(
                className="font-semibold h-12 rounded-t-lg content-center text-center text-lg w-full bg-[var(--card-color-selected)]", children=title
            ),
            html.Div(className="p-4 grow graph", children=graph),
        ],
    )
