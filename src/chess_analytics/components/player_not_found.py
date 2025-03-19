from dash import html


def playerNotFound(player_name: str):
    return html.Div(
        className="flex flex-col mt-32 gap-2 items-center justify-center",
        children=[
            html.Div(
                className="flex flex-row gap-1",
                children=[
                    html.Div(className="text-xl", children='Aucun résultat de recherche pour " '),
                    html.Div(className="text-xl text-[var(--primary-color)] font-bold", children=f"{player_name}"),
                    html.Div(className="text-xl", children=' " sur Chess.com'),
                ],
            ),
            html.Div(className="", children="Veuillez vérifier le nom du joueur, et réessayez."),
        ],
    )
